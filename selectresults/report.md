# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-22 09:00 UTC: 2171 candidates, 1438 with trades copytop could copy, 173 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3706 | 1935 | $36,318 | +387.82 | +1.1% | +0.81 |
| every wallet that qualified on the first part (test window) | 14405 | 7369 | $141,619 | -5,820.19 | -4.1% | -4.08 |
| currently copied (test window) | 4282 | 2311 | $42,038 | +2,914.27 | +6.9% | +4.13 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3706 | 1935 | $36,318 | +387.82 | +1.1% | 0.81 | 10890 | 6016 | $106,207 | +6,139.46 | +5.8% | 5.41 |
| copy their sells too | 3707 | 1878 | $36,328 | -179.33 | -0.5% | -0.06 | 10891 | 5891 | $106,217 | +4,684.02 | +4.4% | 4.31 |
| size by conviction (x0.5 / x1 / x1.5) | 3609 | 1876 | $44,660 | +641.32 | +1.4% | 0.55 | 10470 | 5778 | $128,974 | +7,091.68 | +5.5% | 5.21 |
| skip bets under 0.5x their usual | 3531 | 1854 | $34,756 | +549.07 | +1.6% | 1.05 | 10387 | 5737 | $101,573 | +5,918.73 | +5.8% | 5.28 |
| pre-game only | 2901 | 1547 | $28,210 | +572.00 | +2.0% | 1.28 | 8385 | 4724 | $81,091 | +5,600.58 | +6.9% | 5.97 |
| 15s delay | 3794 | 1980 | $37,186 | +392.32 | +1.1% | 0.83 | 11195 | 6224 | $109,211 | +6,865.05 | +6.3% | 5.93 |
| 60s delay | 3706 | 1935 | $36,318 | +387.82 | +1.1% | 0.81 | 10890 | 6016 | $106,207 | +6,139.46 | +5.8% | 5.41 |
| allow 2c over their price | 3875 | 2023 | $37,949 | +406.51 | +1.1% | 0.85 | 11395 | 6304 | $111,132 | +6,624.30 | +6.0% | 5.64 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 976 | +7.6% | 2.64 | 636 | +1.2% | 0.41 |
| conviction:1-2x | 950 | +6.5% | 1.58 | 348 | -9.7% | -1.52 |
| conviction:2x+ | 4499 | +8.3% | 4.56 | 2305 | +3.2% | 1.26 |
| conviction:under 0.5x | 759 | +10.8% | 2.61 | 417 | -2.3% | 0.13 |
| delay_move:flat | 4535 | +10.4% | 5.85 | 2134 | +3.1% | 1.48 |
| delay_move:price fell | 2649 | +4.7% | 2.1 | 1572 | -1.5% | -0.53 |
| exit:settle | 7184 | +8.2% | 6.0 | 3706 | +1.1% | 0.81 |
| kind:moneyline | 5366 | +8.9% | 5.46 | 3065 | +1.3% | 0.85 |
| kind:result | 1035 | +10.2% | 2.8 | 379 | +5.4% | 1.07 |
| kind:totals | 783 | +0.9% | 0.38 | 262 | -8.6% | -1.52 |
| league:atp | 1636 | +8.2% | 2.94 | 1184 | -5.2% | -1.55 |
| league:bra | 50 | +31.2% | 2.47 | 14 | +23.8% | 0.55 |
| league:bun | 10 | +53.1% | 7.25 | 5 | -100.0% | — |
| league:cfb | 28 | -46.9% | -3.22 | 158 | +9.7% | 1.03 |
| league:cs2 | 241 | +17.5% | 2.8 | 154 | -12.3% | -1.46 |
| league:dota2 | 65 | +36.7% | 2.09 | 87 | -12.0% | -0.95 |
| league:ecu1 | 21 | +0.4% | 0.02 | 5 | +10.6% | 0.22 |
| league:epl | 60 | +28.8% | 2.87 | 41 | -23.1% | -1.85 |
| league:ere | 11 | +21.4% | 0.97 | 19 | +85.0% | 3.15 |
| league:isl1 | 7 | +17.4% | 0.53 | 3 | -100.0% | — |
| league:lal | 66 | -3.1% | -0.3 | 18 | +65.8% | 1.0 |
| league:lib | 21 | +39.8% | 2.39 | 9 | +75.3% | 45.75 |
| league:lol | 858 | +18.4% | 3.16 | 244 | -8.1% | -1.22 |
| league:mlb | 2315 | +2.0% | 0.96 | 475 | +4.4% | 1.15 |
| league:mls | 97 | +13.3% | 1.44 | 49 | -15.9% | -1.07 |
| league:nba | 0 | +0.0% | — | 85 | +4.3% | 0.48 |
| league:nfl | 169 | +22.2% | 1.96 | 189 | +26.4% | 2.41 |
| league:nhl | 0 | +0.0% | — | 44 | +32.1% | 2.06 |
| league:nwsl | 13 | -24.3% | -0.91 | 7 | +19.1% | 0.62 |
| league:sea | 98 | +25.0% | 2.69 | 57 | -31.3% | -2.88 |
| league:spl | 27 | +16.7% | 0.91 | 11 | +5.3% | 0.29 |
| league:swe2 | 4 | -27.3% | -0.36 | 7 | +26.2% | 0.92 |
| league:uel | 53 | -26.8% | -2.64 | 0 | +0.0% | — |
| league:uslc | 11 | +109.7% | 6.07 | 15 | +17.2% | 0.78 |
| league:uzb1 | 12 | -28.6% | -1.23 | 0 | +0.0% | — |
| league:wnba | 132 | +15.6% | 2.27 | 41 | -46.0% | -3.74 |
| league:wta | 1165 | +5.1% | 1.32 | 768 | +8.6% | 2.02 |
| price:30-70c | 5417 | +3.0% | 2.32 | 2727 | +3.4% | 2.0 |
| price:over 70c | 1134 | +4.4% | 3.29 | 505 | +1.4% | 0.57 |
| price:under 30c | 633 | +57.0% | 5.93 | 474 | -11.9% | -1.34 |
| timing:in-play | 1700 | +4.2% | 1.25 | 805 | -2.3% | -0.42 |
| timing:pre-game | 5484 | +9.5% | 6.33 | 2901 | +2.0% | 1.28 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 99438 | 50474 | $986,480 | -40,762.36 | -4.1% | -11.11 |
| consistency (winning weeks), top 16 | 8797 | 4713 | $86,514 | -1,364.64 | -1.6% | -1.23 |
| consistency (winning weeks), top 40 | 19001 | 9832 | $188,114 | -5,747.23 | -3.1% | -3.36 |
| copy return, average, top 16 | 4659 | 2383 | $46,255 | -1,017.99 | -2.2% | -1.07 |
| copy return, average, top 40 | 22095 | 11414 | $218,633 | -3,317.82 | -1.5% | -1.82 |
| copy return, lower bound, top 16 | 5852 | 3130 | $57,309 | -631.51 | -1.1% | -0.54 |
| copy return, lower bound, top 40 | 25797 | 13545 | $254,532 | -5,753.49 | -2.3% | -3.22 |
| most active, top 16 | 24327 | 12263 | $241,397 | -14,203.72 | -5.9% | -8.12 |
| most active, top 40 | 46036 | 23417 | $456,490 | -21,949.30 | -4.8% | -9.00 |
| win rate vs the odds, top 16 | 4101 | 2082 | $40,495 | -1,252.10 | -3.1% | -1.52 |
| win rate vs the odds, top 40 | 20644 | 10591 | $205,022 | -3,982.23 | -1.9% | -2.28 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| 0010001000001100 | 35 | 21 | +61.6% | 1.49 | +5.95 |
| 1l2ihj34li12u34 | 36 | 27 | +49.3% | 3.29 | +5.07 |
| BunCaCham | 43 | 39 | +35.9% | 2.6 | +3.46 |
| theowalcott | 71 | 50 | +38.1% | 3.46 | +3.94 |
| 0x20D6436849F930584892730C7F | 148 | 86 | +30.1% | 2.16 | +3.05 |
| plonker2026 | 86 | 53 | +22.2% | 2.28 | +2.81 |
| yabanci | 25 | 17 | +22.8% | 1.58 | +2.91 |
| BreakTheBank | 350 | 181 | +10.5% | 1.96 | +1.31 |
| totoro3miyazaki | 39 | 29 | +28.0% | 1.96 | +2.76 |
| tiger105 | 46 | 30 | +21.9% | 1.57 | +2.20 |
| juice-fruit | 32 | 24 | +26.3% | 1.77 | +2.69 |
| eokho | 708 | 384 | +3.7% | 0.68 | +0.32 |
| THEHIGHLIFE | 518 | 226 | +12.4% | 1.67 | +1.26 |
| xxyx0xx | 209 | 109 | +17.3% | 1.35 | +1.62 |
| 0x16bb9951a36fce71e2ef57890b | 868 | 472 | +6.3% | 1.9 | +0.65 |
| KaneAnalytics | 91 | 54 | +12.3% | 0.88 | +1.21 |
| smithagent | 661 | 353 | +7.9% | 1.09 | +0.76 |
| monkeymashingkeyboard | 1955 | 1100 | +7.1% | 3.07 | +0.69 |
| GamblingOdyssey | 415 | 211 | +7.5% | 1.46 | +0.86 |
| cosmicsteaks | 1332 | 573 | -2.1% | -0.54 | -0.23 |
| Diabolical-Prize | 287 | 148 | +6.2% | 1.15 | +0.77 |
| PEYZ-BIGGEST-FAN | 357 | 182 | +5.6% | 0.83 | +0.63 |
| AmericaFirst1 | 498 | 312 | +6.6% | 1.6 | +0.67 |
| Kkunn | 619 | 271 | +7.5% | 1.49 | +0.86 |
| jiafan | 941 | 559 | +2.5% | 0.59 | +0.21 |
| slimjoe | 694 | 335 | -8.9% | -2.33 | -0.87 |
| shoemanhere | 379 | 157 | -8.4% | -1.17 | -0.84 |
| MurkSniper | 607 | 400 | -1.8% | -0.49 | -0.17 |
| n1ck10s | 914 | 491 | +3.2% | 0.86 | +0.32 |
| UNEB3154s4f251 | 1889 | 1188 | +3.3% | 1.79 | +0.34 |
| TAIWANNUMBERONE | 1560 | 813 | -6.4% | -2.46 | -0.65 |
| 0xf12f7688A0bC8Cc744eF871f70 | 760 | 304 | +4.4% | 0.75 | +0.41 |
| mepawn | 592 | 258 | -5.2% | -0.76 | -0.53 |
| TheRomanProcurator | 3341 | 1667 | +2.2% | 0.97 | +0.22 |
| torta.tech | 1759 | 1047 | -1.7% | -0.72 | -0.16 |
| littlebay | 695 | 456 | +2.0% | 0.51 | +0.20 |
| ic4cream | 799 | 463 | +2.2% | 0.56 | +0.20 |
| nightcity2077 | 1039 | 485 | -1.4% | -0.28 | -0.13 |
| JustADonk | 719 | 432 | +3.0% | 0.65 | +0.26 |
| madkkee | 570 | 409 | +0.5% | 0.21 | +0.06 |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 299 | 130 | -4.0% | -0.64 | no |
| Kch-Temp | 130 | 58 | -8.3% | -0.75 | no |
| EdZachary | 76 | 36 | -3.5% | -0.3 | no |
| KaneAnalytics | 91 | 54 | +12.3% | 0.88 | yes |
| Jsram | 57 | 28 | -16.0% | -1.31 | no |
| Kkunn | 619 | 271 | +7.5% | 1.49 | yes |
| Sisyphus- | 115 | 68 | -1.8% | -0.21 | no |
| PEYZ-BIGGEST-FAN | 357 | 182 | +5.6% | 0.83 | yes |
| theowalcott | 71 | 50 | +38.1% | 3.46 | yes |
| HVAB | 312 | 195 | +0.1% | 0.03 | no |
| BreakTheBank | 350 | 181 | +10.5% | 1.96 | yes |
| Diabolical-Prize | 287 | 148 | +6.2% | 1.15 | yes |
| Talvez10 | 581 | 309 | +2.6% | 0.33 | no |
| BunCaCham | 43 | 39 | +35.9% | 2.6 | yes |
| 0010001000001100 | 35 | 21 | +61.6% | 1.49 | yes |
| totoro3miyazaki | 39 | 29 | +28.0% | 1.96 | yes |
| 1l2ihj34li12u34 | 36 | 27 | +49.3% | 3.29 | yes |
| yabanci | 25 | 17 | +22.8% | 1.58 | yes |
| 0x20D6436849F930584892730C7F | 148 | 86 | +30.1% | 2.16 | yes |
| juice-fruit | 32 | 24 | +26.3% | 1.77 | yes |
| 0x16bb9951a36fce71e2ef57890b | 868 | 472 | +6.3% | 1.9 | yes |
| GamblingOdyssey | 415 | 211 | +7.5% | 1.46 | yes |
| plonker2026 | 86 | 53 | +22.2% | 2.28 | yes |
| xxyx0xx | 209 | 109 | +17.3% | 1.35 | yes |
| monkeymashingkeyboard | 1955 | 1100 | +7.1% | 3.07 | yes |
| Tiger105 | 46 | 30 | +21.9% | 1.57 | yes |
| THEHIGHLIFE | 518 | 226 | +12.4% | 1.67 | yes |
| AmericaFirst1 | 498 | 312 | +6.6% | 1.6 | yes |
| UNEB3154s4f251 | 1889 | 1188 | +3.3% | 1.79 | yes |
