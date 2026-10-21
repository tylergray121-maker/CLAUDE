"""Brokers: a conservative paper simulator and the live Polymarket US one."""

from __future__ import annotations

import itertools
import json
import logging
import time
from dataclasses import dataclass, field

from .fees import maker_rebate, taker_fee
from .strategy import Order

log = logging.getLogger(__name__)


@dataclass
class Position:
    qty: int = 0
    cost: float = 0.0   # dollars paid incl. fees, net of rebates and sale proceeds


@dataclass
class OpenOrder:
    id: str
    slug: str
    side: str
    price: float
    qty: int
    post_only: bool
    placed: float = field(default_factory=time.time)


@dataclass
class Fill:
    ts: float
    slug: str
    side: str
    price: float
    qty: int
    maker: bool
    fee: float     # positive = paid, negative = rebate


@dataclass
class Quote:
    """What the US book looked like at one poll."""
    bid: float | None
    ask: float | None
    bid_qty: float
    ask_qty: float
    last_px: float | None
    traded: float          # cumulative shares traded (for detecting prints)
    ts: float


class PaperBroker:
    """Simulates fills against real Polymarket US quotes, conservatively.

    A resting order fills only when the market trades *through* its price:
    a best ask strictly below our bid (or a print below it), and the mirror
    for asks. Merely touching our price is not a fill, because queue
    position is unknown. Takes fill at the displayed price, up to the
    displayed size, and pay the taker fee.
    """

    def __init__(self, cash: float):
        self.cash = cash
        self.positions: dict[str, Position] = {}
        self.open_orders: dict[str, OpenOrder] = {}
        self.fills: list[Fill] = []
        self.fees_paid = 0.0
        self.rebates = 0.0
        self._ids = itertools.count(1)
        self._last: dict[str, Quote] = {}

    # -- broker interface -------------------------------------------------
    def sync(self) -> None:
        pass

    def place(self, slug: str, order: Order, quote: Quote | None = None) -> str | None:
        if order.post_only:
            oid = f"paper-{next(self._ids)}"
            self.open_orders[oid] = OpenOrder(oid, slug, order.side, order.price,
                                              order.qty, True)
            return oid
        q = quote or self._last.get(slug)
        if q is None:
            return None
        if order.side == "BUY" and q.ask is not None and q.ask <= order.price:
            self._fill(slug, "BUY", q.ask, min(order.qty, int(q.ask_qty)), maker=False)
        elif order.side == "SELL" and q.bid is not None and q.bid >= order.price:
            self._fill(slug, "SELL", q.bid, min(order.qty, int(q.bid_qty)), maker=False)
        return None

    def cancel(self, oid: str) -> None:
        self.open_orders.pop(oid, None)

    def cancel_all(self) -> None:
        self.open_orders.clear()

    # -- simulation -------------------------------------------------------
    def observe(self, slug: str, q: Quote) -> None:
        prev = self._last.get(slug)
        self._last[slug] = q
        printed = prev is not None and q.traded > prev.traded and q.last_px is not None
        for oid, o in list(self.open_orders.items()):
            if o.slug != slug or o.placed >= q.ts:
                continue
            if o.side == "BUY":
                hit = ((q.ask is not None and q.ask < o.price - 1e-9)
                       or (printed and q.last_px < o.price - 1e-9))
            else:
                held = self.positions.get(slug, Position()).qty
                o.qty = min(o.qty, held)
                hit = o.qty > 0 and ((q.bid is not None and q.bid > o.price + 1e-9)
                                     or (printed and q.last_px > o.price + 1e-9))
            if hit:
                del self.open_orders[oid]
                self._fill(slug, o.side, o.price, o.qty, maker=True)

    def settle(self, slug: str, value: float) -> None:
        """Market resolved: each contract pays ``value`` (1 or 0)."""
        p = self.positions.pop(slug, None)
        for oid in [k for k, o in self.open_orders.items() if o.slug == slug]:
            del self.open_orders[oid]
        if p and p.qty:
            self.cash += p.qty * value
            self.fills.append(Fill(time.time(), slug, "SETTLE", value, p.qty, False, 0.0))

    def _fill(self, slug, side, price, qty, maker):
        if qty <= 0:
            return
        fee = -maker_rebate(price, qty) if maker else taker_fee(price, qty)
        p = self.positions.setdefault(slug, Position())
        if side == "BUY":
            qty = min(qty, int((self.cash - max(fee, 0)) // price))
            if qty <= 0:
                return
            self.cash -= price * qty + fee
            p.qty += qty
            p.cost += price * qty + fee
        else:
            qty = min(qty, p.qty)
            if qty <= 0:
                return
            avg = p.cost / p.qty
            self.cash += price * qty - fee
            p.qty -= qty
            p.cost -= avg * qty
            if p.qty == 0:
                self.positions.pop(slug, None)
        if fee > 0:
            self.fees_paid += fee
        else:
            self.rebates -= fee
        self.fills.append(Fill(time.time(), slug, side, price, qty, maker, fee))
        log.info("paper %s %s %d @ %.3f (%s, fee %+.2f)", side, slug, qty, price,
                 "maker" if maker else "taker", fee)

    def equity(self, marks: dict[str, float]) -> float:
        return self.cash + sum(p.qty * marks.get(s, p.cost / p.qty if p.qty else 0)
                               for s, p in self.positions.items())


class LiveBroker:
    """Places real orders through the official ``polymarket-us`` SDK.

    Every order is a limit order: post-only GTC for quotes, IOC for takes,
    flagged as automatic. Positions, cash and open orders are re-read from
    the exchange on every ``sync()``.
    """

    def __init__(self, key_id: str, secret_key: str, state_file: str = "live_orders.json"):
        try:
            from polymarket_us import PolymarketUS
        except ImportError as e:  # pragma: no cover
            raise SystemExit("live trading needs: pip install polymarket-us") from e
        self.client = PolymarketUS(key_id=key_id, secret_key=secret_key)
        self.cash = 0.0
        self.positions: dict[str, Position] = {}
        self.open_orders: dict[str, OpenOrder] = {}
        self.fills: list[Fill] = []
        self.fees_paid = self.rebates = 0.0
        # Only orders this bot created are ever managed or cancelled; manual
        # orders on the account are left alone. Persisted across restarts.
        self.state_file = state_file
        try:
            with open(state_file) as f:
                self.mine: set[str] = set(json.load(f))
        except (OSError, ValueError):
            self.mine = set()

    def _save(self) -> None:
        with open(self.state_file, "w") as f:
            json.dump(sorted(self.mine), f)

    def sync(self) -> None:
        bal = self.client.account.balances().get("balances", [])
        # currentBalance, not buyingPower: the risk manager subtracts open bids
        # itself, and buyingPower already has them taken out.
        self.cash = sum(_amount(b.get("currentBalance")) for b in bal
                        if b.get("currency", "USD") == "USD")
        self.positions = {}
        cursor = None
        while True:
            params = {"limit": 100, **({"cursor": cursor} if cursor else {})}
            resp = self.client.portfolio.positions(params)
            for slug, p in (resp.get("positions") or {}).items():
                qty = int(float(p.get("netPosition") or 0))
                if qty > 0:
                    self.positions[slug] = Position(qty, _amount(p.get("cost")))
            cursor = resp.get("nextCursor")
            if resp.get("eof", True) or not cursor:
                break
        self.open_orders = {}
        live_ids = set()
        for o in self.client.orders.list().get("orders", []):
            live_ids.add(o.get("id"))
            if o.get("id") not in self.mine:
                continue
            side = "BUY" if o.get("side") == "ORDER_SIDE_BUY" else "SELL"
            self.open_orders[o["id"]] = OpenOrder(
                o["id"], o.get("marketSlug", ""), side, _amount(o.get("price")),
                int(o.get("leavesQuantity") or o.get("quantity") or 0), True)
        if self.mine - live_ids:  # filled or cancelled since last sync
            self.mine &= live_ids
            self._save()

    def place(self, slug: str, order: Order, quote: Quote | None = None) -> str | None:
        params = {
            "marketSlug": slug,
            "intent": "ORDER_INTENT_BUY_LONG" if order.side == "BUY"
                      else "ORDER_INTENT_SELL_LONG",
            "type": "ORDER_TYPE_LIMIT",
            "price": {"value": f"{order.price:.3f}", "currency": "USD"},
            "quantity": int(order.qty),
            "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL" if order.post_only
                   else "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL",
            "participateDontInitiate": bool(order.post_only),
            "manualOrderIndicator": "MANUAL_ORDER_INDICATOR_AUTOMATIC",
        }
        resp = self.client.orders.create(params)
        log.info("live %s %s %d @ %.3f -> %s", order.side, slug, order.qty,
                 order.price, resp.get("id"))
        oid = resp.get("id")
        if order.post_only and oid:
            self.mine.add(oid)
            self._save()
            self.open_orders[oid] = OpenOrder(oid, slug, order.side, order.price,
                                              order.qty, True)
        return oid if order.post_only else None

    def cancel(self, oid: str) -> None:
        o = self.open_orders.pop(oid, None)
        if o:
            self.client.orders.cancel(oid, {"marketSlug": o.slug})

    def cancel_all(self) -> None:
        """Cancel this bot's orders only (never the account's manual ones)."""
        for oid, o in list(self.open_orders.items()):
            try:
                self.client.orders.cancel(oid, {"marketSlug": o.slug})
            except Exception as e:  # keep cancelling the rest
                log.error("cancel %s failed: %s", oid, e)
        self.open_orders.clear()

    def observe(self, slug: str, q: Quote) -> None:
        pass

    def settle(self, slug: str, value: float) -> None:
        pass  # the exchange settles; sync() picks it up

    def equity(self, marks: dict[str, float]) -> float:
        return self.cash + sum(p.qty * marks.get(s, p.cost / p.qty if p.qty else 0)
                               for s, p in self.positions.items())


def _amount(a) -> float:
    if isinstance(a, dict):
        a = a.get("value")
    try:
        return float(a)
    except (TypeError, ValueError):
        return 0.0
