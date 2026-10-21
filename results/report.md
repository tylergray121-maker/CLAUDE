# Polymarket copy-trade backtest

Window 2026-07-23 → 2026-10-21 (90 days); qualify until 2026-09-21, test after.
Bankroll $200; 5% of equity per typical leader buy (scaled by leader conviction 0.25–3.0x), max 20% per trade, 35% per market; slippage 1.0¢/fill, market taker fees + 0 bps, min order $1, copy delay 30s (shortlist), never more than the leader's own trade size.

Universe: volume leaderboards only. Wallets examined: 1218; simulated: 439; flagged as hard to copy: 603; eligible for ranking: 24.

Polymarket US: 37000 market questions, 24711 game-days; 410 of 101887 copyable trades (0%) were in markets matched to it (33 distinct markets).

Copy delay: 262288 of 262288 simulated fills (100%) were priced from market history 30s after the leader; the rest fell back to the leader's price.

## Plan A — all Polymarket markets

10 wallets qualified (20+ settled copyable bets, profitable at a flat $10 stake before the cutoff). In the test period the typical one returned +1.9% per bet (median); 78% were profitable.

**Validation — top K wallets chosen before the cutoff, scored on bets they opened after it:**

| copy top K | bets | return per bet | t-stat |
|---|---|---|---|
| 1 | 174 | +10.1% | 0.8 |
| 2 | 227 | +4.0% | 0.4 |
| 3 | 262 | +0.5% | 0.1 |
| 5 | 268 | +0.8% | 0.1 |
| 8 | 763 | +1.4% | 0.4 |

Median across K: +1.4% per bet vs +1.9% for a random qualified wallet. (t ≥ 1.65 is roughly 95% confidence the edge isn't luck.)

$200 copying the top 8 through the test period: $274.48 (+37.2%), worst drawdown 14.3%, 114 buys copied.

**Verdict: no reliable edge.** Wallets that looked good before the cutoff did not keep a clear, statistically solid edge afterwards once delay, slippage and fees were paid.

**What the method would pick now (not recommended — see verdict)** — bets opened from 2026-08-21 and settled:

| wallet | settled bets | return per bet | t-stat |
|---|---|---|---|
| `0x91e67d77b45558ce69238bf8a79e2e902b1ee9c5` | 40 | +46.6% | 3.4 |
| `0x3eb31daa061a19855cbf0a4884c202fb86976a2a` | 22 | +40.7% | 2.2 |
| `0x543f6fdd37ca39efd4ee7a98f8b7efeeb8c68323` | 33 | +27.3% | 2.1 |
| `0x16da8936832021a431a3df43d77721b5a8e981b7` | 67 | +18.1% | 4.1 |
| `0xc2e7800b5af46e6093872b177b7a5e7f0563be51` | 25 | +25.2% | 1.6 |
| `0x614dc8d3542c12103d2c6a3553fd761e391d1546` | 36 | +15.8% | 1.4 |
| `0x20d6436849f930584892730c7f96ebb2ac763856` | 180 | +14.5% | 1.1 |
| `0x924379a79c64b77ad5816ad362122a5f6228658e` | 195 | +9.1% | 1.2 |

$200 copying them over that window: $244.91 (+22.5%), worst drawdown 48.3% (in-sample; the validation above is the honest estimate).

## Plan B — only markets also listed on Polymarket US (usable from New York)

No wallet had 20+ settled, profitable copyable bets in the qualifying period.

## Appendix: single wallets, compounding, ranked with hindsight

Percentages here compound a bankroll that grows into the leader's own bet sizes, so they are not comparable between wallets or achievable from $200. Use the plans above.


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
| 3 | `0xf2f6af4f27ec2dcf4072095ab804016e14cd5817` | gopfan2 | +42.4% | +33.3% | 4.0% | +25.9% | 35 | 55% |
| 4 | `0x14494e6733e86a05888610dfabf3c98eeffea618` | SadSquid54333 | +909.0% | +43.1% | 44.7% | +557.2% | 182 | 64% |
| 5 | `0x88c4919de76e526d55a32c1f8afb439dd1f1129a` | Votei14Voude22 | +67.1% | +9.3% | 7.9% | +49.6% | 173 | 73% |
| 6 | `0x16da8936832021a431a3df43d77721b5a8e981b7` | 534312 | +67.5% | +25.9% | 45.5% | +131.2% | 110 | 82% |
| 7 | `0x9106cf79b02f85d8f1e546802ed916648f44afcb` | su281 | +44.4% | +17.1% | 33.5% | +86.5% | 147 | 82% |
| 8 | `0x07046535ff9a910d7343a2c319a3e62234621858` | HH168 | +15.8% | +0.8% | 1.6% | +13.9% | 37 | 75% |
| 9 | `0xc6dd722558dbfbd8fa780efcbe819ed8c6604b9f` | tourists | +20.8% | -5.7% | 15.3% | +6.6% | 76 | 67% |
| 10 | `0xfea31bc088000ff909be1dfd8d0e3f2c7ef2d227` | ndb1 | +9.9% | -6.6% | 13.7% | -0.6% | 85 | 40% |
| 11 | `0x986aaa6c11a36f1ddc0deefbd4ab52279be3e7c7` | SGBEER | +19.1% | -7.1% | 24.5% | +5.0% | 64 | 50% |
| 12 | `0x944e0472b99926f4f712fc97dc0a846a8c5d8c94` | mountaindewd | +30.6% | +1.6% | 45.1% | +15.8% | 65 | 55% |
| 13 | `0xca8f0374e3fc79b485499cc0b038d4f7e783d963` | ScottVan | +75.8% | -0.2% | 48.4% | +42.1% | 218 | 48% |
| 14 | `0x4cc3522b689a6bf1fb4a2444c523e7776db47552` | CrunchWrapoDeLaFuent | +34.7% | +0.0% | 62.3% | +8.5% | 50 | 50% |
| 15 | `0xc2e7800b5af46e6093872b177b7a5e7f0563be51` | beachboy4 | +227.0% | +0.0% | 75.8% | +157.1% | 156 | 73% |

Score = out-of-sample return − 0.5 × max drawdown. Full table in `ranking.csv`; daily equity for the top 10 in `top_equity_curves.csv`.

Caveats: past results don't predict future ones; fills assume you get the leader's price plus slippage; open positions are marked at the current market price; wallets that started positions before the window are only copied from their first in-window buy.
