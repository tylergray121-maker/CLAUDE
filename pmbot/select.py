"""Choose the wallets copytop follows by backtesting copytop itself.

    python -m pmbot.select --days 45 --out-dir selectresults

Each candidate sports wallet's buys are replayed the way copytop copies them
on Polymarket US: only markets US listed (each one looked up on the US
gateway under the prefix US uses for that league and kind of market: game
winners, soccer results, totals); priced at our copy delay from CLOB
minute bars plus half a cent of spread; skipped when that is more than 1c
above the leader's price (copytop never chases); $10 a signal, one signal
per wallet and outcome per 10 minutes, at most $50 in an outcome; the US
taker fee; the leader's sells closing ours when the price holds, settlement
otherwise. Wallets are chosen on the first part of the window and checked
on the rest, so the report shows whether choosing this way held up, and
which patterns (league, market, price, timing, conviction) helped or hurt.

The universe comes from volume leaderboards and the all-time profit board:
weekly or monthly profit boards pick wallets for having just won, which
overlaps the test window and would flatter it.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import math
import os
import re
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, replace
from statistics import median

from collections import Counter

from copybt.api import Client, HTTPError
from copybt.data import PriceHistory, fetch_leaderboard, fetch_markets, fetch_trades

from . import data as pmdata
from .copy import league, load_leaders, price_band
from .fees import taker_fee
from .mapping import intl_slug

log = logging.getLogger("pmbot.select")

_DATE = r"[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-\d{4}-\d{2}-\d{2}"
_KINDS = ((re.compile(rf"^{_DATE}$"), "moneyline"),
          (re.compile(rf"^{_DATE}-(?:total-)?\d+pt\d+$"), "totals"),
          (re.compile(rf"^{_DATE}-[a-z0-9]+$"), "result"))


_TOTAL = re.compile(r"-total-(?=\d+pt\d+$)")


def us_name(intl: str) -> str:
    """The international slug as US names it (totals drop '-total-')."""
    return _TOTAL.sub("-", intl)


def kind_of(slug: str) -> str:
    """Game winner, total, or one-outcome result market ('...-ray', '...-draw'),
    by the international (or prefix-stripped US) slug; '' for anything else."""
    for rx, k in _KINDS:
        if rx.match(slug):
            return k
    return ""


@dataclass
class Rules:
    delay_s: int = 30          # signal to order: data API lag plus one poll
    half_spread: float = 0.005  # US ask over the minute-bar price
    max_slip: float = 0.01     # copytop's limit over the leader's price
    stake: float = 10.0
    market_cap: float = 50.0
    dedupe_s: int = 600
    min_leader_usd: float = 5.0
    min_price: float = 0.05
    max_price: float = 0.95
    copy_sells: bool = True
    conviction_sizing: bool = False  # stake x0.5 under 0.5x their usual bet, x1.5 at 2x+
    min_conviction: float = 0.0      # skip bets smaller than this multiple of their usual
    pregame_only: bool = False


def copies(trades, markets, pairs, rules: Rules, price_at=None) -> list[dict]:
    """Simulated copytop lots for one wallet's trades, oldest first."""
    out: list[dict] = []
    held: dict[str, list[dict]] = defaultdict(list)
    spent: dict[str, float] = defaultdict(float)
    last: dict[str, int] = {}
    sizes: list[float] = []
    for t in trades:
        lg, k = league(t.slug), kind_of(t.slug)
        if (lg, k) not in pairs:
            continue
        p = price_at(t.asset, t.ts + rules.delay_s) if price_at else None
        if t.side == "BUY":
            notional = t.price * t.size
            prior = median(sizes[-200:]) if sizes else notional
            sizes.append(notional)
            if notional < rules.min_leader_usd or t.ts - last.get(t.asset, -10**12) < rules.dedupe_s:
                continue
            conviction = notional / prior if prior > 0 else 1.0
            if conviction < rules.min_conviction:
                continue
            m = markets.get(t.condition_id)
            start = m.start_ts if m else None
            if rules.pregame_only and (not start or t.ts >= start):
                continue
            ask = round((p if p is not None else t.price) + rules.half_spread, 4)
            if ask > t.price + rules.max_slip + 1e-9:
                out.append({"wallet": t.wallet, "ts": t.ts, "skipped": "price_moved"})
                continue
            if not rules.min_price <= ask <= rules.max_price:
                continue
            stake = rules.stake * (stake_multiple(conviction) if rules.conviction_sizing else 1.0)
            qty = int(min(stake, rules.market_cap - spent[t.asset]) // ask)
            if qty < 1:
                continue
            last[t.asset] = t.ts
            spent[t.asset] += ask * qty
            lot = {"wallet": t.wallet, "ts": t.ts, "slug": t.slug, "title": t.title,
                   "outcome": t.outcome, "asset": t.asset, "cond": t.condition_id,
                   "league": lg, "kind": k, "leader_price": t.price, "price": ask,
                   "qty": qty, "cost": round(ask * qty + taker_fee(ask, qty), 4),
                   "price_band": price_band(ask),
                   "timing": ("unknown" if not start else
                              "in-play" if t.ts >= start else "pre-game"),
                   "hours_to_start": round((start - t.ts) / 3600, 2) if start else None,
                   "conviction": round(conviction, 3),
                   "delay_move": round(p - t.price, 4) if p is not None else None,
                   "leader_usd": round(notional, 2), "exit": None, "pnl": None}
            held[t.asset].append(lot)
            out.append(lot)
        elif rules.copy_sells and held.get(t.asset):
            bid = round((p if p is not None else t.price) - rules.half_spread, 4)
            if bid < t.price - rules.max_slip - 1e-9 or bid <= 0:
                continue
            for lot in held.pop(t.asset):
                fee = taker_fee(bid, lot["qty"])
                lot.update(exit="sell", exit_ts=t.ts,
                           pnl=round(bid * lot["qty"] - fee - lot["cost"], 4))
    for asset, lots in held.items():
        for lot in lots:
            m = markets.get(lot["cond"])
            if m and m.resolved and asset in m.prices:
                lot.update(exit="settle", exit_ts=m.resolve_ts,
                           pnl=round(lot["qty"] * m.prices[asset] - lot["cost"], 4))
    return out


def stake_multiple(conviction: float) -> float:
    """Bet more when they bet big relative to their usual size."""
    return 0.5 if conviction < 0.5 else 1.5 if conviction >= 2 else 1.0


def us_prefixes(us) -> dict[tuple, str]:
    """The slug prefix US uses for each (league, kind), e.g. ('nba', 'totals') -> 'tsc'."""
    seen: dict[tuple, Counter] = defaultdict(Counter)
    for m in us:
        intl = intl_slug(m.slug)
        k = kind_of(intl)
        if k:
            seen[(league(intl), k)][m.slug.split("-", 1)[0]] += 1
    return {key: c.most_common(1)[0][0] for key, c in seen.items()}


def listed_on_us(client: Client, intl: str, prefix: str) -> bool:
    try:
        r = client.get(pmdata.US_GATEWAY, f"/v1/market/slug/{prefix}-{us_name(intl)}")
    except HTTPError:
        return False
    return bool(isinstance(r, dict) and (r.get("market") or r.get("slug")))


def stats(lots: list[dict]) -> dict:
    """Per-copy return statistics over closed lots."""
    closed = [x for x in lots if x.get("pnl") is not None]
    rs = [x["pnl"] / x["cost"] for x in closed if x["cost"] > 0]
    n = len(rs)
    staked = sum(x["cost"] for x in closed)
    pnl = sum(x["pnl"] for x in closed)
    mean = sum(rs) / n if n else 0.0
    sd = math.sqrt(sum((r - mean) ** 2 for r in rs) / (n - 1)) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n else 0.0
    return {"n": n, "won": sum(1 for x in closed if x["pnl"] > 0),
            "staked": round(staked, 2), "pnl": round(pnl, 2),
            "roi": round(pnl / staked, 4) if staked else None,
            "mean": round(mean, 4), "t": round(mean / se, 2) if se > 0 else None,
            "lcb": round(mean - se, 4) if n else None}


def pick(by_wallet: dict[str, list[dict]], min_n: int, k: int,
         active_since: int | None = None) -> list[str]:
    """Top ``k`` wallets by the lower confidence bound (mean - 1 s.e.) of their
    per-copy return, among those with ``min_n`` closed copies and a positive
    bound (and a copy since ``active_since``, if given)."""
    scored = []
    for w, lots in by_wallet.items():
        s = stats(lots)
        if s["n"] < min_n or not s["lcb"] or s["lcb"] <= 0:
            continue
        if active_since and not any(x["ts"] >= active_since for x in lots if "price" in x):
            continue
        scored.append((s["lcb"], w))
    return [w for _, w in sorted(scored, reverse=True)[:k]]


def _segments(lots: list[dict]) -> dict[str, list[dict]]:
    seg: dict[str, list[dict]] = defaultdict(list)
    for x in lots:
        if "price" not in x:
            continue
        c = x["conviction"]
        dm = x["delay_move"]
        for key in (f"league:{x['league']}", f"kind:{x['kind']}",
                    f"price:{x['price_band']}", f"timing:{x['timing']}",
                    "conviction:" + ("under 0.5x" if c < 0.5 else "0.5-1x" if c < 1
                                     else "1-2x" if c < 2 else "2x+"),
                    "delay_move:" + ("n/a" if dm is None else "price fell" if dm < -0.0049
                                     else "flat" if dm < 0.0051 else "price rose"),
                    f"exit:{x['exit'] or 'open'}"):
            seg[key].append(x)
    return seg


def _row(label: str, s: dict) -> str:
    f = lambda v, fmt: "—" if v is None else format(v, fmt)
    return (f"| {label} | {s['n']} | {s['won']} | ${s['staked']:,.0f} | {s['pnl']:+,.2f} | "
            f"{f(s['roi'], '+.1%')} | {f(s['t'], '+.2f')} |")


HEAD = "| | copies | won | staked | P&L | return | t |\n|---|---|---|---|---|---|---|"


def parse_args(argv=None):
    p = argparse.ArgumentParser(prog="pmbot.select", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--days", type=int, default=45)
    p.add_argument("--split", type=float, default=0.67, help="share of the window to choose on")
    p.add_argument("--per-board", type=int, default=100)
    p.add_argument("--max-trades", type=int, default=15000)
    p.add_argument("--shortlist", type=int, default=60,
                   help="wallets re-simulated with copy-delay prices")
    p.add_argument("--min-copies", type=int, default=15,
                   help="closed copies needed to be chosen (on the choosing window)")
    p.add_argument("--leaders", type=int, default=16)
    p.add_argument("--delay", type=int, default=Rules.delay_s)
    p.add_argument("--leaders-file", default=os.path.join(os.path.dirname(__file__),
                                                          "leaders.json"))
    p.add_argument("--workers", type=int, default=10)
    p.add_argument("--max-rps", type=float, default=15.0)
    p.add_argument("--cache-dir", default=".cache-select")
    p.add_argument("--out-dir", default="selectresults")
    return p.parse_args(argv)


def main(argv=None) -> int:
    a = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    os.makedirs(a.out_dir, exist_ok=True)
    client = Client(cache_dir=a.cache_dir, max_rps=a.max_rps)
    end_ts = int(time.time()) // 3600 * 3600
    start_ts = end_ts - a.days * 86400
    split_ts = start_ts + int((end_ts - start_ts) * a.split)

    # What Polymarket US lists now: (league, kind of market).
    us = pmdata.us_markets(Client(cache_dir=None, max_rps=a.max_rps))
    pairs = {(league(s), kind_of(s)) for s in (intl_slug(m.slug) for m in us
                                              if m.market_type not in pmdata.LONG_RUNNING)}
    pairs = {p for p in pairs if p[1]}
    log.info("Polymarket US lists %d league/market kinds", len(pairs))

    # Candidates.
    meta = fetch_leaderboard(client, periods=("WEEK", "MONTH", "ALL"), orders=("VOL",),
                             categories=("SPORTS",), per_board=a.per_board)
    for w, m in fetch_leaderboard(client, periods=("ALL",), orders=("PNL",),
                                  categories=("SPORTS",), per_board=a.per_board).items():
        meta.setdefault(w, m)
    current = load_leaders(a.leaders_file)
    for w, name in current.items():
        meta.setdefault(w, {"name": name, "best_rank": 0, "boards": ["current"]})
    wallets = sorted(meta)
    log.info("%d candidate wallets (%d currently copied)", len(wallets), len(current))

    # Trades, kept only where copytop could copy them.
    hist: dict[str, list] = {}
    truncated: set[str] = set()
    with ThreadPoolExecutor(a.workers) as pool:
        futs = {pool.submit(fetch_trades, client, w, start_ts, end_ts, a.max_trades): w
                for w in wallets}
        for i, fut in enumerate(as_completed(futs), 1):
            w = futs[fut]
            try:
                trades, trunc = fut.result()
            except Exception as e:
                log.warning("trades %s: %s", w, e)
                continue
            if trunc:
                truncated.add(w)
            hist[w] = [t for t in trades if (league(t.slug), kind_of(t.slug)) in pairs]
            if i % 50 == 0 or i == len(futs):
                log.info("trades: %d/%d wallets", i, len(futs))
    hist = {w: t for w, t in hist.items() if t and w not in truncated}
    # Exactly which of these markets US listed (open now, or looked up by slug).
    open_now = {us_name(intl_slug(m.slug)) for m in us}
    prefix = us_prefixes(us)
    slugs = sorted({t.slug for ts in hist.values() for t in ts})
    todo = [x for x in slugs if us_name(x) not in open_now]
    found = {x for x in slugs if us_name(x) in open_now}
    with ThreadPoolExecutor(a.workers) as pool:
        for x, ok in zip(todo, pool.map(lambda x: listed_on_us(
                client, x, prefix[(league(x), kind_of(x))]), todo)):
            if ok:
                found.add(x)
    by_pair: dict[tuple, list] = defaultdict(lambda: [0, 0])
    for x in slugs:
        e = by_pair[(league(x), kind_of(x))]
        e[0] += x in found
        e[1] += 1
    log.info("listed on Polymarket US: %d of %d markets the candidates traded; by league: %s",
             len(found), len(slugs), ", ".join(f"{lg}/{k} {a}/{b}" for (lg, k), (a, b) in
                                                 sorted(by_pair.items(), key=lambda kv: -kv[1][1])[:30]))
    hist = {w: [t for t in ts if t.slug in found] for w, ts in hist.items()}
    hist = {w: t for w, t in hist.items() if t}
    conds = {t.condition_id for ts in hist.values() for t in ts}
    log.info("%d wallets with copyable trades (%d skipped as too high-frequency); "
             "resolving %d markets", len(hist), len(truncated), len(conds))
    markets = fetch_markets(client, conds, workers=a.workers)

    # Holding to settlement beat copying their sells in both windows of the
    # first run (their exits lose the spread and the fee twice); it is the base.
    rules = replace(Rules(), delay_s=a.delay, copy_sells=False)
    # Pass 1: at the leader's price plus spread, every wallet.
    quick = {w: copies(t, markets, pairs, rules) for w, t in hist.items()}
    train_q = {w: [x for x in lots if x["ts"] < split_ts] for w, lots in quick.items()}
    # The validation pool is chosen on the first part only; final candidates
    # on the whole window (they never feed the validation numbers).
    pool_val = set(pick(train_q, a.min_copies, a.shortlist))
    short = pool_val | set(pick(quick, a.min_copies, a.shortlist)) | {w for w in current if w in hist}
    log.info("re-pricing %d wallets at a %ds copy delay", len(short), a.delay)
    prices = PriceHistory(client)
    prices.prefetch({(t.asset, t.ts + d) for w in short for t in hist[w]
                     for d in {a.delay, 15, 60}}, workers=a.workers)

    def run(r: Rules) -> dict[str, list[dict]]:
        return {w: copies(hist[w], markets, pairs, r, prices.price_at) for w in short}

    lots = run(rules)
    train = {w: [x for x in v if x["ts"] < split_ts] for w, v in lots.items()}
    test = {w: [x for x in v if x["ts"] >= split_ts] for w, v in lots.items()}

    # Validation: choose on the first part, score on the rest.
    chosen = pick({w: v for w, v in train.items() if w in pool_val}, a.min_copies, a.leaders)
    flat = lambda d, ws: [x for w in ws for x in d.get(w, [])]
    v_rows = [("chosen on the first part (test window)", stats(flat(test, chosen))),
              ("every wallet that qualified on the first part (test window)",
               stats(flat(test, pool_val))),
              ("currently copied (test window)", stats(flat(test, [w for w in current if w in short])))]

    # Patterns, chosen on train and checked on test, across the chosen wallets.
    seg_tr, seg_te = _segments(flat(train, chosen)), _segments(flat(test, chosen))

    # Variants on the chosen wallets.
    variants = []
    for label, r in ((f"base: {a.delay}s delay, 1c limit, hold to settlement", rules),
                     ("copy their sells too", replace(rules, copy_sells=True)),
                     ("size by conviction (x0.5 / x1 / x1.5)", replace(rules, conviction_sizing=True)),
                     ("skip bets under 0.5x their usual", replace(rules, min_conviction=0.5)),
                     ("pre-game only", replace(rules, pregame_only=True)),
                     ("15s delay", replace(rules, delay_s=15)),
                     ("60s delay", replace(rules, delay_s=60)),
                     ("allow 2c over their price", replace(rules, max_slip=0.02))):
        d = {w: copies(hist[w], markets, pairs, r, prices.price_at) for w in chosen}
        variants.append((label, stats(flat({w: [x for x in v if x["ts"] >= split_ts]
                                             for w, v in d.items()}, chosen)),
                         stats(flat(d, chosen))))

    # Final pick on the whole window, among wallets copied in the last week.
    final = pick(lots, a.min_copies + 5, a.leaders, active_since=end_ts - 7 * 86400)

    # Outputs.
    names = {w: meta.get(w, {}).get("name") or current.get(w) or w[:10] for w in hist}
    wrows = []
    for w in sorted(short, key=lambda w: -(stats(lots[w])["lcb"] or -9)):
        s, st, se = stats(lots[w]), stats(train[w]), stats(test[w])
        moved = sum(1 for x in lots[w] if x.get("skipped") == "price_moved")
        wrows.append({"wallet": w, "name": names[w], "chosen_on_first_part": w in chosen,
                      "final_pick": w in final, "currently_copied": w in current,
                      "boards": ";".join(meta.get(w, {}).get("boards", [])),
                      **{f"all_{k}": v for k, v in s.items()},
                      **{f"first_{k}": v for k, v in st.items()},
                      **{f"last_{k}": v for k, v in se.items()},
                      "missed_price_moved": moved})
    with open(os.path.join(a.out_dir, "wallets.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(wrows[0]) if wrows else ["wallet"])
        wr.writeheader()
        wr.writerows(wrows)
    with open(os.path.join(a.out_dir, "copies.csv"), "w", newline="") as f:
        keys = ["wallet", "ts", "slug", "outcome", "league", "kind", "timing", "price_band",
                "leader_price", "price", "qty", "cost", "conviction", "delay_move",
                "leader_usd", "exit", "pnl"]
        wr = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        wr.writeheader()
        for w in final or chosen:
            wr.writerows(x for x in lots[w] if "price" in x)
    picks = []
    for w in final:
        s = stats(lots[w])
        picks.append({"wallet": w, "name": names[w], "copy_return": s["roi"],
                      "copy_t": s["t"], "copies": s["n"], "won": s["won"],
                      "copy_pnl_per_10usd": round(10 * (s["mean"] or 0), 2)})
    with open(os.path.join(a.out_dir, "leaders.json"), "w") as f:
        json.dump({"chosen": time.strftime("%Y-%m-%d", time.gmtime(end_ts)),
                   "rule": (f"Backtest of copytop itself over {a.days} days on markets "
                            f"Polymarket US listed ({a.delay}s copy delay, $10 a signal, US "
                            f"taker fee, never more than 1c over the leader, held to "
                            f"settlement): wallets with "
                            f"{a.min_copies + 5}+ closed copies, copied in the last week, "
                            f"ranked by the lower bound of their per-copy return."),
                   "leaders": picks}, f, indent=1)

    lines = ["# Which wallets to copy on Polymarket US", "",
             f"Backtest of copytop's own rules over {a.days} days to "
             f"{time.strftime('%Y-%m-%d %H:%M', time.gmtime(end_ts))} UTC: {len(wallets)} "
             f"candidates, {len(hist)} with trades copytop could copy, {len(short)} re-priced "
             f"at a {a.delay}s copy delay. Choosing window: first {a.split:.0%}; test window: "
             f"the rest ({(end_ts - split_ts) / 86400:.0f} days).", "",
             "## Does choosing this way hold up?", "",
             f"Wallets ranked on the choosing window only (lower bound of per-copy return, "
             f"{a.min_copies}+ closed copies), then scored on the test window they never saw:", "",
             HEAD, *[_row(k, s) for k, s in v_rows], "",
             "## Copy rules, on the chosen wallets", "",
             "| | test window | | | | | | whole window | | | | | |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
             *[f"| {lab} | {t['n']} | {t['won']} | ${t['staked']:,.0f} | {t['pnl']:+,.2f} | "
               f"{(t['roi'] or 0):+.1%} | {t['t'] if t['t'] is not None else '—'} | {w['n']} | "
               f"{w['won']} | ${w['staked']:,.0f} | {w['pnl']:+,.2f} | {(w['roi'] or 0):+.1%} | "
               f"{w['t'] if w['t'] is not None else '—'} |" for lab, t, w in variants], "",
             "## Patterns, on the chosen wallets (choosing window → test window)", "",
             "| pattern | copies | return | t | → copies | return | t |",
             "|---|---|---|---|---|---|---|"]
    for key in sorted(set(seg_tr) | set(seg_te)):
        a1, b1 = stats(seg_tr.get(key, [])), stats(seg_te.get(key, []))
        if a1["n"] + b1["n"] < 10:
            continue
        f = lambda s: (f"{s['n']} | {(s['roi'] or 0):+.1%} | "
                       f"{s['t'] if s['t'] is not None else '—'}")
        lines.append(f"| {key} | {f(a1)} | {f(b1)} |")
    lines += ["", "## Final picks (whole window, copied in the last week)", "",
              "| wallet | copies | won | return | t | per $10 copy |", "|---|---|---|---|---|---|"]
    for p in picks:
        lines.append(f"| {p['name'][:28]} | {p['copies']} | {p['won']} | "
                     f"{(p['copy_return'] or 0):+.1%} | {p['copy_t']} | "
                     f"{p['copy_pnl_per_10usd']:+.2f} |")
    lines += ["", "## Currently copied wallets", "",
              "| wallet | copies | won | return | t | in final picks |", "|---|---|---|---|---|---|"]
    for w, name in current.items():
        s = stats(lots.get(w, [])) if w in lots else None
        if s:
            lines.append(f"| {name[:28]} | {s['n']} | {s['won']} | {(s['roi'] or 0):+.1%} | "
                         f"{s['t']} | {'yes' if w in final else 'no'} |")
        else:
            lines.append(f"| {name[:28]} | — | — | — | — | no copyable trades |")
    with open(os.path.join(a.out_dir, "report.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
