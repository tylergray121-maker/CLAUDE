"""Collect public data on top wallets from Polymarket's data API."""

from __future__ import annotations

import logging

from copybt.api import DATA_API, Client, HTTPError

log = logging.getLogger(__name__)

CATEGORIES = ("POLITICS", "SPORTS", "CRYPTO", "CULTURE", "ECONOMICS", "TECH",
              "FINANCE", "WEATHER", "MENTIONS")


def leaderboard(client: Client, category: str, period: str, n: int) -> list[dict]:
    out = []
    for offset in range(0, n, 50):
        try:
            page = client.get(DATA_API, "/v1/leaderboard", {
                "category": category, "timePeriod": period, "orderBy": "PNL",
                "limit": 50, "offset": offset}) or []
        except HTTPError as e:
            log.warning("leaderboard %s/%s: %s", category, period, e)
            break
        out += [r for r in page if isinstance(r, dict) and r.get("proxyWallet")]
        if len(page) < 50:
            break
    return out[:n]


def alltime_pnl(client: Client, wallet: str) -> float | None:
    """The wallet's all-time leaderboard profit, if the API will look it up."""
    try:
        rows = client.get(DATA_API, "/v1/leaderboard", {
            "category": "OVERALL", "timePeriod": "ALL", "orderBy": "PNL",
            "user": wallet, "limit": 1}) or []
    except HTTPError:
        return None
    for r in rows if isinstance(rows, list) else []:
        if str(r.get("proxyWallet", "")).lower() == wallet.lower():
            try:
                return float(r.get("pnl"))
            except (TypeError, ValueError):
                return None
    return None


def paged(client: Client, path: str, params: dict, cap: int, page: int = 500,
          max_offset: int = 10000) -> tuple[list[dict], bool]:
    """Offset pagination tolerant of servers that cap the page size.
    Returns (rows, truncated)."""
    rows: list[dict] = []
    offset = 0
    while len(rows) < cap and offset <= max_offset:
        try:
            batch = client.get(DATA_API, path, {**params, "limit": page, "offset": offset})
        except HTTPError as e:
            if offset == 0:
                log.debug("%s %s: %s", path, params.get("user"), e)
            break
        batch = [r for r in (batch or []) if isinstance(r, dict)]
        if not batch:
            return rows, False
        rows += batch
        offset += len(batch)
    return rows[:cap], len(rows) >= cap or offset > max_offset


def wallet_data(client: Client, wallet: str, caps: dict | None = None) -> dict:
    caps = {"closed": 5000, "trades": 1000, "rewards": 3000, "events": 1000,
            **(caps or {})}
    # The API lists closed positions best-first, so a capped read of a busy
    # wallet would see only its winners: read from both ends and merge.
    half = caps["closed"] // 2
    best, t1 = paged(client, "/closed-positions", {"user": wallet, "sortBy": "REALIZEDPNL",
                                                   "sortDirection": "DESC"}, half, page=50)
    worst, t2 = ([], False) if not t1 else paged(
        client, "/closed-positions", {"user": wallet, "sortBy": "REALIZEDPNL",
                                      "sortDirection": "ASC"}, half, page=50)
    seen, closed = set(), []
    for r in best + worst:
        k = (r.get("conditionId"), r.get("asset") or r.get("outcomeIndex"))
        if k not in seen:
            seen.add(k)
            closed.append(r)
    closed_trunc = t1 and t2
    # Losing positions are never "closed": they resolve to $0 and stay in
    # /positions unredeemed. Read those worst-first so a cap keeps the losses.
    opened, open_trunc = paged(client, "/positions", {
        "user": wallet, "sizeThreshold": 0.01, "sortBy": "CASHPNL",
        "sortDirection": "ASC"}, caps["closed"], page=500)
    trades_all, _ = paged(client, "/trades", {"user": wallet, "takerOnly": "false"},
                          caps["trades"])
    trades_taker, _ = paged(client, "/trades", {"user": wallet, "takerOnly": "true"},
                            caps["trades"])
    acts = {}
    for t in ("REWARD", "MERGE", "SPLIT", "CONVERSION", "REDEEM"):
        cap = caps["rewards"] if t == "REWARD" else caps["events"]
        acts[t], acts[t + "_truncated"] = paged(client, "/activity",
                                                {"user": wallet, "type": t}, cap)
    return {"wallet": wallet, "closed": closed, "closed_truncated": closed_trunc,
            "open": opened, "open_truncated": open_trunc, "trades_all": trades_all, "trades_taker": trades_taker,
            "activity": acts}
