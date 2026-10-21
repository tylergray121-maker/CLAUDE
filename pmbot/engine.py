"""Main loop: refresh pairs, poll both venues, quote, enforce risk, log."""

from __future__ import annotations

import json
import logging
import os
import signal
import time
from dataclasses import asdict, dataclass, field

from copybt.api import Client

from . import data, mapping
from .broker import PaperBroker, Quote
from .fees import taker_fee_per_contract
from .risk import RiskManager
from .strategy import MarketView, Order, StrategyConfig, decide

log = logging.getLogger(__name__)


@dataclass
class EngineConfig:
    mode: str = "paper"              # scan | paper | live
    out_dir: str = "botresults"
    minutes: float = 60.0            # stop after this long (0 = run until stopped)
    cycle_seconds: float = 15.0
    max_markets: int = 60
    max_price_gap: float = 0.08      # reject pairs whose prices disagree by more
    remap_minutes: float = 60.0
    pairs_file: str = ""             # use a reviewed mapping instead of auto-matching
    workers: int = 8
    max_rps: float = 10.0


@dataclass
class ScanStats:
    """How often the US price is through fair value by more than fees."""
    observations: int = 0
    gaps: list = field(default_factory=list)          # us_mid - fair
    buy_opps: int = 0       # fair - ask - fee >= edge (we could buy)
    sell_opps: int = 0      # bid - fee - fair >= edge (only usable when holding)
    opp_log: list = field(default_factory=list)


class Engine:
    def __init__(self, ecfg: EngineConfig, scfg: StrategyConfig, risk: RiskManager,
                 broker=None):
        self.ecfg, self.scfg, self.risk = ecfg, scfg, risk
        self.broker = broker or PaperBroker(risk.cfg.bankroll)
        self.client = Client(cache_dir=None, max_rps=ecfg.max_rps, retries=2, timeout=15)
        self.pairs: list[mapping.Pair] = []
        self.markets: dict[str, data.USMarket] = {}
        self.stats = ScanStats()
        self.marks: dict[str, float] = {}
        self.verified: set[str] = set()   # pairs whose live prices agree
        self._stop = False
        os.makedirs(ecfg.out_dir, exist_ok=True)
        self._events = open(os.path.join(ecfg.out_dir, "events.jsonl"), "a")

    # -- setup --------------------------------------------------------------
    def refresh_pairs(self) -> None:
        us = data.us_markets(self.client)
        self.markets = {m.slug: m for m in us}
        if self.ecfg.pairs_file:
            pairs = [p for p in mapping.load(self.ecfg.pairs_file) if p.us_slug in self.markets]
        else:
            intl = data.intl_options(self.client)
            pairs = mapping.match(us, intl)
            intl_by_token = {o.token: o for o in intl}
            kept, rejected = [], []
            for p in pairs:
                m, o = self.markets[p.us_slug], intl_by_token[p.intl_token]
                if None in (m.bid, m.ask, o.bid, o.ask):
                    kept.append((p, o.volume24h))  # checked against live books later
                    continue
                gap = abs((m.bid + m.ask) / 2 - (o.bid + o.ask) / 2)
                if gap <= self.ecfg.max_price_gap:
                    kept.append((p, o.volume24h))
                else:
                    rejected.append({**p.to_json(), "price_gap": round(gap, 3)})
            kept.sort(key=lambda x: -x[1])  # most active reference markets first
            pairs = [p for p, _ in kept]
            mapping.save(pairs, os.path.join(self.ecfg.out_dir, "pairs.json"))
            with open(os.path.join(self.ecfg.out_dir, "pairs_rejected.json"), "w") as f:
                json.dump(rejected, f, indent=1)
            log.info("pairs: %d kept, %d rejected on price", len(pairs), len(rejected))
        self.pairs = pairs[:self.ecfg.max_markets]

    # -- loop ---------------------------------------------------------------
    def run(self) -> None:
        signal.signal(signal.SIGINT, self._signal)
        signal.signal(signal.SIGTERM, self._signal)
        end = time.time() + self.ecfg.minutes * 60 if self.ecfg.minutes else float("inf")
        next_remap = 0.0
        try:
            while not self._stop and time.time() < end:
                t0 = time.time()
                if t0 >= next_remap:
                    self.refresh_pairs()
                    next_remap = t0 + self.ecfg.remap_minutes * 60
                self.cycle()
                if self.risk.halted:
                    log.error("HALTED: %s", self.risk.halted)
                    break
                time.sleep(max(0.0, self.ecfg.cycle_seconds - (time.time() - t0)))
        finally:
            self.shutdown()

    def _signal(self, *_):
        self._stop = True

    def cycle(self) -> None:
        self.broker.sync()
        pairs = self.pairs
        us_q = data.fetch_parallel(lambda p: data.us_quote(self.client, p.us_slug),
                                   pairs, self.ecfg.workers)
        ref = data.fetch_parallel(lambda p: data.intl_book(self.client, p.intl_token),
                                  pairs, self.ecfg.workers)
        now = time.time()
        for p, uq, (rb, ra, rs) in zip(pairs, us_q, ref):
            if uq is None:
                continue
            q, state = uq
            m = self.markets.get(p.us_slug)
            ok, why = m.tradable(now) if m else (False, "unknown")
            if state and state != "MARKET_STATE_OPEN":
                ok, why = False, state.lower()
            fair = (rb + ra) / 2 if rb is not None and ra is not None else None
            if q.bid is not None and q.ask is not None:
                self.marks[p.us_slug] = (q.bid + q.ask) / 2
            if p.us_slug not in self.verified and fair is not None and \
                    q.bid is not None and q.ask is not None:
                gap = abs((q.bid + q.ask) / 2 - fair)
                if gap > self.ecfg.max_price_gap:
                    self._log("pair_rejected", slug=p.us_slug, token=p.intl_token,
                              gap=round(gap, 3), us=p.us_label, intl=p.intl_label)
                    self.pairs = [x for x in self.pairs if x is not p]
                    continue
                self.verified.add(p.us_slug)
            if p.us_slug not in self.verified:
                ok, why = False, "unverified pair"
            v = MarketView(p.us_slug, p.tick, q.bid, q.ask, q.bid_qty, q.ask_qty,
                           fair, rs, ok, why)
            self.broker.observe(p.us_slug, q)
            self._scan(v)
            if self.ecfg.mode != "scan":
                self._trade(v, q)
        self._settle_closed(now)
        eq = self.broker.equity(self.marks)
        if self.ecfg.mode != "scan" and self.risk.check(eq):
            self.broker.cancel_all()
        self._summary(eq)

    def _scan(self, v: MarketView) -> None:
        if v.fair is None or v.fair_spread is None or v.fair_spread > self.scfg.max_fair_spread:
            return
        s = self.stats
        s.observations += 1
        if v.us_bid is not None and v.us_ask is not None:
            s.gaps.append(round((v.us_bid + v.us_ask) / 2 - v.fair, 4))
        if v.us_ask is not None:
            e = v.fair - v.us_ask - taker_fee_per_contract(v.us_ask)
            if e >= self.scfg.taker_edge:
                s.buy_opps += 1
                self._log("opportunity", slug=v.slug, side="BUY", edge=round(e, 4),
                          us_ask=v.us_ask, ask_qty=v.us_ask_qty, fair=v.fair,
                          fair_spread=v.fair_spread, tradable=v.tradable, note=v.note)
        if v.us_bid is not None:
            e = v.us_bid - taker_fee_per_contract(v.us_bid) - v.fair
            if e >= self.scfg.taker_edge:
                s.sell_opps += 1
                self._log("opportunity", slug=v.slug, side="SELL", edge=round(e, 4),
                          us_bid=v.us_bid, bid_qty=v.us_bid_qty, fair=v.fair,
                          fair_spread=v.fair_spread, tradable=v.tradable, note=v.note)

    def _trade(self, v: MarketView, q: Quote) -> None:
        b = self.broker
        held = b.positions.get(v.slug).qty if v.slug in b.positions else 0
        room = self.risk.room(v.slug, b.positions, b.open_orders, b.cash)
        want = decide(v, held, room, self.scfg) if not self.risk.halted else []
        mine = [o for o in b.open_orders.values() if o.slug == v.slug]
        # Keep resting orders that still match a desired quote; cancel the rest.
        for o in mine:
            match = next((w for w in want if w.post_only and w.side == o.side
                          and abs(w.price - o.price) < self.scfg.requote_move
                          and w.qty == o.qty), None)
            if match:
                want.remove(match)
            else:
                b.cancel(o.id)
                self._log("cancel", slug=v.slug, side=o.side, price=o.price, qty=o.qty)
        for w in want:
            if w.side == "BUY" and w.price * w.qty > self.risk.room(
                    v.slug, b.positions, b.open_orders, b.cash) + 1e-9:
                continue
            if not self.risk.allow_order():
                self._log("throttled", slug=v.slug)
                break
            oid = b.place(v.slug, w, q)
            self._log("order", slug=v.slug, side=w.side, price=w.price, qty=w.qty,
                      post_only=w.post_only, fair=v.fair, id=oid)

    def _settle_closed(self, now: float) -> None:
        if not isinstance(self.broker, PaperBroker):
            return
        for slug in list(self.broker.positions):
            m = self.markets.get(slug)
            if m and m.tradable(now)[0]:
                continue
            value = data.us_settlement(self.client, slug)
            if value is not None and m is not None and (m.end or 0) <= now:
                self.broker.settle(slug, value)
                self._log("settle", slug=slug, value=value)

    # -- output ---------------------------------------------------------------
    def _log(self, kind: str, **kw) -> None:
        self._events.write(json.dumps({"ts": round(time.time(), 3), "kind": kind, **kw}) + "\n")
        self._events.flush()

    def _summary(self, equity: float) -> None:
        b, s = self.broker, self.stats
        summary = {
            "ts": time.time(), "mode": self.ecfg.mode, "pairs": len(self.pairs),
            "equity": round(equity, 2), "cash": round(b.cash, 2),
            "positions": {k: asdict(v) for k, v in b.positions.items()},
            "open_orders": len(b.open_orders), "fills": len(b.fills),
            "fees_paid": round(b.fees_paid, 2), "rebates": round(b.rebates, 2),
            "halted": self.risk.halted,
            "scan": {"observations": s.observations, "buy_opps": s.buy_opps,
                     "sell_opps": s.sell_opps},
        }
        with open(os.path.join(self.ecfg.out_dir, "summary.json"), "w") as f:
            json.dump(summary, f, indent=1)

    def shutdown(self) -> None:
        try:
            if self.ecfg.mode != "scan":
                self.broker.cancel_all()
                self._log("cancel_all", reason="shutdown")
        finally:
            self._summary(self.broker.equity(self.marks))
            self._write_report()
            self._events.close()

    def _write_report(self) -> None:
        from statistics import median
        s, b = self.stats, self.broker
        gaps = sorted(abs(g) for g in s.gaps)
        pct = lambda q: gaps[min(len(gaps) - 1, int(q * len(gaps)))] if gaps else 0
        lines = [
            f"# Polymarket US bot — {self.ecfg.mode} run", "",
            f"Pairs tracked: {len(self.pairs)}; observations with a trustworthy "
            f"reference price: {s.observations}.", "",
            "## Is there an edge to take?", "",
            f"US mid vs international mid, absolute gap: median {100 * pct(.5):.2f}¢, "
            f"90th pct {100 * pct(.9):.2f}¢, 99th pct {100 * pct(.99):.2f}¢.",
            f"Times a US price was through fair value by ≥ {100 * self.scfg.taker_edge:.0f}¢ "
            f"after the taker fee: {s.buy_opps} to buy, {s.sell_opps} to sell "
            f"(see `events.jsonl`, kind=opportunity).", "",
        ]
        if self.ecfg.mode != "scan":
            start = self.risk.cfg.bankroll
            eq = b.equity(self.marks)
            lines += [
                "## Trading", "",
                f"Equity ${eq:.2f} from ${start:.2f} ({eq - start:+.2f}), cash "
                f"${b.cash:.2f}; {len(b.fills)} fills; taker fees ${b.fees_paid:.2f}; "
                f"maker rebates ${b.rebates:.2f}; open positions {len(b.positions)}.",
                f"Halted: {self.risk.halted or 'no'}.", "",
            ]
        with open(os.path.join(self.ecfg.out_dir, "report.md"), "w") as f:
            f.write("\n".join(lines) + "\n")
