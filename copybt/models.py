from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Trade:
    ts: int            # unix seconds
    asset: str         # outcome token id
    condition_id: str  # market id
    side: str          # "BUY" | "SELL"
    price: float       # 0..1 per share
    size: float        # shares
    title: str = ""
    outcome: str = ""
    tx: str = ""

    @property
    def notional(self) -> float:
        return self.price * self.size


@dataclass
class Market:
    condition_id: str
    resolved: bool
    resolve_ts: int | None
    prices: dict[str, float] = field(default_factory=dict)  # token -> payout/mark
    question: str = ""
