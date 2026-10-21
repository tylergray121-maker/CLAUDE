# Polymarket copy-trade backtest

Window 2026-07-23 → 2026-10-21 (90 days); qualify until 2026-09-21, test after.
Bankroll $200; 5% of equity per typical leader buy (scaled by leader conviction 0.25–3.0x), max 20% per trade, 35% per market; slippage 1.0¢/fill, market taker fees + 0 bps, min order $1, copy delay 30s (shortlist), never more than the leader's own trade size.

Universe: volume leaderboards only. Wallets examined: 1218; simulated: 439; flagged as hard to copy: 603; eligible for ranking: 28.

Polymarket US: 37000 market questions, 24711 game-days; 719 of 115219 copyable trades (1%) were in markets matched to it (37 distinct markets).

Copy delay: 380407 of 380407 simulated fills (100%) were priced from market history 30s after the leader; the rest fell back to the leader's price.

## Plan A — all Polymarket markets

28 wallets qualified (profitable in the qualifying period, enough copyable buys). Typical qualified wallet in the test period: -6.2% (median); 36% of them made money.

**Validation — wallets chosen using the qualifying period only, scored on the test period:**

| copy top K together | test return | test max DD | buys copied |
|---|---|---|---|
| 1 | +4250.8% | 27.5% | 1338 |
| 2 | +1880.3% | 37.7% | 1592 |
| 3 | +1140.5% | 34.2% | 1929 |
| 5 | +1015.6% | 39.8% | 2368 |
| 8 | +303.3% | 31.4% | 5993 |

Median across portfolio sizes: +1140.5% vs -6.2% for a random qualified wallet.

**Verdict: the method held up out of sample; best with K = 1.**

**Picks for now** — ranked on 2026-08-21 onward, each copy sized 5.0% of equity per typical leader buy:

| wallet | recent return | max DD | buys | markets | win rate |
|---|---|---|---|---|---|
| `0x91e67d77b45558ce69238bf8a79e2e902b1ee9c5` | +849.9% | 51.8% | 92 | 40 | 78% |

Copied together over that window: $200 → $1899.84 (+849.9%), max drawdown 51.8%. This is in-sample — the validation table is the honest estimate.

## Plan B — only markets also listed on Polymarket US (usable from New York)

No wallet was profitable in the qualifying period with enough copyable buys.

## Best single wallets (ranked with hindsight)

**0x20d6436849f930584892730c7f96ebb2ac763856** (0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357)

- $200 → $190393.26 over the window (+95096.6%), max drawdown 63.2%
- Qualifying period +2088.0%, out-of-sample test +4250.8%
- At double slippage: +55777.9%
- 1338 buys / 112 sells copied across 186 markets, win rate 49%
- Leader: 22.3 trades/day, median trade $22, avg buy price 37¢

### Top 15

| # | wallet | name | return | test | max DD | 2x slip | buys | win |
|---|---|---|---|---|---|---|---|---|
| 1 | `0x20d6436849f930584892730c7f96ebb2ac763856` | 0x20D6436849F9305848 | +95096.6% | +4250.8% | 63.2% | +55777.9% | 1338 | 49% |
| 2 | `0x03e8a544e97eeff5753bc1e90d46e5ef22af1697` | weflyhigh | +216.3% | +53.0% | 11.2% | +203.7% | 44 | 67% |
| 3 | `0x7cf93583951552553bc0d243a8582a3410ed2798` | MysticFind | +64.6% | +47.7% | 30.8% | +21.6% | 85 | 44% |
| 4 | `0xf2f6af4f27ec2dcf4072095ab804016e14cd5817` | gopfan2 | +42.4% | +33.3% | 4.0% | +25.9% | 35 | 55% |
| 5 | `0x14494e6733e86a05888610dfabf3c98eeffea618` | SadSquid54333 | +909.0% | +43.1% | 44.7% | +557.2% | 182 | 64% |
| 6 | `0x88c4919de76e526d55a32c1f8afb439dd1f1129a` | Votei14Voude22 | +67.1% | +9.3% | 7.9% | +49.6% | 173 | 73% |
| 7 | `0x16da8936832021a431a3df43d77721b5a8e981b7` | 534312 | +67.5% | +25.9% | 45.5% | +131.2% | 110 | 82% |
| 8 | `0x9106cf79b02f85d8f1e546802ed916648f44afcb` | su281 | +44.4% | +17.1% | 33.5% | +86.5% | 147 | 82% |
| 9 | `0x07046535ff9a910d7343a2c319a3e62234621858` | HH168 | +15.8% | +0.8% | 1.6% | +13.9% | 37 | 75% |
| 10 | `0xc6dd722558dbfbd8fa780efcbe819ed8c6604b9f` | tourists | +20.8% | -5.7% | 15.3% | +6.6% | 76 | 67% |
| 11 | `0xfea31bc088000ff909be1dfd8d0e3f2c7ef2d227` | ndb1 | +9.9% | -6.6% | 13.7% | -0.6% | 85 | 40% |
| 12 | `0x986aaa6c11a36f1ddc0deefbd4ab52279be3e7c7` | SGBEER | +19.1% | -7.1% | 24.5% | +5.0% | 64 | 50% |
| 13 | `0x944e0472b99926f4f712fc97dc0a846a8c5d8c94` | mountaindewd | +30.6% | +1.6% | 45.1% | +15.8% | 65 | 55% |
| 14 | `0xf1236fe4389007cd730d2eaff0d7df90917972e4` | Artimis | -7.1% | -13.7% | 18.0% | -18.1% | 66 | 65% |
| 15 | `0xca8f0374e3fc79b485499cc0b038d4f7e783d963` | ScottVan | +75.8% | -0.2% | 48.4% | +42.1% | 218 | 48% |

Score = out-of-sample return − 0.5 × max drawdown. Full table in `ranking.csv`; daily equity for the top 10 in `top_equity_curves.csv`.

Caveats: past results don't predict future ones; fills assume you get the leader's price plus slippage; open positions are marked at the current market price; wallets that started positions before the window are only copied from their first in-window buy.
