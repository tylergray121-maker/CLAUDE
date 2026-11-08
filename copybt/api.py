"""Small cached HTTP client for Polymarket's public APIs (stdlib only)."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import random
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

DATA_API = "https://data-api.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"
LB_API = "https://lb-api.polymarket.com"

USER_AGENT = "copybt/0.1 (+polymarket copy-trade backtester)"


class HTTPError(Exception):
    def __init__(self, status: int, url: str, body: str = ""):
        super().__init__(f"HTTP {status} for {url}: {body[:200]}")
        self.status = status
        self.url = url


def _touch(path: str) -> None:
    """Mark a cache file as used by this run. The search workflow deletes the
    files a successful run did not touch, so the cache holds only the working
    set instead of growing every day past GitHub's 10 GB cache limit."""
    try:
        os.utime(path)
    except OSError:
        pass


def _prune(data, keep: tuple[str, ...]):
    if isinstance(data, list):
        return [{k: r[k] for k in keep if k in r} if isinstance(r, dict) else r
                for r in data]
    if isinstance(data, dict):
        if any(isinstance(v, list) and v and isinstance(v[0], dict)
               for v in data.values()) and not any(k in data for k in keep):
            return {k: _prune(v, keep) if isinstance(v, list) else v
                    for k, v in data.items()}
        return {k: data[k] for k in keep if k in data}
    return data


# Polymarket retired Data API v1 on 2026-11-02 (every v1 path answers HTTP 410).
# v2 lives under /v2, wraps rows as {"data": ..., "pagination": {...}}, names
# fields in snake_case, pages by cursor only (an `offset` is a 400), filters a
# market with `condition` instead of `market`, and sorts the leaderboard with
# `sort_by` (PNL or VOLUME). The client translates v1-style calls, so callers
# keep v1 paths, params and field names. v2 answers are cached by CloudFront
# for up to 5 minutes per URL, so a call that skips our cache (the copier's
# polls) adds a unique `_` param to get fresh rows.
_V2_PATHS = {"/trades": "/v2/trades", "/activity": "/v2/activity",
             "/positions": "/v2/positions", "/v1/leaderboard": "/v2/leaderboard"}
_V1_NAMES = {"token_id": "asset", "user_id": "proxyWallet", "volume": "vol",
             "current_size": "size", "current_price": "curPrice"}


def _v1_key(k: str) -> str:
    if k in _V1_NAMES:
        return _V1_NAMES[k]
    head, *rest = k.split("_")
    return head + "".join(p[:1].upper() + p[1:] for p in rest)


def _v1_row(row):
    if not isinstance(row, dict):
        return row
    out = {_v1_key(k): v for k, v in row.items()}
    if "rank" not in out and ("rankPnl" in out or "rankVolume" in out):
        out["rank"] = out.get("rankPnl") or out.get("rankVolume")
    return out


def _v2_params(path: str, params: dict) -> tuple[dict, int]:
    """v1-style params -> (v2 params without paging, v1 offset)."""
    p = dict(params)
    offset = int(p.pop("offset", 0) or 0)
    if "market" in p:
        p["condition"] = p.pop("market")
    if "orderBy" in p:
        order = str(p.pop("orderBy")).upper()
        p["sort_by"] = "VOLUME" if order in ("VOL", "VOLUME") else order
    return p, offset


class Client:
    """GET-only JSON client with a disk cache, retries and a global rate limit."""

    def __init__(self, cache_dir: str | None = ".cache", max_rps: float = 8.0,
                 retries: int = 5, timeout: float = 30.0):
        self.cache_dir = cache_dir
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
        self.min_interval = 1.0 / max_rps if max_rps > 0 else 0.0
        self.retries = retries
        self.timeout = timeout
        self._lock = threading.Lock()
        self._next_slot = 0.0
        self.requests_made = 0
        # v2 cursors by (path, params) -> {row offset: next cursor or None at the end}
        self._cursors: dict[tuple, dict[int, str | None]] = {}
        self._cursor_lock = threading.Lock()

    def _cache_path(self, url: str) -> str | None:
        if not self.cache_dir:
            return None
        h = hashlib.sha1(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, h[:2], h + ".json")

    def _throttle(self) -> None:
        if not self.min_interval:
            return
        with self._lock:
            now = time.monotonic()
            wait = self._next_slot - now
            self._next_slot = max(now, self._next_slot) + self.min_interval
        if wait > 0:
            time.sleep(wait)

    # Compact per-key storage for derived data (e.g. a wallet's parsed trades).
    def load_blob(self, key: str):
        if not self.cache_dir:
            return None
        path = self._cache_path("blob:" + key)[:-5] + ".json.gz"
        if not os.path.exists(path):
            return None
        _touch(path)
        with gzip.open(path, "rt") as f:
            return json.load(f)

    def save_blob(self, key: str, data) -> None:
        if not self.cache_dir:
            return
        path = self._cache_path("blob:" + key)[:-5] + ".json.gz"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.{threading.get_ident()}.tmp"
        with gzip.open(tmp, "wt") as f:
            json.dump(data, f, separators=(",", ":"))
        os.replace(tmp, path)

    def get(self, base: str, path: str, params: dict | list | None = None,
            use_cache: bool = True, keep: tuple[str, ...] | None = None):
        """GET JSON. ``keep`` prunes records to those keys before caching."""
        query = urllib.parse.urlencode(params or {}, doseq=True)
        url = f"{base}{path}" + (f"?{query}" if query else "")
        cpath = self._cache_path(url) if use_cache else None
        if cpath and os.path.exists(cpath):
            _touch(cpath)
            with open(cpath) as f:
                data = json.load(f)
            if isinstance(data, dict) and "__http_error__" in data:
                raise HTTPError(data["__http_error__"], url, "(cached)")
            return data

        if base == DATA_API and path in _V2_PATHS and not isinstance(params, list):
            data = self._get_v2(path, params or {}, fresh=not use_cache)
        else:
            data = self._fetch(url, cpath)
        if keep:
            data = _prune(data, keep)
        if cpath:
            self._write(cpath, data)
        return data

    def _get_v2(self, path: str, params: dict, fresh: bool = False) -> list:
        """One v1-style page from Data API v2: rows with v1 field names. A v1
        offset is reached by following v2 cursors, remembered per query so
        sequential pages cost one request each."""
        v2path = DATA_API + _V2_PATHS[path]
        p, offset = _v2_params(path, params)
        key = (v2path, tuple(sorted((k, str(v)) for k, v in p.items())))
        with self._cursor_lock:
            known = self._cursors.get(key, {0: ""})
            at = max(o for o in known if o <= offset) if offset else 0
            cursor = known.get(at, "")
        while True:
            if cursor is None:  # past the last page
                return []
            q = {**p, "cursor": cursor} if cursor else dict(p)
            if fresh:  # past CloudFront's 5-minute cache
                q["_"] = f"{time.time_ns():x}"
            body = self._fetch(f"{v2path}?{urllib.parse.urlencode(q, doseq=True)}", None)
            data = body.get("data") if isinstance(body, dict) else body
            rows = [data] if isinstance(data, dict) else list(data or [])
            pag = (body.get("pagination") if isinstance(body, dict) else None) or {}
            nxt = pag.get("next_cursor") if pag.get("has_more") and rows else None
            end = at + len(rows)
            with self._cursor_lock:
                if len(self._cursors) > 2000 and key not in self._cursors:
                    self._cursors.pop(next(iter(self._cursors)))
                self._cursors.setdefault(key, {0: ""})[end] = nxt
            if at >= offset:  # the page asked for
                break
            if end > offset:  # the offset falls inside this page
                rows = rows[offset - at:]
                break
            if not rows:
                return []
            at, cursor = end, nxt
        return [_v1_row(r) for r in rows]

    def _fetch(self, url: str, cpath: str | None):
        last_err: Exception | None = None
        for attempt in range(self.retries):
            self._throttle()
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT, "Accept": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    self.requests_made += 1
                    data = json.loads(resp.read().decode())
                break
            except urllib.error.HTTPError as e:
                body = e.read().decode(errors="replace") if e.fp else ""
                last_err = HTTPError(e.code, url, body)
                # 4xx other than 429 won't get better by retrying.
                if e.code != 429 and 400 <= e.code < 500:
                    if e.code == 404 and cpath:
                        self._write(cpath, {"__http_error__": 404})
                    raise last_err
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError,
                    ConnectionError) as e:
                last_err = e
            time.sleep(min(30.0, (2 ** attempt) + random.random()))
        else:
            raise last_err  # type: ignore[misc]
        return data

    @staticmethod
    def _write(cpath: str, data) -> None:
        os.makedirs(os.path.dirname(cpath), exist_ok=True)
        tmp = f"{cpath}.{threading.get_ident()}.tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, separators=(",", ":"))
        os.replace(tmp, cpath)
