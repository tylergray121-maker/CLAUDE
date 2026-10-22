"""Fetch wallets, trade histories and market resolutions from Polymarket.

Response shapes vary between API versions, so every parser here reads fields
defensively and drops records it cannot interpret instead of guessing.
"""

from __future__ import annotations

import json
import logging
import sys
from bisect import bisect_left
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from .api import CLOB_API, DATA_API, GAMMA_API, LB_API, Client, HTTPError
from .models import Market, Trade

log = logging.getLogger(__name__)

LEADERBOARD_PERIODS = ("DAY", "WEEK", "MONTH", "ALL")
LEADERBOARD_ORDERS = ("PNL", "VOL")


def _as_list(payload) -> list:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "results", "items", "leaderboard", "history"):
            if isinstance(payload.get(key), list):
                return payload[key]
    return []


def _json_list(value) -> list:
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value.strip().startswith("["):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return []
    return []


def _parse_ts(value) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        v = float(value)
        return int(v / 1000) if v > 1e12 else int(v)
    s = str(value).strip()
    if s.isdigit():
        return _parse_ts(int(s))
    s = s.replace("Z", "+00:00")
    if s.endswith("+00"):
        s += ":00"
    for candidate in (s, s.replace(" ", "T", 1)):
        try:
            dt = datetime.fromisoformat(candidate)
        except ValueError:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    return None


# --------------------------------------------------------------------------
# Wallet discovery
# --------------------------------------------------------------------------

def fetch_leaderboard(client: Client, periods=LEADERBOARD_PERIODS,
                      orders=LEADERBOARD_ORDERS, categories=("OVERALL",),
                      per_board: int = 500) -> dict[str, dict]:
    """Union of leaderboard wallets -> {wallet: {name, best_rank, boards}}."""
    wallets: dict[str, dict] = {}

    def add(addr, name, rank, board):
        if not addr or not isinstance(addr, str) or not addr.startswith("0x"):
            return
        addr = addr.lower()
        w = wallets.setdefault(addr, {"name": name or "", "best_rank": rank,
                                      "boards": []})
        w["best_rank"] = min(w["best_rank"], rank)
        w["boards"].append(board)
        if name and not w["name"]:
            w["name"] = name

    for cat in categories:
        for period in periods:
            for order in orders:
                board = f"{cat}/{period}/{order}"
                got = 0
                for offset in range(0, per_board, 50):
                    try:
                        page = _as_list(client.get(DATA_API, "/v1/leaderboard", {
                            "category": cat, "timePeriod": period,
                            "orderBy": order, "limit": 50, "offset": offset}))
                    except HTTPError as e:
                        log.warning("leaderboard %s offset %d: %s", board, offset, e)
                        break
                    if not page:
                        break
                    for i, row in enumerate(page):
                        add(row.get("proxyWallet") or row.get("address"),
                            row.get("userName") or row.get("name"),
                            int(row.get("rank") or offset + i + 1), board)
                    got += len(page)
                    if len(page) < 50:
                        break
                log.info("leaderboard %s: %d wallets", board, got)

    if not wallets:
        # Older leaderboard service, kept as a fallback.
        log.warning("v1 leaderboard returned nothing; trying lb-api fallback")
        for window in ("1d", "7d", "1m", "all"):
            for kind in ("profit", "volume"):
                try:
                    rows = _as_list(client.get(LB_API, f"/{kind}", {
                        "window": window, "limit": per_board}))
                except HTTPError as e:
                    log.warning("lb-api %s/%s: %s", kind, window, e)
                    continue
                for i, row in enumerate(rows):
                    add(row.get("proxyWallet"), row.get("name") or row.get("pseudonym"),
                        i + 1, f"lb/{window}/{kind}")
    return wallets


# --------------------------------------------------------------------------
# Trade history
# --------------------------------------------------------------------------

def _parse_trade(row: dict, wallet: str = "") -> Trade | None:
    try:
        side = str(row.get("side", "")).upper()
        if side not in ("BUY", "SELL"):
            return None
        price = float(row["price"])
        size = float(row["size"])
        ts = _parse_ts(row.get("timestamp"))
        asset = str(row.get("asset") or row.get("asset_id") or "")
        cond = str(row.get("conditionId") or row.get("market") or "").lower()
    except (KeyError, TypeError, ValueError):
        return None
    if ts is None or not asset or not cond or size <= 0 or not 0 < price < 1:
        return None
    return Trade(ts=ts, asset=asset, condition_id=cond, side=side, price=price,
                 size=size, title=str(row.get("title") or ""),
                 outcome=str(row.get("outcome") or ""),
                 tx=str(row.get("transactionHash") or ""),
                 wallet=wallet or str(row.get("proxyWallet") or "").lower(),
                 slug=str(row.get("slug") or ""))


def _compact(t: Trade) -> Trade:
    """Share repeated strings across trades and drop the tx hash (only needed
    for de-duplication while paging). Cuts memory several-fold."""
    i = sys.intern
    return Trade(ts=t.ts, asset=i(t.asset), condition_id=i(t.condition_id),
                 side=i(t.side), price=t.price, size=t.size, title=i(t.title),
                 outcome=i(t.outcome), tx="", wallet=i(t.wallet), slug=i(t.slug))


_TRADE_FIELDS = ("ts", "asset", "condition_id", "side", "price", "size", "title",
                 "outcome", "tx", "wallet", "slug")


def fetch_trades(client: Client, wallet: str, start_ts: int, end_ts: int,
                 max_trades: int = 20000, page_size: int = 500,
                 max_offset: int = 3000) -> tuple[list[Trade], bool]:
    """Cached wrapper: stores only the parsed fields, gzipped, per wallet."""
    key = f"trades:{wallet.lower()}:{start_ts}:{end_ts}:{max_trades}"
    blob = client.load_blob(key)
    if blob is not None:
        return [_compact(Trade(**dict(zip(_TRADE_FIELDS, row))))
                for row in blob["t"]], blob["x"]
    trades, truncated = _fetch_trades(client, wallet, start_ts, end_ts, max_trades,
                                      page_size, max_offset)
    trades = [_compact(t) for t in trades]
    client.save_blob(key, {"x": truncated, "t": [
        [getattr(t, f) for f in _TRADE_FIELDS] for t in trades]})
    return trades, truncated


def _fetch_trades(client: Client, wallet: str, start_ts: int, end_ts: int,
                  max_trades: int, page_size: int,
                  max_offset: int) -> tuple[list[Trade], bool]:
    """All TRADE activity for ``wallet`` in [start_ts, end_ts], oldest first.

    Pages newest-to-oldest by offset, and re-anchors ``end`` on the oldest
    timestamp seen whenever the API's offset cap is reached. Returns
    (trades, truncated) where truncated means ``max_trades`` was hit.
    """
    seen: set[tuple] = set()
    out: list[Trade] = []
    cursor_end = end_ts
    while True:
        offset = 0
        oldest = cursor_end
        progressed = False
        exhausted = False
        while offset <= max_offset:
            try:
                page = _as_list(client.get(DATA_API, "/activity", {
                    "user": wallet, "type": "TRADE", "limit": page_size,
                    "offset": offset, "start": start_ts, "end": cursor_end,
                    "sortBy": "TIMESTAMP", "sortDirection": "DESC"},
                    use_cache=False))
            except HTTPError as e:
                if e.status == 400 and offset > 0:
                    break  # offset cap reached; re-anchor below
                raise
            for row in page:
                t = _parse_trade(row, wallet.lower())
                if t is None or t.ts < start_ts:
                    continue
                key = (t.tx, t.asset, t.side, t.size, t.price, t.ts)
                if key in seen:
                    continue
                seen.add(key)
                out.append(t)
                progressed = True
                oldest = min(oldest, t.ts)
            if len(out) >= max_trades:
                out.sort(key=lambda t: t.ts)
                return out, True
            if len(page) < page_size:
                exhausted = True
                break
            offset += page_size
        if exhausted or not progressed or oldest <= start_ts:
            break
        # Re-anchor on the oldest second seen; dedupe handles the overlap.
        cursor_end = oldest
    out.sort(key=lambda t: t.ts)
    return out, False


# --------------------------------------------------------------------------
# Market resolutions
# --------------------------------------------------------------------------

def _market_from_gamma(row: dict) -> Market | None:
    cond = row.get("conditionId")
    tokens = [str(t) for t in _json_list(row.get("clobTokenIds"))]
    prices = _json_list(row.get("outcomePrices"))
    if not cond or not tokens or len(tokens) != len(prices):
        return None
    try:
        prices = [float(p) for p in prices]
    except (TypeError, ValueError):
        return None
    uma = str(row.get("umaResolutionStatus") or "").lower()
    closed = bool(row.get("closed"))
    decisive = max(prices) >= 0.98 and sum(prices) <= 1.02
    resolved = uma == "resolved" or (closed and decisive)
    resolve_ts = None
    if resolved:
        resolve_ts = (_parse_ts(row.get("closedTime"))
                      or _parse_ts(row.get("umaEndDate"))
                      or _parse_ts(row.get("endDate")))
    fee_rate, fee_exp = 0.0, 1.0
    sched = row.get("feeSchedule")
    if row.get("feesEnabled") and isinstance(sched, dict):
        try:
            fee_rate = float(sched.get("rate") or 0)
            fee_exp = float(sched.get("exponent") or 1)
        except (TypeError, ValueError):
            pass
    return Market(condition_id=cond.lower(), resolved=resolved,
                  resolve_ts=resolve_ts, prices=dict(zip(tokens, prices)),
                  question=str(row.get("question") or ""),
                  fee_rate=fee_rate, fee_exponent=fee_exp,
                  start_ts=_parse_ts(row.get("gameStartTime")))


def _market_from_clob(row: dict) -> Market | None:
    cond = row.get("condition_id")
    tokens = row.get("tokens") or []
    if not cond or not tokens:
        return None
    prices: dict[str, float] = {}
    any_winner = False
    for tok in tokens:
        tid = str(tok.get("token_id") or "")
        if not tid:
            continue
        if tok.get("winner") is True:
            any_winner = True
        try:
            prices[tid] = float(tok.get("price") or 0)
        except (TypeError, ValueError):
            prices[tid] = 0.0
    resolved = bool(row.get("closed")) and any_winner
    if resolved:
        prices = {str(t.get("token_id")): 1.0 if t.get("winner") else 0.0
                  for t in tokens if t.get("token_id")}
    return Market(condition_id=cond.lower(), resolved=resolved,
                  resolve_ts=_parse_ts(row.get("end_date_iso")) if resolved else None,
                  prices=prices, question=str(row.get("question") or ""))


GAMMA_KEYS = ("conditionId", "clobTokenIds", "outcomePrices", "closed",
              "umaResolutionStatus", "closedTime", "umaEndDate", "endDate",
              "question", "feesEnabled", "feeSchedule", "gameStartTime")
CLOB_KEYS = ("condition_id", "tokens", "closed", "end_date_iso", "question")


def fetch_markets(client: Client, condition_ids: set[str], batch: int = 50,
                  workers: int = 8) -> dict[str, Market]:
    """Resolve markets via gamma in parallel batches, CLOB per market as fallback."""
    ids = sorted({c.lower() for c in condition_ids if c})
    out: dict[str, Market] = {}

    def gamma_batch(chunk: list[str], closed: str | None) -> list[Market]:
        params: list[tuple] = [("condition_ids", c) for c in chunk]
        params.append(("limit", len(chunk)))
        if closed:
            params.append(("closed", closed))
        try:
            rows = _as_list(client.get(GAMMA_API, "/markets", params, keep=GAMMA_KEYS))
        except HTTPError as e:
            log.warning("gamma markets batch failed: %s", e)
            return []
        return [m for m in map(_market_from_gamma, rows) if m]

    def clob_one(cond: str) -> list[Market]:
        try:
            m = _market_from_clob(client.get(CLOB_API, f"/markets/{cond}",
                                             keep=CLOB_KEYS))
        except HTTPError as e:
            log.debug("clob market %s: %s", cond, e)
            return []
        return [m] if m else []

    # Most markets a 90-day backtest touches have closed, so ask for those first.
    for label, closed in (("closed", "true"), ("open", None)):
        todo = [c for c in ids if c not in out]
        chunks = [todo[i:i + batch] for i in range(0, len(todo), batch)]
        _run_parallel(f"gamma {label}", chunks, lambda ch: gamma_batch(ch, closed),
                      out, workers)
    todo = [c for c in ids if c not in out]
    if todo:
        _run_parallel("clob fallback", todo, clob_one, out, workers)
    missing = len(ids) - len(out)
    if missing:
        log.warning("%d of %d markets could not be resolved", missing, len(ids))
    return out


def _run_parallel(label, jobs, fn, out: dict, workers: int) -> None:
    if not jobs:
        return
    step = max(1, len(jobs) // 20)
    with ThreadPoolExecutor(workers) as pool:
        for i, markets in enumerate(pool.map(fn, jobs), 1):
            for m in markets:
                out[m.condition_id] = m
            if i % step == 0 or i == len(jobs):
                log.info("%s: %d/%d requests, %d markets known", label, i,
                         len(jobs), len(out))


# --------------------------------------------------------------------------
# Price history (only used when a copy delay is simulated)
# --------------------------------------------------------------------------

class PriceHistory:
    """Copy-delay prices from the CLOB prices-history endpoint.

    Only small two-hour windows around trades are fetched (minute bars), so
    memory and disk stay bounded however many tokens are involved.
    """

    def __init__(self, client: Client):
        self.client = client
        self._windows: dict[tuple[str, int], list[tuple[int, float]]] = {}
        self.hits = self.misses = 0

    def _fetch(self, key: tuple[str, int]) -> list[tuple[int, float]]:
        token, hour = key
        try:
            rows = _as_list(self.client.get(CLOB_API, "/prices-history", {
                "market": token, "startTs": hour * 3600,
                "endTs": hour * 3600 + 7200, "fidelity": 1}))
        except (HTTPError, ValueError, TypeError) as e:
            log.debug("price history %s: %s", token, e)
            return []
        out = []
        for r in rows:
            t, p = _parse_ts(r.get("t")), r.get("p")
            if t is not None and p is not None:
                out.append((t, float(p)))
        return sorted(out)

    def prefetch(self, points: set[tuple[str, int]], workers: int = 8) -> None:
        keys = sorted({(tok, ts // 3600) for tok, ts in points} - set(self._windows))
        if not keys:
            return
        step = max(1, len(keys) // 20)
        with ThreadPoolExecutor(workers) as pool:
            for i, (key, pts) in enumerate(zip(keys, pool.map(self._fetch, keys)), 1):
                self._windows[key] = pts
                if i % step == 0 or i == len(keys):
                    log.info("price history: %d/%d windows", i, len(keys))

    def price_at(self, token: str, ts: int) -> float | None:
        """First minute-bar price within an hour at or after ``ts``, else None."""
        key = (token, ts // 3600)
        if key not in self._windows:
            self._windows[key] = self._fetch(key)
        pts = self._windows[key]
        j = bisect_left(pts, (ts, -1.0))
        if j < len(pts) and pts[j][0] - ts <= 3600:
            self.hits += 1
            return pts[j][1]
        self.misses += 1
        return None
