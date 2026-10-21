# Polymarket copy-trade backtest

Window 2026-07-23 → 2026-10-21 (90 days); qualify until 2026-09-21, test after.
Bankroll $200; 5% of equity per typical leader buy (scaled by leader conviction 0.25–3.0x), max 20% per trade, 35% per market; slippage 1.0¢/fill, market taker fees + 0 bps, min order $1, copy delay 30s (shortlist), never more than the leader's own trade size.

Wallets examined: 1500; simulated: 666; flagged as hard to copy: 558; eligible for ranking: 23.

Polymarket US lists 36697 markets; 494 of 96677 copyable trades (1%) were in markets matched to it (65 distinct markets).

Copy delay: 332175 of 332175 simulated fills (100%) were priced from market history 30s after the leader; the rest fell back to the leader's price.

## Plan A — all Polymarket markets

23 wallets qualified (profitable in the qualifying period, enough copyable buys). Typical qualified wallet in the test period: +43.1% (median); 61% of them made money.

**Validation — wallets chosen using the qualifying period only, scored on the test period:**

| copy top K together | test return | test max DD | buys copied |
|---|---|---|---|
| 1 | +78.2% | 31.9% | 812 |
| 2 | -22.9% | 57.9% | 1405 |
| 3 | +65.3% | 48.0% | 3320 |
| 5 | +23.1% | 36.9% | 5363 |
| 8 | +17.2% | 20.4% | 6225 |

**Verdict: the method held up out of sample; best with K = 1.**

**Picks for now** — ranked on 2026-08-21 onward, each copy sized 5.0% of equity per typical leader buy:

| wallet | recent return | max DD | buys | markets | win rate |
|---|---|---|---|---|---|
| `0xe5241830e8876c115d7dc8311ad9f43d85fdd34f` | +7005.8% | 79.2% | 1326 | 258 | 63% |

Copied together over that window: $200 → $14211.52 (+7005.8%), max drawdown 79.2%. This is in-sample — the validation table is the honest estimate.

## Plan B — only markets also listed on Polymarket US (usable from New York)

1 wallets qualified (profitable in the qualifying period, enough copyable buys). Typical qualified wallet in the test period: -10.5% (median); 0% of them made money.

**Validation — wallets chosen using the qualifying period only, scored on the test period:**

| copy top K together | test return | test max DD | buys copied |
|---|---|---|---|
| 1 | -10.5% | 71.5% | 88 |

**Verdict: no edge.** Picking wallets by past results did not beat chance out of sample after fees and slippage, so this backtest gives no reason to copy any of these wallets.

**What the method would pick now (not recommended — see verdict)** — ranked on 2026-08-21 onward, each copy sized 5.0% of equity per typical leader buy:

| wallet | recent return | max DD | buys | markets | win rate |
|---|---|---|---|---|---|
| `0x20d6436849f930584892730c7f96ebb2ac763856` | +466.5% | 17.1% | 49 | 14 | 56% |

Copied together over that window: $200 → $1132.94 (+466.5%), max drawdown 17.1%. This is in-sample — the validation table is the honest estimate.

## Best single wallets (ranked with hindsight)

**0x20d6436849f930584892730c7f96ebb2ac763856** (0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357)

- $200 → $190408.59 over the window (+95104.3%), max drawdown 63.2%
- Qualifying period +2088.0%, out-of-sample test +4251.2%
- At double slippage: +55785.3%
- 1338 buys / 112 sells copied across 186 markets, win rate 49%
- Leader: 22.3 trades/day, median trade $22, avg buy price 37¢

### Top 15

| # | wallet | name | return | test | max DD | 2x slip | buys | win |
|---|---|---|---|---|---|---|---|---|
| 1 | `0x20d6436849f930584892730c7f96ebb2ac763856` | 0x20D6436849F9305848 | +95104.3% | +4251.2% | 63.2% | +55785.3% | 1338 | 49% |
| 2 | `0x73e35ce0b7e36ef3ce29ebd12b30b28007383239` | Stonktrader | +661.8% | +645.8% | 73.4% | +325.9% | 116 | 61% |
| 3 | `0x1a80db0b051af4c1a10cbaad4d35df5d71ea6b2b` | arshobing | +1551.4% | +357.1% | 72.0% | +637.0% | 128 | 43% |
| 4 | `0x0d23fc6838433dbff11e4667ef5991e9dd9d2d56` | tiger105 | +171.9% | +150.8% | 37.6% | +114.1% | 146 | 63% |
| 5 | `0xd8860bbbdf24d02b74d875b2d987986f62b96f88` | btystu | +376.7% | +92.3% | 2.1% | +350.4% | 31 | 100% |
| 6 | `0x80d5aebbe7a714879177e4dae0014195beb3987e` | 0x80d5aebbE7a7148791 | +274.3% | +78.3% | 6.2% | +261.3% | 27 | 100% |
| 7 | `0xbc1dacd4b84582fc310e4213421bca24e82da53c` | Fvalp | +117.9% | +102.5% | 65.7% | +130.6% | 317 | 57% |
| 8 | `0xe5d29f2276769fd3574bbaa846a563b6c8a0776e` | Koliniko | +821.1% | +76.1% | 29.5% | +767.0% | 42 | 100% |
| 9 | `0x95c6c9a6727ed203e97230dda61ab19a020e1508` | DelidelaDele | +151.9% | +99.8% | 94.6% | +123.8% | 297 | 58% |
| 10 | `0xc49fe658479db29e1a2fefebf0735f657dca9e05` | jizzbucket57 | +31837.8% | +78.2% | 55.4% | +23584.4% | 812 | 66% |
| 11 | `0x03e8a544e97eeff5753bc1e90d46e5ef22af1697` | weflyhigh | +216.3% | +53.0% | 11.2% | +203.7% | 44 | 67% |
| 12 | `0x1ee9a5fc09665909c0cce297c581703bfbb9197f` | vinii | +121.3% | +32.7% | 23.6% | +97.1% | 111 | 51% |
| 13 | `0x14494e6733e86a05888610dfabf3c98eeffea618` | SadSquid54333 | +909.0% | +43.1% | 44.7% | +557.2% | 182 | 64% |
| 14 | `0xadaf1c42e0a88e2942e7adfe559e30c1796bf9f2` | gesst | +46.5% | +13.9% | 14.8% | +16.3% | 70 | 44% |
| 15 | `0xc9a24fa249cf907c598544a4d46c077c1edf77d3` | 0x7A3f9C2D8b41E6a570 | +663.9% | +0.0% | 36.5% | +584.4% | 90 | 77% |

Score = out-of-sample return − 0.5 × max drawdown. Full table in `ranking.csv`; daily equity for the top 10 in `top_equity_curves.csv`.

Caveats: past results don't predict future ones; fills assume you get the leader's price plus slippage; open positions are marked at the current market price; wallets that started positions before the window are only copied from their first in-window buy.
