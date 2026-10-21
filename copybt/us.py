"""Which international Polymarket markets are also listed on Polymarket US.

Polymarket US (QCX LLC) is a separate CFTC-regulated exchange with its own
market ids, so markets are matched on slug or normalised question text.
"""

from __future__ import annotations

import logging
import re

from .api import Client, HTTPError

log = logging.getLogger(__name__)

US_GATEWAY = "https://gateway.polymarket.us"


def normalize(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _rows(payload) -> list[dict]:
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if isinstance(payload, dict):
        for key in ("markets", "data", "results", "items"):
            if isinstance(payload.get(key), list):
                return [r for r in payload[key] if isinstance(r, dict)]
    return []


_VS = re.compile(r"^(.+?)\s+(?:vs\.?|v\.?|@|at)\s+(.+)$", re.I)
_DATE = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")
_WIN_ON = re.compile(r"^will (.+?) win on (20\d\d-\d\d-\d\d)", re.I)


def game_teams(title: str) -> frozenset[str] | None:
    """{team a, team b} for 'A vs. B' style titles, ignoring ': O/U 2.5' etc."""
    m = _VS.match(title.split(":")[0].strip())
    if not m:
        return None
    a, b = normalize(m.group(1)), normalize(m.group(2))
    return frozenset((a, b)) if a and b and a != b else None


def _day(ts_or_iso) -> int | None:
    if isinstance(ts_or_iso, (int, float)):
        return int(ts_or_iso) // 86400
    m = _DATE.search(str(ts_or_iso or ""))
    if not m:
        return None
    from datetime import date
    return date(int(m[1]), int(m[2]), int(m[3])).toordinal() - date(1970, 1, 1).toordinal()


class USMarkets:
    def __init__(self, slugs: set[str], questions: set[str],
                 games: set[tuple] | None = None, team_days: set[tuple] | None = None):
        self.slugs = slugs
        self.questions = questions
        self.games = games or set()          # (frozenset(teams), day)
        self.team_days = team_days or set()  # (team, day)

    def __len__(self) -> int:
        return len(self.questions | self.slugs) + len(self.games)

    def lists(self, title: str, slug: str = "", ts: int | None = None) -> bool:
        if (slug and slug.lower() in self.slugs) or normalize(title) in self.questions:
            return True
        # US game entries are stored for game day +/- 1, so look up one day.
        m = _WIN_ON.match(title.strip())
        if m:
            return (normalize(m.group(1)), _day(m.group(2))) in self.team_days
        teams = game_teams(title)
        day = _day(slug) or (_day(ts) if ts else None)
        return bool(teams) and day is not None and (teams, day) in self.games


def fetch_us_markets(client: Client, page_size: int = 100,
                     max_pages: int = 2000, sample: list | None = None) -> USMarkets:
    slugs: set[str] = set()
    questions: set[str] = set()
    games: set[tuple] = set()
    team_days: set[tuple] = set()
    for closed in ("false", "true"):
        for page in range(max_pages):
            try:
                rows = _rows(client.get(US_GATEWAY, "/v1/markets", {
                    "closed": closed, "limit": page_size,
                    "offset": page * page_size}))
            except HTTPError as e:
                log.warning("Polymarket US markets (closed=%s, page %d): %s",
                            closed, page, e)
                break
            before = len(slugs) + len(questions) + len(games)
            for r in rows:
                if r.get("slug"):
                    slugs.add(str(r["slug"]).lower())
                q = r.get("question") or r.get("title")
                if q:
                    questions.add(normalize(str(q)))
                desc = str(r.get("description") or "")
                if desc.lower().startswith("will "):
                    # Futures carry the international-style question here.
                    first = desc.split("?")[0]
                    questions.add(normalize(re.sub(r",.*$", "", first)))
                day = _day(r.get("gameStartTime") or r.get("endDate"))
                teams = game_teams(str(q or ""))
                if teams and day is not None:
                    for d in (day - 1, day, day + 1):
                        games.add((teams, d))
                        for t in teams:
                            team_days.add((t, d))
                if sample is not None and len(sample) < 400:
                    sample.append({k: r.get(k) for k in (
                        "question", "title", "slug", "marketType", "category",
                        "gameStartTime", "endDate", "closed")} |
                        {"description": desc[:120]})
            # Stop on an empty page, or if paging isn't moving (offset ignored).
            if len(rows) < page_size or len(slugs) + len(questions) + len(games) == before:
                break
    log.info("Polymarket US: %d slugs, %d questions, %d game-days", len(slugs),
             len(questions), len(games))
    return USMarkets(slugs, questions, games, team_days)
