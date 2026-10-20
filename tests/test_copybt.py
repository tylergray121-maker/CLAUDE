import os
import tempfile
import unittest
from unittest import mock

from copybt import cli, data
from copybt.models import Market, Trade
from copybt.sim import SimConfig, profile, simulate

DAY = 86400
T0 = 1_700_000_000
COND = "0xc1"
YES, NO = "111", "222"


def trade(ts, side, price, size, asset=YES, cond=COND, title="Will X happen?"):
    return Trade(ts=ts, asset=asset, condition_id=cond, side=side, price=price,
                 size=size, title=title, tx=f"0x{ts}{side}")


def resolved(winner=YES, ts=T0 + 5 * DAY, cond=COND):
    return {cond: Market(cond, True, ts, {YES: 1.0 if winner == YES else 0.0,
                                          NO: 0.0 if winner == YES else 1.0})}


NOFRICTION = SimConfig(slippage=0.0, base_pct=0.10)


class SimulateTest(unittest.TestCase):
    def run_sim(self, trades, markets, cfg=NOFRICTION, end=T0 + 10 * DAY):
        return simulate(trades, markets, cfg, T0, end, T0 + 3 * DAY)

    def test_winning_buy_pays_out_at_resolution(self):
        # 10% of $200 = $20 at 50c -> 40 shares -> $40 on resolution.
        r = self.run_sim([trade(T0 + 60, "BUY", 0.5, 100)], resolved(YES))
        self.assertAlmostEqual(r.final_equity, 220.0)
        self.assertEqual(r.buys_copied, 1)
        self.assertEqual(r.win_rate, 1.0)

    def test_losing_buy_goes_to_zero(self):
        r = self.run_sim([trade(T0 + 60, "BUY", 0.5, 100)], resolved(NO))
        self.assertAlmostEqual(r.final_equity, 180.0)
        self.assertAlmostEqual(r.max_drawdown_pct, 10.0)
        self.assertEqual(r.win_rate, 0.0)

    def test_slippage_reduces_shares(self):
        cfg = SimConfig(slippage=0.05, base_pct=0.10)
        r = self.run_sim([trade(T0 + 60, "BUY", 0.5, 100)], resolved(YES), cfg)
        self.assertAlmostEqual(r.final_equity, 180 + 20 / 0.55)

    def test_proportional_partial_sell(self):
        trades = [trade(T0 + 60, "BUY", 0.5, 100),
                  trade(T0 + 120, "SELL", 0.8, 50)]  # leader sells half
        r = self.run_sim(trades, resolved(YES))
        # 40 shares: 20 sold at 0.8 = 16, 20 redeemed at 1.0 = 20.
        self.assertAlmostEqual(r.final_equity, 180 + 16 + 20)
        self.assertEqual(r.sells_copied, 1)

    def test_sell_of_position_opened_before_window_is_ignored(self):
        r = self.run_sim([trade(T0 + 60, "SELL", 0.8, 50)], resolved(YES))
        self.assertAlmostEqual(r.final_equity, 200.0)
        self.assertEqual(r.sells_copied, 0)

    def test_conviction_scales_size_without_lookahead(self):
        # First buy is sized 1x (no history); second is 3x larger -> clipped 3x.
        c1, c2 = "0xa", "0xb"
        trades = [trade(T0 + 60, "BUY", 0.5, 100, asset="a", cond=c1),
                  trade(T0 + 120, "BUY", 0.5, 300, asset="b", cond=c2)]
        markets = {c1: Market(c1, True, T0 + DAY, {"a": 1.0}),
                   c2: Market(c2, True, T0 + DAY, {"b": 1.0})}
        cfg = SimConfig(slippage=0.0, base_pct=0.05, max_trade_pct=1.0)
        r = self.run_sim(trades, markets, cfg)
        # $10 -> 20 shares; then 0.05*200*3 = $30 -> 60 shares.
        self.assertAlmostEqual(r.final_equity, 200 - 10 - 30 + 20 + 60)

    def test_caps_and_min_order(self):
        cfg = SimConfig(slippage=0.0, base_pct=0.5, max_trade_pct=0.2,
                        max_market_pct=0.3)
        trades = [trade(T0 + 60, "BUY", 0.5, 100),
                  trade(T0 + 61, "BUY", 0.5, 100),
                  trade(T0 + 62, "BUY", 0.5, 100)]
        r = self.run_sim(trades, resolved(YES), cfg)
        # $40 (trade cap), then $20 (market cap 60), then nothing left.
        self.assertEqual(r.buys_copied, 2)
        self.assertEqual(r.skipped, {"market_cap": 1})
        self.assertAlmostEqual(r.final_equity, 140 + 120)

    def test_skips_buys_with_nothing_left_to_win(self):
        r = self.run_sim([trade(T0 + 60, "BUY", 0.995, 100)], resolved(YES))
        self.assertEqual(r.skipped, {"price_too_high": 1})

    def test_trades_after_resolution_ignored(self):
        trades = [trade(T0 + 60, "BUY", 0.5, 100),
                  trade(T0 + 6 * DAY, "BUY", 0.5, 100)]
        r = self.run_sim(trades, resolved(YES))
        self.assertEqual(r.buys_copied, 1)

    def test_open_position_marked_at_current_price(self):
        markets = {COND: Market(COND, False, None, {YES: 0.75, NO: 0.25})}
        r = self.run_sim([trade(T0 + 60, "BUY", 0.5, 100)], markets)
        self.assertAlmostEqual(r.final_equity, 180 + 40 * 0.75)

    def test_train_test_split(self):
        c1, c2 = "0xa", "0xb"
        trades = [trade(T0 + 60, "BUY", 0.5, 100, asset="a", cond=c1),
                  trade(T0 + 4 * DAY, "BUY", 0.5, 100, asset="b", cond=c2)]
        markets = {c1: Market(c1, True, T0 + DAY, {"a": 1.0}),
                   c2: Market(c2, True, T0 + 5 * DAY, {"b": 0.0})}
        r = self.run_sim(trades, markets)
        self.assertAlmostEqual(r.train_return_pct, 10.0)
        self.assertAlmostEqual(r.test_return_pct, -10.0)

    def test_delay_uses_worse_of_leader_and_delayed_price(self):
        cfg = SimConfig(slippage=0.0, base_pct=0.10, delay_seconds=5)
        r = simulate([trade(T0 + 60, "BUY", 0.5, 100)], resolved(YES), cfg,
                     T0, T0 + 10 * DAY, T0 + 3 * DAY, lambda a, t: 0.8)
        self.assertAlmostEqual(r.final_equity, 180 + 20 / 0.8)


class ProfileTest(unittest.TestCase):
    def test_flags(self):
        ts = [trade(T0 + i, "BUY", 0.97, 10,
                    title="Bitcoin Up or Down - Oct 20, 3:15PM-3:30PM ET")
              for i in range(2000)]
        p = profile(ts, T0, T0 + 10 * DAY)
        self.assertEqual(set(p.flags),
                         {"high_frequency", "short_duration_markets", "bonder"})


class ParserTest(unittest.TestCase):
    def test_parse_trade(self):
        t = data._parse_trade({"side": "BUY", "price": "0.42", "size": 10,
                               "timestamp": 1700000000, "asset": "9",
                               "conditionId": "0xABC"})
        self.assertEqual((t.condition_id, t.price, t.size), ("0xabc", 0.42, 10.0))
        self.assertIsNone(data._parse_trade({"side": "MERGE"}))
        self.assertIsNone(data._parse_trade({"side": "BUY", "price": 1.0, "size": 1,
                                             "timestamp": 1, "asset": "x",
                                             "conditionId": "c"}))

    def test_parse_ts(self):
        self.assertEqual(data._parse_ts("2024-11-06 12:00:00+00"), 1730894400)
        self.assertEqual(data._parse_ts("2024-11-06T12:00:00Z"), 1730894400)
        self.assertEqual(data._parse_ts(1730894400000), 1730894400)

    def test_gamma_market(self):
        m = data._market_from_gamma({
            "conditionId": "0xC", "closed": True, "clobTokenIds": '["1","2"]',
            "outcomePrices": '["0","1"]', "closedTime": "2024-11-06 12:00:00+00"})
        self.assertTrue(m.resolved)
        self.assertEqual(m.prices, {"1": 0.0, "2": 1.0})
        self.assertEqual(m.resolve_ts, 1730894400)
        live = data._market_from_gamma({
            "conditionId": "0xD", "closed": False, "clobTokenIds": '["1","2"]',
            "outcomePrices": '["0.4","0.6"]'})
        self.assertFalse(live.resolved)

    def test_clob_market(self):
        m = data._market_from_clob({
            "condition_id": "0xE", "closed": True, "end_date_iso": "2024-11-06T12:00:00Z",
            "tokens": [{"token_id": "1", "winner": False, "price": 0},
                       {"token_id": "2", "winner": True, "price": 1}]})
        self.assertTrue(m.resolved)
        self.assertEqual(m.prices, {"1": 0.0, "2": 1.0})


class PagingTest(unittest.TestCase):
    def test_reanchors_past_offset_cap_without_duplicates(self):
        rows = [{"side": "BUY", "price": 0.5, "size": 1, "timestamp": T0 + i // 3,
                 "asset": "a", "conditionId": "c", "transactionHash": f"0x{i}"}
                for i in range(1234)]  # three trades per second

        class Paged:
            def get(self, base, path, params=None, use_cache=True):
                if params["offset"] > 200:
                    raise data.HTTPError(400, path)
                hits = sorted((r for r in rows
                               if params["start"] <= r["timestamp"] <= params["end"]),
                              key=lambda r: -r["timestamp"])
                return hits[params["offset"]:params["offset"] + params["limit"]]

        out, truncated = data.fetch_trades(Paged(), "0xw", T0, T0 + 10_000,
                                           page_size=100, max_offset=10_000)
        self.assertFalse(truncated)
        self.assertEqual(len(out), 1234)
        self.assertEqual(len({t.tx for t in out}), 1234)
        self.assertEqual([t.ts for t in out], sorted(t.ts for t in out))


class FakeClient:
    """Serves canned API responses keyed on path."""

    requests_made = 0

    def __init__(self, now):
        self.now = now

    def get(self, base, path, params=None, use_cache=True):
        params = dict(params) if isinstance(params, dict) else params
        if path == "/v1/leaderboard":
            if params["offset"] > 0 or params["category"] != "OVERALL":
                return []
            return [{"rank": "1", "proxyWallet": "0x" + "a" * 40, "userName": "good"},
                    {"rank": "2", "proxyWallet": "0x" + "b" * 40, "userName": "bad"}]
        if path == "/activity":
            if params["offset"] > 0:
                return []
            win = params["user"] == "0x" + "a" * 40
            rows = []
            for i in range(20):
                ts = self.now - (80 - i * 3) * DAY
                rows.append({"side": "BUY", "price": 0.5, "size": 100, "timestamp": ts,
                             "asset": f"{'w' if win else 'l'}{i}",
                             "conditionId": f"0xc{i}", "title": "Will X?",
                             "transactionHash": f"0x{i}"})
            return rows[::-1]
        if path == "/markets":
            out = []
            for k, v in params:
                if k == "condition_ids":
                    i = int(v[3:])
                    out.append({"conditionId": v, "closed": True,
                                "clobTokenIds": f'["w{i}","l{i}"]',
                                "outcomePrices": '["1","0"]',
                                "closedTime": self.now - (79 - i * 3) * DAY})
            return out
        raise AssertionError(f"unexpected request {path}")


class EndToEndTest(unittest.TestCase):
    def test_cli_ranks_the_profitable_wallet(self):
        import time
        now = int(time.time()) // 3600 * 3600
        with tempfile.TemporaryDirectory() as out, \
                mock.patch.object(cli, "Client", return_value=FakeClient(now)):
            rc = cli.main(["--days", "90", "--out-dir", out, "--min-buys", "5",
                           "--cache-dir", ""])
            self.assertEqual(rc, 0)
            with open(os.path.join(out, "report.md")) as f:
                report = f.read()
            self.assertIn("**0x" + "a" * 40 + "**", report)
            with open(os.path.join(out, "ranking.csv")) as f:
                ranking = f.read().splitlines()
            self.assertEqual(len(ranking), 3)
            self.assertTrue(ranking[1].startswith("0x" + "a" * 40))


if __name__ == "__main__":
    unittest.main()
