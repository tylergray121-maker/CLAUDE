"""Backtest copy-trading every reachable Polymarket wallet with a small bankroll.

    python -m copybt --days 90 --bankroll 200
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
from datetime import datetime, timezone

from .api import Client
from .data import PriceHistory, fetch_leaderboard, fetch_markets, fetch_trades
from .portfolio import build_plan, render
from .sim import SimConfig, profile, simulate
from .us import fetch_us_markets

log = logging.getLogger("copybt")


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="copybt", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_argument_group("universe")
    g.add_argument("--wallets-file", help="extra wallets, one 0x address per line "
                   "(e.g. picks copied from Gravia)")
    g.add_argument("--no-leaderboard", action="store_true",
                   help="only backtest --wallets-file")
    g.add_argument("--categories", default="OVERALL",
                   help="comma list: OVERALL,POLITICS,SPORTS,CRYPTO,CULTURE,...")
    g.add_argument("--per-board", type=int, default=500,
                   help="wallets per leaderboard (period x order x category)")
    g.add_argument("--max-wallets", type=int, default=1500)
    g.add_argument("--max-trades", type=int, default=20000,
                   help="wallets with more trades in the window are flagged, not run")

    g = p.add_argument_group("window")
    g.add_argument("--days", type=int, default=90)
    g.add_argument("--end", help="window end, ISO time (default: now, hour-aligned); "
                   "pin it to reuse a previous run's cache")
    g.add_argument("--split", type=float, default=0.67,
                   help="fraction of the window used to qualify; the rest is the test")

    g = p.add_argument_group("copy rules")
    d = SimConfig()
    g.add_argument("--bankroll", type=float, default=d.start_cash)
    g.add_argument("--base-pct", type=float, default=d.base_pct)
    g.add_argument("--max-trade-pct", type=float, default=d.max_trade_pct)
    g.add_argument("--max-market-pct", type=float, default=d.max_market_pct)
    g.add_argument("--slippage", type=float, default=d.slippage,
                   help="absolute price penalty per fill, e.g. 0.01 = 1 cent")
    g.add_argument("--fee-bps", type=float, default=d.fee_bps,
                   help="flat fee on top of each market's own taker fees")
    g.add_argument("--no-market-fees", action="store_true",
                   help="ignore Polymarket's per-market taker fees")
    g.add_argument("--min-order", type=float, default=d.min_order_usd)
    g.add_argument("--delay-seconds", type=int, default=30,
                   help="copy latency, priced from CLOB price history; applied to "
                   "the shortlist (0 = fill at the leader's price)")
    g.add_argument("--shortlist", type=int, default=60,
                   help="wallets re-simulated with the copy delay")

    g = p.add_argument_group("ranking")
    g.add_argument("--min-buys", type=int, default=15)
    g.add_argument("--include-flagged", action="store_true",
                   help="rank HFT / bonder / 5-minute-market wallets too")
    g.add_argument("--stress-top", type=int, default=25,
                   help="re-run the top N at double slippage")
    g.add_argument("--no-us", action="store_true",
                   help="skip the Polymarket US (New York) market filter")

    g = p.add_argument_group("runtime")
    g.add_argument("--workers", type=int, default=8)
    g.add_argument("--max-rps", type=float, default=8.0)
    g.add_argument("--cache-dir", default=".cache")
    g.add_argument("--out-dir", default="results")
    g.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def load_wallet_file(path: str) -> list[str]:
    out = []
    with open(path) as f:
        for line in f:
            w = line.strip().split(",")[0].strip().lower()
            if w.startswith("0x") and len(w) == 42:
                out.append(w)
    return out


def score(row: dict) -> float:
    # Out-of-sample return, penalised by the worst drawdown over the window.
    return row["test_return_pct"] - 0.5 * row["max_drawdown_pct"]


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    client = Client(cache_dir=args.cache_dir, max_rps=args.max_rps)

    end_ts = int(time.time()) // 3600 * 3600  # hour-aligned so caches are reusable
    if args.end:
        end_ts = int(datetime.fromisoformat(args.end.replace("Z", "+00:00"))
                     .timestamp())
    start_ts = end_ts - args.days * 86400
    split_ts = start_ts + int((end_ts - start_ts) * args.split)
    cfg = SimConfig(start_cash=args.bankroll, base_pct=args.base_pct,
                    max_trade_pct=args.max_trade_pct,
                    max_market_pct=args.max_market_pct, slippage=args.slippage,
                    fee_bps=args.fee_bps, market_fees=not args.no_market_fees,
                    min_order_usd=args.min_order,
                    delay_seconds=args.delay_seconds)

    # 1. Wallet universe ---------------------------------------------------
    meta: dict[str, dict] = {}
    if not args.no_leaderboard:
        cats = [c.strip().upper() for c in args.categories.split(",") if c.strip()]
        meta = fetch_leaderboard(client, categories=cats, per_board=args.per_board)
    if args.wallets_file:
        for w in load_wallet_file(args.wallets_file):
            meta.setdefault(w, {"name": "", "best_rank": 0, "boards": ["file"]})
    wallets = sorted(meta, key=lambda w: meta[w]["best_rank"])[:args.max_wallets]
    if not wallets:
        log.error("no wallets found: check network access to data-api.polymarket.com")
        return 1
    log.info("backtesting %d wallets over %d days", len(wallets), args.days)

    # 2. Trade histories ---------------------------------------------------
    histories: dict[str, tuple[list, bool]] = {}
    with ThreadPoolExecutor(args.workers) as pool:
        futs = {pool.submit(fetch_trades, client, w, start_ts, end_ts,
                            args.max_trades): w for w in wallets}
        for i, fut in enumerate(as_completed(futs), 1):
            w = futs[fut]
            try:
                histories[w] = fut.result()
            except Exception as e:  # keep going; one bad wallet shouldn't stop the run
                log.warning("trades for %s failed: %s", w, e)
            if i % 50 == 0 or i == len(futs):
                log.info("fetched %d/%d wallets (%d requests)", i, len(futs),
                         client.requests_made)

    # 3. Market resolutions ------------------------------------------------
    # Only wallets that can be ranked need their markets resolved; flagged
    # wallets (bots, 5-minute markets, bonders) are most of the market count.
    profiles = {w: profile(trades, start_ts, end_ts, trunc)
                for w, (trades, trunc) in histories.items()}
    to_run = {w for w, (trades, trunc) in histories.items()
              if trades and not trunc
              and (args.include_flagged or not profiles[w].flags)}
    conds = {t.condition_id for w in to_run for t in histories[w][0]}
    log.info("%d wallets to simulate (%d flagged as hard to copy); resolving %d markets",
             len(to_run), sum(1 for p in profiles.values() if p.flags), len(conds))
    markets = fetch_markets(client, conds, workers=args.workers)

    prices = PriceHistory(client) if args.delay_seconds > 0 else None
    price_at = prices.price_at if prices else None

    # 4. Simulate ----------------------------------------------------------
    # Pass 1 fills at the leader's price for every wallet (cheap). Wallets
    # that look promising in either the qualifying or the most recent window
    # are then re-run with the copy delay priced from market history.
    span = split_ts - start_ts
    quick, quick_recent = {}, {}
    for w in to_run:
        trades = histories[w][0]
        quick[w] = simulate(trades, markets, cfg, start_ts, end_ts, split_ts)
        quick_recent[w] = simulate(trades, markets, cfg, end_ts - span, end_ts,
                                   end_ts - span // 2)

    def promise(w):
        a, b = quick[w], quick_recent[w]
        sa = (a.train_return_pct - 0.5 * a.train_max_drawdown_pct
              if a.buys_copied >= args.min_buys else -1e9)
        sb = (b.return_pct - 0.5 * b.max_drawdown_pct
              if b.buys_copied >= args.min_buys else -1e9)
        return max(sa, sb)

    shortlist = {w for w in sorted(to_run, key=promise, reverse=True)[:args.shortlist]
                 if promise(w) > 0}
    if prices:
        log.info("re-simulating %d shortlisted wallets with a %ds copy delay",
                 len(shortlist), args.delay_seconds)
        prices.prefetch({(t.asset, t.ts + args.delay_seconds)
                         for w in shortlist for t in histories[w][0]
                         if t.condition_id in markets}, workers=args.workers)

    rows: list[dict] = []
    curves: dict[str, list] = {}
    for w in wallets:
        if w not in histories:
            continue
        trades, _ = histories[w]
        prof = profiles[w]
        row = {"wallet": w, "name": meta[w].get("name", ""),
               "best_leaderboard_rank": meta[w].get("best_rank"),
               "flags": ";".join(prof.flags), **_prefix(asdict(prof), "lead_")}
        row.pop("lead_flags")
        if w in to_run:
            res = (simulate(trades, markets, cfg, start_ts, end_ts, split_ts, price_at)
                   if w in shortlist and price_at else quick[w])
            row["shortlisted"] = w in shortlist
            curves[w] = res.daily_equity
            r = asdict(res)
            r.pop("daily_equity")
            skipped = r.pop("skipped")
            row.update(r)
            row["skipped"] = ";".join(f"{k}={v}" for k, v in sorted(skipped.items()))
        rows.append(row)

    ran = [r for r in rows if "final_equity" in r]
    eligible = [r for r in ran
                if r["shortlisted"]
                and r["buys_copied"] >= args.min_buys and r["train_return_pct"] > 0
                and (args.include_flagged or not r["flags"])]
    eligible_ids = {r["wallet"] for r in eligible}
    for r in ran:
        r["score"] = round(score(r), 2)
        r["eligible"] = r["wallet"] in eligible_ids
    eligible.sort(key=score, reverse=True)

    # 5. Stress test the leaders -------------------------------------------
    stress_cfg = replace(cfg, slippage=cfg.slippage * 2)
    for r in eligible[:args.stress_top]:
        trades, _ = histories[r["wallet"]]
        s = simulate(trades, markets, stress_cfg, start_ts, end_ts, split_ts, price_at)
        r["return_pct_2x_slippage"] = s.return_pct

    # 6. Portfolios: all markets, and only markets also on Polymarket US ----
    os.makedirs(args.out_dir, exist_ok=True)
    run_hist = {w: histories[w][0] for w in shortlist}
    plans = [build_plan("Plan A — all Polymarket markets", run_hist, markets, cfg,
                        start_ts, end_ts, split_ts, args.min_buys, price_at=price_at)]
    us_note = ""
    if not args.no_us:
        us = fetch_us_markets(client)
        if len(us):
            us_hist = {w: [t for t in tr if us.lists(t.title, t.slug)]
                       for w, tr in run_hist.items()}
            n_all = sum(len(t) for t in run_hist.values())
            n_us = sum(len(t) for t in us_hist.values())
            titles = {t.title for tr in us_hist.values() for t in tr}
            us_note = (f"Polymarket US lists {len(us.questions)} markets; "
                       f"{n_us} of {n_all} copyable trades "
                       f"({(n_us / n_all if n_all else 0):.0%}) were in markets "
                       f"matched to it ({len(titles)} distinct markets).")
            with open(os.path.join(args.out_dir, "us_matched_markets.txt"), "w") as f:
                f.write("\n".join(sorted(titles)))
            plans.append(build_plan(
                "Plan B — only markets also listed on Polymarket US (usable from New York)",
                us_hist, markets, cfg, start_ts, end_ts, split_ts, args.min_buys,
                price_at=price_at))
        else:
            us_note = ("Could not load the Polymarket US market list, so no "
                       "New York-usable plan was produced.")
        log.info(us_note)

    for i, plan in enumerate(plans):
        if plan.recent and plan.recent.fills:
            name = "picks_trades_" + ("all" if i == 0 else "us") + ".csv"
            _write_csv(os.path.join(args.out_dir, name), [
                {**f, "date": datetime.fromtimestamp(f["ts"], timezone.utc)
                 .strftime("%Y-%m-%d %H:%M")} for f in plan.recent.fills])

    # 7. Output ------------------------------------------------------------
    ranked = eligible + sorted([r for r in rows if r["wallet"] not in eligible_ids],
                               key=lambda r: r.get("score", -1e9), reverse=True)
    _write_csv(os.path.join(args.out_dir, "ranking.csv"), ranked)
    _write_curves(os.path.join(args.out_dir, "top_equity_curves.csv"),
                  [r["wallet"] for r in eligible[:10]], curves)
    report = _report(args, cfg, start_ts, end_ts, split_ts, rows, ran, eligible)
    head, _, rest = report.partition("## Recommendation")
    portfolio_md = [us_note, ""] if us_note else []
    if prices:
        total = prices.hits + prices.misses
        portfolio_md += [
            f"Copy delay: {prices.hits} of {total} simulated fills "
            f"({(prices.hits / total if total else 0):.0%}) were priced from market "
            "history 30s after the leader; the rest fell back to the leader's "
            "price.", ""]
    for plan in plans:
        portfolio_md += render(plan, cfg, _date)
    report = (head + "\n".join(portfolio_md) + "\n"
              + ("## Best single wallets (ranked with hindsight)" + rest.replace(
                  "## Top 15", "### Top 15") if rest else ""))
    with open(os.path.join(args.out_dir, "report.md"), "w") as f:
        f.write(report)
    print(report)
    return 0


def _prefix(d: dict, p: str) -> dict:
    return {p + k: v for k, v in d.items()}


def _write_csv(path: str, rows: list[dict]) -> None:
    cols: list[str] = []
    for r in rows:
        cols += [k for k in r if k not in cols]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v)
                        for k, v in r.items()})


def _write_curves(path: str, wallets: list[str], curves: dict) -> None:
    if not wallets:
        return
    days = [d for d, _ in curves[wallets[0]]]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date"] + wallets)
        for i, d in enumerate(days):
            w.writerow([_date(d)] + [round(curves[x][i][1], 2) for x in wallets])


def _date(ts: int) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d")


def _report(args, cfg, start_ts, end_ts, split_ts, rows, ran, eligible) -> str:
    flagged = sum(1 for r in rows if r["flags"])
    lines = [
        "# Polymarket copy-trade backtest",
        "",
        f"Window {_date(start_ts)} → {_date(end_ts)} ({args.days} days); "
        f"qualify until {_date(split_ts)}, test after.",
        f"Bankroll ${cfg.start_cash:.0f}; {cfg.base_pct:.0%} of equity per typical "
        f"leader buy (scaled by leader conviction {cfg.conviction_min}–"
        f"{cfg.conviction_max}x), max {cfg.max_trade_pct:.0%} per trade, "
        f"{cfg.max_market_pct:.0%} per market; slippage {cfg.slippage*100:.1f}¢/fill, "
        f"{'market taker fees' if cfg.market_fees else 'no market fees'} "
        f"+ {cfg.fee_bps:g} bps, min order ${cfg.min_order_usd:g}, "
        f"copy delay {args.delay_seconds}s (shortlist), never more than the "
        f"leader's own trade size.",
        "",
        f"Wallets examined: {len(rows)}; simulated: {len(ran)}; "
        f"flagged as hard to copy: {flagged}; eligible for ranking: {len(eligible)}.",
        "",
    ]
    if not eligible:
        lines.append("No wallet passed the filters (profitable in the qualifying "
                     "period, enough copyable buys, no copyability flags).")
        return "\n".join(lines) + "\n"

    best = eligible[0]
    lines += [
        "## Recommendation",
        "",
        f"**{best['wallet']}** {('(' + best['name'] + ')') if best['name'] else ''}",
        "",
        f"- $200 → ${best['final_equity']:.2f} over the window "
        f"({best['return_pct']:+.1f}%), max drawdown {best['max_drawdown_pct']:.1f}%",
        f"- Qualifying period {best['train_return_pct']:+.1f}%, "
        f"out-of-sample test {best['test_return_pct']:+.1f}%",
        f"- At double slippage: {best.get('return_pct_2x_slippage', float('nan')):+.1f}%",
        f"- {best['buys_copied']} buys / {best['sells_copied']} sells copied across "
        f"{best['markets_traded']} markets, win rate {best['win_rate']:.0%}",
        f"- Leader: {best['lead_trades_per_day']:.1f} trades/day, median trade "
        f"${best['lead_median_trade_usd']:.0f}, avg buy price "
        f"{best['lead_avg_buy_price']*100:.0f}¢",
        "",
        "## Top 15",
        "",
        "| # | wallet | name | return | test | max DD | 2x slip | buys | win |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(eligible[:15], 1):
        lines.append(
            f"| {i} | `{r['wallet']}` | {r['name'][:20]} | {r['return_pct']:+.1f}% | "
            f"{r['test_return_pct']:+.1f}% | {r['max_drawdown_pct']:.1f}% | "
            f"{r.get('return_pct_2x_slippage', float('nan')):+.1f}% | "
            f"{r['buys_copied']} | {r['win_rate']:.0%} |")
    lines += [
        "",
        "Score = out-of-sample return − 0.5 × max drawdown. Full table in "
        "`ranking.csv`; daily equity for the top 10 in `top_equity_curves.csv`.",
        "",
        "Caveats: past results don't predict future ones; fills assume you get the "
        "leader's price plus slippage; open positions are marked at the current "
        "market price; wallets that started positions before the window are only "
        "copied from their first in-window buy.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
