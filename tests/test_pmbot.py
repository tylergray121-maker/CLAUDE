import json
import os
import tempfile
import time
import unittest

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
        pairs = mapping.match_games([m], {fx["intl"]["slug"]: fx["intl"]})
        self.assertEqual(len(pairs), 1)
        tokens = json.loads(fx["intl"]["clobTokenIds"])
        self.assertEqual(pairs[0].intl_token, tokens[0])        # Bucks, not Wizards
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


class FakeVenues:
    """Gateway, gamma and CLOB responses for one futures market."""

    def __init__(self):
        self.us_bid, self.us_ask, self.traded = 0.60, 0.61, 0.0
        self.ref_bid, self.ref_ask = 0.62, 0.63
        self.state, self.settlement, self.listed = "MARKET_STATE_OPEN", 0.84, True

    def get(self, base, path, params=None, use_cache=True, keep=None):
        px = lambda v: {"value": f"{v:.4f}", "currency": "USD"}
        if path == "/v1/markets/brewers/settlement":
            return {"slug": "brewers", "settlement": self.settlement}
        if path == "/v1/markets":
            if params["offset"] > 0 or not self.listed:
                return {"markets": []}
            return {"markets": [{
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

        def handler(req):
            body = json.loads(req.content) if req.content else None
            self.requests.append((req.method, req.url.path, body, dict(req.headers)))
            p = req.url.path
            if p == "/v1/account/balances":
                return httpx.Response(200, json={"balances": [
                    {"currentBalance": 200.0, "buyingPower": 150.0, "currency": "USD"}]})
            if p == "/v1/portfolio/positions":
                return httpx.Response(200, json={"positions": {"brewers": {
                    "netPosition": "8", "cost": {"value": "4.80", "currency": "USD"}}},
                    "eof": True})
            if p == "/v1/orders/open":
                return httpx.Response(200, json={"orders": self.open})
            if p == "/v1/orders":
                return httpx.Response(200, json={"id": "bot-1", "executions": []})
            if p.endswith("/cancel"):
                return httpx.Response(200, text="")
            return httpx.Response(404, json={"message": p})

        seed = base64.b64encode(bytes(SigningKey.generate())).decode()
        self.dir = tempfile.mkdtemp()
        self.b = LiveBroker("key-id", seed, os.path.join(self.dir, "orders.json"))
        self.b.client._http = httpx.Client(transport=httpx.MockTransport(handler))

    def test_sync_reads_cash_positions_and_ignores_manual_orders(self):
        self.b.sync()
        self.assertEqual(self.b.cash, 200.0)          # currentBalance, not buyingPower
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

    def test_take_is_ioc_and_sell_closes_long(self):
        self.b.place("brewers", Order("SELL", 0.7, 3, False))
        body = self.requests[-1][2]
        self.assertEqual((body["intent"], body["tif"], body["participateDontInitiate"]),
                         ("ORDER_INTENT_SELL_LONG", "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL", False))
