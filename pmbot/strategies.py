"""Strategy plugins.

A strategy names the US markets it wants watched (``watch``) and returns the
orders it wants in them (``orders``). The engine fetches quotes, enforces the
shared risk limits, and gives each market to one strategy at a time: the
first strategy to want orders in a market owns it until its position and
orders there are gone, so strategies never trade against each other.
"""

from __future__ import annotations

from dataclasses import replace

from .data import LONG_RUNNING
from .strategy import MarketView, Order, StrategyConfig, decide


class Strategy:
    name = "base"

    def watch(self, eng, now: float) -> set[str]:
        """Extra US market slugs to poll this cycle."""
        return set()

    def orders(self, eng, views: dict[str, MarketView], now: float) -> dict[str, list[Order]]:
        return {}


class FairValue(Strategy):
    """Quote around the international midpoint; take only clear mispricings."""

    name = "fairvalue"

    def __init__(self, cfg: StrategyConfig):
        self.cfg = cfg

    def orders(self, eng, views, now):
        return {slug: decide(v, eng.held(slug), eng.room(slug), self.cfg)
                for slug, v in views.items() if v.fair is not None}


class SportsGameDay(FairValue):
    """Modelled on the high-volume sports wallets in the top-wallet study.

    The ones active now trade game markets (not futures), mostly on game
    day, mostly at 20-80c, with about half their volume as resting orders
    around a sharp price. This quotes the same way, around the
    international Polymarket price, but stops before kick-off: in-play
    trading needs faster data than a polling bot has.
    """

    name = "sportsgameday"

    def __init__(self, cfg: StrategyConfig, window_hours: float = 24.0):
        super().__init__(replace(cfg, min_price=max(cfg.min_price, 0.15),
                                 max_price=min(cfg.max_price, 0.85)))
        self.window_s = window_hours * 3600

    def orders(self, eng, views, now):
        game_day = {}
        for slug, v in views.items():
            m = eng.markets.get(slug)
            if m is None or m.market_type in LONG_RUNNING or not m.game_start:
                continue
            if not (0 < m.game_start - now <= self.window_s):
                continue
            game_day[slug] = v
        return super().orders(eng, game_day, now)


REGISTRY = {"fairvalue": FairValue, "sportsgameday": SportsGameDay}


def build(names: str, cfg: StrategyConfig, leaders_file: str = "", **copy_opts) -> list[Strategy]:
    out = []
    out_dir = copy_opts.pop("out_dir", ".")
    for n in [x.strip() for x in names.split(",") if x.strip()]:
        if n == "reenter":
            from .reenter import ReEnter
            out.append(ReEnter(out_dir))
            continue
        if n == "evsniper":
            import os
            from .ev import EVSniper
            out.append(EVSniper(cfg, os.environ.get("ODDS_API_KEY", ""),
                                **{k[3:]: v for k, v in copy_opts.items() if k.startswith("ev_")}))
            continue
        if n == "copytop":
            from .copy import CopyTop, load_leaders
            out.append(CopyTop(cfg, load_leaders(leaders_file),
                               **{k: v for k, v in copy_opts.items() if not k.startswith("ev_")}))
            continue
        if n not in REGISTRY:
            raise SystemExit(f"unknown strategy {n!r}; choose from "
                             f"{', '.join([*REGISTRY, 'copytop'])}")
        out.append(REGISTRY[n](cfg))
    return out
