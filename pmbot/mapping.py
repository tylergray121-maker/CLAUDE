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

from .data import LONG_RUNNING, IntlOption, USMarket, _json_list

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


# Words that change what is being bet on. Both sides of a pair must carry the
# same set: "NBA Eastern Conference Champion" is not "win the NBA Finals",
# and "Champions League Final Qualifiers" is not "win the Champions League".
# (Plain winning - champion, winner, finals, title - carries no tag.)
_CONCEPTS = {
    "conference": "conf", "eastern": "east", "east": "east", "western": "west",
    "west": "west", "division": "div", "divisional": "div",
    "qualifiers": "qualify", "qualify": "qualify", "qualifies": "qualify",
    "qualification": "qualify", "reach": "qualify", "advance": "qualify",
    "semifinal": "round", "semifinals": "round", "quarterfinal": "round",
    "quarterfinals": "round", "playoffs": "playoff", "playoff": "playoff",
    "mvp": "mvp", "rookie": "rookie", "coach": "coach", "defensive": "defensive",
    "nominee": "nominate", "nominees": "nominate", "nomination": "nominate",
    "nominated": "nominate", "last": "last", "bottom": "last",
    "relegated": "relegate", "relegation": "relegate", "promoted": "promote",
    "promotion": "promote", "top": "top", "popular": "popular",
    "primary": "primary", "runner": "runnerup", "second": "second",
}


def concepts(text: str, drop: set[str] = frozenset()) -> frozenset[str]:
    """Bet-type tags in ``text``, ignoring the outcome's own name ("West Ham")."""
    return frozenset(_CONCEPTS[w] for w in words(text) if w in _CONCEPTS and w not in drop)


def prices_agree(a: float, b: float, max_gap: float = 0.08) -> bool:
    """Absolute and, for cheap contracts, relative agreement: 4c vs 0.2c is
    within 8c but plainly not the same bet."""
    if abs(a - b) > max_gap:
        return False
    lo, hi = min(a, b), max(a, b)
    return not (lo < 0.25 and hi - lo > 0.02 and hi > 2 * max(lo, 0.001))


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


GAME_TYPES = ("moneyline", "drawable_outcome")
_US_PREFIX = re.compile(r"^[a-z]{2,8}-(?=[a-z0-9]+-)")
# Outcome names that say nothing about which event they belong to.
GENERIC = {"yes", "no", "other", "none", "draw", "tie", "over", "under", "up", "down",
           "change", "increase", "decrease", "cut", "hike", "hold", "pause", "bps"}


def intl_slug(us_slug: str) -> str:
    """aec-nba-mil-was-2026-10-21 -> nba-mil-was-2026-10-21"""
    return _US_PREFIX.sub("", us_slug, count=1)


def match_games(us: list[USMarket], intl_rows: dict[str, dict]) -> list[Pair]:
    """Exact game pairs: the US slug is the international slug plus a venue
    prefix, and the US market's long side names the outcome it prices."""
    pairs = []
    for m in us:
        if m.market_type not in GAME_TYPES:
            continue
        r = intl_rows.get(intl_slug(m.slug))
        if not r:
            continue
        outcomes = [str(o) for o in _json_list(r.get("outcomes"))]
        tokens = [str(t) for t in _json_list(r.get("clobTokenIds"))]
        if len(outcomes) != len(tokens) or not m.long_label:
            continue
        want = m.long_label.strip().lower()
        idx = next((i for i, o in enumerate(outcomes) if o.strip().lower() == want), None)
        if idx is None:
            continue
        pairs.append(Pair(m.slug, tokens[idx], 1.0, f"{m.question[:80]}: {m.long_label}",
                          f"{r.get('question')} [{outcomes[idx]}]", m.tick))
    return pairs


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
            names = name_words | set(words(o.label))
            if concepts(us_ctx_text, names) != concepts(intl_text, names):
                continue  # different kind of bet on the same team
            cs = jaccard(us_ctx, content(intl_text, name_words | set(words(o.label))))
            # "No change" or "Yes" says nothing about the event, so the event
            # wording must carry the match (ECB vs Bank of Russia).
            generic = set(words(o.label)) <= GENERIC
            if cs < (0.6 if generic else min_context):
                continue
            # Teams meet several times a season, so a game must end within a
            # day of its counterpart; futures and elections get more slack.
            gap_days = max_end_gap_days if m.market_type in LONG_RUNNING else 1.5
            if m.end and o.end and abs(m.end - o.end) > gap_days * 86400:
                continue
            if m.market_type not in LONG_RUNNING and not (m.end and o.end):
                continue  # a game without dates can't be matched safely
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
