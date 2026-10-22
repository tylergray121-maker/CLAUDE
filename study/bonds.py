"""Backtest "bonding": buying near-certain outcomes shortly before close.

For resolved binary markets, take the favorite's price h hours before the
market closed; if it is inside the price band, buy it (paying a spread
allowance plus the Polymarket US taker fee) and collect $1 if it won.

    python -m study.bonds --days 90 --min-volume 20000
"""

from __future__ import annotations

import argparse
import logging
import math
import os
import sys
from bisect import bisect_right
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from statistics import mean, stdev

from copybt.api import CLOB_API, GAMMA_API, Client, HTTPError
from copybt.data import _json_list, _parse_ts

from .features import category

log = logging.getLogger("bonds")

HORIZONS_H = (1, 6, 24, 72, 168)
BANDS = ((0.90, 0.95), (0.95, 0.98), (0.98, 0.995))
US_THETA = 0.0695


def resolved_markets(client: Client, days: int, min_volume: float, cap: int) -> list[dict]:
    end = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(days=days)
    keep = ("conditionId", "question", "slug", "clobTokenIds", "outcomes",
            "outcomePrices", "closedTime", "endDate", "volumeNum", "events")
    out = []
    offset = 0
    while offset < 100000:
        try:
            rows = client.get(GAMMA_API, "/markets", {
                "closed": "true", "end_date_min": start.isoformat(),
                "end_date_max": end.isoformat(), "volume_num_min": min_volume,
                "order": "volumeNum", "ascending": "false", "limit": 500,
                "offset": offset}, keep=keep) or []
        except HTTPError as e:
            log.warning("gamma closed markets offset %d: %s", offset, e)
            break
        for r in rows:
            prices = [float(p) for p in _json_list(r.get("outcomePrices")) or []]
            toks = _json_list(r.get("clobTokenIds"))
            if len(prices) != 2 or len(toks) != 2 or max(prices) < 0.99:
                continue  # binary, decisively resolved only
            closed = _parse_ts(r.get("closedTime")) or _parse_ts(r.get("endDate"))
            if not closed:
                continue
            ev = r.get("events") or []
            out.append({"id": r.get("conditionId"), "question": r.get("question") or "",
                        "slug": r.get("slug") or "", "token0": str(toks[0]),
                        "yes_won": prices[0] > 0.5, "closed": closed,
                        "volume": float(r.get("volumeNum") or 0),
                        "eventSlug": (ev[0] or {}).get("slug", "") if ev else ""})
        if not rows or len(out) >= cap:
            break
        offset += len(rows)  # the API caps pages below the requested limit
    log.info("%d resolved binary markets", len(out))
    return out[:cap]


def price_path(client: Client, m: dict) -> list[tuple[int, float]]:
    """Hourly prices of outcome 0 over the last 8 days before close."""
    try:
        h = client.get(CLOB_API, "/prices-history", {
            "market": m["token0"], "startTs": int(m["closed"] - 8 * 86400),
            "endTs": int(m["closed"]), "fidelity": 60})
    except HTTPError:
        return []
    pts = [(int(x["t"]), float(x["p"])) for x in (h or {}).get("history", [])
           if "t" in x and "p" in x]
    return sorted(pts)


def backtest(markets: list[dict], paths: dict, slippage: float, maker: bool):
    """Returns {(horizon, band): [per-bet returns]} and per-category returns."""
    res, by_cat = defaultdict(list), defaultdict(list)
    for m in markets:
        pts = paths.get(m["id"]) or []
        if not pts:
            continue
        times = [t for t, _ in pts]
        for h in HORIZONS_H:
            i = bisect_right(times, m["closed"] - h * 3600) - 1
            if i < 0 or m["closed"] - h * 3600 - times[i] > 6 * 3600:
                continue  # no recent enough price at that horizon
            p0 = pts[i][1]
            side_won = m["yes_won"]
            p = p0
            if 1 - p0 > p0:          # favorite is outcome 1
                p, side_won = 1 - p0, not m["yes_won"]
            for lo, hi in BANDS:
                if lo <= p < hi:
                    cost = min(p + slippage, 0.999)
                    if not maker:
                        cost += US_THETA * cost * (1 - cost)
                    r = (1.0 if side_won else 0.0) / cost - 1
                    res[(h, (lo, hi))].append(r)
                    if h == 24:
                        by_cat[category(m)].append(r)
    return res, by_cat


def summarize(rs: list[float]) -> dict:
    if len(rs) < 2:
        return {"n": len(rs)}
    m, sd = mean(rs), stdev(rs)
    losses = sum(1 for r in rs if r < -0.5)
    return {"n": len(rs), "mean": m, "t": m / (sd / math.sqrt(len(rs))) if sd else 0.0,
            "loss_rate": losses / len(rs)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="study.bonds")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--min-volume", type=float, default=20000)
    ap.add_argument("--max-markets", type=int, default=6000)
    ap.add_argument("--slippage", type=float, default=0.005)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-rps", type=float, default=10)
    ap.add_argument("--cache-dir", default=".cache-study")
    ap.add_argument("--out-dir", default="studyresults")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    client = Client(cache_dir=a.cache_dir, max_rps=a.max_rps)
    markets = resolved_markets(client, a.days, a.min_volume, a.max_markets)
    with ThreadPoolExecutor(a.workers) as pool:
        paths = dict(zip([m["id"] for m in markets],
                         pool.map(lambda m: price_path(client, m), markets)))
    log.info("price paths for %d markets", sum(1 for p in paths.values() if p))

    lines = ["# Bonding backtest: buy the favorite shortly before close", "",
             f"{len(markets)} decisively resolved binary markets closing in the last "
             f"{a.days} days with ${a.min_volume:,.0f}+ volume; favorite bought at the "
             f"last hourly price before each horizon, plus {100 * a.slippage:.1f}¢ "
             "slippage. Return per bet = payout / cost − 1.", ""]
    for maker, label in ((False, "taker (pays the Polymarket US fee)"),
                         (True, "maker (no fee; assumes your resting bid fills)")):
        res, by_cat = backtest(markets, paths, a.slippage, maker)
        lines += [f"## As {label}", "",
                  "| hours before close | price band | bets | losses | avg return per bet | t-stat |",
                  "|---|---|---|---|---|---|"]
        for h in HORIZONS_H:
            for band in BANDS:
                s = summarize(res.get((h, band), []))
                if s["n"] < 2:
                    continue
                lines.append(f"| {h} | {band[0]:.2f}–{band[1]:.3f} | {s['n']} | "
                             f"{s['loss_rate']:.1%} | {s['mean']:+.2%} | {s['t']:.1f} |")
        lines += ["", "24 hours before close, all bands, by category: " + ", ".join(
            f"{c} {mean(v):+.2%} ({len(v)} bets)" for c, v in
            sorted(by_cat.items(), key=lambda kv: -len(kv[1])) if len(v) >= 10) + ".", ""]
    os.makedirs(a.out_dir, exist_ok=True)
    with open(os.path.join(a.out_dir, "bonds.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
