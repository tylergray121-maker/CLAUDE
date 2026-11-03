# Polymarket copy-trade backtest

Window 2026-07-23 → 2026-10-21 (90 days); qualify until 2026-09-21, test after.
Bankroll $200; 5% of equity per typical leader buy (scaled by leader conviction 0.25–3.0x), max 20% per trade, 35% per market; slippage 1.0¢/fill, market taker fees + 0 bps, min order $1, copy delay 30s (shortlist), never more than the leader's own trade size.

Universe: volume leaderboards only. Wallets examined: 1134; simulated: 384; flagged as hard to copy: 514; eligible for ranking: 22.

Polymarket US: 34120 market questions, 24300 game-days; 395 of 108676 copyable trades (0%) were in markets matched to it (31 distinct markets).

Copy delay: 278300 of 278309 simulated fills (100%) were priced from market history 30s after the leader; the rest fell back to the leader's price.

## Plan A — all Polymarket markets

10 wallets qualified (20+ settled copyable bets, profitable at a flat $10 stake before the cutoff). In the test period the typical one returned +3.2% per bet (median); 67% were profitable.

**Validation — top K wallets chosen before the cutoff, scored on bets they opened after it:**

| copy top K | bets | return per bet | t-stat |
|---|---|---|---|
| 1 | 174 | +9.4% | 0.7 |
| 2 | 213 | +9.1% | 0.9 |
| 3 | 213 | +9.1% | 0.9 |
| 5 | 329 | +8.0% | 1.1 |
| 8 | 627 | +1.2% | 0.3 |

Median across K: +9.1% per bet vs +3.2% for a random qualified wallet. (t ≥ 1.65 is roughly 95% confidence the edge isn't luck.)

$200 copying the top 5 through the test period: $899.69 (+349.8%), worst drawdown 81.0%, 960 buys copied.

**Verdict: no reliable edge.** Wallets that looked good before the cutoff did not keep a clear, statistically solid edge afterwards once delay, slippage and fees were paid.

**What the method would pick now (not recommended — see verdict)** — bets opened from 2026-08-21 and settled:

| wallet | settled bets | return per bet | t-stat |
|---|---|---|---|
| `0xc2e7800b5af46e6093872b177b7a5e7f0563be51` | 25 | +25.2% | 1.6 |
| `0x71a44a004f34ebbb8b5cc5995a250116afc4809d` | 62 | +8.3% | 2.3 |
| `0x3835957ad7188313391213e8647baaf4a2ed3493` | 50 | +11.9% | 1.2 |
| `0xeb490d0534bb68b4c2ce139b219a728cd2c3693e` | 70 | +12.2% | 1.2 |
| `0x20d6436849f930584892730c7f96ebb2ac763856` | 180 | +14.5% | 1.1 |

$200 copying them over that window: $75.50 (-62.3%), worst drawdown 62.3% (in-sample; the validation above is the honest estimate).

## Plan B — only markets also listed on Polymarket US (usable from New York)

No wallet had 20+ settled, profitable copyable bets in the qualifying period.

## Appendix: single wallets, compounding, ranked with hindsight

Percentages here compound a bankroll that grows into the leader's own bet sizes, so they are not comparable between wallets or achievable from $200. Use the plans above.


**0x20d6436849f930584892730c7f96ebb2ac763856** (0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357)

- $200 → $187426.32 over the window (+93613.2%), max drawdown 63.2%
- Qualifying period +2088.0%, out-of-sample test +4183.0%
- At double slippage: +54363.9%
- 1338 buys / 112 sells copied across 186 markets, win rate 49%
- Leader: 22.3 trades/day, median trade $22, avg buy price 37¢

### Top 15

| # | wallet | name | return | test | max DD | 2x slip | buys | win |
|---|---|---|---|---|---|---|---|---|
| 1 | `0x20d6436849f930584892730c7f96ebb2ac763856` | 0x20D6436849F9305848 | +93613.2% | +4183.0% | 63.2% | +54363.9% | 1338 | 49% |
| 2 | `0x03e8a544e97eeff5753bc1e90d46e5ef22af1697` | weflyhigh | +216.3% | +53.0% | 11.2% | +203.7% | 44 | 67% |
| 3 | `0x9106cf79b02f85d8f1e546802ed916648f44afcb` | su281 | +67.5% | +36.0% | 33.5% | +118.7% | 147 | 85% |
| 4 | `0x71a44a004f34ebbb8b5cc5995a250116afc4809d` | HRAImail-.- | +150.2% | +32.5% | 34.8% | +117.6% | 203 | 86% |
| 5 | `0xe9b710551dd82a44e79203c2394a2b10163ace7b` | googleplay | +93.2% | +0.0% | 2.3% | +88.4% | 28 | 100% |
| 6 | `0x4e59cee7a51cb9d1be92dffb5119f9af508ae56a` | shineforever | +20.9% | +9.0% | 33.4% | +16.6% | 162 | 49% |
| 7 | `0xfea31bc088000ff909be1dfd8d0e3f2c7ef2d227` | ndb1 | +9.5% | -6.6% | 13.8% | -0.7% | 85 | 41% |
| 8 | `0xca8f0374e3fc79b485499cc0b038d4f7e783d963` | ScottVan | +75.8% | -0.2% | 48.4% | +42.1% | 218 | 48% |
| 9 | `0x264cbb7263b0c336c58fb5a5de1773896e6bbaca` | sdhyky | +98.6% | -0.8% | 49.2% | +49.4% | 143 | 49% |
| 10 | `0xc6dd722558dbfbd8fa780efcbe819ed8c6604b9f` | tourists | +4.4% | -16.5% | 25.1% | -8.0% | 76 | 58% |
| 11 | `0xc2e7800b5af46e6093872b177b7a5e7f0563be51` | beachboy4 | +227.0% | +0.0% | 75.8% | +157.1% | 156 | 73% |
| 12 | `0xb37aa8834f9baefc6fb3312f59df8ddf0348f1b1` | Raskell | +228.0% | -25.1% | 41.3% | +60.5% | 319 | 55% |
| 13 | `0xd426adbc3c4461c86099c26221c877f20e42334a` | 881112 | +91.2% | -20.2% | 65.1% | +60.2% | 103 | 48% |
| 14 | `0x9aeb534c42b58b21673d5e03e9da14fbd15b2729` | The-Joker | +3.8% | -31.1% | 62.6% | -11.6% | 251 | 58% |
| 15 | `0x88c4919de76e526d55a32c1f8afb439dd1f1129a` | Votei14Voude22 | -26.6% | -52.0% | 58.3% | -29.3% | 173 | 73% |

Score = out-of-sample return − 0.5 × max drawdown. Full table in `ranking.csv`; daily equity for the top 10 in `top_equity_curves.csv`.

Caveats: past results don't predict future ones; fills assume you get the leader's price plus slippage; open positions are marked at the current market price; wallets that started positions before the window are only copied from their first in-window buy.
