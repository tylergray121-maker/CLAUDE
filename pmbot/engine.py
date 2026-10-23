"""Main loop: refresh pairs, poll both venues, quote, enforce risk, log."""

from __future__ import annotations

import json
import logging
import os
import re
import signal
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field, replace

from copybt.api import Client

from . import data, mapping
from .broker import SHORT, PaperBroker, Quote, split_side
from .fees import taker_fee_per_contract
from .risk import RiskManager
from .strategies import FairValue, Strategy
from .strategy import MarketView, Order, StrategyConfig

log = logging.getLogger(__name__)

# Totals are named differently: international "...-2026-10-21-total-2pt5" is
# US "...-2026-10-21-2pt5".
_TOTAL = re.compile(r"-total-(?=\d+pt\d+$)")
# Team codes Polymarket US spells differently from the international site
# (seen: aec-nba-gs-lal, aec-nba-ind-no, aec-nba-pho-por). Only a fallback:
# the bet's outcome name must still match the US market's side.
_ALIASES = {"nba": {"gsw": "gs", "nop": "no", "phx": "pho", "sas": "sa", "nyk": "ny"}}
_GAME_SLUG = re.compile(r"^([a-z0-9]+)-([a-z0-9]+)-([a-z0-9]+)-(\d{4}-\d{2}-\d{2}.*)$")


TENNIS = ("atp", "wta", "itf", "challenger")


def _person(name: str) -> str:
    return " ".join(re.findall(r"[a-z]+", name.lower()))


def players_key(league: str, a: str, b: str) -> tuple:
    return (league, frozenset({_person(a), _person(b)}))


def us_spellings(intl_slug: str) -> list[str]:
    """The international slug as US may name it: totals without '-total-',
    and team codes US spells differently."""
    out = [intl_slug, _TOTAL.sub("-", intl_slug)]
    m = _GAME_SLUG.match(intl_slug)
    alias = _ALIASES.get(m.group(1), {}) if m else {}
    if m and (m.group(2) in alias or m.group(3) in alias):
        lg, a, b, rest = m.groups()
        x = f"{lg}-{alias.get(a, a)}-{alias.get(b, b)}-{rest}"
        out += [x, _TOTAL.sub("-", x)]
    return list(dict.fromkeys(out))


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
    resume: bool = False             # continue the paper account in out_dir/state.json
    snapshot_seconds: float = 60.0   # how often state.json and paper.json are written
    equity_seconds: float = 300.0    # how often an equity point is recorded
    # Limits as shares of account value, re-set every cycle (0 = use the
    # fixed dollar limits). The stake is at least min_stake dollars.
    total_pct: float = 0.0
    market_pct: float = 0.0
    wallet_pct: float = 0.0
    stake_pct: float = 0.0
    min_stake: float = 1.0
    # Size the bot as if the account held at most this much (0 = all of it).
    # The bot then counts only its own contracts against its caps: money the
    # owner keeps in the account, or bets by hand, is not the bot's to spend.
    sizing_cap_usd: float = 0.0


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
                 broker=None, strategies: list[Strategy] | None = None):
        self.ecfg, self.scfg, self.risk = ecfg, scfg, risk
        self.strategies = strategies if strategies is not None else [FairValue(scfg)]
        self.owner: dict[str, str] = {}   # market slug -> strategy that trades it
        self.broker = broker or PaperBroker(risk.cfg.bankroll)
        self.client = Client(cache_dir=None, max_rps=ecfg.max_rps, retries=2, timeout=15)
        self.pairs: list[mapping.Pair] = []
        self.all_pairs: list[mapping.Pair] = []
        self.markets: dict[str, data.USMarket] = {}
        self.by_intl_slug: dict[str, data.USMarket] = {}  # international slug -> US game market
        self.by_players: dict[tuple, list] = {}   # tennis: (league, {players}) -> US match markets
        self.stats = ScanStats()
        self.marks: dict[str, float] = {}
        self.verified: set[str] = set()   # pairs whose live prices agree
        self.map_stats: dict = {}
        self.labels: dict[str, str] = {}   # slug -> readable market name
        self.ends: dict[str, float] = {}   # slug -> scheduled close, for held markets
        self.states: dict[str, str] = {}   # slug -> last US book state
        self.equity_hist: list[list] = []  # [ts, equity, cash]
        self.started = time.time()
        self.start_cash = risk.cfg.bankroll
        self._next_snapshot = self._next_equity = 0.0
        self._stop = False
        os.makedirs(ecfg.out_dir, exist_ok=True)
        self._events = open(os.path.join(ecfg.out_dir, "events.jsonl"), "a")
        if ecfg.resume and ecfg.mode in ("paper", "live"):
            self._load_state()
        if ecfg.mode == "live" and not self.equity_hist:
            self.start_cash = self.broker.equity({})  # the real account's value at the start

    # -- setup --------------------------------------------------------------
    def refresh_pairs(self) -> None:
        self._apply_pairs(self._build_pairs(self.client))

    def _build_pairs(self, client) -> dict:
        """Fetch the US market list and map it, without touching the engine's
        state (so it can run in a background thread while trading goes on)."""
        us = data.us_markets(client)
        markets = {m.slug: m for m in us}
        # Game, spread, total and prop markets: the US slug is the international
        # one plus a venue prefix. Ambiguous ones (two US markets) are dropped.
        seen: dict[str, list] = defaultdict(list)
        for m in us:
            if m.market_type not in data.LONG_RUNNING:
                seen[mapping.intl_slug(m.slug)].append(m)
        by_intl_slug = {k: v[0] for k, v in seen.items() if len(v) == 1}
        self._dump_market_types(us)
        intl = []
        if self.ecfg.pairs_file:
            pairs = [p for p in mapping.load(self.ecfg.pairs_file) if p.us_slug in markets]
        else:
            intl = data.intl_options(client)
            pairs = mapping.match(us, intl)
            # Games: exact slug matches for games starting within two days.
            now = time.time()
            # Games from 6 hours ago (in play) to 2 days ahead.
            games = [m for m in us if m.market_type in mapping.GAME_TYPES
                     and m.game_start and -6 * 3600 < m.game_start - now <= 2 * 86400]
            rows = data.intl_by_slugs(client, sorted({mapping.intl_slug(m.slug)
                                                           for m in games}))
            game_pairs = mapping.match_games(games, rows)
            log.info("games: %d US game markets in the next 48h, %d international "
                     "matches, %d pairs", len(games), len(rows), len(game_pairs))
            intl_by_token = {o.token: o for o in intl}
            kept, rejected = [], []
            for p in pairs:
                m, o = markets[p.us_slug], intl_by_token[p.intl_token]
                if None in (m.bid, m.ask, o.bid, o.ask):
                    kept.append((p, o.volume24h))  # checked against live books later
                    continue
                us_mid, ref_mid = (m.bid + m.ask) / 2, (o.bid + o.ask) / 2
                gap = abs(us_mid - ref_mid)
                if mapping.prices_agree(us_mid, ref_mid, self.ecfg.max_price_gap):
                    kept.append((p, o.volume24h))
                else:
                    rejected.append({**p.to_json(), "price_gap": round(gap, 3)})
            kept.sort(key=lambda x: -x[1])  # most active reference markets first
            # Game pairs first: they are what sportsgameday trades.
            pairs = game_pairs + [p for p, _ in kept if p.us_slug not in
                                  {g.us_slug for g in game_pairs}]
            mapping.save(pairs, os.path.join(self.ecfg.out_dir, "pairs.json"))
            with open(os.path.join(self.ecfg.out_dir, "pairs_rejected.json"), "w") as f:
                json.dump(rejected, f, indent=1)
            log.info("pairs: %d kept, %d rejected on price", len(pairs), len(rejected))
        # Tennis: US match slugs use other player codes (and sometimes another
        # date) than the international site, so index matches by player names.
        by_players: dict[tuple, list] = defaultdict(list)
        for m in us:
            lg = m.slug.split("-")[1] if m.slug.count("-") > 2 else ""
            if lg in TENNIS and m.market_type == "moneyline" and m.long_label and m.short_label:
                by_players[players_key(lg, m.long_label, m.short_label)].append(m)
        return {"markets": markets, "by_intl_slug": by_intl_slug, "pairs": pairs,
                "by_players": dict(by_players),
                "map_stats": {"us_markets": len(us), "pairs": len(pairs),
                              "tracked": min(len(pairs), self.ecfg.max_markets),
                              "intl_options": len(intl) if not self.ecfg.pairs_file else None}}

    def _apply_pairs(self, r: dict) -> None:
        self.markets, self.by_intl_slug = r["markets"], r["by_intl_slug"]
        self.by_players = r.get("by_players", {})
        self.all_pairs = r["pairs"]
        self.pairs = r["pairs"][:self.ecfg.max_markets]
        for p in r["pairs"]:
            self.labels[p.us_slug] = p.us_label
        self.map_stats = r["map_stats"]
        if not self.all_pairs:
            log.error("no US market could be paired with a reference price; "
                      "check pairs.json / the mapping before trusting this run")

    def _dump_market_types(self, us: list) -> None:
        """Counts and samples of US market types, for checking the mapping."""
        from collections import Counter
        kinds = Counter((m.market_type, m.category) for m in us)
        samples: dict = {}
        for m in us:
            k = f"{m.market_type}/{m.category}"
            if m.market_type not in data.LONG_RUNNING and len(samples.setdefault(k, [])) < 15:
                samples[k].append({"slug": m.slug, "question": m.question, "title": m.title,
                                   "game_start": m.game_start, "end": m.end,
                                   "bid": m.bid, "ask": m.ask})
        with open(os.path.join(self.ecfg.out_dir, "us_market_types.json"), "w") as f:
            json.dump({"counts": {f"{a}/{b}": n for (a, b), n in kinds.most_common()},
                       "samples": samples}, f, indent=1)

    # -- loop ---------------------------------------------------------------
    def run(self) -> None:
        signal.signal(signal.SIGINT, self._signal)
        signal.signal(signal.SIGTERM, self._signal)
        end = time.time() + self.ecfg.minutes * 60 if self.ecfg.minutes else float("inf")
        next_remap = 0.0
        failures = 0
        refresh = None
        pool = ThreadPoolExecutor(1)
        try:
            while not self._stop and time.time() < end:
                t0 = time.time()
                if refresh is not None and refresh.done():
                    try:
                        self._apply_pairs(refresh.result())
                    except Exception:
                        log.exception("market refresh failed; keeping the previous maps")
                    refresh = None
                if t0 >= next_remap:
                    if not self.markets:
                        self.refresh_pairs()   # the first one blocks: nothing maps without it
                    elif refresh is None:
                        # Later ones run beside trading (paging ~80k US markets
                        # takes minutes), on their own client and request budget.
                        refresh = pool.submit(self._build_pairs, Client(
                            cache_dir=None, max_rps=3, retries=2, timeout=15))
                    next_remap = t0 + self.ecfg.remap_minutes * 60
                try:
                    self.cycle()
                    failures = 0
                except Exception:
                    # A rejected order or a network blip must not end the run:
                    # every cycle starts from a fresh sync, so just go again.
                    # An exchange outage can last minutes: back off (up to a
                    # minute between tries) instead of ending the run.
                    failures += 1
                    log.exception("cycle failed (%d in a row)", failures)
                    if failures >= 10:
                        time.sleep(min(60.0, 5.0 * (failures - 9)))
                if self.risk.halted:
                    log.error("HALTED: %s", self.risk.halted)
                    break
                time.sleep(max(0.0, self.ecfg.cycle_seconds - (time.time() - t0)))
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
            self.shutdown()

    def _signal(self, *_):
        self._stop = True

    def scale_limits(self, equity: float) -> None:
        """Follow the account's value: caps and stake as shares of equity."""
        e, c = self.ecfg, self.risk.cfg
        if equity <= 0:
            return
        if e.sizing_cap_usd:
            equity = min(equity, e.sizing_cap_usd)
        if e.total_pct:
            c.max_total_usd = round(equity * e.total_pct, 2)
        if e.market_pct:
            c.max_market_usd = round(max(equity * e.market_pct, e.min_stake), 2)
        if e.stake_pct:
            self.scfg.order_usd = round(max(equity * e.stake_pct, e.min_stake), 2)
        if e.wallet_pct:
            for x in self.strategies:
                if hasattr(x, "max_wallet_usd"):
                    x.max_wallet_usd = round(max(equity * e.wallet_pct, e.min_stake), 2)

    def cycle(self) -> None:
        self.broker.sync()
        if self.ecfg.mode != "scan":
            self.scale_limits(self.broker.equity(self.marks))
        now = time.time()
        n_fills = len(self.broker.fills)
        by_slug = {p.us_slug: p for p in self.pairs}
        # Always watch holdings, and (live) positions that just disappeared.
        slugs = set(by_slug) | set(self.broker.positions) | set(getattr(self.broker, "vanished", {}))
        for strat in self.strategies:
            slugs |= strat.watch(self, now)
        slugs = sorted(slugs)
        us_q = data.fetch_parallel(lambda s: data.us_quote(self.client, s), slugs,
                                   self.ecfg.workers)
        paired = [by_slug[s] for s in slugs if s in by_slug]
        ref = dict(zip([p.us_slug for p in paired], data.fetch_parallel(
            lambda p: data.intl_book(self.client, p.intl_token), paired, self.ecfg.workers)))
        views: dict[str, tuple[MarketView, Quote]] = {}
        for slug, uq in zip(slugs, us_q):
            if uq is None:
                continue
            q, state = uq
            m = self.markets.get(split_side(slug)[0])
            ok, why = m.tradable(now) if m else (False, "unknown")
            if state:
                self.states[slug] = state
            if state and state != "MARKET_STATE_OPEN":
                ok, why = False, state.lower()
            if m and m.end:
                self.ends[slug] = m.end
            if q.bid is not None and q.ask is not None:
                self.marks[slug] = (q.bid + q.ask) / 2
            fair = rs = None
            if slug in ref:
                rb, ra, rs = ref[slug]
                fair = (rb + ra) / 2 if rb is not None and ra is not None else None
                p = by_slug[slug]
                if slug not in self.verified and fair is not None and \
                        q.bid is not None and q.ask is not None:
                    gap = abs((q.bid + q.ask) / 2 - fair)
                    if not mapping.prices_agree((q.bid + q.ask) / 2, fair,
                                                self.ecfg.max_price_gap):
                        self._log("pair_rejected", slug=slug, token=p.intl_token,
                                  gap=round(gap, 3), us=p.us_label, intl=p.intl_label)
                        self.pairs = [x for x in self.pairs if x is not p]
                        fair = rs = None
                    else:
                        self.verified.add(slug)
                if slug not in self.verified:
                    fair = rs = None  # never trade on an unverified reference
            v = MarketView(slug, m.tick if m else 0.01, q.bid, q.ask, q.bid_qty,
                           q.ask_qty, fair, rs, ok, why,
                           end=m.end if m else None, market_type=m.market_type if m else "")
            views[slug] = (v, q)
            self.broker.observe(slug, q)
            if fair is not None:
                self._scan(v)
        if self.ecfg.mode != "scan" and not self.risk.halted:
            self._trade_all(views, now)
        self._settle_closed(now)
        for strat in self.strategies:
            if hasattr(strat, "on_fills"):
                strat.on_fills(self, self.broker.fills[n_fills:])
        eq = self.broker.equity(self.marks)
        if self.ecfg.mode != "scan" and self.risk.check(eq):
            self.broker.cancel_all()
        self._summary(eq)
        if now >= self._next_equity:
            self.equity_hist.append([int(now), round(eq, 2), round(self.broker.cash, 2)])
            self._next_equity = now + self.ecfg.equity_seconds
        if self.ecfg.mode in ("paper", "live") and now >= self._next_snapshot:
            self.save_state()
            self.write_dashboard(eq)
            self._next_snapshot = now + self.ecfg.snapshot_seconds

    # -- helpers strategies use -------------------------------------------------
    def held(self, slug: str) -> int:
        p = self.broker.positions.get(slug)
        return p.qty if p else 0

    def token_index(self) -> dict[str, str]:
        """International outcome token -> the US market that prices the same thing."""
        return {p.intl_token: p.us_slug for p in self.all_pairs}

    def _tennis_match(self, intl_slug: str, title: str, ts) -> "data.USMarket | None":
        """The US match market for an international tennis match-winner market,
        found by the two players' names (title 'A vs. B') and the nearest start."""
        lg = intl_slug.split("-")[0]
        if lg not in TENNIS or not re.match(r"^[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-\d{4}-\d{2}-\d{2}$",
                                            intl_slug):
            return None   # only the match winner, not sets, totals or spreads
        names = re.split(r"\s+vs\.?\s+", title.split(":")[-1].strip(), flags=re.I)
        if len(names) != 2:
            return None
        cands = self.by_players.get(players_key(lg, *names), [])
        try:
            t0 = float(ts)
        except (TypeError, ValueError):
            t0 = time.time()
        cands = [m for m in cands if m.game_start and abs(m.game_start - t0) < 36 * 3600]
        return min(cands, key=lambda m: abs(m.game_start - t0)) if cands else None

    def lists(self, intl_slug: str) -> bool:
        """Polymarket US lists this international game/spread/total/prop market."""
        return any(s in self.by_intl_slug for s in us_spellings(intl_slug))

    def us_for_trade(self, t: dict, index: dict[str, str] | None = None) -> str | None:
        """The US market, or its short side, for an international trade.

        Paired tokens first; otherwise the trade's own market slug and
        outcome name, so any game, spread, total or prop Polymarket US also
        lists is found, whichever side the trade was on.
        """
        index = self.token_index() if index is None else index
        slug = index.get(str(t.get("asset")))
        if slug:
            return slug
        isl = str(t.get("slug") or "")
        m = next((self.by_intl_slug[s] for s in us_spellings(isl) if s in self.by_intl_slug), None)
        if m is None:
            m = self._tennis_match(isl, str(t.get("title") or ""), t.get("timestamp"))
        outcome = str(t.get("outcome") or "").strip().lower()
        if m is None or not outcome:
            return None
        if m.long_label and m.long_label.strip().lower() == outcome:
            slug = m.slug
        elif m.short_label and m.short_label.strip().lower() == outcome:
            slug = m.slug + SHORT
        else:
            return None
        self.labels.setdefault(slug, f"{t.get('title') or m.question}: {t.get('outcome')}")
        return slug

    def room(self, slug: str) -> float:
        b = self.broker
        own = getattr(b, "own", None) if self.ecfg.sizing_cap_usd else None
        return self.risk.room(slug, b.positions if own is None else own, b.open_orders, b.cash)

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

    def _trade_all(self, views: dict, now: float) -> None:
        b = self.broker
        # Release markets a strategy no longer has anything in (live, a settled
        # position stays owned until its payout is booked, so it is scored).
        for slug in list(self.owner):
            if not self.held(slug) and not any(o.slug == slug for o in b.open_orders.values()) \
                    and slug not in getattr(b, "vanished", {}):
                del self.owner[slug]
        plain = {s: v for s, (v, _) in views.items()}
        want: dict[str, list[Order]] = defaultdict(list)
        claimed = dict(self.owner)
        for strat in self.strategies:
            for slug, orders in strat.orders(self, plain, now).items():
                if not orders or slug not in views:
                    continue
                if claimed.setdefault(slug, strat.name) != strat.name:
                    continue  # another strategy trades this market
                want[slug] += [replace(o, tag=strat.name) for o in orders]
        for slug, (v, q) in views.items():
            self._reconcile(v, q, want.get(slug, []))

    def _reconcile(self, v: MarketView, q: Quote, want: list[Order]) -> None:
        b = self.broker
        want = list(want)
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
            if w.side == "BUY" and w.price * w.qty > self.room(v.slug) + 1e-9:
                continue
            if not self.risk.allow_order():
                self._log("throttled", slug=v.slug)
                break
            oid = b.place(v.slug, w, q)
            self.owner.setdefault(v.slug, w.tag)
            self._log("order", slug=v.slug, side=w.side, price=w.price, qty=w.qty,
                      post_only=w.post_only, fair=v.fair, strategy=w.tag, id=oid)

    CLOSED_STATES = {"MARKET_STATE_CLOSED", "MARKET_STATE_EXPIRED", "MARKET_STATE_TERMINATED"}

    def _settle_closed(self, now: float) -> None:
        """Pay out paper positions in markets that have finished.

        Only a market that is closed (by its book state, or gone from the open
        list after its scheduled end) is settled, at a final value of 0..1:
        the book's daily `settlementPx` mark is not a payout.
        """
        live = not isinstance(self.broker, PaperBroker)
        # Live, the exchange pays out; positions it settled show up as vanished.
        for slug in list(getattr(self.broker, "vanished", {}) if live else self.broker.positions):
            m = self.markets.get(split_side(slug)[0])
            end = m.end if m else self.ends.get(slug)
            closed = (self.states.get(slug) in self.CLOSED_STATES
                      or (m is None and end is not None and now > end))
            if live and not closed and self.states.get(slug) == "MARKET_STATE_OPEN" \
                    and slug in self.marks:
                # Gone while the market still trades: sold outside the bot (by
                # hand in the app). Book it at the current mid, not as a payout,
                # unless the price says the game is decided: the exchange pays
                # winners out before it marks the market closed.
                tag = self.owner.get(slug) or next(
                    (f.tag for f in reversed(self.broker.fills) if f.slug == slug and f.tag), "")
                mark = self.marks[slug]
                if mark >= 0.95 or mark <= 0.05:
                    self.broker.settle(slug, 1.0 if mark >= 0.95 else 0.0, tag)
                    self._log("settle", slug=slug, value=round(mark), early=True)
                else:
                    self.broker.sold_outside(slug, mark, tag)
                    self._log("sold_outside", slug=slug, price=mark)
                self.owner.pop(slug, None)
                continue
            if not closed:
                continue
            value = data.us_settlement(self.client, slug)
            if value is None or not 0.0 <= value <= 1.0:
                continue
            tag = self.owner.get(slug) or next(
                (f.tag for f in reversed(self.broker.fills) if f.slug == slug and f.tag), "")
            self.broker.settle(slug, value, tag)
            if live:
                self.owner.pop(slug, None)
            self._log("settle", slug=slug, value=value)

    # -- persistence and dashboard ------------------------------------------------
    def _state_path(self) -> str:
        return os.path.join(self.ecfg.out_dir, "state.json")

    def save_state(self) -> None:
        r = self.risk
        state = {"version": 1, "saved": time.time(), "started": self.started, "mode": self.ecfg.mode,
                 "start_cash": self.start_cash, "broker": self.broker.to_state(),
                 "owner": self.owner, "labels": {k: v for k, v in self.labels.items()
                                                 if k in self.broker.positions or k in self.owner
                                                 or any(f.slug == k for f in self.broker.fills[-200:])},
                 "ends": {k: v for k, v in self.ends.items() if k in self.broker.positions},
                 "equity": self.equity_hist[-20000:],
                 "risk": {"day": r._day, "day_start_equity": r._day_start_equity,
                          "halted": r.halted},
                 "strategy_stats": {x.name: dict(x.stats) for x in self.strategies
                                    if getattr(x, "stats", None) is not None},
                 "strategy_state": {x.name: x.to_state() for x in self.strategies
                                    if hasattr(x, "to_state")},
                 "scan": {"observations": self.stats.observations,
                          "buy_opps": self.stats.buy_opps, "sell_opps": self.stats.sell_opps,
                          "gaps": self.stats.gaps[-5000:]}}
        tmp = self._state_path() + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f)
        os.replace(tmp, self._state_path())

    def _load_state(self) -> None:
        try:
            with open(self._state_path()) as f:
                st = json.load(f)
        except (OSError, ValueError):
            log.info("no saved paper account: starting with $%.2f", self.risk.cfg.bankroll)
            return
        if st.get("mode", "paper") != self.ecfg.mode:
            log.warning("saved state is from a %s run; not resuming it in %s mode",
                        st.get("mode", "paper"), self.ecfg.mode)
            return
        if isinstance(self.broker, PaperBroker):
            self.broker = PaperBroker.from_state(st["broker"])
        else:
            self.broker.load_state(st["broker"])
        self.started = st.get("started", self.started)
        self.start_cash = st.get("start_cash", self.start_cash)
        self.owner = st.get("owner", {})
        self.labels.update(st.get("labels", {}))
        self.ends.update(st.get("ends", {}))
        self.equity_hist = st.get("equity", [])
        rk = st.get("risk", {})
        today = int(time.time() // 86400)
        if rk.get("day") == today:  # a daily-loss halt lasts until the UTC day ends
            self.risk._day, self.risk._day_start_equity = rk["day"], rk["day_start_equity"]
            # Only a daily-loss halt carries over: a kill-file halt is
            # re-checked against the file itself on every cycle.
            if not str(rk.get("halted", "")).startswith("kill file") \
                    and self.risk.cfg.daily_loss_limit > 0:
                self.risk.halted = rk.get("halted", "")
        for x in self.strategies:
            saved = st.get("strategy_stats", {}).get(x.name)
            if saved and getattr(x, "stats", None) is not None:
                # Counters are fresh (zero) here; Counter.update adds, so this restores them.
                x.stats.update(saved)
            if hasattr(x, "load_state") and x.name in st.get("strategy_state", {}):
                x.load_state(st["strategy_state"][x.name])
        sc = st.get("scan", {})
        self.stats.observations = sc.get("observations", 0)
        self.stats.buy_opps, self.stats.sell_opps = sc.get("buy_opps", 0), sc.get("sell_opps", 0)
        self.stats.gaps = sc.get("gaps", [])
        log.info("resumed paper account: cash $%.2f, %d positions, %d fills, started %s",
                 self.broker.cash, len(self.broker.positions), len(self.broker.fills),
                 time.strftime("%Y-%m-%d %H:%M", time.gmtime(self.started)))

    def performance(self, since: float = 0.0) -> dict[str, dict]:
        """Settled results by source (each strategy, 'manual' for bets the bot
        didn't place), plus 'all': bets closed, won, win rate, dollars staked,
        realized P&L, ROI and open exposure. A bet closes when it settles or
        is sold; its stake is the cost basis of the contracts closed."""
        b = self.broker
        out: dict[str, dict] = {}

        def row(k):
            return out.setdefault(k, {"settled": 0, "won": 0, "staked": 0.0, "pnl": 0.0,
                                      "open_cost": 0.0, "open_value": 0.0})
        for f in b.fills:
            if f.side not in ("SETTLE", "SELL") or f.ts < since:
                continue
            stake = f.qty * f.price - (f.fee if f.side == "SELL" else 0.0) - f.pnl
            for k in (f.tag or "manual", "all"):
                r = row(k)
                r["settled"] += 1
                r["won"] += f.pnl > 0
                r["staked"] += stake
                r["pnl"] += f.pnl
        if not since:
            for slug, p in b.positions.items():
                mark = self.marks.get(slug, p.cost / p.qty if p.qty else 0.0)
                for k in (self.owner.get(slug) or "manual", "all"):
                    r = row(k)
                    r["open_cost"] += p.cost
                    r["open_value"] += p.qty * mark
        for r in out.values():
            r["win_rate"] = round(r["won"] / r["settled"], 4) if r["settled"] else None
            r["roi"] = round(r["pnl"] / r["staked"], 4) if r["staked"] > 0 else None
            for k in ("staked", "pnl", "open_cost", "open_value"):
                r[k] = round(r[k], 2)
        return out

    def _strategy_stats(self) -> dict:
        out = {}
        for strat in self.strategies:
            for k, v in (getattr(strat, "stats", None) or {}).items():
                out[f"{strat.name}_{k}"] = v
        for strat in self.strategies:
            if strat.name == "copytop":
                out["copytop_leaders"] = len(strat.leaders)
                out["copytop_filled"] = sum(1 for f in self.broker.fills if f.tag == "copytop"
                                            and f.side in ("BUY", "SELL"))
            if hasattr(strat, "summary"):
                out.update(strat.summary())
        return out

    def _preview_summary(self) -> dict:
        c = getattr(self.broker, "checker", None)
        if c is None:
            return {"preview": "off", "preview_accepted": 0, "preview_rejected": 0,
                    "preview_unchecked": 0, "preview_errors": 0, "preview_last_reject": ""}
        return {"preview": "on", "preview_accepted": c.stats["accepted"],
                "preview_rejected": c.stats["rejected"],
                "preview_unchecked": c.stats["unchecked"],
                "preview_errors": c.stats["errors"], "preview_last_reject": c.last_reject}

    def write_dashboard(self, equity: float) -> None:
        """paper.json: every row the dashboard shows, tagged by `kind`."""
        b, s = self.broker, self.stats
        iso = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t)) if t else None
        name = lambda slug: self.labels.get(slug) or slug
        held_value = sum(p.qty * self.marks.get(k, p.cost / p.qty) for k, p in b.positions.items())
        at_cost = sum(p.cost for p in b.positions.values())
        gaps = sorted(abs(g) for g in s.gaps)
        pct = lambda q: round(100 * gaps[min(len(gaps) - 1, int(q * len(gaps)))], 2) if gaps else None
        perf = self.performance()
        today = self.performance(since=time.time() // 86400 * 86400)
        rows = [{
            "kind": "summary", "mode": self.ecfg.mode, "updated": iso(time.time()),
            "started": iso(self.started),
            "start_cash": round(self.start_cash, 2), "equity": round(equity, 2),
            "pnl": round(equity - self.start_cash, 2),
            "pnl_pct": round((equity / self.start_cash - 1), 5) if self.start_cash else 0,
            "cash": round(getattr(b, "account_cash", b.cash), 2),
            "spendable": round(b.cash, 2), "positions_value": round(held_value, 2),
            "positions_cost": round(at_cost, 2), "unrealized": round(held_value - at_cost, 2),
            "realized": round(b.realized, 2), "fees_paid": round(b.fees_paid, 2),
            "rebates": round(b.rebates, 2), "fills": len(b.fills),
            "open_orders": len(b.open_orders), "positions": len(b.positions),
            "halted": self.risk.halted or "", "strategies": ",".join(x.name for x in self.strategies),
            "maker_edge_c": round(100 * self.scfg.maker_edge, 2),
            "taker_edge_c": round(100 * self.scfg.taker_edge, 2),
            "us_markets": self.map_stats.get("us_markets", 0),
            "pairs": self.map_stats.get("pairs", 0), "tracked": len(self.pairs),
            "observations": s.observations, "gap_median_c": pct(.5), "gap_p90_c": pct(.9),
            "buy_opps": s.buy_opps, "sell_opps": s.sell_opps,
            **self._preview_summary(), **self._strategy_stats(),
            **{f"balance_{k}": v for k, v in getattr(b, "balance_info", {}).items()},
            **{f"perf_{k}": v for k, v in perf.get("all", {}).items()},
            **{f"perf_today_{k}": v for k, v in today.get("all", {}).items()}}]
        rows += [{"kind": "perf", "id": k, "source": k, **v} for k, v in perf.items()]
        # Equity: every point for the last 2 days, hourly before that.
        cut = time.time() - 2 * 86400
        last_hour = None
        for t, e, c in self.equity_hist:
            if t < cut:
                h = t // 3600
                if h == last_hour:
                    continue
                last_hour = h
            rows.append({"kind": "equity", "ts": iso(t), "equity": e, "cash": c})
        for slug, p in sorted(b.positions.items(), key=lambda kv: -kv[1].cost):
            mark = self.marks.get(slug)
            value = p.qty * (mark if mark is not None else p.cost / p.qty)
            rows.append({"kind": "position", "slug": slug, "market": name(slug),
                         "qty": p.qty, "avg_price": round(p.cost / p.qty, 4),
                         "mark": round(mark, 4) if mark is not None else None,
                         "value": round(value, 2), "pnl": round(value - p.cost, 2),
                         "strategy": self.owner.get(slug, ""),
                         "copied": next((x.copied_from(slug) for x in self.strategies
                                         if hasattr(x, "copied_from")), ""),
                         "closes": iso(self.ends.get(slug))})
        for i, f in enumerate(b.fills[-100:][::-1]):
            rows.append({"kind": "fill", "id": f"f{len(b.fills) - i}", "ts": iso(f.ts),
                         "slug": f.slug, "market": name(f.slug),
                         "side": f.side, "price": f.price, "qty": f.qty,
                         "liquidity": "settlement" if f.side == "SETTLE" else
                                      ("maker" if f.maker else "taker"),
                         "fee": round(f.fee, 2), "pnl": round(f.pnl, 2), "strategy": f.tag})
        for o in sorted(b.open_orders.values(), key=lambda o: o.slug):
            rows.append({"kind": "order", "id": o.id, "slug": o.slug, "market": name(o.slug),
                         "side": o.side, "price": o.price, "qty": o.qty,
                         "strategy": o.tag, "placed": iso(o.placed)})
        for strat in self.strategies:
            if hasattr(strat, "dashboard_rows"):
                rows += strat.dashboard_rows()
        tmp = os.path.join(self.ecfg.out_dir, "paper.json.tmp")
        with open(tmp, "w") as fh:
            json.dump(rows, fh, separators=(",", ":"))
        os.replace(tmp, os.path.join(self.ecfg.out_dir, "paper.json"))

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
            eq = self.broker.equity(self.marks)
            self._summary(eq)
            if self.ecfg.mode in ("paper", "live"):
                self.save_state()
                self.write_dashboard(eq)
            self._write_report()
            self._events.close()

    def _write_report(self) -> None:
        s, b = self.stats, self.broker
        gaps = sorted(abs(g) for g in s.gaps)
        pct = lambda q: gaps[min(len(gaps) - 1, int(q * len(gaps)))] if gaps else 0
        lines = [
            f"# Polymarket US bot — {self.ecfg.mode} run", "",
            f"Mapping: {self.map_stats.get('us_markets', 0)} open US markets, "
            f"{self.map_stats.get('intl_options') or 0} international outcomes, "
            f"{self.map_stats.get('pairs', 0)} pairs ({len(self.pairs)} tracked after "
            f"live price checks); observations with a trustworthy reference price: "
            f"{s.observations}.", "",
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
