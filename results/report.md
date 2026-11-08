# Polymarket copy-trade backtest

Window 2026-07-23 → 2026-10-21 (90 days); qualify until 2026-09-21, test after.
Bankroll $200; 5% of equity per typical leader buy (scaled by leader conviction 0.25–3.0x), max 20% per trade, 35% per market; slippage 1.0¢/fill, market taker fees + 0 bps, min order $1, copy delay 30s (shortlist), never more than the leader's own trade size.

Universe: volume leaderboards only. Wallets examined: 1115; simulated: 383; flagged as hard to copy: 500; eligible for ranking: 25.

Polymarket US: 37186 market questions, 24986 game-days; 302 of 95424 copyable trades (0%) were in markets matched to it (36 distinct markets).

Copy delay: 242133 of 242136 simulated fills (100%) were priced from market history 30s after the leader; the rest fell back to the leader's price.

## Plan A — all Polymarket markets

8 wallets qualified (20+ settled copyable bets, profitable at a flat $10 stake before the cutoff). In the test period the typical one returned +5.4% per bet (median); 86% were profitable.

**Validation — top K wallets chosen before the cutoff, scored on bets they opened after it:**

| copy top K | bets | return per bet | t-stat |
|---|---|---|---|
| 1 | 174 | +9.5% | 0.8 |
| 2 | 179 | +18.0% | 1.4 |
| 3 | 179 | +18.0% | 1.4 |
| 5 | 295 | +13.2% | 1.5 |
| 8 | 411 | +9.0% | 1.4 |

Median across K: +13.2% per bet vs +5.4% for a random qualified wallet. (t ≥ 1.65 is roughly 95% confidence the edge isn't luck.)

$200 copying the top 3 through the test period: $620.09 (+210.0%), worst drawdown 28.2%, 58 buys copied.

**Verdict: no reliable edge.** Wallets that looked good before the cutoff did not keep a clear, statistically solid edge afterwards once delay, slippage and fees were paid.

**What the method would pick now (not recommended — see verdict)** — bets opened from 2026-08-21 and settled:

| wallet | settled bets | return per bet | t-stat |
|---|---|---|---|
| `0x94c4fe3b18435aa92024c7c1589537fcda3f43ca` | 71 | +45.3% | 1.6 |
| `0xc2e7800b5af46e6093872b177b7a5e7f0563be51` | 25 | +25.2% | 1.6 |
| `0xeb490d0534bb68b4c2ce139b219a728cd2c3693e` | 70 | +12.2% | 1.2 |

$200 copying them over that window: $47.60 (-76.2%), worst drawdown 78.8% (in-sample; the validation above is the honest estimate).

## Plan B — only markets also listed on Polymarket US (usable from New York)

No wallet had 20+ settled, profitable copyable bets in the qualifying period.

## Appendix: single wallets, compounding, ranked with hindsight

Percentages here compound a bankroll that grows into the leader's own bet sizes, so they are not comparable between wallets or achievable from $200. Use the plans above.


**0x20d6436849f930584892730c7f96ebb2ac763856** (0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357)

- $200 → $187287.34 over the window (+93543.7%), max drawdown 63.2%
- Qualifying period +2088.0%, out-of-sample test +4179.8%
- At double slippage: +54331.9%
- 1338 buys / 112 sells copied across 186 markets, win rate 50%
- Leader: 22.3 trades/day, median trade $22, avg buy price 37¢

### Top 15

| # | wallet | name | return | test | max DD | 2x slip | buys | win |
|---|---|---|---|---|---|---|---|---|
| 1 | `0x20d6436849f930584892730c7f96ebb2ac763856` | 0x20D6436849F9305848 | +93543.7% | +4179.8% | 63.2% | +54331.9% | 1338 | 50% |
| 2 | `0x94c4fe3b18435aa92024c7c1589537fcda3f43ca` | Railcool | +533.3% | +340.0% | 12.8% | +470.0% | 57 | 62% |
| 3 | `0x03e8a544e97eeff5753bc1e90d46e5ef22af1697` | weflyhigh | +216.3% | +53.0% | 11.2% | +203.7% | 44 | 67% |
| 4 | `0x9106cf79b02f85d8f1e546802ed916648f44afcb` | su281 | +83.5% | +48.9% | 33.5% | +139.9% | 147 | 85% |
| 5 | `0xe9b710551dd82a44e79203c2394a2b10163ace7b` | googleplay | +93.2% | +0.0% | 2.3% | +88.4% | 28 | 100% |
| 6 | `0x4e59cee7a51cb9d1be92dffb5119f9af508ae56a` | shineforever | +20.9% | +9.0% | 33.4% | +16.6% | 162 | 49% |
| 7 | `0xfcd0eadb24d78e016e88b9e2a7029e349ba6391d` | GroyperFinance | +15.8% | +3.4% | 24.6% | +12.2% | 34 | 63% |
| 8 | `0xfea31bc088000ff909be1dfd8d0e3f2c7ef2d227` | ndb1 | +2.1% | -12.9% | 19.4% | -7.5% | 85 | 40% |
| 9 | `0x264cbb7263b0c336c58fb5a5de1773896e6bbaca` | sdhyky | +102.0% | +0.9% | 49.2% | +52.8% | 143 | 49% |
| 10 | `0xca8f0374e3fc79b485499cc0b038d4f7e783d963` | ScottVan | +75.8% | -0.2% | 48.4% | +42.1% | 218 | 48% |
| 11 | `0xc6dd722558dbfbd8fa780efcbe819ed8c6604b9f` | tourists | +7.9% | -13.8% | 22.6% | -5.0% | 76 | 67% |
| 12 | `0x4cc3522b689a6bf1fb4a2444c523e7776db47552` | CrunchWrapoDeLaFuent | +34.7% | +0.0% | 62.3% | +8.5% | 50 | 50% |
| 13 | `0xc2e7800b5af46e6093872b177b7a5e7f0563be51` | beachboy4 | +227.0% | +0.0% | 75.8% | +157.1% | 156 | 73% |
| 14 | `0x05f6cb63d4ffdfaecd7ad8acd0765b6f6a5a25a1` | ethBELIVER | +22.1% | -6.2% | 69.9% | -5.4% | 85 | 56% |
| 15 | `0xd426adbc3c4461c86099c26221c877f20e42334a` | 881112 | +83.3% | -23.5% | 65.1% | +54.4% | 103 | 46% |

Score = out-of-sample return − 0.5 × max drawdown. Full table in `ranking.csv`; daily equity for the top 10 in `top_equity_curves.csv`.

Caveats: past results don't predict future ones; fills assume you get the leader's price plus slippage; open positions are marked at the current market price; wallets that started positions before the window are only copied from their first in-window buy.
