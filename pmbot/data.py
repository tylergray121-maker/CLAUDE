"""Market data: Polymarket US (where we trade) and international (reference).

Only public endpoints are used here. Shapes follow the official
``polymarket-us`` SDK and responses probed from the live APIs; parsers are
defensive and drop records they can't read.
"""

from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime

from copybt.api import Client, HTTPError

from .broker import Quote

log = logging.getLogger(__name__)

US_GATEWAY = "https://gateway.polymarket.us"
GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"

# Season-long or election markets: their gameStartTime is not a kickoff.
LONG_RUNNING = {"futures", "election"}


def amount(a) -> float | None:
    if isinstance(a, dict):
        a = a.get("value")
    try:
        return float(a)
    except (TypeError, ValueError):
        return None


def parse_time(s) -> float | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _json_list(v) -> list:
    if isinstance(v, list):
        return v
    try:
        out = json.loads(v) if isinstance(v, str) else []
        return out if isinstance(out, list) else []
    except json.JSONDecodeError:
        return []


@dataclass
class USMarket:
    slug: str
    question: str          # event-level, e.g. "World Series Champion"
    title: str             # outcome, e.g. "Milwaukee Brewers"
    description: str
    market_type: str       # futures | election | moneyline | ...
    category: str
    game_start: float | None
    end: float | None
    tick: float
    status: str
    bid: float | None
    ask: float | None

    def tradable(self, now: float, pre_game_s: float = 600,
                 min_to_end_s: float = 3600) -> tuple[bool, str]:
        if self.status not in ("MARKET_STATUS_OPEN", ""):
            return False, self.status.lower()
        if self.end and self.end - now < min_to_end_s:
            return False, "closing soon"
        if (self.market_type not in LONG_RUNNING and self.game_start
                and now > self.game_start - pre_game_s):
            return False, "in-play"
        return True, ""


def parse_us_market(m: dict) -> USMarket | None:
    slug = m.get("slug")
    if not slug or m.get("closed") or m.get("archived") or m.get("hidden"):
        return None
    return USMarket(
        slug=slug, question=str(m.get("question") or ""),
        title=str(m.get("title") or m.get("titleShort") or ""),
        description=str(m.get("description") or ""),
        market_type=str(m.get("marketType") or m.get("sportsMarketType") or ""),
        category=str(m.get("category") or ""),
        game_start=parse_time(m.get("gameStartTime")), end=parse_time(m.get("endDate")),
        tick=float(m.get("orderPriceMinTickSize") or 0.01),
        status=str(m.get("status") or ""),
        bid=amount(m.get("bestBidQuote")), ask=amount(m.get("bestAskQuote")))


def us_markets(client: Client, page: int = 100, max_pages: int = 300) -> list[USMarket]:
    out, seen = [], set()
    for i in range(max_pages):
        try:
            rows = (client.get(US_GATEWAY, "/v1/markets", {
                "active": "true", "closed": "false", "limit": page,
                "offset": i * page}, use_cache=False) or {}).get("markets", [])
        except HTTPError as e:
            log.warning("US markets page %d: %s", i, e)
            break
        new = 0
        for r in rows:
            m = parse_us_market(r)
            if m and m.slug not in seen:
                seen.add(m.slug)
                out.append(m)
                new += 1
        if len(rows) < page or not new:
            break
    log.info("Polymarket US: %d open markets", len(out))
    return out


def us_quote(client: Client, slug: str) -> tuple[Quote, str] | None:
    """Best bid/ask with sizes from the order book, plus market state."""
    try:
        md = (client.get(US_GATEWAY, f"/v1/markets/{slug}/book", use_cache=False)
              or {}).get("marketData") or {}
    except HTTPError as e:
        log.debug("US book %s: %s", slug, e)
        return None
    bids = [(amount(l.get("px")), float(l.get("qty") or 0)) for l in md.get("bids") or []]
    asks = [(amount(l.get("px")), float(l.get("qty") or 0)) for l in md.get("offers") or []]
    bids = [b for b in bids if b[0] is not None]
    asks = [a for a in asks if a[0] is not None]
    bb = max(bids, default=(None, 0.0))
    ba = min(asks, default=(None, 0.0))
    stats = md.get("stats") or {}
    q = Quote(bid=bb[0], ask=ba[0], bid_qty=bb[1], ask_qty=ba[1],
              last_px=amount(stats.get("lastTradePx")),
              traded=float(stats.get("sharesTraded") or 0), ts=time.time())
    return q, str(md.get("state") or "")


def us_settlement(client: Client, slug: str) -> float | None:
    try:
        return amount((client.get(US_GATEWAY, f"/v1/markets/{slug}/settlement",
                                  use_cache=False) or {}).get("settlement"))
    except HTTPError:
        return None


@dataclass
class IntlOption:
    """One tradeable outcome token on the international exchange."""
    token: str
    label: str        # team / candidate / outcome name
    question: str
    event: str
    end: float | None
    bid: float | None
    ask: float | None
    volume24h: float


def parse_intl_market(m: dict) -> list[IntlOption]:
    if m.get("closed") or not m.get("active") or m.get("enableOrderBook") is False:
        return []
    tokens = [str(t) for t in _json_list(m.get("clobTokenIds"))]
    outcomes = [str(o) for o in _json_list(m.get("outcomes"))]
    if not tokens or len(tokens) != len(outcomes):
        return []
    events = m.get("events") or []
    event = str((events[0] or {}).get("title") or "") if events else ""
    common = dict(question=str(m.get("question") or ""), event=event,
                  end=parse_time(m.get("endDate")),
                  volume24h=float(m.get("volume24hr") or 0))
    lower = [o.lower() for o in outcomes]
    if lower == ["yes", "no"] or lower == ["no", "yes"]:
        label = str(m.get("groupItemTitle") or m.get("question") or "")
        return [IntlOption(tokens[lower.index("yes")], label,
                           bid=_f(m.get("bestBid")), ask=_f(m.get("bestAsk")), **common)]
    # Head-to-head style ("Avalanche" vs "Flyers"): one option per outcome.
    # Gamma's bestBid/bestAsk refer to the first outcome only.
    return [IntlOption(t, o, bid=None, ask=None, **common)
            for t, o in zip(tokens, outcomes)]


def _f(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def intl_options(client: Client, page: int = 500, max_pages: int = 200,
                 min_volume24h: float = 0.0) -> list[IntlOption]:
    keep = ("question", "groupItemTitle", "clobTokenIds", "outcomes", "endDate",
            "events", "bestBid", "bestAsk", "volume24hr", "closed", "active",
            "enableOrderBook")
    out = []
    for i in range(max_pages):
        try:
            rows = client.get(GAMMA, "/markets", {
                "active": "true", "closed": "false", "limit": page,
                "offset": i * page}, use_cache=False, keep=keep) or []
        except HTTPError as e:
            log.warning("intl markets page %d: %s", i, e)
            break
        for r in rows:
            if isinstance(r.get("events"), list):  # keep only the event title
                r["events"] = [{"title": (e or {}).get("title")} for e in r["events"][:1]]
            out += [o for o in parse_intl_market(r) if o.volume24h >= min_volume24h]
        if len(rows) < page:
            break
    log.info("international: %d active outcome tokens", len(out))
    return out


def intl_book(client: Client, token: str) -> tuple[float | None, float | None, float]:
    """(best bid, best ask, spread) from the CLOB book; spread inf if one-sided."""
    try:
        b = client.get(CLOB, "/book", {"token_id": token}, use_cache=False) or {}
    except HTTPError:
        return None, None, float("inf")
    bids = [_f(l.get("price")) for l in b.get("bids") or []]
    asks = [_f(l.get("price")) for l in b.get("asks") or []]
    bid = max((x for x in bids if x is not None), default=None)
    ask = min((x for x in asks if x is not None), default=None)
    spread = ask - bid if bid is not None and ask is not None else float("inf")
    return bid, ask, spread


def fetch_parallel(fn, items, workers: int = 8) -> list:
    with ThreadPoolExecutor(workers) as pool:
        return list(pool.map(fn, items))

