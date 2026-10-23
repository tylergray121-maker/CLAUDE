"""Re-enter the bot's positions after the owner cashed them out by hand.

A one-shot list, ``reenter.json`` in the output directory (the live desk
copies it there from the live-desk branch), names each position to buy back:

    {"id": "2026-10-23", "positions": [{"slug": "aec-nba-det-mia-2026-10-23", "qty": 12,
                    "max_price": 0.56}, ...]}

The list is read once (by its ``id``) and kept with the account. Each position is bought
back as cash allows, pre-game only (the market must still be tradable) and
never above its ``max_price`` (what the bot paid plus a cent), so it is the
same bet at the same price, not a chase after a line that moved. Entries
are dropped once filled or once their game starts.
"""

from __future__ import annotations

import json
import logging
import os

from .strategies import Strategy
from .strategy import MarketView, Order

log = logging.getLogger(__name__)


class ReEnter(Strategy):
    name = "reenter"

    def __init__(self, out_dir: str):
        self.path = os.path.join(out_dir, "reenter.json")
        self.pending: dict[str, dict] = {}     # slug -> {"qty", "max_price"}
        self.done: list[str] = []              # list ids already loaded (never twice)
        self.stats = {"loaded": 0, "bought": 0, "dropped_started": 0}

    def _load_file(self) -> None:
        try:
            with open(self.path) as f:
                d = json.load(f)
        except (OSError, ValueError):
            return
        try:
            os.remove(self.path)               # one-shot
        except OSError:
            pass
        lid = str(d.get("id", ""))
        if not lid or lid in self.done:
            return
        self.done.append(lid)
        for r in d.get("positions", []):
            if r.get("slug") and int(r.get("qty") or 0) > 0 and r.get("max_price"):
                self.pending[r["slug"]] = {"qty": int(r["qty"]), "max_price": float(r["max_price"])}
                self.stats["loaded"] += 1
        log.info("reenter: %d positions to buy back (list %s)", len(self.pending), lid)

    def watch(self, eng, now):
        self._load_file()
        return set(self.pending)

    def orders(self, eng, views: dict[str, MarketView], now):
        out = {}
        for slug, p in list(self.pending.items()):
            v = views.get(slug)
            m = eng.markets.get(slug.removesuffix(":short"))
            if m is not None and m.game_start and now > m.game_start - 600:
                self.pending.pop(slug)
                self.stats["dropped_started"] += 1
                continue
            if v is None or not v.tradable or v.us_ask is None or v.us_ask > p["max_price"]:
                continue
            qty = min(p["qty"], int(eng.room(slug) // v.us_ask), int(v.us_ask_qty))
            if qty >= 1:
                out[slug] = [Order("BUY", v.us_ask, qty, post_only=False)]
        return out

    def on_fills(self, eng, fills) -> None:
        for f in fills:
            if f.tag == self.name and f.side == "BUY" and f.slug in self.pending:
                self.pending[f.slug]["qty"] -= f.qty
                self.stats["bought"] += f.qty
                if self.pending[f.slug]["qty"] <= 0:
                    self.pending.pop(f.slug)

    def to_state(self) -> dict:
        return {"pending": self.pending, "done": self.done[-50:]}

    def load_state(self, d: dict) -> None:
        self.pending = {k: dict(v) for k, v in d.get("pending", {}).items()}
        self.done = list(d.get("done", []))

    def summary(self) -> dict:
        return {"reenter_pending": len(self.pending), "reenter_bought": self.stats["bought"]}
