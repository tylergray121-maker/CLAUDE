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
    # Taker fee per share = fee_rate * (p * (1 - p)) ** fee_exponent
    fee_rate: float = 0.0
    fee_exponent: float = 1.0

    def taker_fee(self, price: float, shares: float) -> float:
        if self.fee_rate <= 0:
            return 0.0
        return shares * self.fee_rate * (price * (1 - price)) ** self.fee_exponent
