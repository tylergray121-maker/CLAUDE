"""Hard limits that sit between the strategy and the broker."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass


@dataclass
class RiskConfig:
    bankroll: float = 200.0
    max_market_usd: float = 25.0     # cost basis + open bids, per market
    max_total_usd: float = 150.0     # across all markets
    daily_loss_limit: float = 30.0   # halt and cancel everything below this
    max_orders_per_min: int = 30
    kill_file: str = "STOP"          # create this file to halt the bot


class RiskManager:
    def __init__(self, cfg: RiskConfig):
        self.cfg = cfg
        self.halted = ""
        self._day = None
        self._day_start_equity = None
        self._order_times: list[float] = []

    def room(self, slug: str, positions: dict, open_orders: dict, cash: float) -> float:
        """Dollars that may still be committed to new buys in ``slug``."""
        def committed(s=None):
            pos = sum(p.cost for k, p in positions.items() if s is None or k == s)
            bids = sum(o.price * o.qty for o in open_orders.values()
                       if o.side == "BUY" and (s is None or o.slug == s))
            return pos + bids
        pending_all = sum(o.price * o.qty for o in open_orders.values() if o.side == "BUY")
        return max(0.0, min(self.cfg.max_market_usd - committed(slug),
                            self.cfg.max_total_usd - committed(),
                            cash - pending_all))

    def allow_order(self) -> bool:
        now = time.monotonic()
        self._order_times = [t for t in self._order_times if now - t < 60]
        if len(self._order_times) >= self.cfg.max_orders_per_min:
            return False
        self._order_times.append(now)
        return True

    def check(self, equity: float, now: float | None = None) -> str:
        """Returns a halt reason ('' if fine). Halts are sticky."""
        if self.halted:
            return self.halted
        if os.path.exists(self.cfg.kill_file):
            self.halted = f"kill file {self.cfg.kill_file!r} present"
            return self.halted
        day = int((time.time() if now is None else now) // 86400)
        if day != self._day:
            self._day, self._day_start_equity = day, equity
        if self.cfg.daily_loss_limit > 0 and \
                self._day_start_equity - equity >= self.cfg.daily_loss_limit:  # 0 = no daily stop
            self.halted = (f"daily loss limit: equity {equity:.2f} vs "
                           f"{self._day_start_equity:.2f} at start of day")
        return self.halted
