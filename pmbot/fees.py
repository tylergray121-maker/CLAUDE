"""Polymarket US fee schedule.

Taker fee per trade = theta * contracts * p * (1 - p) with theta = 0.0695
(about 1.7 cents per contract at 50 cents). Makers earn a rebate on the same
curve; the lowest volume tier (0.0035) is used so estimates stay
conservative. Check https://docs.polymarket.us/fees before relying on these.
"""

from __future__ import annotations

import math

TAKER_THETA = 0.0695
MAKER_REBATE_THETA = 0.0035


def taker_fee(price: float, qty: float, theta: float = TAKER_THETA) -> float:
    """Fee in dollars, rounded up to the cent."""
    return math.ceil(theta * qty * price * (1 - price) * 100 - 1e-9) / 100


def taker_fee_per_contract(price: float, theta: float = TAKER_THETA) -> float:
    return theta * price * (1 - price)


def maker_rebate(price: float, qty: float, theta: float = MAKER_REBATE_THETA) -> float:
    """Rebate in dollars, rounded down to the cent."""
    return math.floor(theta * qty * price * (1 - price) * 100 + 1e-9) / 100
