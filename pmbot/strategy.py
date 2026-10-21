"""Quoting rules: pure functions from market state to desired orders.

Fair value is the international Polymarket midpoint for the same outcome.
The bot rests post-only bids below fair value and post-only asks above it
for contracts it holds (maker: no taker fee, small rebate), and only takes
liquidity when a US price is through fair value by more than the taker fee
plus a margin. Only the long (YES) side is traded: buy to open, sell what
is held to close, so there is never a short position.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .fees import taker_fee_per_contract


@dataclass
class StrategyConfig:
    maker_edge: float = 0.02      # quote at least this far from fair value
    taker_edge: float = 0.03      # take only when this far through fair, after fees
    order_usd: float = 5.0        # size of one quote / take
    max_fair_spread: float = 0.04  # reference book must be this tight to trust it
    min_price: float = 0.05       # skip long shots and near-certainties
    max_price: float = 0.95
    requote_move: float = 0.01    # cancel/replace when the desired price moves this much
    taker_enabled: bool = True
    maker_enabled: bool = True


@dataclass
class MarketView:
    slug: str
    tick: float
    us_bid: float | None
    us_ask: float | None
    us_bid_qty: float
    us_ask_qty: float
    fair: float | None        # reference midpoint
    fair_spread: float | None
    tradable: bool = True     # open, not in-play, not about to close
    note: str = ""
    end: float | None = None  # scheduled close (unix seconds)
    market_type: str = ""


@dataclass
class Order:
    side: str          # "BUY" | "SELL"  (long side only)
    price: float
    qty: int
    post_only: bool    # True: maker quote (GTC); False: IOC take
    tag: str = ""      # strategy that wants it


def floor_tick(x: float, tick: float) -> float:
    return round(math.floor(x / tick + 1e-9) * tick, 6)


def ceil_tick(x: float, tick: float) -> float:
    return round(math.ceil(x / tick - 1e-9) * tick, 6)


def fair_ok(v: MarketView, cfg: StrategyConfig) -> bool:
    return (v.tradable and v.fair is not None and v.fair_spread is not None
            and v.fair_spread <= cfg.max_fair_spread
            and cfg.min_price <= v.fair <= cfg.max_price)


def decide(v: MarketView, held: int, room_usd: float,
           cfg: StrategyConfig) -> list[Order]:
    """Desired orders for one market.

    ``held``: contracts currently held. ``room_usd``: how much more may be
    bought in this market under the risk limits.
    """
    if not fair_ok(v, cfg):
        return []
    fair, tick, out = v.fair, v.tick, []
    budget = min(cfg.order_usd, room_usd)

    # Takes: only when the US book is through fair value by more than the
    # fee plus a margin, and never for more than the displayed size.
    if cfg.taker_enabled:
        ask = v.us_ask
        if (ask is not None and cfg.min_price <= ask <= cfg.max_price
                and fair - ask - taker_fee_per_contract(ask) >= cfg.taker_edge):
            qty = min(int(budget // ask), int(v.us_ask_qty))
            if qty >= 1:
                out.append(Order("BUY", ask, qty, post_only=False))
        bid = v.us_bid
        if (held > 0 and bid is not None
                and bid - taker_fee_per_contract(bid) - fair >= cfg.taker_edge):
            qty = min(held, int(v.us_bid_qty))
            if qty >= 1:
                out.append(Order("SELL", bid, qty, post_only=False))
    if any(not o.post_only for o in out):
        return out  # act on the mispricing first; requote next cycle

    if cfg.maker_enabled:
        # Bid: one tick above the best bid, but never above fair - edge,
        # and never crossing the ask (post-only would reject it anyway).
        px = floor_tick(fair - cfg.maker_edge, tick)
        if v.us_bid is not None:
            px = min(px, round(v.us_bid + tick, 6))
        if v.us_ask is not None:
            px = min(px, round(v.us_ask - tick, 6))
        if cfg.min_price <= px <= cfg.max_price:
            qty = int(budget // px)
            if qty >= 1:
                out.append(Order("BUY", px, qty, post_only=True))
        # Ask for what we hold: one tick below the best ask, but never
        # below fair + edge, and never crossing the bid.
        if held > 0:
            px = ceil_tick(fair + cfg.maker_edge, tick)
            if v.us_ask is not None:
                px = max(px, round(v.us_ask - tick, 6))
            if v.us_bid is not None:
                px = max(px, round(v.us_bid + tick, 6))
            if px < 1.0:
                out.append(Order("SELL", px, held, post_only=True))
    return out
