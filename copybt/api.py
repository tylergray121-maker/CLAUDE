"""Small cached HTTP client for Polymarket's public APIs (stdlib only)."""

from __future__ import annotations

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

    def get(self, base: str, path: str, params: dict | list | None = None,
            use_cache: bool = True):
        query = urllib.parse.urlencode(params or {}, doseq=True)
        url = f"{base}{path}" + (f"?{query}" if query else "")
        cpath = self._cache_path(url) if use_cache else None
        if cpath and os.path.exists(cpath):
            with open(cpath) as f:
                data = json.load(f)
            if isinstance(data, dict) and "__http_error__" in data:
                raise HTTPError(data["__http_error__"], url, "(cached)")
            return data

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

        if cpath:
            self._write(cpath, data)
        return data

    @staticmethod
    def _write(cpath: str, data) -> None:
        os.makedirs(os.path.dirname(cpath), exist_ok=True)
        tmp = f"{cpath}.{threading.get_ident()}.tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)
        os.replace(tmp, cpath)
