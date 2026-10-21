"""Turn a wallet's raw data into a strategy profile and an archetype."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from statistics import median

SHORT_CRYPTO = re.compile(r"up or down|\d{1,2}(:\d{2})?\s*[ap]m\s*-\s*\d{1,2}(:\d{2})?\s*[ap]m", re.I)

# Ordered: first match wins. Matched against "eventSlug slug title", lowercased.
CATEGORY_RULES = [
    ("crypto", r"\b(bitcoin|btc|ethereum|eth|solana|sol|xrp|doge|crypto|up or down|"
               r"memecoin|binance|coinbase|megaeth|hyperliquid|pump\.fun|airdrop|fdv)\b"),
    ("politics", r"\b(election|elections|president|presidential|trump|biden|harris|vance|"
                 r"senate|house|congress|governor|mayor|primary|nominee|nomination|"
                 r"democrat|democratic|republican|gop|parliament|prime minister|"
                 r"chancellor|cabinet|impeach|poll|electoral|vote|referendum|party)\b"),
    ("geopolitics", r"\b(war|ceasefire|invade|invasion|israel|iran|gaza|hamas|russia|"
                    r"ukraine|putin|zelensky|china|taiwan|nato|north korea|strike|"
                    r"military|nuclear|sanctions|peace deal)\b"),
    ("economics", r"\b(fed|fomc|interest rate|rates|cpi|inflation|recession|gdp|"
                  r"unemployment|jobs report|tariff|tariffs|treasury|s&p|nasdaq|"
                  r"stock|stocks|ipo|earnings|oil|gold)\b"),
    ("sports", r"\b(nba|nfl|mlb|nhl|ncaa|cfb|cbb|epl|ucl|uel|mls|wnba|ufc|mma|f1|nascar|pga|"
               r"atp|wta|fifa|uefa|premier league|la liga|laliga|serie a|bundesliga|ligue 1|"
               r"champions league|world cup|super bowl|stanley cup|world series|"
               r"grand slam|wimbledon|olympic|boxing|esports|lol|cs2|"
               r"counter-strike|valorant|dota|vs\.?|o/u|spread|win on 20\d\d|"
               r"mvp|cy young|heisman|playoffs|finals|championship)\b"),
    ("tech", r"\b(openai|chatgpt|gpt|ai|apple|google|tesla|spacex|nvidia|microsoft|"
             r"meta|anthropic|grok|xai|iphone|launch)\b"),
    ("culture", r"\b(oscar|oscars|grammy|grammys|emmy|movie|box office|album|song|"
                r"spotify|billboard|tweet|tweets|mrbeast|taylor swift|bond|celebrity|"
                r"netflix|tv|eurovision|time person)\b"),
    ("weather", r"\b(temperature|weather|hurricane|rain|snow|°f|°c|degrees|climate)\b"),
]
_CAT = [(name, re.compile(rx, re.I)) for name, rx in CATEGORY_RULES]


def category(row: dict) -> str:
    text = " ".join(str(row.get(k) or "") for k in ("eventSlug", "slug", "title"))
    text = text.replace("-", " ")
    for name, rx in _CAT:
        if rx.search(text):
            return name
    return "other"


def _f(v, default=0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _day(s) -> int | None:
    try:
        return date.fromisoformat(str(s)[:10]).toordinal()
    except ValueError:
        return None


def _cost_pnl(r: dict, is_open: bool) -> tuple[float, float]:
    """(dollars put in, profit) for one position row."""
    if is_open:
        # Unredeemed losers live here at $0: pnl = unrealized + realized.
        pnl = _f(r.get("cashPnl")) + _f(r.get("realizedPnl"))
        cost = (_f(r.get("avgPrice")) * _f(r.get("totalBought"))
                or _f(r.get("initialValue")))
        return cost, pnl
    return _f(r.get("avgPrice")) * _f(r.get("totalBought")), _f(r.get("realizedPnl"))


def profile(d: dict, lb: dict | None = None, alltime_pnl: float | None = None) -> dict:
    """Strategy profile from collect.wallet_data() output.

    ``alltime_pnl`` (from the all-time leaderboard) is used to check how much
    of the wallet's profit the sampled positions account for.
    """
    lb = lb or {}
    closed = d["closed"]
    opened = d.get("open") or []
    p: dict = {"wallet": d["wallet"], "name": lb.get("userName") or "",
               "lb_pnl": _f(lb.get("pnl")), "lb_volume": _f(lb.get("vol")),
               "closed_positions": len(closed),
               "closed_truncated": d.get("closed_truncated", False),
               "open_positions": len(d.get("open") or [])}

    # -- closed positions: what they bet on, at what price, how it went ----
    costs, pnls = [], []
    cat_cost, cat_pnl = Counter(), Counter()
    price_cost = Counter()
    sides = defaultdict(set)
    for r, is_open in [(r, False) for r in closed] + [(r, True) for r in opened]:
        cost, pnl = _cost_pnl(r, is_open)
        costs.append(cost)
        pnls.append(pnl)
        c = category(r)
        cat_cost[c] += cost
        cat_pnl[c] += pnl
        ap = _f(r.get("avgPrice"))
        bucket = ("<20c" if ap < 0.2 else "20-50c" if ap < 0.5 else "50-80c" if ap < 0.8
                  else "80-95c" if ap < 0.95 else ">=95c")
        price_cost[bucket] += cost
        sides[r.get("conditionId")].add(r.get("outcomeIndex"))
    total_cost, total_pnl = sum(costs), sum(pnls)
    pos_pnl = sorted((x for x in pnls if x > 0), reverse=True)
    coverage = (total_pnl / alltime_pnl) if alltime_pnl else None
    p.update({
        "coverage": round(coverage, 3) if coverage is not None else None,
        "reconciled": coverage is not None and 0.7 <= coverage <= 1.3
                      and not d.get("closed_truncated") and not d.get("open_truncated"),
        "realized_pnl": round(total_pnl, 2),
        "cost": round(total_cost, 2),
        "roi": round(total_pnl / total_cost, 4) if total_cost else 0.0,
        "win_rate": round(sum(1 for x in pnls if x > 0) / len(pnls), 3) if pnls else 0.0,
        "median_position_usd": round(median(costs), 2) if costs else 0.0,
        "top1_share": round(pos_pnl[0] / sum(pos_pnl), 3) if pos_pnl else 0.0,
        "top5_share": round(sum(pos_pnl[:5]) / sum(pos_pnl), 3) if pos_pnl else 0.0,
        "both_sides_share": round(sum(1 for s in sides.values() if len(s) > 1)
                                  / len(sides), 3) if sides else 0.0,
    })
    for b in ("<20c", "20-50c", "50-80c", "80-95c", ">=95c"):
        p[f"price_{b}"] = round(price_cost[b] / total_cost, 3) if total_cost else 0.0
    for name, _ in CATEGORY_RULES + [("other", "")]:
        p[f"cat_{name}"] = round(cat_cost[name] / total_cost, 3) if total_cost else 0.0
        p[f"pnl_{name}"] = round(cat_pnl[name], 2)
    p["main_category"] = cat_cost.most_common(1)[0][0] if cat_cost else ""
    p["best_category"] = max(cat_pnl, key=cat_pnl.get) if cat_pnl else ""

    # -- trades: how often, how big, maker or taker, how late ------------------
    ta, tt = d.get("trades_all") or [], d.get("trades_taker") or []
    ts = [int(_f(t.get("timestamp"))) for t in ta if t.get("timestamp")]
    if ts:
        lo, hi = min(ts), max(ts)
        span_days = max((hi - lo) / 86400, 1.0)  # a short burst isn't a daily rate
        in_win = [t for t in tt if int(_f(t.get("timestamp"))) >= lo]
        n_taker = len(in_win)
        usd = lambda t: _f(t.get("size")) * _f(t.get("price"))
        all_usd, taker_usd = sum(map(usd, ta)), sum(map(usd, in_win))
        txs = {t.get("transactionHash") for t in ta if t.get("transactionHash")}
        sizes = [usd(t) for t in ta]
        end_day = {r.get("conditionId"): _day(r.get("endDate")) for r in closed}
        lead = []
        for t in ta:
            e = end_day.get(t.get("conditionId"))
            if e:
                td = datetime.fromtimestamp(int(_f(t.get("timestamp"))), timezone.utc).date()
                lead.append(e - td.toordinal())
        p.update({
            "trades_sampled": len(ta),
            "trades_per_day": round(len(ta) / span_days, 2),   # fills
            "tx_per_day": round(len(txs) / span_days, 2),      # distinct transactions
            "maker_usd_share": round(max(0.0, 1 - taker_usd / all_usd), 3) if all_usd else None,
            "median_trade_usd": round(median(sizes), 2) if sizes else 0.0,
            "maker_share": round(max(0.0, 1 - n_taker / len(ta)), 3),
            "sell_share": round(sum(1 for t in ta if t.get("side") == "SELL") / len(ta), 3),
            "short_crypto_share": round(sum(1 for t in ta if SHORT_CRYPTO.search(
                str(t.get("title") or ""))) / len(ta), 3),
            "same_day_share": round(sum(1 for x in lead if x <= 0) / len(lead), 3) if lead else None,
            "median_days_before_end": median(lead) if lead else None,
            "last_trade": datetime.fromtimestamp(hi, timezone.utc).strftime("%Y-%m-%d"),
        })
    else:
        p.update({"trades_sampled": 0, "trades_per_day": 0.0, "tx_per_day": 0.0,
                  "maker_usd_share": None, "median_trade_usd": 0.0, "maker_share": None, "sell_share": None, "short_crypto_share": 0.0,
                  "same_day_share": None, "median_days_before_end": None, "last_trade": ""})

    # -- activity: rewards, merges, splits, conversions ------------------------
    acts = d.get("activity") or {}
    rewards = acts.get("REWARD") or []
    p["rewards_usd"] = round(sum(_f(r.get("usdcSize")) for r in rewards), 2)
    p["rewards_truncated"] = bool(acts.get("REWARD_truncated"))
    for t in ("MERGE", "SPLIT", "CONVERSION", "REDEEM"):
        p[f"n_{t.lower()}"] = len(acts.get(t) or [])
    p["archetype"], p["why"] = archetype(p)
    return p


def archetype(p: dict) -> tuple[str, str]:
    mk = p.get("maker_usd_share") if p.get("maker_usd_share") is not None \
        else (p.get("maker_share") or 0.0)
    n = p["closed_positions"] + p.get("open_positions", 0)
    if p.get("trades_sampled", 0) >= 300 and p["short_crypto_share"] >= 0.5:
        return "crypto short-term bot", f"{p['short_crypto_share']:.0%} of trades in 5-15 minute crypto markets"
    # Breadth, not transaction counts, separates operations from whales: a
    # whale's few huge orders fill against hundreds of counterparties.
    if n <= 50 or (p["top5_share"] >= 0.8 and n <= 200):
        return "whale / concentrated bets", (f"{n} positions, top 5 = {p['top5_share']:.0%} of gains, "
                                             f"median position ${p['median_position_usd']:,.0f}")
    if n >= 1000:
        kind = "market making" if mk >= 0.6 else "taker flow"
        main = p["main_category"]
        return f"high-volume {main} operation ({kind})", (
            f"{n}+ positions, {mk:.0%} of $ as maker, median position ${p['median_position_usd']:,.0f}")
    # Directional traders who use limit orders also get maker fills and a few
    # dollars of rewards; a market maker quotes both sides or earns real
    # money from rewards.
    rewards_matter = p["rewards_usd"] >= 0.1 * max(p.get("realized_pnl") or 0, 1)
    if mk >= 0.6 and (p["both_sides_share"] >= 0.3 or rewards_matter):
        return "market maker", (f"{mk:.0%} maker fills, ${p['rewards_usd']:,.0f} rewards, "
                                f"{p['both_sides_share']:.0%} of markets on both sides")
    if (p["n_merge"] + p["n_conversion"]) >= 20 and p["both_sides_share"] >= 0.3:
        return "arbitrage / merger", (f"{p['n_merge']} merges, {p['n_conversion']} conversions, "
                                      f"{p['both_sides_share']:.0%} both sides")
    if p["price_>=95c"] >= 0.5:
        return "bonder (near-certain outcomes)", f"{p['price_>=95c']:.0%} of spend at >=95c"
    if p["cat_sports"] >= 0.6:
        late = p.get("same_day_share")
        style = "same-day/in-play" if late is not None and late >= 0.6 else "pre-game/futures"
        return f"sports bettor ({style})", (f"{p['cat_sports']:.0%} of spend in sports, "
                                            f"{(late or 0):.0%} of trades on settlement day")
    if p["cat_politics"] + p["cat_geopolitics"] + p["cat_economics"] >= 0.6:
        return "politics / macro trader", (f"{p['cat_politics'] + p['cat_geopolitics'] + p['cat_economics']:.0%} "
                                           "of spend in politics, geopolitics, economics")
    return "generalist", f"main category {p['main_category']}"
