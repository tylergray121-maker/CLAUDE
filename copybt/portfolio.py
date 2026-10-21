"""Pick a set of wallets to copy together, and check the picking method works.

1. Validation: rank wallets on the qualifying period only, copy the top K
   together with one bankroll, and measure the result on the later test
   period that played no part in the choice. Compare with the typical
   eligible wallet, i.e. what picking at random would have given.
2. Live pick: apply the same ranking to the most recent stretch of the same
   length, and choose the K that held up best in validation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from statistics import median

from .models import Market, Trade
from .sim import SimConfig, SimResult, simulate

DEFAULT_KS = (1, 2, 3, 5, 8)


@dataclass
class Validation:
    k: int
    wallets: list[str]
    test_return_pct: float
    test_max_drawdown_pct: float
    buys_copied: int


@dataclass
class Plan:
    label: str
    candidates: int
    baseline_median_test_pct: float = 0.0
    baseline_share_positive: float = 0.0
    validations: list[Validation] = field(default_factory=list)
    best_k: int = 0
    edge: bool = False
    picks: list[dict] = field(default_factory=list)
    recent: SimResult | None = None
    recent_start: int = 0
    note: str = ""


def portfolio_cfg(cfg: SimConfig, k: int) -> SimConfig:
    # More leaders means more signals; shrink each copy so cash lasts.
    return replace(cfg, base_pct=cfg.base_pct / math.sqrt(k))


def _score(ret: float, dd: float) -> float:
    return ret - 0.5 * dd


def _test_drawdown(res: SimResult, split_ts: int) -> float:
    peak, dd = -math.inf, 0.0
    for ts, e in res.daily_equity:
        if ts < split_ts:
            continue
        peak = max(peak, e)
        if peak > 0:
            dd = max(dd, (peak - e) / peak)
    return 100 * dd


def build_plan(label: str, histories: dict[str, list[Trade]],
               markets: dict[str, Market], cfg: SimConfig, start_ts: int,
               end_ts: int, split_ts: int, min_buys: int,
               ks=DEFAULT_KS, price_at=None) -> Plan:
    singles = {w: simulate(t, markets, cfg, start_ts, end_ts, split_ts, price_at)
               for w, t in histories.items() if t}
    qualified = {w: r for w, r in singles.items()
                 if r.buys_copied >= min_buys and r.train_return_pct > 0}
    plan = Plan(label=label, candidates=len(qualified))
    if not qualified:
        plan.note = "No wallet was profitable in the qualifying period with enough copyable buys."
        return plan

    tests = [r.test_return_pct for r in qualified.values()]
    plan.baseline_median_test_pct = median(tests)
    plan.baseline_share_positive = sum(1 for x in tests if x > 0) / len(tests)

    ranked = sorted(qualified, key=lambda w: _score(
        qualified[w].train_return_pct, qualified[w].train_max_drawdown_pct),
        reverse=True)
    for k in ks:
        if k > len(ranked):
            break
        chosen = ranked[:k]
        merged = [t for w in chosen for t in histories[w]]
        res = simulate(merged, markets, portfolio_cfg(cfg, k), start_ts, end_ts,
                       split_ts, price_at)
        plan.validations.append(Validation(k, chosen, res.test_return_pct,
                                           _test_drawdown(res, split_ts),
                                           res.buys_copied))
    if not plan.validations:
        return plan

    best = max(plan.validations,
               key=lambda v: (_score(v.test_return_pct, v.test_max_drawdown_pct), v.k))
    plan.best_k = best.k
    # The method only counts as working if its out-of-sample result is
    # positive and better than picking a qualified wallet at random.
    plan.edge = (best.test_return_pct > 0
                 and best.test_return_pct > plan.baseline_median_test_pct)

    # Live pick: same ranking rule on the most recent window of equal length.
    span = split_ts - start_ts
    recent_start = end_ts - span
    recent_split = recent_start + span // 2
    plan.recent_start = recent_start
    recent = {}
    for w, t in histories.items():
        if not t:
            continue
        r = simulate(t, markets, cfg, recent_start, end_ts, recent_split, price_at)
        if r.buys_copied >= min_buys and r.return_pct > 0:
            recent[w] = r
    picks = sorted(recent, key=lambda w: _score(recent[w].return_pct,
                                                recent[w].max_drawdown_pct),
                   reverse=True)[:plan.best_k]
    plan.picks = [{"wallet": w, "return_pct": recent[w].return_pct,
                   "max_drawdown_pct": recent[w].max_drawdown_pct,
                   "buys_copied": recent[w].buys_copied,
                   "markets_traded": recent[w].markets_traded,
                   "win_rate": recent[w].win_rate} for w in picks]
    if picks:
        merged = [t for w in picks for t in histories[w]]
        plan.recent = simulate(merged, markets, portfolio_cfg(cfg, len(picks)),
                               recent_start, end_ts, recent_split, price_at)
    return plan


def render(plan: Plan, cfg: SimConfig, fmt_date) -> list[str]:
    out = [f"## {plan.label}", ""]
    if plan.note:
        return out + [plan.note, ""]
    out += [
        f"{plan.candidates} wallets qualified (profitable in the qualifying "
        f"period, enough copyable buys). Typical qualified wallet in the test "
        f"period: {plan.baseline_median_test_pct:+.1f}% (median); "
        f"{plan.baseline_share_positive:.0%} of them made money.",
        "",
        "**Validation — wallets chosen using the qualifying period only, "
        "scored on the test period:**",
        "",
        "| copy top K together | test return | test max DD | buys copied |",
        "|---|---|---|---|",
    ]
    for v in plan.validations:
        out.append(f"| {v.k} | {v.test_return_pct:+.1f}% | "
                   f"{v.test_max_drawdown_pct:.1f}% | {v.buys_copied} |")
    out.append("")
    if not plan.edge:
        out += [
            "**Verdict: no edge.** Picking wallets by past results did not beat "
            "chance out of sample after fees and slippage, so this backtest "
            "gives no reason to copy any of these wallets.",
            ""]
    else:
        out += [f"**Verdict: the method held up out of sample; best with "
                f"K = {plan.best_k}.**", ""]
    if plan.picks:
        r = plan.recent
        out += [
            ("**Picks for now**" if plan.edge else
             "**What the method would pick now (not recommended — see verdict)**")
            + f" — ranked on {fmt_date(plan.recent_start)} onward, each copy "
            f"sized {portfolio_cfg(cfg, len(plan.picks)).base_pct:.1%} of equity "
            "per typical leader buy:",
            "",
            "| wallet | recent return | max DD | buys | markets | win rate |",
            "|---|---|---|---|---|---|",
        ]
        for p in plan.picks:
            out.append(f"| `{p['wallet']}` | {p['return_pct']:+.1f}% | "
                       f"{p['max_drawdown_pct']:.1f}% | {p['buys_copied']} | "
                       f"{p['markets_traded']} | {p['win_rate']:.0%} |")
        if r:
            out += ["", f"Copied together over that window: ${cfg.start_cash:.0f} → "
                    f"${r.final_equity:.2f} ({r.return_pct:+.1f}%), max drawdown "
                    f"{r.max_drawdown_pct:.1f}%. This is in-sample — the "
                    "validation table is the honest estimate."]
        out.append("")
    return out
