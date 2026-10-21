# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 45 days to 2026-10-21 21:00 UTC: 267 candidates, 88 with trades copytop could copy, 21 re-priced at a 30s copy delay. Choosing window: first 67%; test window: the rest (15 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 379 | 220 | $3,613 | +161.19 | +4.5% | +1.13 |
| all re-priced wallets (test window) | 2372 | 1239 | $23,165 | +1,531.51 | +6.6% | +2.88 |
| currently copied (test window) | 1771 | 913 | $17,438 | +367.41 | +2.1% | +1.09 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| as copytop runs (30s delay, copy sells) | 379 | 220 | $3,613 | +161.19 | +4.5% | 1.13 | 889 | 530 | $8,528 | +1,005.10 | +11.8% | 3.8 |
| hold to settlement (ignore their sells) | 379 | 223 | $3,613 | +190.71 | +5.3% | 1.29 | 889 | 543 | $8,528 | +1,076.28 | +12.6% | 4.05 |
| 15s delay | 389 | 226 | $3,714 | +147.22 | +4.0% | 1.06 | 901 | 536 | $8,647 | +968.73 | +11.2% | 3.66 |
| 60s delay | 379 | 218 | $3,614 | +117.45 | +3.2% | 0.9 | 886 | 527 | $8,499 | +958.64 | +11.3% | 3.65 |
| allow 2c over their price | 405 | 236 | $3,859 | +128.79 | +3.3% | 0.98 | 937 | 559 | $8,992 | +969.90 | +10.8% | 3.64 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 52 | +28.0% | 2.12 | 48 | +1.2% | 0.35 |
| conviction:1-2x | 50 | +24.8% | 1.34 | 25 | -0.7% | -0.02 |
| conviction:2x+ | 318 | +14.8% | 2.73 | 255 | +9.6% | 1.57 |
| conviction:under 0.5x | 90 | +15.7% | 1.83 | 51 | -17.8% | -0.84 |
| delay_move:flat | 388 | +19.0% | 3.84 | 306 | +4.0% | 1.03 |
| delay_move:price fell | 122 | +11.6% | 1.36 | 73 | +6.3% | 0.48 |
| exit:sell | 15 | -20.3% | -2.37 | 3 | -9.7% | -17.14 |
| exit:settle | 495 | +18.3% | 4.18 | 376 | +4.6% | 1.15 |
| kind:moneyline | 207 | +17.6% | 2.38 | 143 | +5.6% | 0.87 |
| kind:result | 170 | +7.6% | 0.9 | 130 | +19.1% | 2.53 |
| kind:totals | 133 | +28.9% | 4.19 | 106 | -15.1% | -1.65 |
| league:atp | 30 | +19.7% | 0.86 | 19 | -39.8% | -1.3 |
| league:bun | 7 | +26.6% | 1.26 | 4 | -45.2% | -0.87 |
| league:cfb | 34 | +18.9% | 1.03 | 14 | +6.4% | 0.29 |
| league:cs2 | 12 | -21.1% | -1.23 | 13 | +23.0% | 0.92 |
| league:dota2 | 21 | +1.7% | 0.11 | 9 | +7.0% | 0.2 |
| league:epl | 78 | +8.3% | 0.59 | 75 | +13.2% | 1.42 |
| league:lal | 22 | +9.9% | 0.53 | 3 | -1.3% | -0.04 |
| league:lol | 54 | +8.9% | 0.75 | 49 | +12.6% | 0.95 |
| league:mlb | 7 | +93.2% | 2.4 | 4 | -32.4% | -1.43 |
| league:mls | 32 | -3.1% | -0.02 | 26 | +22.3% | 1.32 |
| league:nfl | 75 | +47.2% | 4.53 | 11 | +80.5% | 1.42 |
| league:nhl | 83 | +17.1% | 1.74 | 113 | -22.1% | -2.32 |
| league:sea | 25 | +35.9% | 1.83 | 10 | +4.6% | 0.11 |
| league:uel | 2 | -100.0% | — | 14 | +36.0% | 2.64 |
| league:wta | 13 | -73.0% | -5.22 | 0 | +0.0% | — |
| price:30-70c | 476 | +16.8% | 4.03 | 336 | +3.5% | 0.91 |
| price:over 70c | 18 | -21.0% | -1.72 | 32 | +17.5% | 2.7 |
| price:under 30c | 16 | +71.0% | 1.45 | 11 | -2.6% | -0.04 |
| timing:in-play | 74 | -1.6% | -0.13 | 61 | +5.1% | 0.42 |
| timing:pre-game | 436 | +20.5% | 4.36 | 318 | +4.3% | 1.05 |

## Final picks (whole window, copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| 1l2ihj34li12u34 | 47 | 35 | +48.0% | 3.7 | +5.01 |
| EdZachary | 74 | 50 | +38.1% | 3.36 | +3.95 |
| theowalcott | 78 | 52 | +29.3% | 2.79 | +3.07 |
| 0xd4aa6f8e91cfea29b66a48ebff | 56 | 33 | +33.4% | 2.08 | +3.74 |
| totoro3miyazaki | 51 | 36 | +28.1% | 2.08 | +2.75 |
| Jsram | 161 | 107 | +14.4% | 2.21 | +1.45 |
| Kch-Temp | 175 | 100 | +12.1% | 1.6 | +1.32 |
| monkeymashingkeyboard | 1020 | 553 | +6.0% | 1.78 | +0.62 |
| Soarin22 | 181 | 84 | +7.0% | 1.16 | +1.23 |
| www511zwin | 24 | 14 | +23.6% | 1.06 | +2.42 |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 1226 | 549 | -7.5% | -2.29 | no |
| para-Vision | 368 | 202 | +1.0% | 0.3 | no |
| Kch-Temp | 175 | 100 | +12.1% | 1.6 | yes |
| EdZachary | 74 | 50 | +38.1% | 3.36 | yes |
| ColdBlooded | 354 | 266 | +2.5% | 0.6 | no |
| KaneAnalytics | 156 | 83 | +3.1% | 0.32 | no |
| Jsram | 161 | 107 | +14.4% | 2.21 | yes |
| Kkunn | 642 | 264 | +1.2% | 0.52 | no |
| Sisyphus- | 191 | 114 | -2.6% | -0.4 | no |
| PEYZ-BIGGEST-FAN | 395 | 197 | -3.6% | -0.64 | no |
| theowalcott | 78 | 52 | +29.3% | 2.79 | yes |
| HVAB | 192 | 84 | -7.1% | -1.86 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | — | — | — | — | no copyable trades |
| Talvez10 | 402 | 195 | -5.8% | -1.39 | no |
