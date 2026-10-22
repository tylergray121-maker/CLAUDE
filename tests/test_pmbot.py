import json
import os
import tempfile
import time
import unittest
from collections import deque

from pmbot import data, mapping
from pmbot.broker import PaperBroker, Position, Quote
from pmbot.engine import Engine, EngineConfig
from pmbot.fees import maker_rebate, taker_fee, taker_fee_per_contract
from pmbot.risk import RiskConfig, RiskManager
from pmbot.strategy import MarketView, Order, StrategyConfig, decide

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def fixture(name):
    with open(os.path.join(FIX, name)) as f:
        return json.load(f)


def view(bid=0.49, ask=0.51, fair=0.50, spread=0.01, tick=0.01, qty=100, ok=True):
    return MarketView("m", tick, bid, ask, qty, qty, fair, spread, ok)


def quote(bid, ask, last=None, traded=0.0, ts=None, qty=100):
    return Quote(bid, ask, qty, qty, last, traded, ts if ts is not None else time.time() + 1)


class BackgroundRefreshTest(unittest.TestCase):
    def test_building_maps_leaves_the_engine_alone_until_applied(self):
        d = tempfile.mkdtemp()
        e = Engine(EngineConfig(mode="paper", out_dir=d, minutes=0), StrategyConfig(),
                   RiskManager(RiskConfig(kill_file=os.path.join(d, "STOP"))))
        v = FakeVenues()
        v.game = True
        r = e._build_pairs(v)
        self.assertEqual(e.markets, {})
        self.assertIn(GAME, r["markets"])
        e._apply_pairs(r)
        self.assertIn(GAME, e.markets)
        e.shutdown()


class EVSniperTest(unittest.TestCase):
    def setUp(self):
        from pmbot.ev import EVSniper
        self.d = tempfile.mkdtemp()
        self.calls = []
        self.odds = {"Milwaukee Bucks": 2.2, "Washington Wizards": 1.75}

        def fetch(sport):
            self.calls.append(sport)
            start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.start))
            return [{"commence_time": start, "home_team": "Washington Wizards",
                     "away_team": "Milwaukee Bucks", "bookmakers": [{"key": "pinnacle", "markets": [
                         {"key": "h2h", "outcomes": [{"name": n, "price": p}
                                                     for n, p in self.odds.items()]}]}]}]
        self.ev = EVSniper(StrategyConfig(order_usd=10), "test-key", fetch=fetch)
        self.e = Engine(EngineConfig(mode="paper", out_dir=self.d, minutes=0), StrategyConfig(),
                        RiskManager(RiskConfig(kill_file=os.path.join(self.d, "STOP"))),
                        strategies=[self.ev])
        self.v = self.e.client = FakeVenues()
        self.v.game = True
        self.e.refresh_pairs()
        self.start = time.time() + 3 * 3600
        self.e.markets[GAME].game_start = self.start
        self.e.markets[GAME].slug = GAME

    def tearDown(self):
        self.e.shutdown()

    def test_devig_and_team_matching(self):
        from pmbot.ev import devig, match_events
        self.assertEqual([round(x, 3) for x in devig([2.2, 1.75])], [0.443, 0.557])
        fair = match_events(self.ev.fetch("basketball_nba"), [self.e.markets[GAME]])
        self.assertAlmostEqual(fair[GAME], 0.443, places=3)            # Bucks: the long side
        self.assertAlmostEqual(fair[GAME + ":short"], 0.557, places=3)  # Wizards: the short side

    def test_buys_only_when_the_edge_beats_fee_and_margin(self):
        self.e.cycle()                 # Bucks ask 0.37 vs fair 0.443: +5.7c after the fee
        f = self.e.broker.fills[-1]
        self.assertEqual((f.slug, f.side, f.price, f.tag), (GAME, "BUY", 0.37, "evsniper"))
        self.assertEqual(self.calls, ["basketball_nba"])
        self.e.cycle()                 # no second buy of the same market within the hour
        self.assertEqual(sum(1 for f in self.e.broker.fills if f.side == "BUY"), 1)

    def test_no_edge_no_bet_and_never_in_play(self):
        self.odds = {"Milwaukee Bucks": 2.5, "Washington Wizards": 1.6}   # fair 0.39: too thin
        self.e.cycle()
        self.assertEqual(self.e.broker.fills, [])
        self.assertIn(GAME, self.ev.summary()["evsniper_closest"])         # the near miss shows
        self.odds = {"Milwaukee Bucks": 2.2, "Washington Wizards": 1.75}
        self.ev.next_poll.clear()
        self.e.markets[GAME].game_start = time.time() + 300   # about to start
        self.e.cycle()
        self.assertEqual(self.e.broker.fills, [])

    def test_requests_are_spaced_to_fit_the_monthly_budget(self):
        now = time.time()
        gap = self.ev._interval(4, now)
        days_left = 31 - time.gmtime(now).tm_mday + 1
        self.assertGreaterEqual(gap, 86400 * 4 / (450 / days_left) - 1)
        self.ev.used[time.strftime("%Y-%m", time.gmtime(now))] = 450
        self.assertEqual(self.ev._interval(4, now), float("inf"))

    def test_the_key_is_never_logged(self):
        from pmbot.ev import EVSniper
        ev = EVSniper(StrategyConfig(), "SECRET-KEY-123")
        with self.assertLogs("pmbot.ev", level="WARNING") as logs:
            import urllib.request
            orig = urllib.request.urlopen
            urllib.request.urlopen = lambda *a, **k: (_ for _ in ()).throw(OSError("boom"))
            try:
                self.assertIsNone(ev._fetch("basketball_nba"))
            finally:
                urllib.request.urlopen = orig
        self.assertNotIn("SECRET-KEY-123", "\n".join(logs.output))


class PerformanceTest(unittest.TestCase):
    def test_win_rate_roi_and_profit_by_source(self):
        d = tempfile.mkdtemp()
        e = Engine(EngineConfig(mode="paper", out_dir=d, minutes=0), StrategyConfig(),
                   RiskManager(RiskConfig(bankroll=100, kill_file=os.path.join(d, "STOP"))))
        b = e.broker
        b._fill("a", "BUY", 0.40, 10, False, "copytop")      # $4 + fee
        b._fill("b", "BUY", 0.50, 10, False, "copytop")
        b._fill("c", "BUY", 0.60, 5, False, "")              # a manual bet
        b.settle("a", 1.0, "copytop")                        # won
        b.settle("b", 0.0, "copytop")                        # lost
        perf = e.performance()
        c = perf["copytop"]
        self.assertEqual((c["settled"], c["won"], c["win_rate"]), (2, 1, 0.5))
        self.assertAlmostEqual(c["staked"], 4.0 + 5.0 + 0.17 + 0.18, places=2)
        self.assertAlmostEqual(c["pnl"], (10 - 4.17) - 5.18, places=2)
        self.assertAlmostEqual(c["roi"], c["pnl"] / c["staked"], places=3)
        self.assertEqual(perf["manual"]["settled"], 0)
        self.assertGreater(perf["manual"]["open_cost"], 3.0)
        self.assertEqual(perf["all"]["settled"], 2)
        e.write_dashboard(b.equity(e.marks))
        rows = json.load(open(os.path.join(d, "paper.json")))
        self.assertEqual(rows[0]["perf_win_rate"], 0.5)
        self.assertEqual({r["source"] for r in rows if r["kind"] == "perf"}, {"copytop", "manual", "all"})
        e.shutdown()


class DiscoverTest(unittest.TestCase):
    def test_wallets_that_bet_often_on_a_tag_are_found(self):
        from pmbot.select import discover

        class C:
            def get(self, base, path, params=None, **kw):
                if path == "/events":
                    return [] if params["offset"] else [
                        {"markets": [{"conditionId": "0xc1"}, {"conditionId": "0xc2"}]}]
                return [{"proxyWallet": "0xAAA", "side": "BUY", "name": "esp"}] * 9 + \
                       [{"proxyWallet": "0xbbb", "side": "BUY"}] * 2 + \
                       [{"proxyWallet": "0xccc", "side": "SELL"}] * 20
        got = discover(C(), ["esports"], 0, max_events=50, min_buys=15)
        self.assertEqual(list(got), ["0xaaa"])                 # 18 buys; bbb 4; ccc only sells
        self.assertEqual((got["0xaaa"]["name"], got["0xaaa"]["boards"]), ("esp", ["tag:esports"]))


class ApplyLeadersTest(unittest.TestCase):
    def test_keeps_owner_picks_and_refuses_a_thin_selection(self):
        from pmbot.apply_leaders import merge
        cur = {"leaders": [{"wallet": "0xAAA", "name": "Tiger105", "source": "owner's pick"},
                           {"wallet": "0xBBB", "name": "old"}]}
        sel = {"chosen": "2026-10-23", "method": "m",
               "leaders": [{"wallet": f"0x{i}", "name": f"w{i}"} for i in range(12)]
               + [{"wallet": "0xaaa", "name": "dup"}]}
        new = merge(cur, sel, 10)
        ws = [x["wallet"].lower() for x in new["leaders"]]
        self.assertEqual(ws[0], "0xaaa")                     # owner's pick kept, first
        self.assertNotIn("0xbbb", ws)                         # dropped
        self.assertEqual(len(ws), 13)                         # 12 picks + Tiger105, no dup
        self.assertIsNone(merge(cur, {"leaders": sel["leaders"][:3]}, 10))
        # the no-ranking fallback lost out of sample: never applied
        self.assertIsNone(merge(cur, {**sel, "method": "every qualified wallet (no ranking "
                                      "method beat it out of sample)"}, 10))


class ScaledLimitsTest(unittest.TestCase):
    def test_limits_follow_the_account_value(self):
        from pmbot.copy import CopyTop
        d = tempfile.mkdtemp()
        copy = CopyTop(StrategyConfig(order_usd=1), {}, max_wallet_usd=5)
        scfg = copy.cfg
        e = Engine(EngineConfig(mode="paper", out_dir=d, minutes=0, total_pct=0.88, market_pct=0.053,
                                wallet_pct=0.09, stake_pct=0.0175, min_stake=1.0),
                   scfg, RiskManager(RiskConfig(bankroll=57, kill_file=os.path.join(d, "STOP"))),
                   strategies=[copy])
        e.scale_limits(57.0)
        self.assertEqual((e.risk.cfg.max_total_usd, e.risk.cfg.max_market_usd), (50.16, 3.02))
        self.assertEqual((scfg.order_usd, copy.max_wallet_usd), (1.0, 5.13))     # $1 floor
        e.scale_limits(200.0)
        self.assertEqual((e.risk.cfg.max_total_usd, scfg.order_usd, copy.max_wallet_usd),
                         (176.0, 3.5, 18.0))
        e.scale_limits(20.0)
        self.assertEqual((e.risk.cfg.max_total_usd, scfg.order_usd), (17.6, 1.0))
        e.shutdown()


class RiskTest(unittest.TestCase):
    def test_a_zero_daily_loss_limit_means_no_daily_stop(self):
        d = tempfile.mkdtemp()
        r = RiskManager(RiskConfig(daily_loss_limit=0, kill_file=os.path.join(d, "STOP")))
        self.assertEqual(r.check(30.0, now=1000), "")
        self.assertEqual(r.check(5.0, now=2000), "")      # down $25: still trading
        r = RiskManager(RiskConfig(daily_loss_limit=10, kill_file=os.path.join(d, "STOP")))
        r.check(30.0, now=1000)
        self.assertIn("daily loss", r.check(19.0, now=2000))
        open(os.path.join(d, "STOP"), "w").close()
        r = RiskManager(RiskConfig(daily_loss_limit=0, kill_file=os.path.join(d, "STOP")))
        self.assertIn("kill file", r.check(30.0, now=1000))   # the STOP file still works


class ScorecardTest(unittest.TestCase):
    def test_lots_close_oldest_first_and_credit_every_key(self):
        from pmbot.track import Scorecard
        c = Scorecard()
        c.open("m", ["w:a", "league:nba"], 10, 5.0)
        c.open("m", ["w:b", "league:nba"], 10, 6.0)
        c.close("m", 15, 15.0)                       # sold 15 at $1: all of a's lot, half of b's
        self.assertEqual(c.summary("w:a")["pnl"], 5.0)
        self.assertEqual(c.summary("w:b")["pnl"], 2.0)
        self.assertEqual(c.summary("w:b")["open_usd"], 3.0)
        self.assertEqual(c.summary("league:nba")["settled"], 2)
        c.close("m", 5, 0.0)                         # the rest settles worthless
        self.assertEqual(c.summary("w:b")["pnl"], -1.0)
        self.assertEqual(c.lots, {})

    def test_only_clear_losses_count_as_losing(self):
        from pmbot.track import clearly_losing, summarize
        mixed = summarize([[-5, 5]] * 6 + [[5, 5]] * 4)
        self.assertFalse(clearly_losing(mixed, 10))    # 4 of 10 at even money: could be luck
        bad = summarize([[-5, 5]] * 9 + [[5, 5]])
        self.assertTrue(clearly_losing(bad, 10))
        self.assertFalse(clearly_losing(bad, 15))      # not enough bets yet


class SelectTest(unittest.TestCase):
    """The leader-selection backtest copies the way copytop does."""

    def setUp(self):
        from copybt.models import Market, Trade
        self.Trade = Trade
        self.m = {"c1": Market("c1", True, 2_000_000, {"A": 1.0, "B": 0.0}, start_ts=1_500_000)}
        self.pairs = {("nba", "moneyline")}

    def t(self, ts, side, price, size=100, asset="A", slug="nba-mil-was-2026-10-21"):
        return self.Trade(ts, asset, "c1", side, price, size, "Bucks vs. Wizards", "Bucks",
                          "", "0xw", slug)

    def test_market_kinds(self):
        from pmbot.select import kind_of
        self.assertEqual(kind_of("nba-mil-was-2026-10-21"), "moneyline")
        self.assertEqual(kind_of("nba-mil-was-2026-10-21-total-229pt5"), "totals")
        self.assertEqual(kind_of("nba-mil-was-2026-10-21-229pt5"), "totals")   # US naming
        self.assertEqual(kind_of("lal-ray-ath-2026-10-10-ray"), "result")
        self.assertEqual(kind_of("nba-mil-was-2026-10-21-spread-home-6pt5"), "")
        self.assertEqual(kind_of("will-x-win-the-2026-world-series"), "")

    def test_copies_like_copytop(self):
        from pmbot.select import Rules, copies, stats
        trades = [self.t(1_000_000, "BUY", 0.40),
                  self.t(1_000_100, "BUY", 0.41),            # same outcome within 10 min
                  self.t(1_000_700, "BUY", 0.42),
                  self.t(1_001_400, "BUY", 0.43, size=5),    # leader bet under $5
                  self.t(1_002_000, "BUY", 0.40, slug="nba-mil-was-2026-10-21-odd-even")]
        lots = copies(trades, self.m, self.pairs, Rules())
        self.assertEqual([(x["price"], x["qty"]) for x in lots], [(0.405, 24), (0.425, 23)])
        s = stats(lots)                                       # both settle at 1.0
        self.assertEqual((s["n"], s["won"]), (2, 2))
        self.assertAlmostEqual(s["pnl"], (24 + 23) - lots[0]["cost"] - lots[1]["cost"], delta=0.01)
        self.assertEqual(lots[0]["timing"], "pre-game")

    def test_never_chases_and_caps_a_market(self):
        from pmbot.select import Rules, copies
        moved = lambda tok, ts: 0.43                           # price 3c higher at our delay
        lots = copies([self.t(1_000_000, "BUY", 0.40)], self.m, self.pairs, Rules(), moved)
        self.assertEqual(lots, [{"wallet": "0xw", "ts": 1_000_000, "skipped": "price_moved"}])
        many = [self.t(1_000_000 + 700 * i, "BUY", 0.50) for i in range(8)]
        lots = copies(many, self.m, self.pairs, Rules())
        self.assertLessEqual(sum(x["qty"] * x["price"] for x in lots), 50)
        self.assertEqual(len(lots), 6)               # five $10 copies, then the last $2

    def test_their_sell_closes_ours_if_the_price_holds(self):
        from pmbot.select import Rules, copies
        trades = [self.t(1_000_000, "BUY", 0.40), self.t(1_100_000, "SELL", 0.60)]
        lots = copies(trades, self.m, self.pairs, Rules())
        self.assertEqual(lots[0]["exit"], "sell")
        self.assertGreater(lots[0]["pnl"], 0)
        held = copies(trades, self.m, self.pairs, Rules(copy_sells=False))
        self.assertEqual(held[0]["exit"], "settle")

    def test_markouts_and_the_rankings_built_on_them(self):
        from pmbot.select import METHODS, Rules, copies
        drift = lambda tok, ts: 0.40 if ts < 1_000_100 else 0.48    # moves our way after the fill
        lots = copies([self.t(1_000_000, "BUY", 0.40)], self.m, self.pairs,
                      Rules(delay_s=30), drift)
        self.assertEqual((lots[0]["mo30"], lots[0]["mo120"]), (0.075, 0.075))  # 0.48 - 0.405 ask
        L = [{"mo120": 0.05 + 0.01 * (i % 2), "mo30": 0.02, "pnl": 1.0, "cost": 5.0}
             for i in range(12)]
        self.assertAlmostEqual(METHODS["markout 2h, average"](L), 0.055, places=4)
        self.assertLess(METHODS["markout 2h, lower bound"](L), 0.055)
        self.assertIsNone(METHODS["markout 30m, average"](L[:5]))         # too few
        self.assertAlmostEqual(METHODS["copy return, shrunk"](L), 0.2 * 12 / 72, places=4)

    def test_walk_forward_scores_methods_only_on_unseen_windows(self):
        from pmbot.select import walk_forward
        day, end = 86400, 100 * 86400
        lot = lambda ts, pnl, price=0.5: {"ts": ts, "pnl": pnl, "cost": 5.0, "price": price}
        good = [lot(end - d * day, 5.0 if d % 3 else -5.0) for d in range(1, 90)]   # 2/3 winners
        bad = [lot(end - d * day, -5.0 if d % 3 else 5.0) for d in range(1, 90)]
        wf = walk_forward({"good": good, "bad": bad}, end, 45, 15, 3, 10, sizes=(1,))
        self.assertGreater(wf[("copy return, average", 1)]["mean"], 0)       # picks "good"
        self.assertAlmostEqual(wf[("all", None)]["mean"], 0.0, places=2)    # both wallets
        self.assertEqual(wf[("copy return, average", 1)]["n"], 45)          # 3 folds x 15 days

    def test_pick_needs_enough_copies_and_a_positive_bound(self):
        from pmbot.select import pick
        win = {"pnl": 5.0, "cost": 5.0, "ts": 1, "price": 0.5}
        lose = {"pnl": -5.0, "cost": 5.0, "ts": 1, "price": 0.5}
        d = {"good": [win] * 12 + [lose] * 4, "few": [win] * 5, "bad": [win] * 8 + [lose] * 8}
        self.assertEqual(pick(d, 10, 5), ["good"])


class ShortSideTest(unittest.TestCase):
    def test_short_book_is_the_long_book_flipped(self):
        q = Quote(0.36, 0.37, 40, 100, 0.36, 5, 1.0).flipped()
        self.assertEqual((q.bid, q.ask, q.bid_qty, q.ask_qty, q.last_px),
                         (0.63, 0.64, 100, 40, 0.64))

    def test_short_orders_use_short_intents_priced_on_the_long_side(self):
        from pmbot.broker import order_params
        p = order_params("g:short", Order("BUY", 0.63, 5, post_only=False))
        self.assertEqual((p["marketSlug"], p["intent"], p["price"]["value"]),
                         ("g", "ORDER_INTENT_BUY_SHORT", "0.370"))
        p = order_params("g", Order("SELL", 0.4, 5, post_only=False))
        self.assertEqual((p["marketSlug"], p["intent"], p["price"]["value"]),
                         ("g", "ORDER_INTENT_SELL_LONG", "0.400"))


class FeesTest(unittest.TestCase):
    def test_taker_fee_curve(self):
        self.assertAlmostEqual(taker_fee_per_contract(0.5), 0.017375)
        self.assertEqual(taker_fee(0.5, 100), 1.74)   # rounded up to the cent
        self.assertEqual(taker_fee(0.05, 1), 0.01)
        self.assertEqual(maker_rebate(0.5, 100), 0.08)


class StrategyTest(unittest.TestCase):
    cfg = StrategyConfig(maker_edge=0.02, taker_edge=0.03, order_usd=5)

    def test_bid_never_above_fair_minus_edge(self):
        out = decide(view(bid=0.49, ask=0.51, fair=0.50), 0, 100, self.cfg)
        self.assertEqual(out, [Order("BUY", 0.48, 10, True)])

    def test_bid_pennies_a_low_best_bid(self):
        out = decide(view(bid=0.40, ask=0.60, fair=0.50), 0, 100, self.cfg)
        self.assertEqual(out[0].price, 0.41)

    def test_ask_for_held_contracts_never_below_fair_plus_edge(self):
        out = decide(view(bid=0.49, ask=0.51, fair=0.50), 7, 100, self.cfg)
        self.assertIn(Order("SELL", 0.52, 7, True), out)
        out = decide(view(bid=0.40, ask=0.60, fair=0.50), 7, 100, self.cfg)
        self.assertIn(Order("SELL", 0.59, 7, True), out)

    def test_take_only_when_through_fair_after_fees(self):
        # 0.50 - 0.46 - 0.0172 fee = 0.023 < 0.03: no take, maker bid instead
        out = decide(view(bid=0.45, ask=0.46, fair=0.50), 0, 100, self.cfg)
        self.assertTrue(all(o.post_only for o in out))
        out = decide(view(bid=0.44, ask=0.45, fair=0.50), 0, 100, self.cfg)
        self.assertEqual(out, [Order("BUY", 0.45, 11, False)])

    def test_take_limited_by_displayed_size(self):
        v = view(bid=0.40, ask=0.45, fair=0.50, qty=3)
        self.assertEqual(decide(v, 0, 100, self.cfg)[0].qty, 3)

    def test_no_orders_without_trustworthy_fair_value(self):
        self.assertEqual(decide(view(spread=0.10), 0, 100, self.cfg), [])
        self.assertEqual(decide(view(fair=None), 0, 100, self.cfg), [])
        self.assertEqual(decide(view(ok=False), 0, 100, self.cfg), [])
        self.assertEqual(decide(view(fair=0.97, bid=0.96, ask=0.98), 0, 100, self.cfg), [])

    def test_respects_risk_room(self):
        self.assertEqual(decide(view(), 0, 0.3, self.cfg), [])
        self.assertEqual(decide(view(), 0, 2.0, self.cfg)[0].qty, 4)

    def test_fine_ticks(self):
        out = decide(view(bid=0.4995, ask=0.5005, fair=0.50, tick=0.001), 0, 100, self.cfg)
        self.assertEqual(out[0].price, 0.48)


class RiskTest(unittest.TestCase):
    def test_room(self):
        r = RiskManager(RiskConfig(max_market_usd=25, max_total_usd=40))
        pos = {"a": Position(10, 6.0), "b": Position(20, 12.0)}
        from pmbot.broker import OpenOrder
        orders = {"1": OpenOrder("1", "a", "BUY", 0.5, 10, True)}
        # market a: 25 - (6 position + 5 bid) = 14; total: 40 - 23 = 17
        self.assertAlmostEqual(r.room("a", pos, orders, cash=100), 14)
        # market c: total limit binds (40 - 23)
        self.assertAlmostEqual(r.room("c", pos, orders, cash=100), 17)
        # cash binds, net of cash already promised to open bids
        self.assertAlmostEqual(r.room("c", pos, orders, cash=8), 3)

    def test_daily_loss_halts(self):
        r = RiskManager(RiskConfig(daily_loss_limit=30, kill_file="/nonexistent/STOP"))
        self.assertEqual(r.check(200, now=0), "")
        self.assertEqual(r.check(175, now=10), "")
        self.assertIn("daily loss", r.check(169, now=20))
        self.assertIn("daily loss", r.check(250, now=30))  # sticky

    def test_kill_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "STOP")
            r = RiskManager(RiskConfig(kill_file=path))
            self.assertEqual(r.check(200), "")
            open(path, "w").close()
            self.assertIn("kill file", r.check(200))


class PaperBrokerTest(unittest.TestCase):
    def test_touch_is_not_a_fill_trade_through_is(self):
        b = PaperBroker(100)
        b.place("m", Order("BUY", 0.48, 10, True))
        b.observe("m", quote(0.47, 0.48))                  # touch
        self.assertEqual(b.positions, {})
        b.observe("m", quote(0.46, 0.47))                  # through
        self.assertEqual(b.positions["m"].qty, 10)
        self.assertAlmostEqual(b.cash, 100 - 4.8 + maker_rebate(0.48, 10))

    def test_print_below_bid_fills(self):
        b = PaperBroker(100)
        b.observe("m", quote(0.47, 0.49, last=0.48, traded=10))
        b.place("m", Order("BUY", 0.48, 10, True))
        b.observe("m", quote(0.47, 0.49, last=0.48, traded=20))  # print at our price
        self.assertEqual(b.positions, {})
        b.observe("m", quote(0.46, 0.49, last=0.47, traded=30))  # print below
        self.assertEqual(b.positions["m"].qty, 10)

    def test_order_placed_after_quote_does_not_fill_on_it(self):
        b = PaperBroker(100)
        b.place("m", Order("BUY", 0.48, 10, True))
        b.observe("m", quote(0.40, 0.45, ts=time.time() - 5))
        self.assertEqual(b.positions, {})

    def test_take_pays_fee_and_sell_is_capped_by_holding(self):
        b = PaperBroker(100)
        q = quote(0.44, 0.45, qty=5)
        b.observe("m", q)
        b.place("m", Order("BUY", 0.45, 10, False), q)      # only 5 displayed
        self.assertEqual(b.positions["m"].qty, 5)
        self.assertAlmostEqual(b.cash, 100 - 2.25 - taker_fee(0.45, 5))
        b.place("m", Order("SELL", 0.70, 9, True))
        b.observe("m", quote(0.71, 0.72))
        self.assertNotIn("m", b.positions)
        self.assertEqual(b.fills[-1].qty, 5)

    def test_settlement(self):
        b = PaperBroker(10)
        q = quote(0.3, 0.4)
        b.place("m", Order("BUY", 0.4, 5, False), q)
        b.settle("m", 1.0)
        self.assertAlmostEqual(b.cash, 10 - 2.0 - taker_fee(0.4, 5) + 5)
        self.assertEqual(b.positions, {})


class DataTest(unittest.TestCase):
    def test_us_market_from_real_response(self):
        ms = [data.parse_us_market(m) for m in fixture("pmbot_us_markets.json")]
        m = next(x for x in ms if x.title == "Milwaukee Brewers")
        self.assertEqual((m.question, m.market_type, m.tick), ("World Series Champion", "futures", 0.001))
        self.assertIsNotNone(m.bid)
        ok, _ = m.tradable(m.end - 7200)
        self.assertTrue(ok)                       # futures: season start isn't kickoff
        self.assertFalse(m.tradable(m.end - 60)[0])

    def test_us_book_from_real_response(self):
        class C:
            def get(self, base, path, params=None, use_cache=True, keep=None):
                return fixture("pmbot_us_book.json")
        q, state = data.us_quote(C(), "x")
        self.assertEqual((q.bid, q.ask, state), (0.90, 0.901, "MARKET_STATE_OPEN"))
        self.assertGreater(q.bid_qty, 1000)
        self.assertGreater(q.traded, 0)

    def test_intl_book_from_real_response(self):
        class C:
            def get(self, base, path, params=None, use_cache=True, keep=None):
                return fixture("pmbot_intl_book.json")
        bid, ask, spread = data.intl_book(C(), "t")
        self.assertLess(bid, ask)
        self.assertAlmostEqual(spread, ask - bid)

    def test_listing_stops_cleanly_at_the_offset_limit(self):
        from copybt.api import HTTPError
        rows = fixture("pmbot_intl_markets.json")

        class C:
            calls = []
            def get(self, base, path, params=None, use_cache=True, keep=None):
                self.calls.append(params)
                if params["offset"] >= 4:
                    raise HTTPError(422, path, "offset too large")
                return rows
        c = C()
        opts = data.intl_options(c)
        self.assertEqual(len(opts), 2 * len([o for m in rows for o in data.parse_intl_market(m)]))
        self.assertEqual(c.calls[0]["order"], "volume24hr")

    def test_intl_market_from_real_response(self):
        opts = [o for m in fixture("pmbot_intl_markets.json") for o in data.parse_intl_market(m)]
        self.assertTrue(opts)
        self.assertTrue(all(o.token and o.label for o in opts))


def us_market(title, question, desc, end=1.8e9, slug="us-1", bid=0.62, ask=0.63):
    return data.USMarket(slug, question, title, desc, "futures", "sports", None, end,
                         0.001, "MARKET_STATUS_OPEN", bid, ask)


def intl_opt(label, question, event="", end=1.8e9, token="t1", bid=0.62, ask=0.63):
    return data.IntlOption(token, label, question, event, end, bid, ask, 1000.0)


class MappingTest(unittest.TestCase):
    def test_futures_match(self):
        us = [us_market("Milwaukee Brewers", "World Series Champion",
                        "Will Milwaukee Brewers win the 2026 MLB World Series, scheduled ...")]
        intl = [intl_opt("Milwaukee Brewers", "Will the Milwaukee Brewers win the 2026 World Series?",
                         "World Series Champion 2026"),
                intl_opt("Milwaukee Brewers", "Will the Milwaukee Brewers win the 2026 NL Central?",
                         token="t2")]
        pairs = mapping.match(us, intl)
        self.assertEqual([p.intl_token for p in pairs], ["t1"])

    def test_wrong_season_or_far_end_date_rejected(self):
        us = [us_market("Milwaukee Brewers", "World Series Champion",
                        "Will Milwaukee Brewers win the 2026 MLB World Series?")]
        self.assertEqual(mapping.match(us, [intl_opt(
            "Milwaukee Brewers", "Will the Milwaukee Brewers win the 2027 World Series?")]), [])
        self.assertEqual(mapping.match(us, [intl_opt(
            "Milwaukee Brewers", "Will the Milwaukee Brewers win the 2026 World Series?",
            end=1.8e9 + 200 * 86400)]), [])

    def test_game_matched_exactly_by_slug_and_long_side(self):
        fx = fixture("pmbot_game.json")
        m = data.parse_us_market(fx["us"])
        self.assertEqual((m.market_type, m.long_label), ("moneyline", "Bucks"))
        self.assertEqual(mapping.intl_slug(m.slug), fx["intl"]["slug"])
        self.assertEqual(m.short_label, "Wizards")
        pairs = mapping.match_games([m], {fx["intl"]["slug"]: fx["intl"]})
        tokens = json.loads(fx["intl"]["clobTokenIds"])
        self.assertEqual([(p.us_slug, p.intl_token) for p in pairs],
                         [(m.slug, tokens[0]), (m.slug + ":short", tokens[1])])  # Bucks, Wizards
        m.long_label = "Wizards"
        self.assertEqual(mapping.match_games([m], {fx["intl"]["slug"]: fx["intl"]})[0].intl_token,
                         tokens[1])
        self.assertEqual(mapping.intl_slug("atc-lal-ray-ath-2026-10-10-ray"),
                         "lal-ray-ath-2026-10-10-ray")

    def test_generic_outcome_needs_the_same_event(self):
        ecb = us_market("No Change", "European Central Bank Decision in October?",
                        "Will the ECB make no change to rates in October?")
        russia = intl_opt("No change", "Will the Bank of Russia make no change to the key rate "
                          "after the October meeting?", "Bank of Russia decision in October?")
        self.assertEqual(mapping.match([ecb], [russia]), [])

    def test_games_must_be_the_same_meeting(self):
        day = 86400
        def game(end):
            return data.USMarket("us-g", "Avalanche vs. Flyers", "Avalanche", "", "moneyline",
                                 "sports", end - 3 * 3600, end, 0.01, "MARKET_STATUS_OPEN",
                                 0.55, 0.56)
        opt = intl_opt("Avalanche", "Avalanche vs. Flyers", "NHL: Avalanche vs. Flyers",
                       end=1.8e9 + 3600)
        self.assertEqual(len(mapping.match([game(1.8e9)], [opt])), 1)
        self.assertEqual(mapping.match([game(1.8e9 + 20 * day)], [opt]), [])  # rematch

    def test_different_kind_of_bet_on_same_team_rejected(self):
        intl = [intl_opt("Miami Heat", "Will Miami Heat win the 2027 NBA Finals?",
                         "2027 NBA Champion")]
        conf = us_market("Miami Heat", "NBA Eastern Conference Champion", "", )
        champ = us_market("Miami Heat", "2027 NBA Champion", "")
        self.assertEqual(mapping.match([conf], intl), [])
        self.assertEqual(len(mapping.match([champ], intl)), 1)
        q = us_market("Lille OSC", "Champions League Final Qualifiers", "")
        self.assertEqual(mapping.match([q], [intl_opt(
            "Lille", "Will Lille win the 2026-27 UEFA Champions League?")]), [])

    def test_team_names_are_not_bet_types(self):
        us = [us_market("West Ham United", "English Premier League Champion",
                        "Will West Ham United win the 2026-27 English Premier League?")]
        intl = [intl_opt("West Ham", "Will West Ham win the 2026-27 Premier League?",
                         "English Premier League Winner")]
        self.assertEqual(len(mapping.match(us, intl)), 1)

    def test_relative_price_agreement(self):
        self.assertFalse(mapping.prices_agree(0.04, 0.002))     # Lille: 20x apart
        self.assertFalse(mapping.prices_agree(0.06, 0.021))     # Pacers: ~3x
        self.assertTrue(mapping.prices_agree(0.021, 0.025))
        self.assertTrue(mapping.prices_agree(0.62, 0.66))
        self.assertFalse(mapping.prices_agree(0.50, 0.60))      # >8c

    def test_name_containment(self):
        self.assertEqual(mapping.name_similarity("Kyle Larson", "Kyle Larson"), 1.0)
        self.assertLess(mapping.name_similarity("Los Angeles Rams", "Rams"), 0.8)  # too short
        self.assertGreaterEqual(mapping.name_similarity("Larson", "Kyle Larson"), 0.8)
        self.assertLess(mapping.name_similarity("Kyle Busch", "Kyle Larson"), 0.8)


class PreviewCheckerTest(unittest.TestCase):
    def checker(self, behaviour, per_minute=20):
        from pmbot.broker import PreviewChecker

        class Err(Exception):
            def __init__(self, code):
                super().__init__(f"HTTP {code}: price outside allowed range")
                self.status_code = code

        class Orders:
            def preview(self, params):
                b = behaviour(params)
                if isinstance(b, int):
                    raise Err(b)
                return b

        class Client:
            orders = Orders()
        return PreviewChecker("k", "s", per_minute=per_minute, client=Client())

    def test_rejections_block_the_paper_order(self):
        c = self.checker(lambda p: 400)
        b = PaperBroker(100)
        b.checker = c
        self.assertIsNone(b.place("m", Order("BUY", 0.48, 10, True)))
        self.assertEqual(b.open_orders, {})
        self.assertEqual(c.stats["rejected"], 1)
        self.assertIn("price outside", c.last_reject)

    def test_rejected_state_in_a_200_answer(self):
        c = self.checker(lambda p: {"order": {"state": "ORDER_STATE_REJECTED"}})
        self.assertEqual(c.check("m", Order("BUY", 0.48, 10, True))[0], False)

    def test_outages_and_auth_errors_dont_stop_paper_trading(self):
        for code in (401, 429, 500):
            c = self.checker(lambda p, code=code: code)
            b = PaperBroker(100)
            b.checker = c
            self.assertIsNotNone(b.place("m", Order("BUY", 0.48, 10, True)))
            self.assertEqual(c.stats["errors"], 1)

    def test_rate_cap(self):
        c = self.checker(lambda p: {"order": {"state": "ORDER_STATE_NEW"}}, per_minute=2)
        for _ in range(3):
            c.check("m", Order("BUY", 0.48, 10, True))
        self.assertEqual((c.stats["accepted"], c.stats["unchecked"]), (2, 1))


class StrategyPluginTest(unittest.TestCase):
    def engine_with(self, markets):
        e = Engine.__new__(Engine)
        e.markets = {m.slug: m for m in markets}
        e.broker = PaperBroker(200)
        e.risk = RiskManager(RiskConfig(kill_file="/nonexistent/STOP"))
        return e

    def test_sports_game_day_window_and_band(self):
        from pmbot.strategies import SportsGameDay
        now = 1.8e9
        def game(slug, start, kind="moneyline"):
            return data.USMarket(slug, "A vs. B", "A", "", kind, "sports", start,
                                 start + 3 * 3600, 0.01, "MARKET_STATUS_OPEN", 0.49, 0.51)
        ms = [game("soon", now + 3600), game("next-week", now + 7 * 86400),
              game("started", now - 60), game("future", now + 3600, "futures")]
        e = self.engine_with(ms)
        views = {m.slug: view(fair=0.50) for m in ms}
        views["soon-longshot"] = view(fair=0.10, bid=0.09, ask=0.11)
        e.markets["soon-longshot"] = game("soon-longshot", now + 3600)
        got = SportsGameDay(StrategyConfig()).orders(e, views, now)
        self.assertEqual(sorted(k for k, v in got.items() if v), ["soon"])

    def test_one_strategy_per_market(self):
        from pmbot.strategies import Strategy
        class Grab(Strategy):
            def __init__(self, name, side):
                self.name, self.side = name, side
            def orders(self, eng, views, now):
                return {s: [Order(self.side, 0.4, 1, True)] for s in views}
        d = tempfile.mkdtemp()
        e = Engine(EngineConfig(mode="paper", out_dir=d, minutes=0), StrategyConfig(),
                   RiskManager(RiskConfig(kill_file=os.path.join(d, "STOP"))),
                   strategies=[Grab("first", "BUY"), Grab("second", "BUY")])
        v = view(); q = quote(0.49, 0.51)
        e._trade_all({"m": (v, q)}, time.time())
        tags = {o.slug: e.owner["m"] for o in e.broker.open_orders.values()}
        self.assertEqual(tags, {"m": "first"})
        self.assertEqual(len(e.broker.open_orders), 1)
        e.shutdown()


GAME = "aec-nba-mil-was-2099-01-01"


class FakeVenues:
    """Gateway, gamma and CLOB responses for one futures market."""

    def __init__(self):
        self.us_bid, self.us_ask, self.traded = 0.60, 0.61, 0.0
        self.ref_bid, self.ref_ask = 0.62, 0.63
        self.state, self.settlement, self.listed = "MARKET_STATE_OPEN", 0.84, True
        self.leader_trades: list[dict] = []
        # A US game market (long side Bucks, short side Wizards), listed when set.
        self.game, self.game_bid, self.game_ask, self.game_settlement = False, 0.36, 0.37, 0.0
        self.game_state = "MARKET_STATE_OPEN"
        self.form: dict = {}   # (wallet, period) -> (pnl, vol) on the leaderboard

    def get(self, base, path, params=None, use_cache=True, keep=None):
        px = lambda v: {"value": f"{v:.4f}", "currency": "USD"}
        if path == "/v1/leaderboard":
            f = self.form.get((params["user"], params["timePeriod"]))
            return [{"proxyWallet": params["user"], "pnl": f[0], "vol": f[1]}] if f else []
        if path == "/trades":
            return [t for t in self.leader_trades if t["proxyWallet"] == params["user"]][::-1]
        if path == "/v1/markets/brewers/settlement":
            return {"slug": "brewers", "settlement": self.settlement}
        if path == f"/v1/markets/{GAME}/settlement":
            return {"slug": GAME, "settlement": self.game_settlement}
        if path == f"/v1/markets/{GAME}/book":
            return {"marketData": {"marketSlug": GAME, "state": self.game_state,
                    "bids": [{"px": px(self.game_bid), "qty": "40"}],
                    "offers": [{"px": px(self.game_ask), "qty": "100"}], "stats": {}}}
        if path == "/v1/markets":
            if params["offset"] > 0 or not self.listed:
                return {"markets": []}
            game = [{"slug": GAME, "question": "Bucks vs Wizards", "marketType": "moneyline",
                     "gameStartTime": "2099-01-01T00:00:00Z", "endDate": "2099-01-15T00:00:00Z",
                     "status": "MARKET_STATUS_OPEN", "orderPriceMinTickSize": 0.01,
                     "marketSides": [{"description": "Bucks", "long": True},
                                     {"description": "Wizards", "long": False}]}] \
                if self.game else []
            return {"markets": game + [{
                "slug": "brewers", "question": "World Series Champion",
                "title": "Milwaukee Brewers", "marketType": "futures",
                "description": "Will Milwaukee Brewers win the 2026 MLB World Series?",
                "endDate": "2099-11-06T21:20:09Z", "orderPriceMinTickSize": 0.01,
                "status": "MARKET_STATUS_OPEN", "active": True, "closed": False,
                "bestBidQuote": px(self.us_bid), "bestAskQuote": px(self.us_ask)}]}
        if path == "/markets":
            return [] if params["offset"] > 0 else [{
                "question": "Will the Milwaukee Brewers win the 2026 World Series?",
                "groupItemTitle": "Milwaukee Brewers", "clobTokenIds": '["tokY", "tokN"]',
                "outcomes": '["Yes", "No"]', "endDate": "2099-11-01T00:00:00Z",
                "events": [{"title": "World Series Champion 2026"}], "bestBid": self.ref_bid,
                "bestAsk": self.ref_ask, "volume24hr": 5000, "active": True, "closed": False}]
        if path == "/v1/markets/brewers/book":
            return {"marketData": {"marketSlug": "brewers", "state": self.state,
                    "bids": [{"px": px(self.us_bid), "qty": "100"}],
                    "offers": [{"px": px(self.us_ask), "qty": "100"}],
                    "stats": {"lastTradePx": px(self.us_bid), "sharesTraded": str(self.traded)}}}
        if path == "/book":
            return {"bids": [{"price": str(self.ref_bid), "size": "500"}],
                    "asks": [{"price": str(self.ref_ask), "size": "500"}]}
        raise AssertionError(path)


class CopyTopTest(unittest.TestCase):
    LEADER = "0x" + "1" * 40

    def setUp(self):
        from pmbot.copy import CopyTop
        self.d = tempfile.mkdtemp()
        self.copy = CopyTop(StrategyConfig(order_usd=10), {self.LEADER: "primm"})
        self.e = Engine(EngineConfig(mode="paper", out_dir=self.d, minutes=0), StrategyConfig(),
                        RiskManager(RiskConfig(kill_file=os.path.join(self.d, "STOP"))),
                        strategies=[self.copy])
        self.v = self.e.client = FakeVenues()
        self.e.refresh_pairs()
        self.n = 0
        self.t0 = int(time.time()) - 100

    def tearDown(self):
        self.e.shutdown()

    def trade(self, side, price, size=100, asset="tokY", tx=None):
        self.n += 1
        self.v.leader_trades.append({"proxyWallet": self.LEADER, "side": side, "asset": asset,
                                     "price": price, "size": size, "timestamp": self.t0 + self.n,
                                     "title": "Brewers", "transactionHash": tx or f"0x{self.n}"})

    def test_copies_new_buys_only_at_or_near_the_leaders_price(self):
        self.trade("BUY", 0.40)                     # made before the bot started watching
        self.e.cycle()
        self.assertEqual(self.e.broker.fills, [])
        self.trade("BUY", 0.62)                     # US ask is 0.61: copy it
        self.e.cycle()
        f = self.e.broker.fills[-1]
        self.assertEqual((f.side, f.price, f.qty, f.maker, f.tag), ("BUY", 0.61, 16, False, "copytop"))
        self.assertGreater(f.fee, 0)                # taker fee paid
        self.assertEqual(self.e.owner["brewers"], "copytop")

    def test_does_not_chase_a_moved_price_or_copy_fills_twice(self):
        self.e.cycle()
        self.trade("BUY", 0.55)                     # US ask 0.61 > 0.56: wait, then give up
        self.e.cycle()
        self.assertEqual(self.e.broker.fills, [])
        self.copy.pending["brewers"]["at"] -= 1000
        self.e.cycle()
        self.assertEqual(self.copy.stats["expired_price_moved"], 1)
        self.trade("BUY", 0.62, tx="0xsame")
        self.trade("BUY", 0.62, tx="0xsame")        # same order, second fill
        self.e.cycle()
        self.assertEqual(len(self.e.broker.fills), 1)
        self.assertEqual(self.copy.stats["skip_repeat"], 1)

    def test_held_to_settlement_unless_sells_are_copied(self):
        self.e.cycle()
        self.trade("BUY", 0.62)
        self.e.cycle()
        self.trade("SELL", 0.61)                    # ignored by default
        self.e.cycle()
        self.assertEqual(self.e.held("brewers"), 16)

    def test_bigger_bets_get_bigger_copies_with_conviction_sizing(self):
        self.copy.conviction_sizing = True
        self.copy.sizes[self.LEADER] = deque([20.0] * 20)
        self.e.cycle()
        self.copy.sizes[self.LEADER] = deque([20.0] * 20)
        self.trade("BUY", 0.62, size=100)             # $62: 3x their usual $20
        self.e.cycle()
        self.assertEqual(self.e.broker.fills[-1].qty, 24)   # $15 at 0.61
        self.assertIn("conviction:2x+", self.copy.card.keys_for("brewers"))

    def test_leader_sell_closes_the_copy(self):
        self.copy.copy_sells = True
        self.e.cycle()
        self.trade("BUY", 0.62)
        self.e.cycle()
        self.trade("SELL", 0.61)                    # US bid 0.60 >= 0.61 - 1c
        self.e.cycle()
        self.assertNotIn("brewers", self.e.broker.positions)
        self.assertEqual(self.e.broker.fills[-1].side, "SELL")

    def test_one_copy_per_market_per_leader_within_ten_minutes(self):
        self.e.cycle()
        self.trade("BUY", 0.62)
        self.e.cycle()
        self.trade("BUY", 0.62)                     # a separate order, minutes later
        self.e.cycle()
        self.assertEqual(sum(f.side == "BUY" for f in self.e.broker.fills), 1)
        self.assertEqual(self.copy.stats["skip_recently_copied"], 1)

    def test_counters_survive_a_restart(self):
        from pmbot.copy import CopyTop
        self.e.cycle()
        self.trade("BUY", 0.62)
        self.e.cycle()
        self.e.save_state()
        again = CopyTop(StrategyConfig(), {self.LEADER: "primm"})
        e2 = Engine(EngineConfig(mode="paper", out_dir=self.d, minutes=0, resume=True),
                    StrategyConfig(), RiskManager(RiskConfig(kill_file=os.path.join(self.d, "STOP"))),
                    strategies=[again])
        self.assertEqual(again.stats["copied_buys"], 1)
        e2._events.close()

    def game_trade(self, side, price, outcome, slug="nba-mil-was-2099-01-01", size=100):
        self.n += 1
        self.v.leader_trades.append({"proxyWallet": self.LEADER, "side": side,
                                     "asset": f"tok-{outcome}", "price": price, "size": size,
                                     "timestamp": self.t0 + self.n, "title": "Bucks vs. Wizards",
                                     "slug": slug, "outcome": outcome,
                                     "transactionHash": f"0x{self.n}"})

    def test_copies_either_side_of_a_game_found_by_its_slug(self):
        self.v.game = True
        self.e.refresh_pairs()
        self.e.cycle()
        self.game_trade("BUY", 0.64, "Wizards")     # the US market's short side
        self.e.cycle()
        f = self.e.broker.fills[-1]
        # Wizards cost 1 - the Bucks bid (0.36); size is the Bucks bid's 40.
        self.assertEqual((f.slug, f.side, f.price, f.qty), (GAME + ":short", "BUY", 0.64, 15))
        self.assertEqual(self.copy.stats["mapped_short_side"], 1)
        self.assertIn("Wizards", self.e.labels[GAME + ":short"])
        self.game_trade("BUY", 0.37, "Bucks")       # other side of a game we hold: skip
        self.e.cycle()
        self.assertEqual(self.copy.stats["skip_holding_other_side"], 1)
        cash = self.e.broker.cash
        self.v.game_state = "MARKET_STATE_CLOSED"    # Bucks lost: Wizards pay 1
        self.e.cycle()
        self.assertNotIn(GAME + ":short", self.e.broker.positions)
        self.assertAlmostEqual(self.e.broker.cash, cash + 15)

    def test_counts_why_a_trade_was_not_copied(self):
        self.v.game = True
        self.e.refresh_pairs()
        self.e.cycle()
        self.game_trade("BUY", 0.5, "Over")          # listed game, outcome names differ
        self.game_trade("BUY", 0.5, "Yankees", slug="mlb-nyy-bos-2099-01-02")
        self.e.cycle()
        self.assertEqual(self.copy.stats["listed_side_unknown"], 1)
        self.assertEqual(self.copy.stats["missed_mlb"], 1)
        self.assertEqual(self.e.broker.fills, [])

    def test_totals_are_found_under_the_us_name(self):
        self.v.game = True
        self.e.refresh_pairs()
        m = self.e.markets[GAME]
        self.e.by_intl_slug["nba-mil-was-2099-01-01-229pt5"] = m   # as US names a total
        t = {"slug": "nba-mil-was-2099-01-01-total-229pt5", "outcome": "Bucks", "asset": "x"}
        self.assertEqual(self.e.us_for_trade(t), GAME)
        self.assertTrue(self.e.lists("nba-mil-was-2099-01-01-total-229pt5"))

    def test_each_copy_is_scored_against_its_wallet_and_patterns(self):
        self.v.game = True
        self.e.refresh_pairs()
        self.e.cycle()
        self.game_trade("BUY", 0.64, "Wizards")
        self.e.cycle()
        self.assertEqual(self.copy.copied_from(GAME + ":short"), "primm")
        self.v.game_state = "MARKET_STATE_CLOSED"    # Wizards win
        self.e.cycle()
        s = self.copy.card.summary(f"w:{self.LEADER}")
        self.assertEqual((s["settled"], s["won"], s["copies"], s["open_usd"]), (1, 1, 1, 0))
        self.assertAlmostEqual(s["pnl"], 15 - s["staked"], places=2)
        self.assertEqual(self.copy.card.summary("league:nba")["settled"], 1)
        self.assertEqual(self.copy.card.summary("kind:moneyline")["settled"], 1)
        self.assertEqual(self.copy.card.summary("timing:pre-game")["settled"], 1)
        self.assertEqual(self.copy.card.summary("price:30-70c")["settled"], 1)
        rows = self.copy.dashboard_rows()
        self.assertEqual([r["name"] for r in rows if r["kind"] == "leader"], ["primm"])
        self.assertIn("league:nba", [r["id"] for r in rows if r["kind"] == "pattern"])

    def test_a_wallet_that_falls_off_is_benched_but_its_exits_are_copied(self):
        self.copy.copy_sells = True
        self.e.cycle()
        self.trade("BUY", 0.62)                      # copied while in form
        self.e.cycle()
        self.v.form = {(self.LEADER, "WEEK"): (-900, 20000), (self.LEADER, "MONTH"): (-1500, 50000)}
        self.copy._next_form = 0
        self.e.cycle()
        self.assertEqual(self.copy.status[self.LEADER][0], "benched")
        self.assertIn("this week", self.copy.status[self.LEADER][1])
        self.assertEqual(self.copy.summary()["copytop_benched"], "primm")
        self.copy.recent.clear()
        self.trade("BUY", 0.62)                      # no new copies...
        self.e.cycle()
        self.assertEqual(self.copy.stats["skip_benched_wallet"], 1)
        self.trade("SELL", 0.61)                     # ...but their exit still closes ours
        self.e.cycle()
        self.assertNotIn("brewers", self.e.broker.positions)
        self.v.form = {(self.LEADER, "WEEK"): (400, 20000), (self.LEADER, "MONTH"): (-200, 50000)}
        self.copy._next_form = 0
        self.e.cycle()
        self.assertEqual(self.copy.status[self.LEADER][0], "copying")   # back in form

    def test_a_losing_week_alone_only_flags_cooling_off(self):
        self.v.form = {(self.LEADER, "WEEK"): (-300, 20000), (self.LEADER, "MONTH"): (2500, 60000)}
        self.e.cycle()
        self.assertEqual(self.copy.status[self.LEADER][0], "cooling")
        self.trade("BUY", 0.62)
        self.e.cycle()
        self.assertEqual(len(self.e.broker.fills), 1)

    def test_clearly_losing_copies_bench_a_wallet_a_few_losses_do_not(self):
        key = f"w:{self.LEADER}"
        self.copy.card.results[key] = [[-5.0, 5.0]] * 4 + [[4.0, 5.0]]
        self.copy._judge(self.e)
        self.assertEqual(self.copy.status[self.LEADER][0], "copying")   # 5 bets: too few
        self.copy.card.results[key] = [[-5.0, 5.0]] * 9 + [[4.0, 5.0]]
        self.copy._judge(self.e)
        self.assertEqual(self.copy.status[self.LEADER][0], "benched")
        self.assertIn("10 settled", self.copy.status[self.LEADER][1])

    def test_a_clearly_losing_pattern_is_skipped(self):
        self.v.game = True
        self.e.refresh_pairs()
        self.copy.card.results["league:nba"] = [[-5.0, 5.0]] * 13 + [[4.0, 5.0]] * 2
        self.copy._judge(self.e)
        self.assertIn("league:nba", self.copy.skipped)
        self.e.cycle()
        self.game_trade("BUY", 0.64, "Wizards")
        self.e.cycle()
        self.assertEqual(self.copy.stats["skip_losing_pattern"], 1)
        self.assertEqual(self.e.broker.fills, [])

    def test_scorecard_survives_a_restart(self):
        from pmbot.copy import CopyTop
        self.e.cycle()
        self.trade("BUY", 0.62)
        self.e.cycle()
        self.copy.status[self.LEADER] = ["cooling", "x"]
        self.e.save_state()
        again = CopyTop(StrategyConfig(), {self.LEADER: "primm"})
        e2 = Engine(EngineConfig(mode="paper", out_dir=self.d, minutes=0, resume=True),
                    StrategyConfig(), RiskManager(RiskConfig(kill_file=os.path.join(self.d, "STOP"))),
                    strategies=[again])
        self.assertEqual(again.copied_from("brewers"), "primm")
        self.assertEqual(again.status[self.LEADER], ["cooling", "x"])
        e2._events.close()

    def test_a_wallets_sell_only_closes_the_copies_of_that_wallet(self):
        self.copy.copy_sells = True
        other = "0x" + "2" * 40
        self.copy.leaders[other] = "theowalcott"
        self.e.cycle()
        self.trade("BUY", 0.62)                      # primm: 16 contracts
        self.e.cycle()
        self.n += 1
        self.v.leader_trades.append({"proxyWallet": other, "side": "BUY", "asset": "tokY",
                                     "price": 0.62, "size": 100, "timestamp": self.t0 + self.n,
                                     "title": "Brewers", "transactionHash": "0xother"})
        self.e.cycle()                               # theowalcott: 16 more
        self.assertEqual(self.e.held("brewers"), 32)
        self.trade("SELL", 0.61)                     # primm exits
        self.e.cycle()
        self.assertEqual(self.e.held("brewers"), 16)
        self.assertEqual(self.copy.copied_from("brewers"), "theowalcott")
        self.assertEqual(self.copy.card.summary(f"w:{self.LEADER}")["settled"], 1)
        self.assertEqual(self.copy.card.summary(f"w:{other}")["settled"], 0)
        self.assertIsNotNone(self.copy.summary()["copytop_lag_median_s"])

    def test_us_team_spellings_map_only_when_the_side_matches(self):
        from pmbot.engine import us_spellings
        self.assertIn("nba-gs-lal-2026-10-21", us_spellings("nba-gsw-lal-2026-10-21"))
        self.assertIn("nba-ind-no-2026-10-21-229pt5", us_spellings("nba-ind-nop-2026-10-21-total-229pt5"))
        self.assertEqual(us_spellings("wnba-phx-lv-2026-10-21"), ["wnba-phx-lv-2026-10-21"])
        self.v.game = True
        self.e.refresh_pairs()
        m = self.e.markets[GAME]
        self.e.by_intl_slug = {"nba-ind-no-2099-01-01": m}   # US spells New Orleans 'no'
        t = {"slug": "nba-ind-nop-2099-01-01", "outcome": "Wizards", "asset": "x"}
        self.assertEqual(self.e.us_for_trade(t), GAME + ":short")
        self.assertIsNone(self.e.us_for_trade({**t, "outcome": "Lakers"}))   # wrong side: no bet

    def test_tennis_matches_are_found_by_player_names(self):
        from pmbot.data import USMarket
        from pmbot.engine import players_key
        start = time.time() + 3600
        m = USMarket("aec-wta-annli-zeyson-2026-10-20", "Who will win", "", "", "moneyline",
                     "sports", start, start + 86400, 0.01, "MARKET_STATUS_OPEN", 0.4, 0.41,
                     "Ann Li", "Zeynep Sonmez")
        self.e.markets[m.slug] = m
        self.e.by_players = {players_key("wta", "Ann Li", "Zeynep Sonmez"): [m]}
        t = {"slug": "wta-annli-sonmez-2026-10-21", "title": "WTA Guangzhou: Ann Li vs. Zeynep Sonmez",
             "outcome": "Zeynep Sonmez", "asset": "x", "timestamp": time.time()}
        self.assertEqual(self.e.us_for_trade(t), m.slug + ":short")
        self.assertEqual(self.e.us_for_trade({**t, "outcome": "Ann Li"}), m.slug)
        self.assertIsNone(self.e.us_for_trade({**t, "slug": "wta-annli-sonmez-2026-10-21-sw1"}))
        self.assertIsNone(self.e.us_for_trade({**t, "timestamp": time.time() - 5 * 86400}))

    def test_stale_trades_are_not_copied_and_a_restart_resumes_the_history(self):
        from pmbot.copy import CopyTop
        self.e.cycle()
        self.n += 1
        self.v.leader_trades.append({"proxyWallet": self.LEADER, "side": "BUY", "asset": "tokY",
                                     "price": 0.62, "size": 100, "timestamp": self.t0 - 1000,
                                     "title": "Brewers", "transactionHash": "0xold"})
        self.trade("BUY", 0.62)
        self.e.cycle()
        self.assertEqual(self.copy.stats["skip_stale"], 1)
        self.assertEqual(len(self.e.broker.fills), 1)
        self.e.save_state()
        self.trade("BUY", 0.62, asset="tokY", tx="0xduring-restart")
        again = CopyTop(StrategyConfig(), {self.LEADER: "primm"})
        e2 = Engine(EngineConfig(mode="paper", out_dir=self.d, minutes=0, resume=True),
                    StrategyConfig(), RiskManager(RiskConfig(kill_file=os.path.join(self.d, "STOP"))),
                    strategies=[again])
        e2.client = self.v
        e2.refresh_pairs()
        again.recent.clear()
        e2.cycle()
        # The trade made during the restart is seen, not dropped as a baseline.
        self.assertEqual(again.stats["leader_trades"], self.copy.stats["leader_trades"] + 1)
        e2._events.close()

    def test_a_kill_file_halt_does_not_outlive_the_file(self):
        self.e.cycle()
        open(os.path.join(self.d, "STOP"), "w").close()
        self.e.cycle()
        self.assertTrue(self.e.risk.halted.startswith("kill file"))
        self.e.save_state()
        os.remove(os.path.join(self.d, "STOP"))       # restarted without the file
        e2 = Engine(EngineConfig(mode="paper", out_dir=self.d, minutes=0, resume=True),
                    StrategyConfig(), RiskManager(RiskConfig(kill_file=os.path.join(self.d, "STOP"))),
                    strategies=[])
        self.assertEqual(e2.risk.halted, "")
        e2._events.close()

    def test_one_wallet_cannot_take_more_than_its_cap(self):
        self.copy.max_wallet_usd = 15.0
        self.e.cycle()
        self.trade("BUY", 0.62)                      # $10 copy: 16 @ 0.61
        self.e.cycle()
        self.copy.recent.clear()
        self.trade("BUY", 0.62)                      # only ~$5 of the cap left
        self.e.cycle()
        buys = [f for f in self.e.broker.fills if f.side == "BUY"]
        self.assertEqual([f.qty for f in buys], [16, 8])
        self.copy.recent.clear()
        self.trade("BUY", 0.62)                      # cap used up
        self.e.cycle()
        self.assertEqual(self.copy.stats["skip_wallet_cap"], 1)

    def test_unmapped_trades_are_counted_not_copied(self):
        self.e.cycle()
        self.trade("BUY", 0.5, asset="not-on-us")
        self.e.cycle()
        self.assertEqual(self.copy.stats["not_on_polymarket_us"], 1)
        self.assertEqual(self.e.broker.fills, [])


class EngineTest(unittest.TestCase):
    def run_engine(self, mode):
        d = tempfile.mkdtemp()
        e = Engine(EngineConfig(mode=mode, out_dir=d, minutes=0),
                   StrategyConfig(), RiskManager(RiskConfig(kill_file=os.path.join(d, "STOP"))))
        e.client = FakeVenues()
        e.refresh_pairs()
        return e, d

    def test_paper_cycle_quotes_then_fills_on_trade_through(self):
        e, d = self.run_engine("paper")
        self.assertEqual([p.us_slug for p in e.pairs], ["brewers"])
        e.cycle()   # fair 0.625: bid at min(0.605 -> 0.60, best bid + 1c 0.61, ask-1c 0.60)
        orders = list(e.broker.open_orders.values())
        self.assertEqual([(o.side, o.price) for o in orders], [("BUY", 0.60)])
        time.sleep(0.01)
        e.client.us_bid, e.client.us_ask = 0.58, 0.59      # sold through our bid
        e.cycle()
        self.assertEqual(e.broker.positions["brewers"].qty, 8)
        # Now holding: an ask at >= fair + 2c is posted.
        self.assertTrue(any(o.side == "SELL" and o.price >= 0.645
                            for o in e.broker.open_orders.values()))
        e.shutdown()
        with open(os.path.join(d, "report.md")) as f:
            self.assertIn("Equity", f.read())

    def test_account_survives_restart_and_feeds_the_dashboard(self):
        e, d = self.run_engine("paper")
        e.cycle()
        time.sleep(0.01)
        e.client.us_bid, e.client.us_ask = 0.58, 0.59
        e.cycle()
        e.shutdown()
        cash, qty = e.broker.cash, e.broker.positions["brewers"].qty
        e2 = Engine(EngineConfig(mode="paper", out_dir=d, minutes=0, resume=True),
                    StrategyConfig(), RiskManager(RiskConfig(kill_file=os.path.join(d, "STOP"))))
        self.assertAlmostEqual(e2.broker.cash, cash)
        self.assertEqual(e2.broker.positions["brewers"].qty, qty)
        self.assertEqual(e2.owner, {"brewers": "fairvalue"})
        self.assertTrue(e2.equity_hist)
        with open(os.path.join(d, "paper.json")) as f:
            rows = json.load(f)
        kinds = {r["kind"] for r in rows}
        self.assertTrue({"summary", "equity", "position", "fill"} <= kinds)
        summary = next(r for r in rows if r["kind"] == "summary")
        self.assertEqual(summary["start_cash"], 200)
        self.assertEqual(summary["fills"], 1)
        fill = next(r for r in rows if r["kind"] == "fill")
        self.assertEqual((fill["liquidity"], fill["strategy"]), ("maker", "fairvalue"))
        e2._events.close()

    def test_settles_only_closed_markets(self):
        e, d = self.run_engine("paper")
        e.cycle()
        time.sleep(0.01)
        e.client.us_bid, e.client.us_ask = 0.58, 0.59
        e.cycle()
        self.assertIn("brewers", e.broker.positions)
        e.cycle()                                  # open market: daily mark 0.84 ignored
        self.assertIn("brewers", e.broker.positions)
        e.client.state, e.client.settlement = "MARKET_STATE_EXPIRED", 1.0
        cash = e.broker.cash
        e.cycle()
        self.assertNotIn("brewers", e.broker.positions)
        self.assertAlmostEqual(e.broker.cash, cash + 8)
        self.assertEqual(e.broker.fills[-1].side, "SETTLE")
        self.assertGreater(e.broker.realized, 0)
        e.shutdown()

    def test_scan_logs_opportunities_without_trading(self):
        e, d = self.run_engine("scan")
        e.client.us_bid, e.client.us_ask = 0.55, 0.56      # 6.5c below fair
        e.cycle()
        self.assertEqual(e.broker.open_orders, {})
        self.assertEqual(e.stats.buy_opps, 1)
        e.shutdown()
        with open(os.path.join(d, "events.jsonl")) as f:
            self.assertIn('"opportunity"', f.read())

    def test_pair_dropped_when_live_prices_disagree(self):
        e, d = self.run_engine("paper")
        e.client.ref_bid, e.client.ref_ask = 0.80, 0.81
        e.cycle()
        self.assertEqual(e.pairs, [])
        self.assertEqual(e.broker.open_orders, {})
        e.shutdown()


if __name__ == "__main__":
    unittest.main()


try:
    import httpx
    import polymarket_us  # noqa: F401
except ImportError:  # the live broker is optional
    httpx = None


@unittest.skipIf(httpx is None, "polymarket-us not installed")
class LiveBrokerTest(unittest.TestCase):
    """Drives the real SDK against a fake exchange to check exactly what
    the bot would send: paths, bodies, signing headers."""

    def setUp(self):
        import base64
        from nacl.signing import SigningKey
        from pmbot.broker import LiveBroker
        self.requests = []
        self.open = [{"id": "manual-1", "marketSlug": "brewers", "side": "ORDER_SIDE_BUY",
                      "price": {"value": "0.40", "currency": "USD"}, "leavesQuantity": 5}]
        self.pos = {"brewers": {"netPosition": "8", "cost": {"value": "4.80", "currency": "USD"}}}
        self.execs = []
        self.reject = False

        def handler(req):
            body = json.loads(req.content) if req.content else None
            self.requests.append((req.method, req.url.path, body, dict(req.headers)))
            p = req.url.path
            if p == "/v1/account/balances":
                return httpx.Response(200, json={"balances": [
                    {"currentBalance": 200.0, "buyingPower": 150.0, "currency": "USD"}]})
            if p == "/v1/portfolio/positions":
                return httpx.Response(200, json={"positions": self.pos, "eof": True})
            if p == "/v1/orders/open":
                return httpx.Response(200, json={"orders": self.open})
            if p == "/v1/orders":
                if self.reject:
                    return httpx.Response(400, json={"message": "market suspended"})
                return httpx.Response(200, json={"id": "bot-1", "executions": self.execs})
            if p == "/v1/order/preview":
                return httpx.Response(200, json={"order": {"state": "ORDER_STATE_NEW"}})
            if p.endswith("/cancel"):
                return httpx.Response(200, text="")
            return httpx.Response(404, json={"message": p})

        seed = base64.b64encode(bytes(SigningKey.generate())).decode()
        self.dir = tempfile.mkdtemp()
        self.b = LiveBroker("key-id", seed, os.path.join(self.dir, "orders.json"))
        self.b.client._http = httpx.Client(transport=httpx.MockTransport(handler))

    def test_sync_reads_cash_positions_and_ignores_manual_orders(self):
        self.b.sync()
        self.assertEqual(self.b.cash, 150.0)          # buyingPower: what we can spend now
        self.assertEqual(self.b.account_cash, 150.0)  # the account's own cash (no open orders)
        self.assertEqual(self.b.balance_info["buyingPower"], 150.0)
        self.assertEqual(self.b.positions["brewers"].qty, 8)
        self.assertEqual(self.b.open_orders, {})      # manual-1 isn't ours
        method, path, _, headers = self.requests[0]
        for h in ("x-pm-access-key", "x-pm-timestamp", "x-pm-signature"):
            self.assertIn(h, headers)

    def test_post_only_quote_body_and_own_order_tracking(self):
        oid = self.b.place("brewers", Order("BUY", 0.6, 8, True))
        self.assertEqual(oid, "bot-1")
        _, path, body, _ = self.requests[-1]
        self.assertEqual(path, "/v1/orders")
        self.assertEqual(body, {
            "marketSlug": "brewers", "intent": "ORDER_INTENT_BUY_LONG",
            "type": "ORDER_TYPE_LIMIT", "price": {"value": "0.600", "currency": "USD"},
            "quantity": 8, "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
            "participateDontInitiate": True,
            "manualOrderIndicator": "MANUAL_ORDER_INDICATOR_AUTOMATIC"})
        # After a restart the bot still knows bot-1 is its own.
        self.open.append({"id": "bot-1", "marketSlug": "brewers", "side": "ORDER_SIDE_BUY",
                          "price": {"value": "0.600", "currency": "USD"}, "leavesQuantity": 8})
        from pmbot.broker import LiveBroker
        again = LiveBroker("key-id", self.b.client.secret_key, os.path.join(self.dir, "orders.json"))
        again.client._http = self.b.client._http
        again.sync()
        self.assertEqual(list(again.open_orders), ["bot-1"])
        again.cancel_all()
        cancels = [p for m, p, _, _ in self.requests if p.endswith("/cancel")]
        self.assertEqual(cancels, ["/v1/order/bot-1/cancel"])   # never manual-1

    def test_order_preview_through_the_sdk(self):
        from pmbot.broker import PreviewChecker
        c = PreviewChecker("key-id", "", client=self.b.client)
        ok, why = c.check("brewers", Order("BUY", 0.6, 8, True))
        _, path, body, headers = self.requests[-1]
        self.assertEqual(path, "/v1/order/preview")
        self.assertEqual(body["request"]["participateDontInitiate"], True)
        self.assertEqual(body["request"]["marketSlug"], "brewers")
        self.assertIn("x-pm-signature", headers)
        self.assertEqual((ok, c.stats["accepted"]), (True, 1))

    def test_spend_buying_power_and_value_the_account_without_bonus(self):
        from pmbot.broker import own_cash, spendable
        row = {"currentBalance": 41.0, "buyingPower": 33.5, "displayedCash": 0.0,
               "displayedBonus": 10.0}
        self.assertEqual(spendable(row), 33.5)        # what the exchange lets us spend
        self.assertEqual(own_cash(row), 33.5)         # buying power + open orders, as the app shows
        self.assertEqual(own_cash({"currentBalance": 41.0, "displayedBonus": 10.0}), 31.0)
        self.assertEqual(spendable({"currentBalance": 41.0, "displayedBonus": 10.0}), 31.0)
        self.assertEqual(spendable({"currentBalance": 200.0}), 200.0)

    def test_a_short_side_take_is_booked_from_its_executions(self):
        self.execs = [{"lastShares": "10", "lastPx": {"value": "0.37", "currency": "USD"},
                       "commissionNotionalCollected": {"value": "0.17", "currency": "USD"}},
                      {"lastShares": "5", "lastPx": {"value": "0.36", "currency": "USD"},
                       "commissionNotionalCollected": {"value": "0.08", "currency": "USD"}}]
        self.b.place("aec-nba-mil-was-2026-10-21:short", Order("BUY", 0.65, 15, False, tag="copytop"))
        body = self.requests[-1][2]
        self.assertEqual((body["marketSlug"], body["intent"], body["price"]["value"],
                          body["synchronousExecution"]),
                         ("aec-nba-mil-was-2026-10-21", "ORDER_INTENT_BUY_SHORT", "0.350", True))
        f = self.b.fills[-1]
        self.assertEqual((f.side, f.qty, f.tag, f.fee), ("BUY", 15, "copytop", 0.25))
        self.assertAlmostEqual(f.price, (10 * 0.63 + 5 * 0.64) / 15, places=4)   # Wizards' price
        self.assertEqual(self.b.positions["aec-nba-mil-was-2026-10-21:short"].qty, 15)

    def test_a_settled_position_is_paid_once_and_our_own_sale_is_not_a_settlement(self):
        self.b.sync()
        self.pos = {}                                  # the exchange settled it
        self.b.sync()
        self.assertEqual(list(self.b.vanished), ["brewers"])
        self.b.settle("brewers", 1.0, "copytop")
        f = self.b.fills[-1]
        self.assertEqual((f.side, f.qty, f.price, f.pnl), ("SETTLE", 8, 1.0, 3.2))
        self.assertEqual(self.b.vanished, {})
        # Sold by the bot: gone from the exchange too, but not "vanished".
        self.pos = {"brewers": {"netPosition": "8", "cost": {"value": "4.80", "currency": "USD"}}}
        self.b.sync()
        self.execs = [{"lastShares": "8", "lastPx": {"value": "0.70", "currency": "USD"},
                       "commissionNotionalCollected": {"value": "0.12", "currency": "USD"}}]
        self.b.place("brewers", Order("SELL", 0.69, 8, False))
        self.assertAlmostEqual(self.b.fills[-1].pnl, 0.7 * 8 - 0.12 - 4.80, places=4)
        self.pos = {}
        self.b.sync()
        self.assertEqual(self.b.vanished, {})
        st = self.b.to_state()
        from pmbot.broker import LiveBroker
        again = LiveBroker("key-id", self.b.client.secret_key, os.path.join(self.dir, "o.json"),
                           client=self.b.client)
        again.load_state(st)
        self.assertEqual(len(again.fills), len(self.b.fills))

    def test_a_hand_sale_is_split_and_a_lagging_positions_list_is_not_a_sale(self):
        self.pos = {}
        self.b.sync()
        self.execs = [{"lastShares": "2", "lastPx": {"value": "0.44", "currency": "USD"},
                       "commissionNotionalCollected": {"value": "0.02", "currency": "USD"}}]
        self.b.place("lyon", Order("BUY", 0.45, 2, False, tag="copytop"))
        self.b.sync()                                  # the list hasn't caught up yet
        self.assertEqual((self.b.positions["lyon"].qty, self.b.vanished), (2, {}))
        # The owner buys 43 more by hand, then sells all 45.
        self.pos = {"lyon": {"netPosition": "45", "cost": {"value": "17.95", "currency": "USD"}}}
        self.b.sync()
        self.b._traded["lyon"] -= 600
        self.pos = {}
        self.b.sync()
        self.b.sold_outside("lyon", 0.395, "copytop")
        sells = [(f.tag, f.qty, round(f.pnl, 2)) for f in self.b.fills if f.side == "SELL"]
        self.assertEqual(sells, [("copytop", 2, round(2 * 0.395 - 0.90, 2)),
                                 ("", 43, round(43 * 0.395 - (17.95 - 0.90), 2))])
        self.assertEqual(self.b.own, {})
        # Tracking survives a restart.
        self.b.place("lyon", Order("BUY", 0.45, 2, False, tag="copytop"))
        from pmbot.broker import LiveBroker
        again = LiveBroker("key-id", self.b.client.secret_key, os.path.join(self.dir, "o.json"),
                           client=self.b.client)
        again.load_state(self.b.to_state())
        self.assertEqual(again.own["lyon"].qty, 2)

    def test_a_rejected_order_books_nothing_and_does_not_raise(self):
        self.reject = True
        self.assertIsNone(self.b.place("brewers", Order("BUY", 0.6, 3, False, tag="copytop")))
        self.assertEqual(self.b.fills, [])

    def test_a_live_settlement_is_credited_to_the_strategy_that_bought(self):
        from pmbot.copy import CopyTop
        copy = CopyTop(StrategyConfig(), {})
        d = tempfile.mkdtemp()
        e = Engine(EngineConfig(mode="live", out_dir=d, minutes=0), StrategyConfig(),
                   RiskManager(RiskConfig(kill_file=os.path.join(d, "STOP"))), self.b,
                   strategies=[copy])
        e.client = v = FakeVenues()
        e.refresh_pairs()
        self.b.sync()
        self.execs = [{"lastShares": "3", "lastPx": {"value": "0.60", "currency": "USD"},
                       "commissionNotionalCollected": {"value": "0.05", "currency": "USD"}}]
        copy._placing["brewers"] = ["w:0xabc", "league:mlb"]
        n = len(self.b.fills)
        self.b.place("brewers", Order("BUY", 0.61, 3, False, tag="copytop"))
        e.owner["brewers"] = "copytop"
        copy.on_fills(e, self.b.fills[n:])
        self.b._traded["brewers"] -= 600                # bought a while ago
        self.pos = {}                                  # the exchange settled it
        v.state = "MARKET_STATE_CLOSED"
        v.settlement = 1.0
        e.cycle()
        settle = [f for f in self.b.fills if f.side == "SETTLE"]
        # The bot's 3 are copytop's; the 8 already held by hand are the owner's.
        self.assertEqual([(f.slug, f.tag, f.qty) for f in settle],
                         [("brewers", "copytop", 3), ("brewers", "", 8)])
        self.assertAlmostEqual(settle[0].pnl, 3 - (3 * 0.6 + 0.05), places=4)
        self.assertAlmostEqual(settle[1].pnl, 8 - 4.80, places=4)
        self.assertEqual(copy.card.summary("w:0xabc")["settled"], 1)
        e.shutdown()

    def test_a_position_sold_by_hand_is_booked_as_a_sale_not_a_settlement(self):
        d = tempfile.mkdtemp()
        e = Engine(EngineConfig(mode="live", out_dir=d, minutes=0), StrategyConfig(),
                   RiskManager(RiskConfig(kill_file=os.path.join(d, "STOP"))), self.b, strategies=[])
        e.client = v = FakeVenues()
        e.refresh_pairs()
        self.b.sync()
        self.pos = {}                                  # sold in the app; market still open
        e.cycle()
        f = self.b.fills[-1]
        self.assertEqual((f.slug, f.side, f.qty), ("brewers", "SELL", 8))
        self.assertEqual(self.b.vanished, {})
        v.state, v.settlement = "MARKET_STATE_CLOSED", 1.0
        e.cycle()                                      # no payout booked later
        self.assertFalse(any(x.side == "SETTLE" for x in self.b.fills))
        e.shutdown()

    def test_take_is_ioc_and_sell_closes_long(self):
        self.b.place("brewers", Order("SELL", 0.7, 3, False))
        body = self.requests[-1][2]
        self.assertEqual((body["intent"], body["tif"], body["participateDontInitiate"]),
                         ("ORDER_INTENT_SELL_LONG", "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL", False))
