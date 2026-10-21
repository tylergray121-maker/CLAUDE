"""Pair each Polymarket US market with the same outcome on the international
exchange, whose price is used as fair value.

US futures look like question "World Series Champion", title "Milwaukee
Brewers", description "Will Milwaukee Brewers win the 2026 MLB World
Series...". The international side is "Will the Milwaukee Brewers win the
2026 World Series?" with group title "Milwaukee Brewers". A pair needs the
outcome name to match, the event wording to overlap, compatible end dates,
and (checked later, with live prices) the two prices to be close.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass

from .data import IntlOption, USMarket

STOP = set("""a an and the of to in on at for by will be is are win wins winner
winning who which what vs v or with from as this that 2026 2027 2028 de la""".split())
_WORD = re.compile(r"[a-z0-9]+")


def words(text: str) -> list[str]:
    return _WORD.findall(text.lower().replace("&", " and "))


def content(text: str, drop: set[str] = frozenset()) -> set[str]:
    return {w for w in words(text) if w not in STOP and w not in drop and len(w) > 1}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def years(text: str) -> set[str]:
    return set(re.findall(r"\b20\d\d\b", text))


@dataclass
class Pair:
    us_slug: str
    intl_token: str
    score: float
    us_label: str
    intl_label: str
    tick: float = 0.01

    def to_json(self) -> dict:
        return asdict(self)


def name_similarity(a: str, b: str) -> float:
    wa, wb = set(words(a)), set(words(b))
    if not wa or not wb:
        return 0.0
    if wa == wb:
        return 1.0
    # "Los Angeles Rams" vs "Rams", "Kyle Larson" vs "Larson": containment
    small, big = (wa, wb) if len(wa) <= len(wb) else (wb, wa)
    if small <= big and (len(small) >= 2 or len(next(iter(small))) >= 5):
        return 0.8
    return jaccard(wa, wb)


def match(us: list[USMarket], intl: list[IntlOption], min_name: float = 0.8,
          min_context: float = 0.2, max_end_gap_days: float = 75) -> list[Pair]:
    by_word: dict[str, list[IntlOption]] = defaultdict(list)
    for o in intl:
        for w in set(words(o.label)) - STOP:
            by_word[w].append(o)
    pairs = []
    for m in us:
        if not m.title:
            continue
        cands = {id(o): o for w in set(words(m.title)) - STOP for o in by_word.get(w, [])}
        us_ctx_text = f"{m.question} {m.description.split('?')[0]}"
        name_words = set(words(m.title))
        us_ctx = content(us_ctx_text, name_words)
        us_years = years(us_ctx_text)
        best, best_score = None, 0.0
        for o in cands.values():
            ns = name_similarity(m.title, o.label)
            if ns < min_name:
                continue
            intl_text = f"{o.question} {o.event}"
            if us_years and years(intl_text) and not (us_years & years(intl_text)):
                continue  # different season
            cs = jaccard(us_ctx, content(intl_text, name_words | set(words(o.label))))
            if cs < min_context:
                continue
            if m.end and o.end and abs(m.end - o.end) > max_end_gap_days * 86400:
                continue
            score = 0.5 * ns + 0.5 * cs
            if score > best_score:
                best, best_score = o, score
        if best:
            pairs.append(Pair(m.slug, best.token, round(best_score, 3),
                              f"{m.question}: {m.title}",
                              f"{best.question} [{best.label}]", m.tick))
    return pairs


def save(pairs: list[Pair], path: str) -> None:
    with open(path, "w") as f:
        json.dump([p.to_json() for p in pairs], f, indent=1)


def load(path: str) -> list[Pair]:
    with open(path) as f:
        return [Pair(**p) for p in json.load(f)]
