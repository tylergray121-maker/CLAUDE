"""Pick wallets to copy, and check the picking method works out of sample.

Wallets are judged on per-bet edge at a flat stake, which doesn't depend on
how a compounding bankroll happened to grow:

1. Every copied position ("bet") is replayed with a fixed $ stake, with the
   copy delay, slippage, fees and order minimums applied.
2. Ranking uses only bets that had *settled* before the cutoff, i.e. what
   you could actually have known then. The score is a lower confidence
   bound on return per bet, so a few lucky bets don't top the list.
3. Validation: the top K wallets by that score are scored on bets they
   opened after the cutoff, pooled, against the typical qualified wallet.
4. The same ranking on the most recent window gives the current picks, and
   a $200 compounding replay of the test period shows what that would have
   meant for your account.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from statistics import mean, median, stdev

from .models import Market, Trade
from .sim import SimConfig, SimResult, simulate

DEFAULT_KS = (1, 2, 3, 5, 8)
MIN_BETS = 20      # settled bets needed to rank a wallet
T_EDGE = 1.65      # one-sided ~95%


@dataclass
class BetStats:
    n: int = 0
    roi: float = 0.0     # mean return per bet (0.05 = +5% of stake)
    t: float = 0.0
    lcb: float = -math.inf  # roi - one standard error

    @classmethod
    def of(cls, rois: list[float]) -> "BetStats":
        if not rois:
            return cls()
        m = mean(rois)
        if len(rois) < 2:
            return cls(len(rois), m, 0.0, -math.inf)
        se = stdev(rois) / math.sqrt(len(rois))
        return cls(len(rois), m, m / se if se else 0.0, m - se)


@dataclass
class Validation:
    k: int
    wallets: list[str]
    test: BetStats


@dataclass
class Plan:
    label: str
    min_bets: int = MIN_BETS
    candidates: int = 0
    baseline_median_roi: float = 0.0
    baseline_share_positive: float = 0.0
    validations: list[Validation] = field(default_factory=list)
    median_roi_over_k: float = 0.0
    best_k: int = 0
    edge: bool = False
    test_200: SimResult | None = None      # $200 compounding, test period
    picks: list[dict] = field(default_factory=list)
    recent: SimResult | None = None        # $200 compounding, recent window
    recent_start: int = 0
    note: str = ""


def portfolio_cfg(cfg: SimConfig, k: int) -> SimConfig:
    # More leaders means more signals; shrink each copy so cash lasts.
    return replace(cfg, base_pct=cfg.base_pct / math.sqrt(k))


def _rois(lots, keep) -> list[float]:
    return [pnl / inv for (entry, settle, inv, pnl) in lots if inv > 0 and keep(entry, settle)]


def build_plan(label: str, histories: dict[str, list[Trade]],
               markets: dict[str, Market], cfg: SimConfig, start_ts: int,
               end_ts: int, split_ts: int, min_buys: int = MIN_BETS,
               ks=DEFAULT_KS, price_at=None) -> Plan:
    plan = Plan(label=label)
    flat = replace(cfg, fixed_stake=cfg.start_cash * cfg.base_pct, start_cash=1e12)
    span = split_ts - start_ts
    recent_start = end_ts - span
    plan.recent_start = recent_start
    min_bets = plan.min_bets = max(min_buys, 1)

    lots = {}
    for w, t in histories.items():
        if t:
            lots[w] = simulate(t, markets, flat, start_ts, end_ts, split_ts,
                               price_at).lots

    # Known at the cutoff: bets opened and settled before it.
    train = {w: BetStats.of(_rois(l, lambda e, s: e < split_ts and s is not None
                                  and s <= split_ts)) for w, l in lots.items()}
    test = {w: _rois(l, lambda e, s: e >= split_ts) for w, l in lots.items()}
    qualified = [w for w, st in train.items() if st.n >= min_bets and st.roi > 0]
    plan.candidates = len(qualified)
    if not qualified:
        plan.note = (f"No wallet had {min_bets}+ settled, profitable copyable bets "
                     "in the qualifying period.")
        return plan

    tested = [mean(test[w]) for w in qualified if len(test[w]) >= 5]
    if tested:
        plan.baseline_median_roi = median(tested)
        plan.baseline_share_positive = sum(1 for x in tested if x > 0) / len(tested)

    ranked = sorted(qualified, key=lambda w: train[w].lcb, reverse=True)
    for k in ks:
        if k > len(ranked):
            break
        chosen = ranked[:k]
        pooled = [r for w in chosen for r in test[w]]
        plan.validations.append(Validation(k, chosen, BetStats.of(pooled)))
    if not plan.validations:
        return plan

    vals = [v for v in plan.validations if v.test.n]
    plan.median_roi_over_k = median(v.test.roi for v in vals) if vals else 0.0
    significant = sum(1 for v in vals if v.test.t >= T_EDGE)
    # Works only if typical (median over K) out-of-sample edge per bet is
    # positive, beats a random qualified wallet, and is statistically clear
    # for at least half of the portfolio sizes.
    plan.edge = (plan.median_roi_over_k > max(0.0, plan.baseline_median_roi)
                 and significant * 2 >= len(vals) and len(vals) > 0)
    best = max(vals, key=lambda v: (v.test.lcb, v.k)) if vals else plan.validations[0]
    plan.best_k = best.k

    # What $200 would have done copying the validated picks in the test period.
    merged = [t for w in best.wallets for t in histories[w]]
    plan.test_200 = simulate(merged, markets, portfolio_cfg(cfg, best.k), split_ts,
                             end_ts, split_ts + (end_ts - split_ts) // 2, price_at)

    # Current picks: same rule on the most recent window of equal length.
    recent = {w: BetStats.of(_rois(l, lambda e, s: e >= recent_start and s is not None))
              for w, l in lots.items()}
    order = sorted([w for w, st in recent.items() if st.n >= min_bets and st.roi > 0],
                   key=lambda w: recent[w].lcb, reverse=True)
    plan.picks = [{"wallet": w, "bets": recent[w].n, "roi": recent[w].roi,
                   "t": recent[w].t} for w in order[:plan.best_k]]
    if plan.picks:
        merged = [t for p in plan.picks for t in histories[p["wallet"]]]
        plan.recent = simulate(merged, markets, portfolio_cfg(cfg, len(plan.picks)),
                               recent_start, end_ts, recent_start + span // 2,
                               price_at, log_fills=True)
    return plan


def render(plan: Plan, cfg: SimConfig, fmt_date) -> list[str]:
    stake = cfg.start_cash * cfg.base_pct
    out = [f"## {plan.label}", ""]
    if plan.note:
        return out + [plan.note, ""]
    out += [
        f"{plan.candidates} wallets qualified ({plan.min_bets}+ settled copyable bets, "
        f"profitable at a flat ${stake:.0f} stake before the cutoff). In the test "
        f"period the typical one returned {plan.baseline_median_roi:+.1%} per bet "
        f"(median); {plan.baseline_share_positive:.0%} were profitable.",
        "",
        "**Validation — top K wallets chosen before the cutoff, scored on bets "
        "they opened after it:**",
        "",
        "| copy top K | bets | return per bet | t-stat |",
        "|---|---|---|---|",
    ]
    for v in plan.validations:
        out.append(f"| {v.k} | {v.test.n} | {v.test.roi:+.1%} | {v.test.t:.1f} |")
    out += ["", f"Median across K: {plan.median_roi_over_k:+.1%} per bet vs "
            f"{plan.baseline_median_roi:+.1%} for a random qualified wallet. "
            f"(t ≥ {T_EDGE} is roughly 95% confidence the edge isn't luck.)", ""]
    if plan.test_200:
        r = plan.test_200
        out += [f"$200 copying the top {plan.best_k} through the test period: "
                f"${r.final_equity:.2f} ({r.return_pct:+.1f}%), worst drawdown "
                f"{r.max_drawdown_pct:.1f}%, {r.buys_copied} buys copied.", ""]
    if not plan.edge:
        out += ["**Verdict: no reliable edge.** Wallets that looked good before "
                "the cutoff did not keep a clear, statistically solid edge "
                "afterwards once delay, slippage and fees were paid.", ""]
    else:
        out += [f"**Verdict: the edge held up out of sample (best with K = "
                f"{plan.best_k}).**", ""]
    if plan.picks:
        out += [("**Current picks**" if plan.edge else
                 "**What the method would pick now (not recommended — see verdict)**")
                + f" — bets opened from {fmt_date(plan.recent_start)} and settled:",
                "", "| wallet | settled bets | return per bet | t-stat |",
                "|---|---|---|---|"]
        for p in plan.picks:
            out.append(f"| `{p['wallet']}` | {p['bets']} | {p['roi']:+.1%} | "
                       f"{p['t']:.1f} |")
        if plan.recent:
            r = plan.recent
            out += ["", f"$200 copying them over that window: ${r.final_equity:.2f} "
                    f"({r.return_pct:+.1f}%), worst drawdown {r.max_drawdown_pct:.1f}% "
                    "(in-sample; the validation above is the honest estimate)."]
        out.append("")
    return out
