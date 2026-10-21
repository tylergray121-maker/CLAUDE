"""Copy the most profitable active sports wallets onto Polymarket US.

The leaders (pmbot/leaders.json, chosen from the top-wallet study) trade on
international Polymarket, whose trades are public. Each cycle this polls
their newest trades; a buy of an outcome that maps to a Polymarket US
market (through the engine's verified pairs) becomes a taker buy on US, at
no more than the leader's price plus a small allowance, so the bot never
chases a price that has moved. A leader's sell closes the copy; otherwise
copies are held to settlement.
"""

from __future__ import annotations

import json
import logging
from collections import Counter

from copybt.api import DATA_API, HTTPError

from .mapping import prices_agree
from .strategies import Strategy
from .strategy import MarketView, Order, StrategyConfig

log = logging.getLogger(__name__)


def load_leaders(path: str) -> dict[str, str]:
    with open(path) as f:
        d = json.load(f)
    return {x["wallet"].lower(): x.get("name") or x["wallet"][:10] for x in d["leaders"]}


STAT_KEYS = ("leader_trades", "mapped", "not_on_polymarket_us", "copied_buys",
             "copied_sells", "expired_price_moved", "skip_repeat", "skip_recently_copied",
             "skip_tiny", "skip_not_open", "skip_price_band", "skip_prices_disagree",
             "skip_no_room_or_size", "skip_exit_price", "poll_errors")


class CopyTop(Strategy):
    name = "copytop"

    def __init__(self, cfg: StrategyConfig, leaders: dict[str, str], max_slip: float = 0.01,
                 signal_ttl_s: float = 180, dedupe_s: float = 600, min_leader_usd: float = 5.0):
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

    # -- signals ------------------------------------------------------------
    def _new_trades(self, eng, wallet: str) -> list[dict]:
        try:
            rows = eng.client.get(DATA_API, "/trades", {"user": wallet, "limit": 50,
                                                        "takerOnly": "false"},
                                  use_cache=False) or []
        except HTTPError as e:
            self.stats["poll_errors"] += 1
            log.debug("leader %s trades: %s", wallet, e)
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
        index = eng.token_index()
        for wallet, name in self.leaders.items():
            for t in self._new_trades(eng, wallet):
                self.stats["leader_trades"] += 1
                slug = index.get(str(t.get("asset")))
                if not slug:
                    self.stats["not_on_polymarket_us"] += 1
                    continue
                self.stats["mapped"] += 1
                side = str(t.get("side", "")).upper()
                try:
                    price, size = float(t["price"]), float(t["size"])
                except (KeyError, TypeError, ValueError):
                    continue
                if side == "BUY" and price * size < self.min_leader_usd:
                    self.stats["skip_tiny"] += 1
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
                                      "leader_usd": round(price * size, 2)}
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
                qty = min(int(min(self.cfg.order_usd, eng.room(slug)) // ask), int(v.us_ask_qty))
                del self.pending[slug]
                if qty < 1:
                    self.stats["skip_no_room_or_size"] += 1
                    continue
                self.stats["copied_buys"] += 1
                self.recent[(sig["wallet"], slug, "BUY")] = now
                out[slug] = [Order("BUY", limit, qty, post_only=False)]
            else:
                held = eng.held(slug)
                del self.pending[slug]
                if held < 1 or v.us_bid is None:
                    continue
                floor = round(max(sig["price"] - self.max_slip, 0.01), 4)
                if v.us_bid < floor:
                    self.stats["skip_exit_price"] += 1
                    continue
                self.stats["copied_sells"] += 1
                out[slug] = [Order("SELL", floor, min(held, int(v.us_bid_qty)), post_only=False)]
        return out
