"""Strategy plugins.

A strategy names the US markets it wants watched (``watch``) and returns the
orders it wants in them (``orders``). The engine fetches quotes, enforces the
shared risk limits, and gives each market to one strategy at a time: the
first strategy to want orders in a market owns it until its position and
orders there are gone, so strategies never trade against each other.
"""

from __future__ import annotations

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


REGISTRY = {"fairvalue": FairValue}
