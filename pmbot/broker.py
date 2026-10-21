"""Brokers: a conservative paper simulator and the live Polymarket US one."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass, field

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
    tag: str = ""


@dataclass
class Fill:
    ts: float
    slug: str
    side: str
    price: float
    qty: int
    maker: bool
    fee: float     # positive = paid, negative = rebate
    tag: str = ""  # strategy
    pnl: float = 0.0  # realized on this fill (sells and settlements)


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

    def flipped(self) -> "Quote":
        """The same book seen from the short side: its bid is 1 - the long ask."""
        inv = lambda x: round(1.0 - x, 6) if x is not None else None
        return Quote(inv(self.ask), inv(self.bid), self.ask_qty, self.bid_qty,
                     inv(self.last_px), self.traded, self.ts)


# A US game market prices one outcome, its long side ("Bucks", or "Yes" in
# soccer). The other outcome ("Wizards", "No") is the market's short side; the
# bot trades it as its own instrument, the market slug plus this suffix, with
# prices quoted for the short side itself.
SHORT = ":short"


def split_side(slug: str) -> tuple[str, bool]:
    """'aec-nba-mil-was-2026-10-21:short' -> ('aec-nba-mil-was-2026-10-21', True)"""
    return (slug[:-len(SHORT)], True) if slug.endswith(SHORT) else (slug, False)


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
        self.realized = 0.0
        self._next_id = 1
        self._last: dict[str, Quote] = {}

    # -- persistence (paper accounts survive restarts) ----------------------
    def to_state(self, keep_fills: int = 2000) -> dict:
        return {"cash": self.cash, "fees_paid": self.fees_paid, "rebates": self.rebates,
                "realized": self.realized, "next_id": self._next_id,
                "positions": {k: asdict(v) for k, v in self.positions.items()},
                "fills": [asdict(f) for f in self.fills[-keep_fills:]]}

    @classmethod
    def from_state(cls, d: dict) -> "PaperBroker":
        b = cls(float(d["cash"]))
        b.fees_paid, b.rebates = float(d.get("fees_paid", 0)), float(d.get("rebates", 0))
        b.realized = float(d.get("realized", 0))
        b._next_id = int(d.get("next_id", 1))
        b.positions = {k: Position(**v) for k, v in d.get("positions", {}).items()}
        b.fills = [Fill(**f) for f in d.get("fills", [])]
        return b

    # -- broker interface -------------------------------------------------
    def sync(self) -> None:
        pass

    checker: "PreviewChecker | None" = None

    def place(self, slug: str, order: Order, quote: Quote | None = None) -> str | None:
        if self.checker is not None:
            ok, why = self.checker.check(slug, order)
            if not ok:
                log.info("exchange preview rejected %s %s %d @ %.3f: %s", order.side, slug,
                         order.qty, order.price, why)
                return None
        if order.post_only:
            oid = f"paper-{self._next_id}"
            self._next_id += 1
            self.open_orders[oid] = OpenOrder(oid, slug, order.side, order.price,
                                              order.qty, True, tag=order.tag)
            return oid
        q = quote or self._last.get(slug)
        if q is None:
            return None
        if order.side == "BUY" and q.ask is not None and q.ask <= order.price:
            self._fill(slug, "BUY", q.ask, min(order.qty, int(q.ask_qty)), False, order.tag)
        elif order.side == "SELL" and q.bid is not None and q.bid >= order.price:
            self._fill(slug, "SELL", q.bid, min(order.qty, int(q.bid_qty)), False, order.tag)
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
                self._fill(slug, o.side, o.price, o.qty, True, o.tag)

    def settle(self, slug: str, value: float, tag: str = "") -> None:
        """Market resolved: each contract pays ``value`` (1 or 0)."""
        p = self.positions.pop(slug, None)
        for oid in [k for k, o in self.open_orders.items() if o.slug == slug]:
            del self.open_orders[oid]
        if p and p.qty:
            self.cash += p.qty * value
            pnl = p.qty * value - p.cost
            self.realized += pnl
            self.fills.append(Fill(time.time(), slug, "SETTLE", value, p.qty, False, 0.0,
                                   tag, round(pnl, 4)))

    def _fill(self, slug, side, price, qty, maker, tag=""):
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
            pnl = price * qty - fee - avg * qty
            self.realized += pnl
            p.qty -= qty
            p.cost -= avg * qty
            if p.qty == 0:
                self.positions.pop(slug, None)
        if fee > 0:
            self.fees_paid += fee
        else:
            self.rebates -= fee
        self.fills.append(Fill(time.time(), slug, side, price, qty, maker, fee, tag,
                               round(pnl, 4) if side == "SELL" else 0.0))
        log.info("paper %s %s %d @ %.3f (%s, fee %+.2f)", side, slug, qty, price,
                 "maker" if maker else "taker", fee)

    def equity(self, marks: dict[str, float]) -> float:
        return self.cash + sum(p.qty * marks.get(s, p.cost / p.qty if p.qty else 0)
                               for s, p in self.positions.items())


class LiveBroker:
    """Places real orders through the official ``polymarket-us`` SDK.

    Every order is a limit order: post-only GTC for quotes, IOC for takes,
    flagged as automatic. Positions, cash and open orders are re-read from
    the exchange on every ``sync()``. Takes execute synchronously and their
    executions are recorded as fills, like the paper broker's, so strategies
    can score them. A position that disappears without the bot selling it
    is listed in ``vanished`` until the engine records its settlement.
    """

    def __init__(self, key_id: str, secret_key: str, state_file: str = "live_orders.json",
                 client=None):
        if client is None:
            try:
                from polymarket_us import PolymarketUS
            except ImportError as e:  # pragma: no cover
                raise SystemExit("live trading needs: pip install polymarket-us") from e
            client = PolymarketUS(key_id=key_id, secret_key=secret_key)
        self.client = client
        self.cash = 0.0
        self.positions: dict[str, Position] = {}
        self.open_orders: dict[str, OpenOrder] = {}
        self.fills: list[Fill] = []
        self.fees_paid = self.rebates = self.realized = 0.0
        self.vanished: dict[str, Position] = {}
        self._held: dict[str, Position] | None = None  # positions as of the last sync
        self._logged_balance = False
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
        bal = [b for b in self.client.account.balances().get("balances", [])
               if b.get("currency", "USD") == "USD"]
        self.cash = sum(spendable(b) for b in bal)
        if not self._logged_balance:
            self._logged_balance = True
            for b in bal:  # amounts only, once, to check what the account reports
                log.info("balance fields: %s", {k: v for k, v in b.items()
                                                if isinstance(v, (int, float))})
        self.positions = {}
        cursor = None
        while True:
            params = {"limit": 100, **({"cursor": cursor} if cursor else {})}
            resp = self.client.portfolio.positions(params)
            for slug, p in (resp.get("positions") or {}).items():
                qty = int(float(p.get("netPosition") or 0))
                if qty > 0:
                    self.positions[slug] = Position(qty, _amount(p.get("cost")))
                elif qty < 0:
                    self.positions[slug + SHORT] = Position(-qty, abs(_amount(p.get("cost"))))
            cursor = resp.get("nextCursor")
            if resp.get("eof", True) or not cursor:
                break
        if self._held is not None:
            for slug, p in self._held.items():
                if slug not in self.positions:
                    self.vanished[slug] = p
        self._remember()
        self.open_orders = {}
        live_ids = set()
        for o in self.client.orders.list().get("orders", []):
            live_ids.add(o.get("id"))
            if o.get("id") not in self.mine:
                continue
            intent = str(o.get("intent") or "")
            short = intent.endswith("_SHORT")
            side = ("BUY" if intent.startswith("ORDER_INTENT_BUY") else "SELL") if intent \
                else ("BUY" if o.get("side") == "ORDER_SIDE_BUY" else "SELL")
            px = _amount(o.get("price"))
            self.open_orders[o["id"]] = OpenOrder(
                o["id"], o.get("marketSlug", "") + (SHORT if short else ""), side,
                round(1 - px, 6) if short else px,
                int(o.get("leavesQuantity") or o.get("quantity") or 0), True)
        if self.mine - live_ids:  # filled or cancelled since last sync
            self.mine &= live_ids
            self._save()

    def _remember(self) -> None:
        self._held = {k: Position(v.qty, v.cost) for k, v in self.positions.items()}

    def to_state(self, keep_fills: int = 2000) -> dict:
        return {"fills": [asdict(f) for f in self.fills[-keep_fills:]],
                "fees_paid": self.fees_paid, "realized": self.realized,
                "held": {k: asdict(v) for k, v in (self._held or {}).items()},
                "vanished": {k: asdict(v) for k, v in self.vanished.items()}}

    def load_state(self, d: dict) -> None:
        self.fills = [Fill(**f) for f in d.get("fills", [])]
        self.fees_paid = float(d.get("fees_paid", 0))
        self.realized = float(d.get("realized", 0))
        self._held = {k: Position(**v) for k, v in d.get("held", {}).items()}
        self.vanished = {k: Position(**v) for k, v in d.get("vanished", {}).items()}

    def place(self, slug: str, order: Order, quote: Quote | None = None) -> str | None:
        params = order_params(slug, order)
        if not order.post_only:
            params["synchronousExecution"] = True  # executions come back in the response
        resp = self.client.orders.create(params) or {}
        log.info("live %s %s %d @ %.3f -> %s", order.side, slug, order.qty,
                 order.price, resp.get("id"))
        if not order.post_only:
            self._record(slug, order, resp.get("executions") or [])
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
            self.client.orders.cancel(oid, {"marketSlug": split_side(o.slug)[0]})

    def cancel_all(self) -> None:
        """Cancel this bot's orders only (never the account's manual ones)."""
        for oid, o in list(self.open_orders.items()):
            try:
                self.client.orders.cancel(oid, {"marketSlug": split_side(o.slug)[0]})
            except Exception as e:  # keep cancelling the rest
                log.error("cancel %s failed: %s", oid, e)
        self.open_orders.clear()

    def observe(self, slug: str, q: Quote) -> None:
        pass

    def _record(self, slug: str, order: Order, executions: list) -> None:
        """Book an IOC take's executions as one fill at their average price."""
        short = split_side(slug)[1]
        qty = notional = fee = 0.0
        for x in executions:
            try:
                q = float(x.get("lastShares") or 0)
            except (TypeError, ValueError):
                q = 0.0
            if q <= 0:
                continue
            px = _amount(x.get("lastPx"))
            if short:
                # Prices are quoted for the long side; read it whichever way
                # respects our limit, in case the exchange reports the short's.
                flipped = 1.0 - px
                ok = flipped <= order.price + 1e-6 if order.side == "BUY" \
                    else flipped >= order.price - 1e-6
                px = flipped if ok else px
            qty += q
            notional += q * px
            fee += _amount(x.get("commissionNotionalCollected"))
        n = int(round(qty))
        if n <= 0:
            return
        avg = notional / qty
        p = self.positions.setdefault(slug, Position())
        pnl = 0.0
        if order.side == "BUY":
            p.qty += n
            p.cost += avg * n + fee
        else:
            sold = min(n, p.qty)
            basis = p.cost / p.qty * sold if p.qty else 0.0
            pnl = avg * n - fee - basis
            p.qty -= sold
            p.cost -= basis
            self.realized += pnl
        if p.qty <= 0:
            self.positions.pop(slug, None)
        self._remember()  # the bot's own sale is not a vanished position
        self.fees_paid += fee
        self.fills.append(Fill(time.time(), slug, order.side, round(avg, 4), n, False,
                               round(fee, 4), order.tag, round(pnl, 4)))

    def settle(self, slug: str, value: float, tag: str = "") -> None:
        """Record the payout of a position the exchange settled (``vanished``)."""
        p = self.vanished.pop(slug, None)
        if p and p.qty:
            pnl = p.qty * value - p.cost
            self.realized += pnl
            self.fills.append(Fill(time.time(), slug, "SETTLE", value, p.qty, False, 0.0,
                                   tag, round(pnl, 4)))

    def equity(self, marks: dict[str, float]) -> float:
        return self.cash + sum(p.qty * marks.get(s, p.cost / p.qty if p.qty else 0)
                               for s, p in self.positions.items())


def order_params(slug: str, order: Order) -> dict:
    """The exact Polymarket US order the bot sends (live) or previews (paper):
    a limit order, post-only GTC for quotes, IOC for takes, flagged automatic.

    Short-side orders use the SHORT intents, and their price is sent as the
    long side's price (Polymarket US always quotes the long side): buying
    "Wizards" at 0.63 is BUY_SHORT at 0.37."""
    base, short = split_side(slug)
    side = "BUY" if order.side == "BUY" else "SELL"
    return {
        "marketSlug": base,
        "intent": f"ORDER_INTENT_{side}_{'SHORT' if short else 'LONG'}",
        "type": "ORDER_TYPE_LIMIT",
        "price": {"value": f"{(1 - order.price) if short else order.price:.3f}",
                  "currency": "USD"},
        "quantity": int(order.qty),
        "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL" if order.post_only
               else "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL",
        "participateDontInitiate": bool(order.post_only),
        "manualOrderIndicator": "MANUAL_ORDER_INDICATOR_AUTOMATIC",
    }


class PreviewChecker:
    """Checks paper orders with Polymarket US's order preview endpoint.

    Preview validates an order exactly as the exchange would and prices its
    fee, without placing it, so a paper order the exchange would reject is
    rejected on paper too. Needs the account's API keys; never trades.
    Capped per minute so it stays well inside API rate limits; orders over
    the cap go through unchecked and are counted as such.
    """

    def __init__(self, key_id: str, secret_key: str, per_minute: int = 20, client=None):
        if client is None:
            try:
                from polymarket_us import PolymarketUS
            except ImportError as e:  # pragma: no cover
                raise SystemExit("order previews need: pip install polymarket-us") from e
            client = PolymarketUS(key_id=key_id, secret_key=secret_key)
        self.client = client
        self.per_minute = per_minute
        self._times: list[float] = []
        self.stats = {"accepted": 0, "rejected": 0, "unchecked": 0, "errors": 0}
        self.last_reject = ""

    def verify_keys(self) -> None:
        """Fails fast if the keys don't authenticate (reads balances, shows nothing)."""
        self.client.account.balances()

    def check(self, slug: str, order: Order) -> tuple[bool, str]:
        now = time.monotonic()
        self._times = [t for t in self._times if now - t < 60]
        if len(self._times) >= self.per_minute:
            self.stats["unchecked"] += 1
            return True, "unchecked"
        self._times.append(now)
        try:
            resp = self.client.orders.preview({"request": order_params(slug, order)})
        except Exception as e:
            status = getattr(e, "status_code", None) or getattr(getattr(e, "response", None),
                                                               "status_code", None)
            if status and 400 <= int(status) < 500 and int(status) not in (401, 403, 429):
                self.stats["rejected"] += 1
                self.last_reject = str(e)[:200]
                return False, self.last_reject
            self.stats["errors"] += 1  # auth, rate limit or outage: don't block paper trading
            return True, f"preview unavailable: {str(e)[:120]}"
        state = str(((resp or {}).get("order") or {}).get("state") or "")
        if state == "ORDER_STATE_REJECTED":
            self.stats["rejected"] += 1
            self.last_reject = state
            return False, state
        self.stats["accepted"] += 1
        return True, "accepted"


def spendable(b: dict) -> float:
    """Real cash in a balance row: the account's own money, not promotional
    bonus credit (``currentBalance`` includes it; the app's balance doesn't).
    Open bids are not subtracted here; the risk manager does that itself."""
    if b.get("displayedCash") is not None:
        return _amount(b.get("displayedCash"))
    bonus = sum(_amount(b.get(k)) for k in ("displayedBonus", "bonusHold", "bonusReservation"))
    return max(0.0, _amount(b.get("currentBalance")) - bonus)


def _amount(a) -> float:
    if isinstance(a, dict):
        a = a.get("value")
    try:
        return float(a)
    except (TypeError, ValueError):
        return 0.0
