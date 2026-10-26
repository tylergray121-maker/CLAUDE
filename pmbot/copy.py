"""Copy the most profitable active sports wallets onto Polymarket US.

The leaders (pmbot/leaders.json, chosen from the top-wallet study) trade on
international Polymarket, whose trades are public. Each cycle this polls
their newest trades; a buy of an outcome that maps to a Polymarket US
market (a verified pair, or the same game/spread/total market by slug, on
either side) becomes a taker buy on US, at
no more than the leader's price plus a small allowance, so the bot never
chases a price that has moved. Copies are held to settlement: in the
backtest (pmbot/select.py) copying the leaders' sells did worse in both
windows, so that is off by default (``copy_sells``). With
``conviction_sizing`` the stake follows how big the bet is for that leader.

Every copy is scored (pmbot/track.py) against the wallet it copied and the
kind of bet it was. A wallet is benched (its buys no longer copied; its
sells still are, to exit) when its own Polymarket results turn: losing this
week and at least 2c per dollar traded over the month, or when our copies
of it are clearly losing. A losing week alone only flags it as cooling off.
A pattern (league, market type, price band, pre-game or in-play) is skipped
when its copies are clearly losing. Both lift by themselves if things turn.
"""

from __future__ import annotations

import json
import logging
import math
import re
import time
from collections import Counter, deque
from statistics import median

from copybt.api import DATA_API

from .broker import SHORT, split_side
from .data import FETCH_ERRORS, fetch_parallel
from .mapping import prices_agree
from .strategies import Strategy
from .strategy import MarketView, Order, StrategyConfig
from .track import Scorecard, clearly_losing

log = logging.getLogger(__name__)

MARKOUTS = (("mo30", 1800), ("mo120", 7200))   # name, seconds after our fill


def markout_stats(xs: list[float]) -> dict:
    """Mean markout in cents of price, how many, and its t-statistic."""
    n = len(xs)
    if not n:
        return {"c": None, "n": 0, "t": None}
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / (n - 1) if n >= 2 else 0.0
    t = mean / math.sqrt(var / n) if var > 0 else None
    return {"c": round(mean * 100, 2), "n": n, "t": round(t, 2) if t is not None else None}


def load_leaders(path: str) -> dict[str, str]:
    with open(path) as f:
        d = json.load(f)
    return {x["wallet"].lower(): x.get("name") or x["wallet"][:10] for x in d["leaders"]}


STAT_KEYS = ("leader_trades", "mapped", "mapped_short_side", "not_on_polymarket_us",
             "listed_side_unknown", "copied_buys", "copied_sells", "expired_price_moved",
             "skip_repeat", "skip_recently_copied", "skip_tiny", "skip_not_open",
             "skip_price_band", "skip_prices_disagree", "skip_no_room_or_size",
             "skip_holding_other_side", "skip_exit_price", "skip_benched_wallet",
             "skip_losing_pattern", "skip_stale", "sells_not_copied", "skip_wallet_cap",
             "poll_errors")
_GAME = re.compile(r"^([a-z0-9]+)-.*\d{4}-\d{2}-\d{2}")
FEED_KEEP = 400                      # the leaders' latest bets shown on the dashboard
TOO_SMALL, WAITING = "too small to copy", "waiting for our price"


def league(intl_slug: str) -> str:
    """'mlb-nyy-bos-2026-10-21-total-8pt5' -> 'mlb'; season-long markets -> 'futures'."""
    m = _GAME.match(intl_slug)
    return m.group(1) if m else "futures"


def price_band(p: float) -> str:
    return "under 30c" if p < 0.30 else "over 70c" if p > 0.70 else "30-70c"


def _usd(v: float) -> str:
    return ("−" if v < 0 else "+") + f"${abs(v):,.0f}"


class CopyTop(Strategy):
    name = "copytop"

    def __init__(self, cfg: StrategyConfig, leaders: dict[str, str], max_slip: float = 0.01,
                 signal_ttl_s: float = 180, dedupe_s: float = 600, min_leader_usd: float = 5.0,
                 form_every_s: float = 7200, min_wallet_n: int = 10, min_pattern_n: int = 15,
                 copy_sells: bool = False, conviction_sizing: bool = False,
                 max_wallet_usd: float = 0.0, min_price: float = 0.0):
        self.cfg = cfg
        self.min_price = min_price                 # copies only; other strategies keep theirs
        self.leaders = leaders
        self.max_slip = max_slip
        self.signal_ttl_s = signal_ttl_s
        self.dedupe_s = dedupe_s
        self.min_leader_usd = min_leader_usd
        self.last_ts: dict[str, int] = {}          # leader -> newest trade timestamp seen
        self.pending: dict[str, dict] = {}         # US slug -> signal
        self.recent: dict[tuple, float] = {}       # (leader, slug, side) -> when copied
        self.seen_tx: set[tuple] = set()           # (leader, tx, asset): one order, many fills
        self.stats: Counter = Counter({k: 0 for k in STAT_KEYS})
        self.form_every_s = form_every_s
        self.min_wallet_n, self.min_pattern_n = min_wallet_n, min_pattern_n
        self.card = Scorecard()
        self.form: dict[str, dict] = {}            # leader -> their own recent Polymarket results
        self.status: dict[str, list] = {}          # leader -> [copying|cooling|benched, why]
        self.skipped: dict[str, str] = {}          # pattern key -> why it is skipped
        self._placing: dict[str, list[str]] = {}   # slug -> scorecard keys of the copy just sent
        self._selling: dict[str, str] = {}         # slug -> wallet key whose copies are being sold
        self._next_form = 0.0
        self.lags: deque = deque(maxlen=500)       # seconds from their trade to our order
        self.copy_sells, self.conviction_sizing = copy_sells, conviction_sizing
        # Most money open copying any one wallet (0 = no cap), so one wallet's
        # big swings (a whale's losing streak) can't dominate the account.
        self.max_wallet_usd = max_wallet_usd
        self.sizes: dict[str, deque] = {}          # leader -> their recent buy sizes ($)
        self.unmapped: Counter = Counter()         # (intl slug, outcome) not on US, for diagnostics
        self.max_age_s = 300                       # never copy a trade older than this
        # Markouts: how far the price moved our way 30 min and 2 h after each
        # copy fill (mid minus our price, per contract), by wallet and pattern.
        # Evidence of information long before settlements can tell.
        self.marking: list[dict] = []              # fills still waiting for a markout
        self.mo: dict[str, dict[str, list[float]]] = {h: {} for h, _ in MARKOUTS}
        self._settled: dict[str, float] = {}       # slug -> settlement price, for markouts
        # The leaders' bets as the bot saw them and what it did with each, for
        # the dashboard's feed: one entry per order (its later fills add to it).
        self.feed: deque = deque(maxlen=FEED_KEEP)
        self._feed_n = 0

    # -- signals ------------------------------------------------------------
    def _fetch(self, eng, wallet: str) -> list[dict] | None:
        try:
            return eng.client.get(DATA_API, "/trades", {"user": wallet, "limit": 50,
                                                        "takerOnly": "false"},
                                  use_cache=False) or []
        except FETCH_ERRORS as e:
            log.debug("leader %s trades: %s", wallet, e)
            return None

    def _new_trades(self, wallet: str, rows: list[dict] | None) -> list[dict]:
        if rows is None:
            self.stats["poll_errors"] += 1
            return []
        rows = [r for r in rows if isinstance(r, dict) and r.get("timestamp")]
        newest = max((int(r["timestamp"]) for r in rows), default=0)
        first = wallet not in self.last_ts
        since = self.last_ts.get(wallet, newest)
        self.last_ts[wallet] = max(since, newest)
        fresh = sorted((r for r in rows if first or int(r["timestamp"]) > since),
                       key=lambda r: int(r["timestamp"]))
        sizes = self.sizes.setdefault(wallet, deque(maxlen=200))
        for r in fresh:  # their usual bet size, for conviction
            try:
                if str(r.get("side", "")).upper() == "BUY":
                    sizes.append(float(r["price"]) * float(r["size"]))
            except (KeyError, TypeError, ValueError):
                pass
        return [] if first else fresh  # baseline: never copy trades from before we watched

    def _note(self, wallet: str, name: str, t: dict) -> dict:
        """The feed entry for a leader trade: fills of one bet (the same outcome
        and side within a minute) are one entry, at their average price. A later
        fill returns {} so the earlier decision stands, unless that was still
        open (too small to judge, or waiting for our price)."""
        try:
            qty = float(t["size"])
            usd = float(t["price"]) * qty
        except (KeyError, TypeError, ValueError):
            qty = usd = 0.0
        ts, side = int(t["timestamp"]), str(t.get("side", "")).upper()
        key = f"{wallet}|{t.get('asset')}|{side}"
        for e in reversed(self.feed):
            if e["key"] == key and abs(ts - e["ts"]) <= 60:
                e["qty"] = round(e.get("qty", 0) + qty, 4)
                e["usd"] = round(e["usd"] + usd, 2)
                e["price"] = round(e["usd"] / e["qty"], 4) if e["qty"] else e["price"]
                return e if e["action"] in (TOO_SMALL, WAITING) else {}
        self._feed_n += 1
        e = {"key": key, "id": f"lt{self._feed_n}", "ts": ts, "leader": name,
             "market": str(t.get("title") or t.get("slug") or ""),
             "outcome": str(t.get("outcome") or ""), "side": side,
             "price": round(usd / qty, 4) if qty else 0.0, "qty": round(qty, 4),
             "usd": round(usd, 2), "league": league(str(t.get("slug") or "")), "action": ""}
        self.feed.append(e)
        return e

    @staticmethod
    def _decide(sig: dict, action: str, **more) -> None:
        """Record on the feed what became of a signal."""
        if sig.get("feed") is not None:
            sig["feed"].update(action=action, **more)

    def conviction(self, wallet: str, usd: float) -> float:
        """This bet's size relative to the leader's usual (median recent) buy."""
        sizes = self.sizes.get(wallet)
        usual = median(sizes) if sizes else 0.0
        return usd / usual if usual > 0 else 1.0

    def watch(self, eng, now):
        self._markouts(eng, now)
        if now >= self._next_form:
            self._check_form(eng)
            self._judge(eng)
            self._next_form = now + self.form_every_s
        index = eng.token_index()
        wallets = list(self.leaders)
        polled = fetch_parallel(lambda w: self._fetch(eng, w), wallets, workers=8)
        for wallet, rows in zip(wallets, polled):
            name = self.leaders[wallet]
            for t in self._new_trades(wallet, rows):
                self.stats["leader_trades"] += 1
                entry = self._note(wallet, name, t)
                slug = eng.us_for_trade(t, index)
                if not slug:
                    if eng.lists(str(t.get("slug") or "")):
                        self.stats["listed_side_unknown"] += 1  # outcome names differ
                        entry["action"] = "on US, but its side didn't match"
                    else:
                        self.stats["not_on_polymarket_us"] += 1
                        self.stats[f"missed_{league(str(t.get('slug') or ''))}"] += 1
                        entry["action"] = "not on Polymarket US"
                    self.unmapped[(str(t.get("slug") or ""), str(t.get("outcome") or ""))] += 1
                    if len(self.unmapped) > 2000:
                        self.unmapped = Counter(dict(self.unmapped.most_common(500)))
                    eng._log("copy_unmapped", leader=name, market=t.get("title"),
                             intl_slug=t.get("slug"), outcome=t.get("outcome"))
                    continue
                self.stats["mapped"] += 1
                if slug.endswith(SHORT):
                    self.stats["mapped_short_side"] += 1
                side = str(t.get("side", "")).upper()
                try:
                    price, size = float(t["price"]), float(t["size"])
                except (KeyError, TypeError, ValueError):
                    continue
                if side == "BUY" and price * size < self.min_leader_usd:
                    self.stats["skip_tiny"] += 1
                    entry["action"] = TOO_SMALL
                    continue
                if now - int(t["timestamp"]) > self.max_age_s:
                    self.stats["skip_stale"] += 1   # e.g. placed while the bot restarted
                    entry["action"] = "too old to copy"
                    continue
                if side == "SELL" and not self.copy_sells:
                    self.stats["sells_not_copied"] += 1  # held to settlement
                    entry["action"] = "a sale (copies are held to settlement)"
                    continue
                if side == "BUY" and self.status.get(wallet, ["copying"])[0] == "benched":
                    self.stats["skip_benched_wallet"] += 1
                    entry["action"] = "wallet benched"
                    continue
                tx = (wallet, t.get("transactionHash"), t.get("asset"))
                if t.get("transactionHash") and tx in self.seen_tx:
                    self.stats["skip_repeat"] += 1  # another fill of an order already seen
                    continue
                self.seen_tx.add(tx)
                key = (wallet, slug, side)
                if now - self.recent.get(key, 0) < self.dedupe_s:
                    self.stats["skip_recently_copied"] += 1
                    entry["action"] = "already copied this market"
                    continue
                if slug in self.pending:
                    self._decide(self.pending[slug], "replaced by a newer bet on it")
                entry["action"] = WAITING
                self.pending[slug] = {"side": side, "price": price, "leader": name,
                                      "wallet": wallet, "at": now,
                                      "trade_ts": int(t["timestamp"]),
                                      "leader_usd": round(price * size, 2),
                                      "conviction": round(self.conviction(wallet, price * size), 2),
                                      "league": league(str(t.get("slug") or "")),
                                      "feed": entry or None}
                eng._log("copy_signal", slug=slug, side=side, leader=name, price=price,
                         leader_usd=round(price * size, 2), market=t.get("title"))
        for slug in [s for s, sig in self.pending.items() if now - sig["at"] > self.signal_ttl_s]:
            self.stats["expired_price_moved"] += 1
            self._decide(self.pending.pop(slug), "price moved away; not copied")
        return set(self.pending) | {m["slug"] for m in self.marking}

    def _markouts(self, eng, now: float) -> None:
        """Record each due markout from the market's mid (its payout once
        settled); one more than 15 minutes overdue without a price is dropped."""
        keep = []
        for m in self.marking:
            for h, after in MARKOUTS:
                if h not in m["todo"] or now < m["ts"] + after:
                    continue
                px = self._settled.get(m["slug"], eng.marks.get(m["slug"]))
                if px is None and now < m["ts"] + after + 900:
                    continue
                m["todo"].remove(h)
                if px is None:
                    continue
                for k in [*m["keys"], "all"]:
                    r = self.mo[h].setdefault(k, [])
                    r.append(round(px - m["px"], 4))
                    del r[:-self.card.keep]
            if m["todo"]:
                keep.append(m)
        self.marking = keep
        waiting = {m["slug"] for m in keep}
        self._settled = {s: p for s, p in self._settled.items() if s in waiting}

    def markouts(self, key: str) -> dict:
        out = {}
        for h, _ in MARKOUTS:
            st = markout_stats(self.mo[h].get(key, []))
            out[f"{h}_c"], out[f"{h}_n"] = st["c"], st["n"]
            if h == "mo120":
                out["mo120_t"] = st["t"]
        return out

    # -- orders ---------------------------------------------------------------
    def orders(self, eng, views: dict[str, MarketView], now):
        out: dict[str, list[Order]] = {}
        for slug, sig in list(self.pending.items()):
            v = views.get(slug)
            if v is None:
                continue
            if v.note not in ("", "in-play"):  # closed, suspended, closing soon...
                self.stats["skip_not_open"] += 1
                self._decide(sig, "market not open on US")
                del self.pending[slug]
                continue
            if sig["side"] == "BUY":
                base, short = split_side(slug)
                if eng.held(base if short else base + SHORT) > 0:
                    self.stats["skip_holding_other_side"] += 1  # would only lock in a loss
                    self._decide(sig, "we hold the other side")
                    del self.pending[slug]
                    continue
                # Round down to the market's tick: the exchange rejects off-tick prices.
                tick = v.tick or 0.01
                limit = round(int(min(sig["price"] + self.max_slip, self.cfg.max_price) / tick
                                  + 1e-9) * tick, 4)
                ask = v.us_ask
                if ask is None or ask > limit:
                    continue  # keep waiting until the signal expires
                floor = max(self.cfg.min_price, self.min_price)
                if ask < floor:
                    self.stats["skip_price_band"] += 1
                    self._decide(sig, f"under the {100 * floor:.0f}¢ floor")
                    del self.pending[slug]
                    continue
                if not prices_agree(ask, sig["price"]):
                    self.stats["skip_prices_disagree"] += 1  # likely not the same bet
                    self._decide(sig, "US price too different (likely not the same bet)")
                    del self.pending[slug]
                    continue
                c = sig.get("conviction", 1.0)
                keys = [f"w:{sig['wallet']}", f"league:{sig.get('league', 'other')}",
                        f"kind:{v.market_type or 'other'}", f"price:{price_band(ask)}",
                        f"timing:{'in-play' if v.note == 'in-play' else 'pre-game'}",
                        "conviction:" + ("under 0.5x" if c < 0.5 else "0.5-2x" if c < 2 else "2x+")]
                losing = [k for k in keys if k in self.skipped]
                if losing:
                    self.stats["skip_losing_pattern"] += 1
                    self._decide(sig, f"losing pattern skipped ({losing[0]})")
                    del self.pending[slug]
                    continue
                stake = self.cfg.order_usd
                if self.conviction_sizing:
                    stake *= 0.5 if c < 0.5 else 1.5 if c >= 2 else 1.0
                if self.max_wallet_usd > 0:
                    left = self.max_wallet_usd - self.card.summary(f"w:{sig['wallet']}")["open_usd"]
                    if left < ask:
                        self.stats["skip_wallet_cap"] += 1
                        self._decide(sig, "this wallet's cap is used up")
                        del self.pending[slug]
                        continue
                    stake = min(stake, left)
                qty = min(int(min(stake, eng.room(slug)) // ask), int(v.us_ask_qty))
                del self.pending[slug]
                if qty < 1:
                    self.stats["skip_no_room_or_size"] += 1
                    self._decide(sig, "no cash or room left to copy")
                    continue
                self.stats["copied_buys"] += 1
                self._decide(sig, "copied", our_price=ask, our_qty=qty)
                self.recent[(sig["wallet"], slug, "BUY")] = now
                self._placing[slug] = keys
                self.lags.append(now - sig.get("trade_ts", now))
                out[slug] = [Order("BUY", limit, qty, post_only=False)]
            else:
                held = eng.held(slug)
                del self.pending[slug]
                # Only the contracts bought copying this wallet (all of them for a
                # position from before the scorecard existed).
                who = f"w:{sig['wallet']}"
                mine = self.card.qty_for(slug, who) if self.card.lots.get(slug) else held
                qty = min(held, mine, int(v.us_bid_qty or 0))
                if qty < 1 or v.us_bid is None:
                    self._decide(sig, "a sale; we hold none of this copy")
                    continue
                tick = v.tick or 0.01
                floor = round(max(-int(-(sig["price"] - self.max_slip) / tick + 1e-9) * tick,
                                  tick), 4)
                if v.us_bid < floor:
                    self.stats["skip_exit_price"] += 1
                    self._decide(sig, "a sale; the US bid is under their price")
                    continue
                self.stats["copied_sells"] += 1
                self._decide(sig, "sold our copy", our_price=v.us_bid, our_qty=qty)
                if self.card.lots.get(slug):
                    self._selling[slug] = who
                out[slug] = [Order("SELL", floor, qty, post_only=False)]
        return out

    # -- scoring ----------------------------------------------------------------
    def on_fills(self, eng, fills) -> None:
        """Credit this cycle's copy fills, sells and settlements to the scorecard."""
        closed = False
        for f in fills:
            if f.tag != self.name:
                continue
            if getattr(f, "note", "") == "hand":
                # Cashed out by the owner: says nothing about the leader.
                self.card.drop(f.slug, f.qty)
                continue
            if f.side == "SETTLE":
                self._settled[f.slug] = f.price
            if f.side == "BUY" and f.slug in self._placing:
                self.card.open(f.slug, self._placing[f.slug], f.qty, f.price * f.qty + f.fee)
                self.marking.append({"slug": f.slug, "keys": list(self._placing[f.slug]),
                                     "px": f.price, "ts": f.ts, "todo": [h for h, _ in MARKOUTS]})
            elif f.side == "SELL" and f.slug in self._selling:
                self.card.close(f.slug, f.qty, f.price * f.qty - f.fee, self._selling[f.slug])
                closed = True
            elif f.side in ("SELL", "SETTLE"):
                fee = f.fee if f.side == "SELL" else 0.0
                self.card.close(f.slug, f.qty, f.price * f.qty - fee)
                closed = True
        self._placing.clear()
        self._selling.clear()
        if closed:
            self._judge(eng)

    def _check_form(self, eng) -> None:
        """Each leader's own sports profit on Polymarket over the last week and month."""
        for wallet in self.leaders:
            f = {}
            for period in ("WEEK", "MONTH"):
                try:
                    rows = eng.client.get(DATA_API, "/v1/leaderboard", {
                        "category": "SPORTS", "timePeriod": period, "orderBy": "PNL",
                        "user": wallet, "limit": 1}, use_cache=False) or []
                except FETCH_ERRORS as e:
                    log.debug("form %s %s: %s", wallet, period, e)
                    continue
                row = next((r for r in rows if isinstance(r, dict)
                            and str(r.get("proxyWallet", "")).lower() == wallet), None)
                try:
                    pnl, vol = float(row["pnl"]), float(row.get("vol") or 0)
                except (TypeError, KeyError, ValueError):
                    continue
                f[f"{period.lower()}_pnl"] = round(pnl, 2)
                f[f"{period.lower()}_roi"] = round(pnl / vol, 4) if vol else None
            if f:
                self.form[wallet] = f

    def _judge(self, eng) -> None:
        for wallet, name in self.leaders.items():
            s, f = self.card.summary(f"w:{wallet}"), self.form.get(wallet, {})
            week, month, month_roi = f.get("week_pnl"), f.get("month_pnl"), f.get("month_roi")
            if clearly_losing(s, self.min_wallet_n):
                new = ["benched", f"our copies of them are {_usd(s['pnl'])} on "
                                  f"{s['settled']} settled bets"]
            elif week is not None and week < 0 and month_roi is not None and month_roi <= -0.02:
                new = ["benched", f"losing on Polymarket: {_usd(week)} this week, "
                                  f"{_usd(month)} this month"]
            elif week is not None and week < 0:
                new = ["cooling", f"{_usd(week)} on Polymarket this week"]
            else:
                new = ["copying", ""]
            old = self.status.get(wallet, ["copying", ""])
            if new[0] != old[0]:
                log.info("leader %s: %s -> %s (%s)", name, old[0], new[0], new[1])
                eng._log("leader_status", leader=name, wallet=wallet, status=new[0],
                         was=old[0], why=new[1])
            self.status[wallet] = new
        # Leagues are judged first, on every copy; the other patterns (market
        # type, price band, timing) only on copies outside skipped leagues, so
        # one losing league is not read as losing moneylines and 30-70c bets
        # everywhere (they are mostly the same bets).
        keys = [k for k in self.card.results if not k.startswith("w:")]
        bad_leagues: set[str] = set()
        for key in sorted(keys, key=lambda k: not k.startswith("league:")):
            if key.startswith("league:"):
                s = self.card.summary(key)
            else:
                s = self.card.summary_without(key, bad_leagues)
            losing = clearly_losing(s, self.min_pattern_n, max_roi=-0.10)
            if losing and key.startswith("league:"):
                bad_leagues.add(key)
            if losing:
                if key not in self.skipped:
                    eng._log("pattern_skipped", pattern=key, pnl=s["pnl"], settled=s["settled"])
                self.skipped[key] = (f"{_usd(s['pnl'])} on {s['settled']} settled bets, "
                                     f"{100 * s['roi']:.0f}% return")
            elif self.skipped.pop(key, None) is not None:
                eng._log("pattern_resumed", pattern=key)

    # -- persistence and dashboard ----------------------------------------------
    def to_state(self) -> dict:
        return {"card": self.card.to_state(), "form": self.form, "status": self.status,
                "skipped": self.skipped, "last_ts": self.last_ts,
                "sizes": {w: list(d) for w, d in self.sizes.items()},
                "marking": self.marking, "mo": self.mo, "settled": self._settled,
                "feed": list(self.feed), "feed_n": self._feed_n}

    def load_state(self, d: dict) -> None:
        self.card.load(d.get("card", {}))
        self.form = d.get("form", {})
        self.status = d.get("status", {})
        self.skipped = d.get("skipped", {})
        # Pick up each leader's history where the last run left off, so trades
        # made during a restart are seen (those over max_age_s are skipped).
        self.last_ts = {w: int(t) for w, t in d.get("last_ts", {}).items()}
        self.sizes = {w: deque(v, maxlen=200) for w, v in d.get("sizes", {}).items()}
        self.marking = d.get("marking", [])
        self.mo = {h: d.get("mo", {}).get(h, {}) for h, _ in MARKOUTS}
        self._settled = d.get("settled", {})
        self.feed = deque(d.get("feed", []), maxlen=FEED_KEEP)
        self._feed_n = int(d.get("feed_n", 0))
        for e in self.feed:   # signals are not kept across a restart
            if e.get("action") == WAITING:
                e["action"] = "not decided (the bot restarted)"

    def copied_from(self, slug: str) -> str:
        names = [self.leaders.get(k[2:], k[2:12]) for k in self.card.keys_for(slug)
                 if k.startswith("w:")]
        return ", ".join(dict.fromkeys(names))

    def summary(self) -> dict:
        by = lambda st: ", ".join(self.leaders[w] for w, (x, _) in self.status.items()
                                  if x == st and w in self.leaders)
        return {"copytop_benched": by("benched"), "copytop_cooling": by("cooling"),
                "copytop_patterns_skipped": ", ".join(sorted(self.skipped)),
                "copytop_lag_median_s": round(median(self.lags), 1) if self.lags else None,
                **{f"copytop_{k}": v for k, v in self.markouts("all").items()},
                "copytop_unmapped_top": "; ".join(f"{s}|{o}|{n}" for (s, o), n
                                                  in self.unmapped.most_common(15))}

    def dashboard_rows(self) -> list[dict]:
        rows = []
        for wallet, name in self.leaders.items():
            st, why = self.status.get(wallet, ["copying", ""])
            rows.append({"kind": "leader", "id": wallet, "name": name, "status": st,
                         "reason": why, **self.card.summary(f"w:{wallet}"),
                         **self.markouts(f"w:{wallet}"),
                         **{k: self.form.get(wallet, {}).get(k) for k in
                            ("week_pnl", "month_pnl", "week_roi", "month_roi")}})
        for key in sorted(set(self.card.copies) | set(self.card.results)):
            if key.startswith("w:"):
                continue
            group, _, value = key.partition(":")
            rows.append({"kind": "pattern", "id": key, "group": group, "value": value,
                         "status": "skipped" if key in self.skipped else "copying",
                         "reason": self.skipped.get(key, ""), **self.card.summary(key),
                         **self.markouts(key)})
        for e in reversed(self.feed):   # newest first
            rows.append({"kind": "leader_trade", **{k: v for k, v in e.items() if k != "key"},
                         "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(e["ts"]))})
        return rows
