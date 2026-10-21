"""Copy-trade simulator: replay a leader's trades against a small bankroll.

The simulation never looks ahead: sizing uses only trades seen so far, fills
use the leader's own print (or a delayed price) plus slippage, and positions
settle at market resolution.
"""

from __future__ import annotations

import math
import re
from bisect import insort
from collections import defaultdict
from dataclasses import dataclass, field
from statistics import median
from typing import Callable

from .models import Market, Trade

DAY = 86400


@dataclass
class SimConfig:
    start_cash: float = 200.0
    base_pct: float = 0.05        # equity spent on a "typical" leader buy
    conviction_min: float = 0.25  # clip on leader size / leader's median size
    conviction_max: float = 3.0
    max_trade_pct: float = 0.20   # cap on any single copied buy
    max_market_pct: float = 0.35  # cap on exposure to one market
    slippage: float = 0.01        # absolute price penalty per fill (1 cent)
    fee_bps: float = 0.0          # flat extra fee on top of market fees
    market_fees: bool = True      # charge each market's taker fee schedule
    min_order_usd: float = 1.0    # Polymarket marketable order minimum
    max_fill_price: float = 0.99  # don't buy when nothing is left to win
    delay_seconds: int = 0        # only used with a price lookup


@dataclass
class SimResult:
    final_equity: float
    return_pct: float
    max_drawdown_pct: float
    train_return_pct: float
    test_return_pct: float
    sharpe: float
    buys_copied: int
    sells_copied: int
    markets_traded: int
    win_rate: float
    skipped: dict[str, int] = field(default_factory=dict)
    daily_equity: list[tuple[int, float]] = field(default_factory=list)


PriceLookup = Callable[[str, int], "float | None"]


def simulate(trades: list[Trade], markets: dict[str, Market], cfg: SimConfig,
             start_ts: int, end_ts: int, split_ts: int,
             price_at: PriceLookup | None = None) -> SimResult:
    fee = cfg.fee_bps / 10000.0
    cash = cfg.start_cash
    pos: dict[str, float] = defaultdict(float)       # our shares per token
    cost: dict[str, float] = defaultdict(float)      # our open cost basis
    realized: dict[str, float] = defaultdict(float)  # our realized PnL per token
    leader: dict[str, float] = defaultdict(float)    # leader shares per token
    last_px: dict[str, float] = {}
    cond_of: dict[str, str] = {}
    assets_of: dict[str, set[str]] = defaultdict(set)
    settled: set[str] = set()
    buy_sizes: list[float] = []
    skipped: dict[str, int] = defaultdict(int)
    buys = sells = 0

    def taker_fee(cond: str, price: float, shares: float) -> float:
        m = markets.get(cond)
        return m.taker_fee(price, shares) if (m and cfg.market_fees) else 0.0

    def equity() -> float:
        return cash + sum(s * last_px.get(a, 0.0) for a, s in pos.items() if s > 0)

    def settle(cond: str) -> None:
        nonlocal cash
        m = markets[cond]
        settled.add(cond)
        for a in assets_of[cond]:
            payout = m.prices.get(a, last_px.get(a, 0.0))
            if pos[a] > 0:
                proceeds = pos[a] * payout
                cash += proceeds
                realized[a] += proceeds - cost[a]
                pos[a] = cost[a] = 0.0
            leader[a] = 0.0
            last_px[a] = payout

    # Resolution events inside the window. A resolved market with no timestamp
    # settles at the end of the window.
    resolutions: list[tuple[int, str]] = []
    traded_conds = {t.condition_id for t in trades}
    for cond in traded_conds:
        m = markets.get(cond)
        if m and m.resolved:
            rts = m.resolve_ts if m.resolve_ts is not None else end_ts
            if rts <= end_ts:
                resolutions.append((max(rts, start_ts), cond))
    resolutions.sort()

    curve: list[tuple[int, float]] = [(start_ts, cash)]
    ri = 0
    for t in sorted(trades, key=lambda t: t.ts):
        if t.ts < start_ts or t.ts > end_ts:
            continue
        while ri < len(resolutions) and resolutions[ri][0] <= t.ts:
            settle(resolutions[ri][1])
            ri += 1
            curve.append((resolutions[ri - 1][0], equity()))
        cond_of[t.asset] = t.condition_id
        assets_of[t.condition_id].add(t.asset)
        if t.condition_id in settled:
            continue  # trade after resolution: bad data, ignore
        last_px[t.asset] = t.price

        delayed = None
        if price_at and cfg.delay_seconds > 0:
            delayed = price_at(t.asset, t.ts + cfg.delay_seconds)

        if t.side == "BUY":
            leader[t.asset] += t.size
            prior = median(buy_sizes) if buy_sizes else t.notional
            insort(buy_sizes, t.notional)
            base = max(t.price, delayed) if delayed is not None else t.price
            fill = base + cfg.slippage
            if fill > cfg.max_fill_price:
                skipped["price_too_high"] += 1
                continue
            eq = equity()
            conviction = t.notional / prior if prior > 0 else 1.0
            conviction = min(cfg.conviction_max, max(cfg.conviction_min, conviction))
            usd = eq * cfg.base_pct * conviction
            usd = min(usd, eq * cfg.max_trade_pct)
            exposure = sum(pos[a] * last_px.get(a, 0.0)
                           for a in assets_of[t.condition_id])
            usd = min(usd, eq * cfg.max_market_pct - exposure)
            usd = min(usd, cash / (1 + fee))
            # Market taker fee is charged on the shares bought; shrink the
            # order so price + fees still fits in the budget.
            fee_per_share = taker_fee(t.condition_id, fill, 1.0)
            shares = usd / (fill + fee_per_share)
            if usd < cfg.min_order_usd:
                reason = ("no_cash" if cash / (1 + fee) < cfg.min_order_usd
                          else "market_cap" if eq * cfg.max_market_pct - exposure
                          < cfg.min_order_usd else "below_min_order")
                skipped[reason] += 1
                continue
            cash -= usd * (1 + fee)
            pos[t.asset] += shares
            cost[t.asset] += usd * (1 + fee)
            buys += 1
        else:
            before = leader[t.asset]
            leader[t.asset] = max(0.0, before - t.size)
            if pos[t.asset] <= 0:
                continue
            frac = 1.0 if before <= 0 else min(1.0, t.size / before)
            base = min(t.price, delayed) if delayed is not None else t.price
            fill = max(0.0, base - cfg.slippage)
            shares = pos[t.asset] * frac
            proceeds = (shares * fill * (1 - fee)
                        - taker_fee(t.condition_id, fill, shares))
            if proceeds < cfg.min_order_usd:
                skipped["sell_below_min"] += 1
                continue
            basis = cost[t.asset] * frac
            cash += proceeds
            realized[t.asset] += proceeds - basis
            pos[t.asset] -= shares
            cost[t.asset] -= basis
            sells += 1
        curve.append((t.ts, equity()))

    while ri < len(resolutions):
        settle(resolutions[ri][1])
        curve.append((resolutions[ri][0], equity()))
        ri += 1

    # Mark whatever is still open at the market's current price.
    for a, s in pos.items():
        if s > 0:
            m = markets.get(cond_of.get(a, ""))
            if m and a in m.prices:
                last_px[a] = m.prices[a]
    final = equity()
    curve.append((end_ts, final))

    traded = [a for a in cond_of if cost[a] > 0 or realized[a] != 0 or pos[a] > 0]
    pnl = {a: realized[a] + pos[a] * last_px.get(a, 0.0) - cost[a] for a in traded}
    wins = sum(1 for v in pnl.values() if v > 0)

    daily = _daily(curve, start_ts, end_ts)
    at_split = _value_at(curve, split_ts)
    return SimResult(
        final_equity=final,
        return_pct=100 * (final / cfg.start_cash - 1),
        max_drawdown_pct=_max_drawdown(curve),
        train_return_pct=100 * (at_split / cfg.start_cash - 1),
        test_return_pct=100 * (final / at_split - 1) if at_split > 0 else -100.0,
        sharpe=_sharpe(daily),
        buys_copied=buys,
        sells_copied=sells,
        markets_traded=len({cond_of[a] for a in traded}),
        win_rate=wins / len(pnl) if pnl else 0.0,
        skipped=dict(skipped),
        daily_equity=daily,
    )


def _value_at(curve: list[tuple[int, float]], ts: int) -> float:
    v = curve[0][1]
    for t, e in curve:
        if t > ts:
            break
        v = e
    return v


def _daily(curve, start_ts, end_ts) -> list[tuple[int, float]]:
    out = []
    i, v = 0, curve[0][1]
    day = start_ts
    while day <= end_ts + DAY - 1:
        while i < len(curve) and curve[i][0] <= day:
            v = curve[i][1]
            i += 1
        out.append((day, v))
        day += DAY
    return out


def _max_drawdown(curve) -> float:
    peak, dd = -math.inf, 0.0
    for _, e in curve:
        peak = max(peak, e)
        if peak > 0:
            dd = max(dd, (peak - e) / peak)
    return 100 * dd


def _sharpe(daily) -> float:
    rets = [b / a - 1 for (_, a), (_, b) in zip(daily, daily[1:]) if a > 0]
    if len(rets) < 2:
        return 0.0
    mu = sum(rets) / len(rets)
    var = sum((r - mu) ** 2 for r in rets) / (len(rets) - 1)
    return 0.0 if var <= 0 else mu / math.sqrt(var) * math.sqrt(365)


# --------------------------------------------------------------------------
# Wallet profile: is this wallet something a $200 copier can follow?
# --------------------------------------------------------------------------

_SHORT_MARKET = re.compile(
    r"up or down|\d{1,2}(:\d{2})?\s*[ap]m\s*-\s*\d{1,2}(:\d{2})?\s*[ap]m", re.I)


@dataclass
class Profile:
    trades: int
    trades_per_day: float
    active_days: int
    markets: int
    median_trade_usd: float
    avg_buy_price: float
    bond_share: float          # buys at >= 95c
    short_market_share: float  # 5/15-minute "Up or Down" style markets
    flags: list[str]


def profile(trades: list[Trade], start_ts: int, end_ts: int,
            truncated: bool = False) -> Profile:
    n = len(trades)
    span_days = max(1.0, (end_ts - start_ts) / DAY)
    buys = [t for t in trades if t.side == "BUY"]
    days = {t.ts // DAY for t in trades}
    short = sum(1 for t in trades if _SHORT_MARKET.search(t.title))
    bond = sum(1 for t in buys if t.price >= 0.95)
    p = Profile(
        trades=n,
        trades_per_day=n / span_days,
        active_days=len(days),
        markets=len({t.condition_id for t in trades}),
        median_trade_usd=median([t.notional for t in trades]) if trades else 0.0,
        avg_buy_price=(sum(t.notional for t in buys) / sum(t.size for t in buys)
                       if buys else 0.0),
        bond_share=bond / len(buys) if buys else 0.0,
        short_market_share=short / n if n else 0.0,
        flags=[],
    )
    if truncated:
        p.flags.append("too_many_trades")
    if p.trades_per_day > 100:
        p.flags.append("high_frequency")
    if p.short_market_share > 0.5:
        p.flags.append("short_duration_markets")
    if p.bond_share > 0.5:
        p.flags.append("bonder")
    return p
