"""How many of the leaders' recent trades copytop could copy on Polymarket US.

    python -m pmbot.coverage [--leaders-file pmbot/leaders.json] [--trades 200]

Maps each leader's latest trades the way the live strategy does and counts
them by age, league and outcome (long side, short side, listed but the
outcome names differ, not on Polymarket US). Older trades are often on games
that already settled and left the US list, so the recent buckets are the
honest coverage number. For unlisted games it shows what US lists for the
same matchup, to spot naming differences.
"""

from __future__ import annotations

import argparse
import os
import re
import tempfile
import time
from collections import Counter, defaultdict

from copybt.api import DATA_API, HTTPError

from .broker import SHORT
from .copy import league, load_leaders
from .engine import Engine, EngineConfig
from .risk import RiskConfig, RiskManager
from .strategy import StrategyConfig

_MATCHUP = re.compile(r"^([a-z0-9]+-[a-z0-9]+-[a-z0-9]+-\d{4}-\d{2}-\d{2})")
AGES = ((3, "<3h"), (12, "3-12h"), (48, "12-48h"), (float("inf"), "older"))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="pmbot.coverage", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--leaders-file", default=os.path.join(os.path.dirname(__file__),
                                                          "leaders.json"))
    p.add_argument("--trades", type=int, default=200, help="latest trades per leader")
    a = p.parse_args(argv)
    d = tempfile.mkdtemp()
    e = Engine(EngineConfig(mode="scan", out_dir=d, minutes=0), StrategyConfig(),
               RiskManager(RiskConfig(kill_file=os.path.join(d, "STOP"))), strategies=[])
    e.refresh_pairs()
    index = e.token_index()
    by_matchup = defaultdict(list)
    for s in e.by_intl_slug:
        m = _MATCHUP.match(s)
        if m:
            by_matchup[m.group(1)].append(s)
    now = time.time()
    table: dict[str, Counter] = defaultdict(Counter)
    leagues: dict[str, Counter] = defaultdict(Counter)
    missed = Counter()
    for wallet, name in load_leaders(a.leaders_file).items():
        try:
            trades = e.client.get(DATA_API, "/trades", {"user": wallet, "limit": a.trades,
                                                        "takerOnly": "false"},
                                  use_cache=False) or []
        except HTTPError as err:
            print(f"{name}: {err}")
            continue
        for t in trades:
            if not isinstance(t, dict) or not t.get("timestamp"):
                continue
            hours = (now - int(t["timestamp"])) / 3600
            age = next(label for limit, label in AGES if hours < limit)
            slug = e.us_for_trade(t, index)
            isl = str(t.get("slug") or "")
            if slug:
                k = "short side" if slug.endswith(SHORT) else "long side"
            elif e.lists(isl):
                k = "listed, outcome names differ"
            else:
                k = "not on Polymarket US"
                if age in ("<3h", "3-12h"):
                    mu = _MATCHUP.match(isl)
                    seen = by_matchup.get(mu.group(1), []) if mu else []
                    missed[(isl, t.get("outcome"), ", ".join(sorted(seen)[:4]))] += 1
            table[age][k] += 1
            leagues[league(isl)]["copyable" if slug else "not"] += 1
    print(f"US: {len(e.markets)} open markets, {len(e.by_intl_slug)} game/spread/total/prop "
          f"slugs, {len(e.all_pairs)} verified pairs\n")
    kinds = ("long side", "short side", "listed, outcome names differ", "not on Polymarket US")
    print(f"{'age':8}" + "".join(f"{k[:22]:>24}" for k in kinds) + f"{'copyable':>10}")
    for _, age in AGES:
        c = table.get(age, Counter())
        n = sum(c.values())
        ok = c["long side"] + c["short side"]
        print(f"{age:8}" + "".join(f"{c[k]:>24}" for k in kinds)
              + f"{(f'{100 * ok / n:.0f}%' if n else '-'):>10}")
    print("\nby league (all ages): copyable / total")
    for lg, c in sorted(leagues.items(), key=lambda kv: -sum(kv[1].values()))[:20]:
        print(f"  {lg:12} {c['copyable']:>5} / {sum(c.values())}")
    print("\nrecent trades not on Polymarket US (international slug | outcome | US lists for "
          "the same matchup):")
    for (isl, outcome, seen), n in missed.most_common(25):
        print(f"  {n:>3}  {isl} | {outcome} | {seen or '-'}")
    e._events.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
