"""Study Polymarket's most profitable wallets.

    python -m study --top 100 --per-category 20
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import median

from copybt.api import Client

from .collect import CATEGORIES, leaderboard, wallet_data
from .features import _f, profile

log = logging.getLogger("study")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="study")
    ap.add_argument("--top", type=int, default=100)
    ap.add_argument("--per-category", type=int, default=20)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-rps", type=float, default=10)
    ap.add_argument("--cache-dir", default=".cache-study")
    ap.add_argument("--out-dir", default="studyresults")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    client = Client(cache_dir=a.cache_dir, max_rps=a.max_rps)
    os.makedirs(a.out_dir, exist_ok=True)

    groups: dict[str, list[str]] = defaultdict(list)
    lb: dict[str, dict] = {}
    for key, cat, period, n in [("all-time top", "OVERALL", "ALL", a.top),
                                ("this month top", "OVERALL", "MONTH", a.top)] + [
            (f"{c.lower()} leaders", c, "ALL", a.per_category) for c in CATEGORIES]:
        rows = leaderboard(client, cat, period, n)
        log.info("%s: %d wallets", key, len(rows))
        for r in rows:
            w = r["proxyWallet"].lower()
            groups[key].append(w)
            lb.setdefault(w, {})[key] = r
    wallets = sorted(lb)
    log.info("%d unique wallets", len(wallets))

    profiles: dict[str, dict] = {}
    with ThreadPoolExecutor(a.workers) as pool:
        futs = {pool.submit(wallet_data, client, w): w for w in wallets}
        for i, fut in enumerate(as_completed(futs), 1):
            w = futs[fut]
            try:
                d = fut.result()
            except Exception as e:
                log.warning("%s failed: %s", w, e)
                continue
            first = lb[w].get("all-time top") or next(iter(lb[w].values()))
            p = profile(d, first)
            p["groups"] = ";".join(k for k in groups if w in groups[k])
            p["top_markets"] = sorted(
                ({"title": r.get("title"), "outcome": r.get("outcome"),
                  "avg_price": _f(r.get("avgPrice")), "pnl": _f(r.get("realizedPnl")),
                  "end": r.get("endDate")} for r in d["closed"]),
                key=lambda x: -x["pnl"])[:3]
            profiles[w] = p
            if i % 25 == 0 or i == len(futs):
                log.info("profiled %d/%d (%d requests)", i, len(futs), client.requests_made)

    rows = sorted(profiles.values(), key=lambda p: -p["lb_pnl"])
    cols = [k for k in rows[0] if k != "top_markets"] if rows else []
    with open(os.path.join(a.out_dir, "wallets.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(rows)
    with open(os.path.join(a.out_dir, "wallets.json"), "w") as f:
        json.dump(rows, f, indent=1)
    report = render(groups, lb, profiles)
    with open(os.path.join(a.out_dir, "report.md"), "w") as f:
        f.write(report)
    print(report)
    return 0


def _med(xs):
    xs = [x for x in xs if x is not None]
    return median(xs) if xs else None


def _pct(x):
    return "—" if x is None else f"{x:.0%}"


def _usd(x):
    return f"${x / 1e6:,.1f}M" if abs(x) >= 1e6 else f"${x / 1e3:,.0f}k" if abs(x) >= 1e3 else f"${x:,.0f}"


def render(groups, lb, profiles) -> str:
    out = ["# What Polymarket's most profitable wallets do", ""]
    for key, members in groups.items():
        ps = [profiles[w] for w in members if w in profiles]
        if not ps:
            continue
        pnl_of = {p["wallet"]: _f(lb[p["wallet"]][key].get("pnl")) for p in ps}
        total = sum(v for v in pnl_of.values() if v > 0) or 1
        by = defaultdict(list)
        for p in ps:
            by[p["archetype"]].append(p)
        out += [f"## {key.capitalize()} ({len(ps)} wallets, {_usd(total)} profit)", "",
                "| strategy | wallets | share of profit | median edge per $ | median win rate "
                "| median maker share | median trades/day |", "|---|---|---|---|---|---|---|"]
        for arch, xs in sorted(by.items(), key=lambda kv: -sum(pnl_of[p["wallet"]] for p in kv[1])):
            share = sum(max(pnl_of[p["wallet"]], 0) for p in xs) / total
            out.append(f"| {arch} | {len(xs)} | {share:.0%} | {_pct(_med(p['roi'] for p in xs))} "
                       f"| {_pct(_med(p['win_rate'] for p in xs))} "
                       f"| {_pct(_med(p['maker_share'] for p in xs))} "
                       f"| {_med(p['trades_per_day'] for p in xs) or 0:.1f} |")
        out.append("")

    top = [profiles[w] for w in groups.get("all-time top", []) if w in profiles]
    if top:
        cats = defaultdict(float)
        for p in top:
            for k, v in p.items():
                if k.startswith("pnl_"):
                    cats[k[4:]] += v
        tot = sum(v for v in cats.values() if v > 0) or 1
        price = {b: sum(p[f"price_{b}"] * p["cost"] for p in top) for b in
                 ("<20c", "20-50c", "50-80c", "80-95c", ">=95c")}
        ptot = sum(price.values()) or 1
        out += ["## All-time top: where the money came from", "",
                "Realized profit by market category: " + ", ".join(
                    f"{c} {_usd(v)} ({v / tot:.0%})" for c, v in
                    sorted(cats.items(), key=lambda kv: -kv[1]) if v > 0) + ".", "",
                "Money spent by entry price: " + ", ".join(
                    f"{b} {v / ptot:.0%}" for b, v in price.items()) + ".", "",
                f"Concentration: {sum(1 for p in top if p['top5_share'] >= 0.8)} of {len(top)} "
                f"made 80%+ of their gains in 5 or fewer markets; median share from the single "
                f"best market {_pct(_med(p['top1_share'] for p in top))}.", "",
                f"Market making: {sum(1 for p in top if p['rewards_usd'] > 0)} received liquidity "
                f"rewards (total {_usd(sum(p['rewards_usd'] for p in top))}); "
                f"{sum(1 for p in top if (p['maker_share'] or 0) >= 0.6)} had 60%+ maker fills "
                "in their recent trades.", "",
                f"Still active (traded in the sample's last 30 days of data): "
                f"{sum(1 for p in top if p['last_trade'] >= '2026-09-21')} of {len(top)}.", ""]

        out += ["## All-time top 30", "",
                "| # | wallet | name | profit | strategy | why | edge per $ | win rate | best category |",
                "|---|---|---|---|---|---|---|---|---|"]
        for i, p in enumerate(top[:30], 1):
            out.append(f"| {i} | `{p['wallet'][:10]}…` | {p['name'][:18]} | {_usd(p['lb_pnl'])} "
                       f"| {p['archetype']} | {p['why']} | {_pct(p['roi'])} | {_pct(p['win_rate'])} "
                       f"| {p['best_category']} |")
        out += ["", "## Examples by strategy (best markets of the top wallets)", ""]
        seen = defaultdict(int)
        for p in top:
            if seen[p["archetype"]] >= 3:
                continue
            seen[p["archetype"]] += 1
            mk = "; ".join(f"{m['title'][:60]} ({m['outcome']} @ {m['avg_price']:.2f}, "
                           f"{_usd(m['pnl'])})" for m in p["top_markets"])
            out.append(f"- **{p['archetype']}** — {p['name'] or p['wallet'][:10]} "
                       f"({_usd(p['lb_pnl'])}): {mk}")
        out.append("")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.exit(main())
