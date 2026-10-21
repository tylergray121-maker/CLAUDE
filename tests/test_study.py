import json
import os
import unittest

from study import collect, features
from study.__main__ import render

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def theo4():
    with open(os.path.join(FIX, "study_theo4.json")) as f:
        fx = json.load(f)
    data = {"wallet": fx["lb"]["proxyWallet"], "closed": fx["closed"], "open": [],
            "trades_all": fx["trades_all"], "trades_taker": fx["trades_taker"],
            "activity": {"REWARD": fx["reward"], "MERGE": fx["merge"]}}
    return data, fx["lb"]


class ProfileTest(unittest.TestCase):
    def test_real_top_wallet(self):
        d, lb = theo4()
        p = features.profile(d, lb)
        self.assertEqual(p["name"], "Theo4")
        self.assertGreater(p["realized_pnl"], 8e6)
        self.assertEqual(p["main_category"], "politics")
        self.assertGreater(p["top1_share"], 0.3)
        self.assertGreater(p["rewards_usd"], 0)
        # 3 of the 5 newest fills (the Harris popular-vote buys at 0.262) are
        # missing from the taker-only list: resting limit orders that filled.
        self.assertEqual(p["maker_share"], 0.6)
        self.assertIn(p["archetype"], ("concentrated conviction", "politics / macro trader"))

    def test_cost_and_pnl_from_closed_position(self):
        d, lb = theo4()
        d["closed"] = d["closed"][:1]  # Trump popular vote: 13.18M shares at 0.3695
        p = features.profile(d, lb)
        self.assertAlmostEqual(p["cost"], 0.3695 * 13175255.227, places=0)
        self.assertAlmostEqual(p["roi"], 8303171.2313 / (0.3695 * 13175255.227), places=3)


def synthetic(**kw):
    base = {"trades_per_day": 2, "trades_sampled": 1000, "short_crypto_share": 0, "maker_share": 0.1,
            "rewards_usd": 0, "both_sides_share": 0, "n_merge": 0, "n_conversion": 0,
            "price_>=95c": 0, "top5_share": 0.3, "closed_positions": 500,
            "cat_sports": 0, "same_day_share": 0, "cat_politics": 0,
            "cat_geopolitics": 0, "cat_economics": 0, "main_category": "other",
            "realized_pnl": 1000}
    return {**base, **kw}


class ArchetypeTest(unittest.TestCase):
    def check(self, expect, **kw):
        self.assertEqual(features.archetype(synthetic(**kw))[0], expect)

    def test_rules(self):
        self.check("bot / high-frequency", trades_per_day=500)
        self.check("bot / high-frequency", short_crypto_share=0.8)
        self.check("generalist", trades_per_day=500, trades_sampled=12)  # one burst
        self.check("market maker", maker_share=0.8, both_sides_share=0.5)
        self.check("market maker", maker_share=0.8, rewards_usd=200)
        # limit-order whale: maker fills, pocket-change rewards, one side only
        self.check("generalist", maker_share=0.8, rewards_usd=50)
        self.check("arbitrage / merger", n_merge=40, both_sides_share=0.5, maker_share=0.1)
        self.check("bonder (near-certain outcomes)", **{"price_>=95c": 0.7})
        self.check("concentrated conviction", top5_share=0.9, closed_positions=40)
        self.check("sports bettor (same-day/in-play)", cat_sports=0.9, same_day_share=0.8)
        self.check("sports bettor (pre-game/futures)", cat_sports=0.9, same_day_share=0.2)
        self.check("politics / macro trader", cat_politics=0.5, cat_economics=0.2)
        self.check("generalist")


class PagingTest(unittest.TestCase):
    def test_server_capped_page_size(self):
        rows = [{"i": i} for i in range(123)]

        class C:
            def get(self, base, path, params=None, use_cache=True, keep=None):
                o = params["offset"]
                return rows[o:o + 50]  # server ignores limit=500, returns 50
        got, trunc = collect.paged(C(), "/x", {}, cap=1000)
        self.assertEqual(len(got), 123)
        self.assertFalse(trunc)
        got, trunc = collect.paged(C(), "/x", {}, cap=60)
        self.assertEqual((len(got), trunc), (60, True))


class RenderTest(unittest.TestCase):
    def test_report_sections(self):
        d, lb = theo4()
        p = features.profile(d, lb)
        p["top_markets"] = [{"title": "Trump popular vote", "outcome": "Yes",
                             "avg_price": 0.37, "pnl": 8.3e6, "end": "2024-11-05"}]
        w = p["wallet"]
        text = render({"all-time top": [w]}, {w: {"all-time top": lb}}, {w: p})
        for s in ("All-time top (1 wallets", "where the money came from", "Theo4",
                  "Examples by strategy"):
            self.assertIn(s, text)


if __name__ == "__main__":
    unittest.main()


class BondsTest(unittest.TestCase):
    def test_favorite_side_band_fee_and_payout(self):
        from study import bonds
        close = 10_000_000
        mk = lambda i, p, yes_won: {"id": f"m{i}", "closed": close, "yes_won": yes_won,
                                     "question": "Will X win on 2026-10-18?", "slug": "",
                                     "eventSlug": ""}
        ms = [mk(1, 0.96, True),    # YES favorite at 96c, wins
              mk(2, 0.03, False),   # NO is the favorite at 97c, wins
              mk(3, 0.96, False),   # favorite loses
              mk(4, 0.50, True)]    # no favorite in any band
        paths = {m["id"]: [(close - 30 * 3600, p), (close - 3000, p)]
                 for m, p in zip(ms, (0.96, 0.03, 0.96, 0.50))}
        res, _ = bonds.backtest(ms, paths, slippage=0.0, maker=True)
        r = res[(24, (0.95, 0.98))]
        self.assertEqual(len(r), 3)
        self.assertAlmostEqual(r[0], 1 / 0.96 - 1)
        self.assertAlmostEqual(r[1], 1 / 0.97 - 1)
        self.assertAlmostEqual(r[2], -1.0)
        taker, _ = bonds.backtest(ms, paths, slippage=0.0, maker=False)
        self.assertLess(taker[(24, (0.95, 0.98))][0], r[0])   # fee costs something
        self.assertNotIn((168, (0.95, 0.98)), res)             # no price that early
