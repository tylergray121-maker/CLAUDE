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


class USMarkets:
    def __init__(self, slugs: set[str], questions: set[str]):
        self.slugs = slugs
        self.questions = questions

    def __len__(self) -> int:
        return len(self.questions | self.slugs)

    def lists(self, title: str, slug: str = "") -> bool:
        return (bool(slug) and slug.lower() in self.slugs) or \
            normalize(title) in self.questions


def fetch_us_markets(client: Client, page_size: int = 100,
                     max_pages: int = 2000) -> USMarkets:
    slugs: set[str] = set()
    questions: set[str] = set()
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
            before = len(slugs) + len(questions)
            for r in rows:
                if r.get("slug"):
                    slugs.add(str(r["slug"]).lower())
                q = r.get("question") or r.get("title")
                if q:
                    questions.add(normalize(str(q)))
            # Stop on an empty page, or if paging isn't moving (offset ignored).
            if len(rows) < page_size or len(slugs) + len(questions) == before:
                break
    log.info("Polymarket US: %d slugs, %d questions", len(slugs), len(questions))
    return USMarkets(slugs, questions)
