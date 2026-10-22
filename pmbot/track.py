"""Scorecard: how each copied wallet, and each kind of bet, has done for us.

Every copy is a lot credited to the wallet it copied and to the patterns it
belongs to (league, market type, price band, pre-game or in-play). Sells
and settlements close lots oldest first. Something is only judged to be
losing when that is clearly not bad luck: enough settled copies, money
lost, and a t-statistic of the per-copy returns at or below -2. Single
sports bets are noisy (a 50c bet returns +100% or -100%), so a handful of
losses alone never cuts anything off.
"""

from __future__ import annotations

import math
from collections import Counter


def summarize(results: list[list[float]]) -> dict:
    """``results`` holds [pnl, cost] for each closed lot."""
    staked = sum(c for _, c in results)
    pnl = sum(p for p, _ in results)
    rs = [p / c for p, c in results if c > 0]
    t = None
    if len(rs) >= 2:
        mean = sum(rs) / len(rs)
        var = sum((r - mean) ** 2 for r in rs) / (len(rs) - 1)
        t = mean / math.sqrt(var / len(rs)) if var > 0 else math.copysign(99.0, mean) if mean else 0.0
    return {"settled": len(results), "won": sum(1 for p, _ in results if p > 0),
            "staked": round(staked, 2), "pnl": round(pnl, 2),
            "roi": round(pnl / staked, 4) if staked else None,
            "t": round(t, 2) if t is not None else None}


def clearly_losing(s: dict, min_n: int, max_roi: float = 0.0) -> bool:
    return (s["settled"] >= min_n and s["pnl"] < 0 and s["roi"] is not None
            and s["roi"] <= max_roi and s["t"] is not None and s["t"] <= -2.0)


class Scorecard:
    def __init__(self, keep: int = 300):
        self.keep = keep                              # results kept per key
        self.lots: dict[str, list[dict]] = {}         # slug -> open lots, oldest first
        self.results: dict[str, list[list[float]]] = {}
        self.copies: Counter = Counter()              # key -> copies opened
        self.closed: list[list] = []                   # [keys, pnl, cost] per closed lot

    def open(self, slug: str, keys: list[str], qty: int, cost: float) -> None:
        self.lots.setdefault(slug, []).append({"keys": list(keys), "qty": qty, "cost": cost})
        for k in keys:
            self.copies[k] += 1

    def close(self, slug: str, qty: int, proceeds: float, key: str | None = None) -> None:
        """``qty`` contracts of ``slug`` sold or settled for ``proceeds`` in total,
        out of the lots carrying ``key`` (any lot if None), oldest first."""
        lots = self.lots.get(slug, [])
        per = proceeds / qty if qty else 0.0
        left = qty
        while left > 0:
            lot = next((l for l in lots if key is None or key in l["keys"]), None)
            if lot is None:
                break
            take = min(left, lot["qty"])
            cost = lot["cost"] * take / lot["qty"]
            for k in lot["keys"]:
                r = self.results.setdefault(k, [])
                r.append([round(per * take - cost, 4), round(cost, 4)])
                del r[:-self.keep]
            self.closed.append([list(lot["keys"]), round(per * take - cost, 4), round(cost, 4)])
            del self.closed[:-5 * self.keep]
            lot["qty"] -= take
            lot["cost"] -= cost
            left -= take
            if lot["qty"] <= 0:
                lots.remove(lot)
        if not lots:
            self.lots.pop(slug, None)

    def summary_without(self, key: str, excluded: set[str]) -> dict:
        """Like ``summary`` over the closed lots with ``key`` that carry none of
        the ``excluded`` keys: a pattern judged on its own, not on bets that a
        worse pattern (e.g. a losing league) already explains."""
        return summarize([[p, c] for keys, p, c in self.closed
                          if key in keys and not excluded.intersection(keys)])

    def summary(self, key: str) -> dict:
        return {**summarize(self.results.get(key, [])), "copies": self.copies[key],
                "open_usd": round(sum(l["cost"] for ls in self.lots.values() for l in ls
                                      if key in l["keys"]), 2)}

    def qty_for(self, slug: str, key: str) -> int:
        return sum(l["qty"] for l in self.lots.get(slug, []) if key in l["keys"])

    def keys_for(self, slug: str) -> list[str]:
        return [k for l in self.lots.get(slug, []) for k in l["keys"]]

    def to_state(self) -> dict:
        return {"lots": self.lots, "results": self.results, "copies": dict(self.copies),
                "closed": self.closed}

    def load(self, d: dict) -> None:
        self.lots = d.get("lots", {})
        self.results = d.get("results", {})
        self.copies = Counter(d.get("copies", {}))
        self.closed = d.get("closed", [])
