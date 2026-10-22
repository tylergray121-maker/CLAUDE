# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 45 days to 2026-10-21 21:00 UTC: 630 candidates, 272 with trades copytop could copy, 45 re-priced at a 30s copy delay. Choosing window: first 67%; test window: the rest (15 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 609 | 349 | $5,904 | -96.88 | -1.6% | -0.47 |
| every wallet that qualified on the first part (test window) | 944 | 520 | $9,229 | -51.45 | -0.6% | -0.25 |
| currently copied (test window) | 635 | 346 | $6,149 | +63.18 | +1.0% | +0.36 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 30s delay, 1c limit, hold to settlement | 609 | 349 | $5,904 | -96.88 | -1.6% | -0.47 | 1973 | 1219 | $19,106 | +2,445.55 | +12.8% | 5.6 |
| copy their sells too | 618 | 310 | $5,995 | -303.74 | -5.1% | -1.48 | 1982 | 1108 | $19,197 | +1,773.86 | +9.2% | 4.61 |
| size by conviction (x0.5 / x1 / x1.5) | 588 | 341 | $7,388 | +100.51 | +1.4% | -0.18 | 1915 | 1179 | $23,196 | +2,893.94 | +12.5% | 5.12 |
| skip bets under 0.5x their usual | 585 | 336 | $5,711 | -68.10 | -1.2% | -0.4 | 1830 | 1127 | $17,806 | +2,335.51 | +13.1% | 5.4 |
| pre-game only | 401 | 220 | $3,856 | -156.62 | -4.1% | -1.04 | 1465 | 875 | $14,092 | +1,980.85 | +14.1% | 5.35 |
| 15s delay | 618 | 354 | $5,997 | -126.89 | -2.1% | -0.59 | 1988 | 1225 | $19,235 | +2,370.34 | +12.3% | 5.45 |
| 60s delay | 600 | 345 | $5,813 | -29.89 | -0.5% | -0.22 | 1955 | 1208 | $18,914 | +2,561.86 | +13.5% | 5.76 |
| allow 2c over their price | 634 | 364 | $6,140 | -133.94 | -2.2% | -0.6 | 2057 | 1273 | $19,883 | +2,402.60 | +12.1% | 5.47 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 128 | +15.4% | 2.17 | 57 | -1.6% | -0.05 |
| conviction:1-2x | 134 | +31.5% | 2.94 | 46 | -6.4% | -0.59 |
| conviction:2x+ | 868 | +18.2% | 5.13 | 431 | +1.4% | 0.12 |
| conviction:under 0.5x | 234 | +18.2% | 3.06 | 75 | -16.4% | -1.31 |
| delay_move:flat | 934 | +23.0% | 6.61 | 413 | -9.6% | -2.14 |
| delay_move:price fell | 430 | +11.5% | 2.54 | 196 | +14.6% | 1.5 |
| exit:settle | 1364 | +19.3% | 6.98 | 609 | -1.6% | -0.47 |
| kind:moneyline | 891 | +22.6% | 6.23 | 317 | -5.2% | -1.06 |
| kind:result | 240 | +14.9% | 2.69 | 163 | -2.8% | -0.2 |
| kind:totals | 233 | +11.1% | 1.82 | 129 | +8.5% | 0.76 |
| league:bra | 8 | +77.6% | 2.99 | 5 | -29.9% | -0.99 |
| league:cfb | 42 | +0.4% | 0.07 | 26 | +10.6% | 0.4 |
| league:cs2 | 200 | +16.4% | 2.48 | 85 | -10.8% | -1.6 |
| league:dota2 | 34 | +5.0% | 0.33 | 2 | +52.9% | 1.49 |
| league:epl | 17 | +61.3% | 4.82 | 41 | -12.6% | -0.87 |
| league:lal | 63 | -8.2% | -0.79 | 27 | +18.1% | 0.26 |
| league:lol | 68 | +6.3% | 0.55 | 29 | -28.1% | -1.61 |
| league:mlb | 407 | +17.2% | 3.86 | 48 | +1.1% | 0.11 |
| league:mls | 61 | +1.9% | 0.24 | 66 | +5.1% | 0.54 |
| league:nfl | 267 | +29.3% | 3.58 | 84 | +11.8% | 1.36 |
| league:nhl | 125 | +25.9% | 3.32 | 106 | -8.6% | -1.1 |
| league:sea | 64 | +41.1% | 3.5 | 60 | +15.8% | 1.79 |
| price:30-70c | 1027 | +17.7% | 6.08 | 415 | -1.2% | -0.33 |
| price:over 70c | 219 | +4.2% | 1.37 | 145 | +0.5% | 0.29 |
| price:under 30c | 118 | +59.4% | 3.37 | 49 | -11.6% | -0.49 |
| timing:in-play | 300 | +13.7% | 2.32 | 208 | +2.9% | 0.43 |
| timing:pre-game | 1064 | +20.9% | 6.63 | 401 | -4.1% | -1.04 |

## Final picks (whole window, copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 21 | 20 | +50.1% | 3.88 | +4.94 |
| 0010001000001100 | 35 | 22 | +69.8% | 1.69 | +6.76 |
| totoro3miyazaki | 33 | 26 | +41.3% | 2.69 | +4.06 |
| 1l2ihj34li12u34 | 28 | 20 | +40.6% | 2.34 | +4.27 |
| BreakTheBank | 130 | 72 | +35.5% | 2.91 | +3.61 |
| yabanci | 23 | 17 | +34.4% | 2.22 | +4.02 |
| theowalcott | 67 | 46 | +31.2% | 2.85 | +3.31 |
| EdZachary | 50 | 33 | +33.2% | 2.4 | +3.38 |
| 0x20D6436849F930584892730C7F | 130 | 76 | +33.7% | 2.19 | +3.44 |
| juice-fruit | 30 | 23 | +29.4% | 1.92 | +2.99 |
| 0x16bb9951a36fce71e2ef57890b | 385 | 227 | +16.6% | 3.22 | +1.68 |
| Kch-Temp | 50 | 31 | +26.4% | 1.69 | +2.62 |
| GamblingOdyssey | 57 | 43 | +19.4% | 1.84 | +1.92 |
| plonker2026 | 34 | 19 | +22.9% | 1.36 | +3.06 |
| xxyx0xx | 112 | 60 | +23.7% | 1.41 | +2.24 |
| monkeymashingkeyboard | 606 | 348 | +10.7% | 2.5 | +1.05 |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 311 | 134 | -6.2% | -0.87 | no |
| para-Vision | 209 | 105 | -11.7% | -1.72 | no |
| Kch-Temp | 50 | 31 | +26.4% | 1.69 | yes |
| EdZachary | 50 | 33 | +33.2% | 2.4 | yes |
| ColdBlooded | 224 | 162 | -11.0% | -2.53 | no |
| KaneAnalytics | 93 | 53 | +6.8% | 0.48 | no |
| Jsram | 49 | 24 | -16.4% | -1.21 | no |
| Kkunn | 35 | 12 | -30.3% | -1.72 | no |
| Sisyphus- | 67 | 41 | +1.8% | 0.16 | no |
| PEYZ-BIGGEST-FAN | 186 | 103 | +6.8% | 1.01 | no |
| theowalcott | 67 | 46 | +31.2% | 2.85 | yes |
| HVAB | 1 | 0 | -100.0% | None | no |
| BreakTheBank | 130 | 72 | +35.5% | 2.91 | yes |
| Diabolical-Prize | 261 | 133 | +5.8% | 1.07 | no |
| Talvez10 | 267 | 135 | -2.5% | -0.79 | no |
