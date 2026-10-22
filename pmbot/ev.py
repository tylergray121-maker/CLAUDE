"""+EV sniper: buy Polymarket US game lines priced below the sharp line.

Fair value comes from Pinnacle, the sharpest sportsbook, through The Odds
API (https://the-odds-api.com, key in ODDS_API_KEY): its two-way moneyline
odds are de-vigged (each side's implied probability divided by their sum).
A US game market is bought, on either side, when its ask is below that fair
probability by more than the taker fee plus a margin, before the game
starts. Odds are polled per sport within a monthly request budget; the free
key has 500 requests a month, so polls are spaced to fit it.

Only game-winner (moneyline) markets of two-outcome sports are traded: a
soccer draw makes the "No" side of a US result market a different bet from
the other team winning.
"""

from __future__ import annotations

import calendar
import json
import logging
import time
import urllib.parse
import urllib.request
from collections import Counter

from .broker import SHORT
from .fees import taker_fee_per_contract
from .strategies import Strategy
from .strategy import MarketView, Order, StrategyConfig

log = logging.getLogger(__name__)

ODDS_API = "https://api.the-odds-api.com/v4"
# Polymarket league prefix -> The Odds API sport key (two-outcome sports only).
SPORTS = {"nba": "basketball_nba", "nfl": "americanfootball_nfl", "nhl": "icehockey_nhl",
          "mlb": "baseball_mlb", "cfb": "americanfootball_ncaaf", "cbb": "basketball_ncaab",
          "wnba": "basketball_wnba"}
STAT_KEYS = ("odds_requests", "odds_errors", "events_priced", "markets_matched",
             "edges_seen", "bought", "skip_no_room", "skip_recently_bought", "skip_price_band")


def devig(prices: list[float]) -> list[float]:
    """Fair probabilities from decimal odds, margin removed proportionally."""
    implied = [1.0 / p for p in prices if p and p > 1.0]
    if len(implied) != len(prices) or not implied:
        return []
    total = sum(implied)
    return [x / total for x in implied]


def _team_match(label: str, full_name: str) -> bool:
    """US labels are nicknames ('Bucks', '76ers'); the feed has full names
    ('Milwaukee Bucks'). Match on the whole nickname word(s)."""
    label, full = label.strip().lower(), f" {full_name.strip().lower()} "
    return bool(label) and f" {label} " in full


def match_events(events: list[dict], us_markets: list, slack_s: float = 3 * 3600) -> dict[str, float]:
    """US slug (or slug + SHORT) -> Pinnacle fair probability of that side."""
    out: dict[str, float] = {}
    for m in us_markets:
        if not (m.long_label and m.short_label and m.game_start):
            continue
        for ev in events:
            try:
                start = calendar.timegm(time.strptime(ev["commence_time"], "%Y-%m-%dT%H:%M:%SZ"))
            except (KeyError, ValueError, TypeError):
                continue
            if abs(start - m.game_start) > slack_s:
                continue
            home, away = ev.get("home_team", ""), ev.get("away_team", "")
            names = {home, away}
            if not any(_team_match(m.long_label, n) for n in names) or \
                    not any(_team_match(m.short_label, n) for n in names):
                continue
            book = next((b for b in ev.get("bookmakers") or [] if b.get("key") == "pinnacle"), None)
            mk = next((x for x in (book or {}).get("markets") or [] if x.get("key") == "h2h"), None)
            outs = (mk or {}).get("outcomes") or []
            if len(outs) != 2:
                continue
            fair = devig([float(o.get("price") or 0) for o in outs])
            if not fair:
                continue
            for o, p in zip(outs, fair):
                if _team_match(m.long_label, o.get("name", "")):
                    out[m.slug] = p
                elif _team_match(m.short_label, o.get("name", "")):
                    out[m.slug + SHORT] = p
            break
    return out


class EVSniper(Strategy):
    name = "evsniper"

    def __init__(self, cfg: StrategyConfig, api_key: str, min_edge: float = 0.02,
                 monthly_budget: int = 450, poll_floor_s: float = 300,
                 rebuy_s: float = 3600, fetch=None):
        self.cfg, self.api_key, self.min_edge = cfg, api_key, min_edge
        self.monthly_budget, self.poll_floor_s, self.rebuy_s = monthly_budget, poll_floor_s, rebuy_s
        self.fetch = fetch or self._fetch
        self.fair: dict[str, tuple[float, float]] = {}   # slug -> (fair prob, when priced)
        self.next_poll: dict[str, float] = {}            # sport -> next poll time
        self.bought: dict[str, float] = {}               # slug -> last buy time
        self.used: dict[str, int] = {}                   # "YYYY-MM" -> requests used
        self.stats: Counter = Counter({k: 0 for k in STAT_KEYS})
        self.last_edges: list[dict] = []
        self.closest: dict[str, dict] = {}     # slug -> its best edge so far, under the bar too
        self.checked: dict[str, float] = {}              # slug -> last time its book was read
        self.check_s = 30

    # -- odds feed ---------------------------------------------------------------
    def _fetch(self, sport: str) -> list[dict] | None:
        q = urllib.parse.urlencode({"apiKey": self.api_key, "regions": "eu", "markets": "h2h",
                                    "oddsFormat": "decimal", "bookmakers": "pinnacle"})
        try:
            with urllib.request.urlopen(f"{ODDS_API}/sports/{sport}/odds?{q}", timeout=15) as r:
                return json.loads(r.read())
        except Exception as e:  # never log the URL: it carries the key
            log.warning("odds feed %s: %s", sport, type(e).__name__)
            return None

    def _interval(self, n_sports: int, now: float) -> float:
        """Seconds between polls of one sport so the month's budget lasts."""
        tm = time.gmtime(now)
        days_left = max(1, 31 - tm.tm_mday + 1)
        left = max(0, self.monthly_budget - self.used.get(time.strftime("%Y-%m", tm), 0))
        per_day = left / days_left
        if per_day <= 0:
            return float("inf")
        return max(self.poll_floor_s, 86400 * max(1, n_sports) / per_day)

    def _refresh(self, eng, now: float) -> None:
        upcoming = [m for m in eng.markets.values() if m.market_type == "moneyline"
                    and m.game_start and 600 < m.game_start - now <= 36 * 3600]
        by_sport: dict[str, list] = {}
        for m in upcoming:
            lg = m.slug.split("-")[1] if m.slug.count("-") > 2 else ""
            if lg in SPORTS:
                by_sport.setdefault(SPORTS[lg], []).append(m)
        gap = self._interval(len(by_sport), now)
        month = time.strftime("%Y-%m", time.gmtime(now))
        for sport, ms in by_sport.items():
            if now < self.next_poll.get(sport, 0):
                continue
            self.next_poll[sport] = now + gap
            events = self.fetch(sport)
            self.used[month] = self.used.get(month, 0) + 1
            self.stats["odds_requests"] += 1
            if events is None:
                self.stats["odds_errors"] += 1
                continue
            self.stats["events_priced"] += len(events)
            fair = match_events(events, ms)
            self.stats["markets_matched"] += len(fair)
            for slug, p in fair.items():
                self.fair[slug] = (p, now)
        # Forget fair values that are stale or for games about to start.
        for slug in list(self.fair):
            base = slug[:-len(SHORT)] if slug.endswith(SHORT) else slug
            m = eng.markets.get(base)
            if m is None or not m.game_start or m.game_start - now < 600 \
                    or now - self.fair[slug][1] > 3 * max(gap, 1800):
                del self.fair[slug]

    def watch(self, eng, now):
        if self.api_key:
            self._refresh(eng, now)
        due = {s for s in self.fair if now - self.checked.get(s, 0) >= self.check_s}
        for s in due:
            self.checked[s] = now
        return due

    # -- orders --------------------------------------------------------------------
    def orders(self, eng, views: dict[str, MarketView], now):
        out: dict[str, list[Order]] = {}
        for slug, (p, _) in self.fair.items():
            v = views.get(slug)
            if v is None or not v.tradable or v.us_ask is None:
                continue
            ask = v.us_ask
            edge = p - ask - taker_fee_per_contract(ask)
            if edge > self.closest.get(slug, {}).get("edge", -9):
                self.closest[slug] = {"slug": slug, "fair": round(p, 4), "ask": ask,
                                      "edge": round(edge, 4), "ts": int(now)}
                if len(self.closest) > 200:
                    del self.closest[min(self.closest, key=lambda k: self.closest[k]["edge"])]
            if edge < self.min_edge:
                continue
            self.stats["edges_seen"] += 1
            self.last_edges = ([{"slug": slug, "fair": round(p, 4), "ask": ask,
                                 "edge": round(edge, 4), "ts": int(now)}] + self.last_edges)[:20]
            if not self.cfg.min_price <= ask <= self.cfg.max_price:
                self.stats["skip_price_band"] += 1
                continue
            if now - self.bought.get(slug, 0) < self.rebuy_s:
                self.stats["skip_recently_bought"] += 1
                continue
            base = slug[:-len(SHORT)] if slug.endswith(SHORT) else slug
            if eng.held(base if slug.endswith(SHORT) else base + SHORT) > 0:
                continue  # never both sides of a game
            qty = min(int(min(self.cfg.order_usd, eng.room(slug)) // ask), int(v.us_ask_qty))
            if qty < 1:
                self.stats["skip_no_room"] += 1
                continue
            self.stats["bought"] += 1
            self.bought[slug] = now
            eng._log("ev_buy", slug=slug, fair=round(p, 4), ask=ask, edge=round(edge, 4), qty=qty)
            out[slug] = [Order("BUY", ask, qty, post_only=False)]
        return out

    def to_state(self) -> dict:
        return {"used": self.used, "bought": self.bought}

    def load_state(self, d: dict) -> None:
        self.used = {k: int(v) for k, v in d.get("used", {}).items()}
        self.bought = {k: float(v) for k, v in d.get("bought", {}).items()}

    def summary(self) -> dict:
        month = time.strftime("%Y-%m", time.gmtime())
        return {"evsniper_requests_this_month": self.used.get(month, 0),
                "evsniper_budget": self.monthly_budget,
                "evsniper_fair_markets": len(self.fair),
                "evsniper_last_edges": "; ".join(
                    f"{e['slug']} fair {e['fair']:.3f} ask {e['ask']:.2f} edge {e['edge']:+.3f}"
                    for e in self.last_edges[:5]),
                # How near it gets: the best edges seen, above or below the bar.
                "evsniper_closest": "; ".join(
                    f"{e['slug']} fair {e['fair']:.3f} ask {e['ask']:.2f} edge {e['edge']:+.3f}"
                    for e in sorted(self.closest.values(), key=lambda e: -e["edge"])[:5])}
