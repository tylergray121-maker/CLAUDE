"""Copy the most profitable active sports wallets onto Polymarket US.

The leaders (pmbot/leaders.json, chosen from the top-wallet study) trade on
international Polymarket, whose trades are public. Each cycle this polls
their newest trades; a buy of an outcome that maps to a Polymarket US
market (a verified pair, or the same game/spread/total market by slug, on
either side) becomes a taker buy on US, at
no more than the leader's price plus a small allowance, so the bot never
chases a price that has moved. A leader's sell closes the copy; otherwise
copies are held to settlement.

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
import re
from collections import Counter, deque
from statistics import median

from copybt.api import DATA_API, HTTPError

from .broker import SHORT, split_side
from .data import fetch_parallel
from .mapping import prices_agree
from .strategies import Strategy
from .strategy import MarketView, Order, StrategyConfig
from .track import Scorecard, clearly_losing

log = logging.getLogger(__name__)


def load_leaders(path: str) -> dict[str, str]:
    with open(path) as f:
        d = json.load(f)
    return {x["wallet"].lower(): x.get("name") or x["wallet"][:10] for x in d["leaders"]}


STAT_KEYS = ("leader_trades", "mapped", "mapped_short_side", "not_on_polymarket_us",
             "listed_side_unknown", "copied_buys", "copied_sells", "expired_price_moved",
             "skip_repeat", "skip_recently_copied", "skip_tiny", "skip_not_open",
             "skip_price_band", "skip_prices_disagree", "skip_no_room_or_size",
             "skip_holding_other_side", "skip_exit_price", "skip_benched_wallet",
             "skip_losing_pattern", "poll_errors")
_GAME = re.compile(r"^([a-z0-9]+)-.*\d{4}-\d{2}-\d{2}")


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
                 form_every_s: float = 7200, min_wallet_n: int = 10, min_pattern_n: int = 15):
        self.cfg = cfg
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

    # -- signals ------------------------------------------------------------
    def _fetch(self, eng, wallet: str) -> list[dict] | None:
        try:
            return eng.client.get(DATA_API, "/trades", {"user": wallet, "limit": 50,
                                                        "takerOnly": "false"},
                                  use_cache=False) or []
        except HTTPError as e:
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
        if first:
            return []  # baseline: never copy trades made before the bot was watching
        return sorted((r for r in rows if int(r["timestamp"]) > since),
                      key=lambda r: int(r["timestamp"]))

    def watch(self, eng, now):
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
                slug = eng.us_for_trade(t, index)
                if not slug:
                    if eng.lists(str(t.get("slug") or "")):
                        self.stats["listed_side_unknown"] += 1  # outcome names differ
                    else:
                        self.stats["not_on_polymarket_us"] += 1
                        self.stats[f"missed_{league(str(t.get('slug') or ''))}"] += 1
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
                    continue
                if side == "BUY" and self.status.get(wallet, ["copying"])[0] == "benched":
                    self.stats["skip_benched_wallet"] += 1
                    continue
                tx = (wallet, t.get("transactionHash"), t.get("asset"))
                if t.get("transactionHash") and tx in self.seen_tx:
                    self.stats["skip_repeat"] += 1  # another fill of an order already seen
                    continue
                self.seen_tx.add(tx)
                key = (wallet, slug, side)
                if now - self.recent.get(key, 0) < self.dedupe_s:
                    self.stats["skip_recently_copied"] += 1
                    continue
                self.pending[slug] = {"side": side, "price": price, "leader": name,
                                      "wallet": wallet, "at": now,
                                      "trade_ts": int(t["timestamp"]),
                                      "leader_usd": round(price * size, 2),
                                      "league": league(str(t.get("slug") or ""))}
                eng._log("copy_signal", slug=slug, side=side, leader=name, price=price,
                         leader_usd=round(price * size, 2), market=t.get("title"))
        for slug in [s for s, sig in self.pending.items() if now - sig["at"] > self.signal_ttl_s]:
            self.stats["expired_price_moved"] += 1
            del self.pending[slug]
        return set(self.pending)

    # -- orders ---------------------------------------------------------------
    def orders(self, eng, views: dict[str, MarketView], now):
        out: dict[str, list[Order]] = {}
        for slug, sig in list(self.pending.items()):
            v = views.get(slug)
            if v is None:
                continue
            if v.note not in ("", "in-play"):  # closed, suspended, closing soon...
                self.stats["skip_not_open"] += 1
                del self.pending[slug]
                continue
            if sig["side"] == "BUY":
                base, short = split_side(slug)
                if eng.held(base if short else base + SHORT) > 0:
                    self.stats["skip_holding_other_side"] += 1  # would only lock in a loss
                    del self.pending[slug]
                    continue
                limit = round(min(sig["price"] + self.max_slip, self.cfg.max_price), 4)
                ask = v.us_ask
                if ask is None or ask > limit:
                    continue  # keep waiting until the signal expires
                if ask < self.cfg.min_price:
                    self.stats["skip_price_band"] += 1
                    del self.pending[slug]
                    continue
                if not prices_agree(ask, sig["price"]):
                    self.stats["skip_prices_disagree"] += 1  # likely not the same bet
                    del self.pending[slug]
                    continue
                keys = [f"w:{sig['wallet']}", f"league:{sig.get('league', 'other')}",
                        f"kind:{v.market_type or 'other'}", f"price:{price_band(ask)}",
                        f"timing:{'in-play' if v.note == 'in-play' else 'pre-game'}"]
                if any(k in self.skipped for k in keys):
                    self.stats["skip_losing_pattern"] += 1
                    del self.pending[slug]
                    continue
                qty = min(int(min(self.cfg.order_usd, eng.room(slug)) // ask), int(v.us_ask_qty))
                del self.pending[slug]
                if qty < 1:
                    self.stats["skip_no_room_or_size"] += 1
                    continue
                self.stats["copied_buys"] += 1
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
                    continue
                floor = round(max(sig["price"] - self.max_slip, 0.01), 4)
                if v.us_bid < floor:
                    self.stats["skip_exit_price"] += 1
                    continue
                self.stats["copied_sells"] += 1
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
            if f.side == "BUY" and f.slug in self._placing:
                self.card.open(f.slug, self._placing[f.slug], f.qty, f.price * f.qty + f.fee)
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
                except HTTPError as e:
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
        for key in [k for k in self.card.results if not k.startswith("w:")]:
            s = self.card.summary(key)
            if clearly_losing(s, self.min_pattern_n, max_roi=-0.10):
                if key not in self.skipped:
                    eng._log("pattern_skipped", pattern=key, pnl=s["pnl"], settled=s["settled"])
                self.skipped[key] = (f"{_usd(s['pnl'])} on {s['settled']} settled bets, "
                                     f"{100 * s['roi']:.0f}% return")
            elif self.skipped.pop(key, None) is not None:
                eng._log("pattern_resumed", pattern=key)

    # -- persistence and dashboard ----------------------------------------------
    def to_state(self) -> dict:
        return {"card": self.card.to_state(), "form": self.form, "status": self.status,
                "skipped": self.skipped}

    def load_state(self, d: dict) -> None:
        self.card.load(d.get("card", {}))
        self.form = d.get("form", {})
        self.status = d.get("status", {})
        self.skipped = d.get("skipped", {})

    def copied_from(self, slug: str) -> str:
        names = [self.leaders.get(k[2:], k[2:12]) for k in self.card.keys_for(slug)
                 if k.startswith("w:")]
        return ", ".join(dict.fromkeys(names))

    def summary(self) -> dict:
        by = lambda st: ", ".join(self.leaders[w] for w, (x, _) in self.status.items()
                                  if x == st and w in self.leaders)
        return {"copytop_benched": by("benched"), "copytop_cooling": by("cooling"),
                "copytop_patterns_skipped": ", ".join(sorted(self.skipped)),
                "copytop_lag_median_s": round(median(self.lags), 1) if self.lags else None}

    def dashboard_rows(self) -> list[dict]:
        rows = []
        for wallet, name in self.leaders.items():
            st, why = self.status.get(wallet, ["copying", ""])
            rows.append({"kind": "leader", "id": wallet, "name": name, "status": st,
                         "reason": why, **self.card.summary(f"w:{wallet}"),
                         **{k: self.form.get(wallet, {}).get(k) for k in
                            ("week_pnl", "month_pnl", "week_roi", "month_roi")}})
        for key in sorted(set(self.card.copies) | set(self.card.results)):
            if key.startswith("w:"):
                continue
            group, _, value = key.partition(":")
            rows.append({"kind": "pattern", "id": key, "group": group, "value": value,
                         "status": "skipped" if key in self.skipped else "copying",
                         "reason": self.skipped.get(key, ""), **self.card.summary(key)})
        return rows
