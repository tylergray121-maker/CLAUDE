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
from .sim import SimConfig, profile, simulate

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
    g.add_argument("--fee-bps", type=float, default=d.fee_bps)
    g.add_argument("--min-order", type=float, default=d.min_order_usd)
    g.add_argument("--delay-seconds", type=int, default=0,
                   help="copy latency; fetches CLOB price history per token (slow)")

    g = p.add_argument_group("ranking")
    g.add_argument("--min-buys", type=int, default=15)
    g.add_argument("--include-flagged", action="store_true",
                   help="rank HFT / bonder / 5-minute-market wallets too")
    g.add_argument("--stress-top", type=int, default=25,
                   help="re-run the top N at double slippage")

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
    start_ts = end_ts - args.days * 86400
    split_ts = start_ts + int((end_ts - start_ts) * args.split)
    cfg = SimConfig(start_cash=args.bankroll, base_pct=args.base_pct,
                    max_trade_pct=args.max_trade_pct,
                    max_market_pct=args.max_market_pct, slippage=args.slippage,
                    fee_bps=args.fee_bps, min_order_usd=args.min_order,
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
    conds = {t.condition_id for trades, trunc in histories.values() if not trunc
             for t in trades}
    log.info("resolving %d markets", len(conds))
    markets = fetch_markets(client, conds)

    prices = (PriceHistory(client, start_ts, end_ts + 86400)
              if args.delay_seconds > 0 else None)
    price_at = prices.price_at if prices else None

    # 4. Simulate ----------------------------------------------------------
    rows: list[dict] = []
    curves: dict[str, list] = {}
    for w in wallets:
        if w not in histories:
            continue
        trades, truncated = histories[w]
        prof = profile(trades, start_ts, end_ts, truncated)
        row = {"wallet": w, "name": meta[w].get("name", ""),
               "best_leaderboard_rank": meta[w].get("best_rank"),
               "flags": ";".join(prof.flags), **_prefix(asdict(prof), "lead_")}
        row.pop("lead_flags")
        if trades and not truncated:
            res = simulate(trades, markets, cfg, start_ts, end_ts, split_ts, price_at)
            curves[w] = res.daily_equity
            r = asdict(res)
            r.pop("daily_equity")
            skipped = r.pop("skipped")
            row.update(r)
            row["skipped"] = ";".join(f"{k}={v}" for k, v in sorted(skipped.items()))
        rows.append(row)

    ran = [r for r in rows if "final_equity" in r]
    eligible = [r for r in ran
                if r["buys_copied"] >= args.min_buys and r["train_return_pct"] > 0
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

    # 6. Output ------------------------------------------------------------
    os.makedirs(args.out_dir, exist_ok=True)
    ranked = eligible + sorted([r for r in rows if r["wallet"] not in eligible_ids],
                               key=lambda r: r.get("score", -1e9), reverse=True)
    _write_csv(os.path.join(args.out_dir, "ranking.csv"), ranked)
    _write_curves(os.path.join(args.out_dir, "top_equity_curves.csv"),
                  [r["wallet"] for r in eligible[:10]], curves)
    report = _report(args, cfg, start_ts, end_ts, split_ts, rows, ran, eligible)
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
        f"fee {cfg.fee_bps:g} bps, min order ${cfg.min_order_usd:g}, "
        f"copy delay {cfg.delay_seconds}s.",
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
