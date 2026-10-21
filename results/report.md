# Polymarket copy-trade backtest

Window 2026-07-23 → 2026-10-21 (90 days); qualify until 2026-09-21, test after.
Bankroll $200; 5% of equity per typical leader buy (scaled by leader conviction 0.25–3.0x), max 20% per trade, 35% per market; slippage 1.0¢/fill, market taker fees + 0 bps, min order $1, copy delay 0s.

Wallets examined: 1500; simulated: 666; flagged as hard to copy: 536; eligible for ranking: 95.

## Recommendation

**0xb851db7fd9c13a5794f4e38c615295ec1c1e0dfe** (kupoz)

- $200 → $264196.00 over the window (+131998.0%), max drawdown 58.5%
- Qualifying period +20.7%, out-of-sample test +109350.1%
- At double slippage: +21472.5%
- 144 buys / 96 sells copied across 28 markets, win rate 61%
- Leader: 5.5 trades/day, median trade $2, avg buy price 20¢

## Top 15

| # | wallet | name | return | test | max DD | 2x slip | buys | win |
|---|---|---|---|---|---|---|---|---|
| 1 | `0xb851db7fd9c13a5794f4e38c615295ec1c1e0dfe` | kupoz | +131998.0% | +109350.1% | 58.5% | +21472.5% | 144 | 61% |
| 2 | `0x7576e41bc6fce96d7bc4e9eb0c9d046d4c2654b6` | Starlord2 | +46521.3% | +1140.4% | 70.5% | +6007.7% | 525 | 65% |
| 3 | `0x73e35ce0b7e36ef3ce29ebd12b30b28007383239` | Stonktrader | +18156.7% | +1011.3% | 58.5% | +6480.0% | 132 | 67% |
| 4 | `0x95c6c9a6727ed203e97230dda61ab19a020e1508` | DelidelaDele | +1044.9% | +818.7% | 78.7% | +729.9% | 209 | 59% |
| 5 | `0xfc0847fe2ea938d6e2624650eb29ef8d8142a137` | 0xfC0847fe2Ea938D6e2 | +861.1% | +620.3% | 56.1% | -82.1% | 1594 | 53% |
| 6 | `0x2c41d0ca2b4b2344912eead711f28cd4dcff133e` | lineth | +3031.1% | +540.9% | 10.2% | +1733.8% | 85 | 55% |
| 7 | `0xaaad37f3bbb45af95818e20e554f8b21371f29e0` | swiftFoxx | +3075.8% | +377.1% | 71.0% | +1984.9% | 278 | 72% |
| 8 | `0x2f9da73ca8430dc4bdbd75f9c76d91592ca5deb3` | themain | +165.8% | +146.1% | 4.6% | +151.2% | 25 | 62% |
| 9 | `0xadaf1c42e0a88e2942e7adfe559e30c1796bf9f2` | gesst | +617.6% | +150.9% | 15.6% | +235.9% | 81 | 62% |
| 10 | `0xbc1dacd4b84582fc310e4213421bca24e82da53c` | Fvalp | +191.7% | +170.1% | 63.5% | +202.5% | 317 | 61% |
| 11 | `0x34142c0027cccc7a9156a280ef3edd1dd67451a1` | ORI- | +143.1% | +133.7% | 56.5% | +61.1% | 155 | 44% |
| 12 | `0xd8860bbbdf24d02b74d875b2d987986f62b96f88` | btystu | +421.1% | +98.0% | 2.0% | +388.2% | 31 | 100% |
| 13 | `0x85af4296fec14602804a6fac8db79cc87042a6eb` | wugds | +135.1% | +83.1% | 5.6% | +127.8% | 18 | 88% |
| 14 | `0x80d5aebbe7a714879177e4dae0014195beb3987e` | 0x80d5aebbE7a7148791 | +275.7% | +78.5% | 6.0% | +263.1% | 26 | 100% |
| 15 | `0xe5d29f2276769fd3574bbaa846a563b6c8a0776e` | Koliniko | +939.4% | +85.6% | 29.4% | +864.7% | 36 | 100% |

Score = out-of-sample return − 0.5 × max drawdown. Full table in `ranking.csv`; daily equity for the top 10 in `top_equity_curves.csv`.

Caveats: past results don't predict future ones; fills assume you get the leader's price plus slippage; open positions are marked at the current market price; wallets that started positions before the window are only copied from their first in-window buy.
