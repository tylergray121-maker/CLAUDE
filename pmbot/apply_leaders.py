"""Apply a leader-selection result to the wallets copytop follows.

    python -m pmbot.apply_leaders selectresults/leaders.json [--min 10]

The new list is the selection's picks plus every wallet the owner added by
hand ("owner's pick" in its source), which are always kept. If the selection
found fewer than --min wallets, the current list is left as it is, so a
thin or failed run can never leave the bot with nothing to copy. Nor is
the "every qualified wallet" fallback applied (copying everyone lost money
out of sample), nor a list whose ranking method did not make money in the
walk-forward test with a t-statistic of at least 2.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.join(os.path.dirname(__file__), "leaders.json")
MIN_T = 2.0   # walk-forward t-statistic the selection's method must reach


def merge(current: dict, picked: dict, min_picks: int = 10) -> dict | None:
    picks = [x for x in picked.get("leaders", []) if x.get("wallet")]
    if len(picks) < min_picks or str(picked.get("method", "")).startswith("every qualified"):
        return None
    if (picked.get("method_t") or 0) < MIN_T or (picked.get("method_return") or 0) <= 0:
        return None   # the ranking method did not clearly make money out of sample
    owner = [x for x in current.get("leaders", []) if "owner" in str(x.get("source", ""))]
    seen, leaders = set(), []
    for x in owner + [{**p, "source": f"selection {picked.get('chosen', '')}: "
                                      f"{picked.get('method') or 'lower bound of copy return'}"}
                      for p in picks]:
        w = x["wallet"].lower()
        if w not in seen:
            seen.add(w)
            leaders.append(x)
    return {"chosen": picked.get("chosen"), "rule": picked.get("rule", ""),
            "method": picked.get("method"), "leaders": leaders}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="pmbot.apply_leaders")
    p.add_argument("selection")
    p.add_argument("--min", type=int, default=10)
    p.add_argument("--out", default=HERE)
    a = p.parse_args(argv)
    with open(a.selection) as f:
        picked = json.load(f)
    with open(a.out) as f:
        current = json.load(f)
    new = merge(current, picked, a.min)
    if new is None:
        print(f"selection has fewer than {a.min} wallets or no method held up out of sample; "
              f"keeping the current "
              f"{len(current.get('leaders', []))}")
        return 1
    with open(a.out, "w") as f:
        json.dump(new, f, indent=1)
    old = {x["wallet"].lower() for x in current.get("leaders", [])}
    now = {x["wallet"].lower() for x in new["leaders"]}
    print(f"{len(now)} wallets ({len(now - old)} new, {len(old - now)} dropped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
