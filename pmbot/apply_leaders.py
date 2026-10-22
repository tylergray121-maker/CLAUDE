"""Apply a leader-selection result to the wallets copytop follows.

    python -m pmbot.apply_leaders selectresults/leaders.json [--min 10]

The new list is the selection's picks plus every wallet the owner added by
hand ("owner's pick" in its source), which are always kept. If the selection
found fewer than --min wallets, the current list is left as it is, so a
thin or failed run can never leave the bot with nothing to copy. Nor is
the "every qualified wallet" fallback applied: it is what the search uses
when no ranking held up out of sample, and copying everyone lost money there.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.join(os.path.dirname(__file__), "leaders.json")


def merge(current: dict, picked: dict, min_picks: int = 10) -> dict | None:
    picks = [x for x in picked.get("leaders", []) if x.get("wallet")]
    if len(picks) < min_picks or str(picked.get("method", "")).startswith("every qualified"):
        return None
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
