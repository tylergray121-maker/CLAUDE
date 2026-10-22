# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-22 06:00 UTC: 2172 candidates, 1439 with trades copytop could copy, 175 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3754 | 1907 | $36,875 | +5.82 | +0.0% | +0.21 |
| every wallet that qualified on the first part (test window) | 14503 | 7369 | $142,654 | -6,221.28 | -4.4% | -4.31 |
| currently copied (test window) | 3393 | 1839 | $32,892 | +2,016.77 | +6.1% | +3.18 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3754 | 1907 | $36,875 | +5.82 | +0.0% | 0.21 | 10773 | 5841 | $105,220 | +5,925.70 | +5.6% | 5.03 |
| copy their sells too | 3755 | 1850 | $36,885 | -616.48 | -1.7% | -0.72 | 10774 | 5716 | $105,230 | +4,319.34 | +4.1% | 3.84 |
| size by conviction (x0.5 / x1 / x1.5) | 3651 | 1845 | $44,842 | +208.91 | +0.5% | -0.04 | 10339 | 5594 | $126,087 | +6,695.86 | +5.3% | 4.81 |
| skip bets under 0.5x their usual | 3596 | 1848 | $35,440 | +274.31 | +0.8% | 0.61 | 10364 | 5637 | $101,422 | +5,543.70 | +5.5% | 4.85 |
| pre-game only | 2770 | 1463 | $26,926 | +207.17 | +0.8% | 0.62 | 7796 | 4386 | $75,257 | +5,205.05 | +6.9% | 5.69 |
| 15s delay | 3861 | 1957 | $37,938 | -56.00 | -0.1% | 0.15 | 11129 | 6068 | $108,750 | +6,579.11 | +6.0% | 5.49 |
| 60s delay | 3754 | 1907 | $36,875 | +5.82 | +0.0% | 0.21 | 10773 | 5841 | $105,220 | +5,925.70 | +5.6% | 5.03 |
| allow 2c over their price | 3938 | 2003 | $38,660 | +107.87 | +0.3% | 0.38 | 11312 | 6150 | $110,502 | +6,614.64 | +6.0% | 5.41 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 1063 | +7.9% | 2.59 | 680 | +2.5% | 0.63 |
| conviction:1-2x | 1153 | +4.0% | 0.99 | 448 | -10.0% | -1.68 |
| conviction:2x+ | 4137 | +9.2% | 4.73 | 2227 | +2.3% | 0.87 |
| conviction:under 0.5x | 666 | +14.9% | 2.84 | 399 | -5.8% | -0.47 |
| delay_move:flat | 4188 | +10.8% | 5.72 | 2032 | +1.1% | 0.7 |
| delay_move:price fell | 2831 | +5.7% | 2.45 | 1722 | -1.2% | -0.43 |
| exit:settle | 7019 | +8.7% | 6.01 | 3754 | +0.0% | 0.21 |
| kind:moneyline | 5507 | +9.0% | 5.41 | 3203 | -0.1% | 0.1 |
| kind:result | 1038 | +9.9% | 2.71 | 379 | +5.4% | 1.07 |
| kind:totals | 474 | +1.6% | 0.42 | 172 | -9.4% | -1.36 |
| league:atp | 2108 | +8.0% | 3.0 | 1417 | -4.8% | -1.4 |
| league:bra | 50 | +31.2% | 2.47 | 14 | +23.8% | 0.55 |
| league:bun | 10 | +53.1% | 7.25 | 5 | -100.0% | — |
| league:cfb | 17 | -11.5% | -0.56 | 136 | -3.0% | -0.17 |
| league:cs2 | 242 | +18.3% | 2.91 | 154 | -12.3% | -1.46 |
| league:dota2 | 65 | +36.7% | 2.09 | 87 | -12.0% | -0.95 |
| league:ecu1 | 21 | +0.4% | 0.02 | 5 | +10.6% | 0.22 |
| league:epl | 60 | +28.8% | 2.87 | 41 | -23.1% | -1.85 |
| league:ere | 11 | +21.4% | 0.97 | 19 | +85.0% | 3.15 |
| league:isl1 | 7 | +17.4% | 0.53 | 3 | -100.0% | — |
| league:lal | 67 | -4.6% | -0.47 | 18 | +65.8% | 1.0 |
| league:lib | 21 | +39.8% | 2.39 | 9 | +75.3% | 45.75 |
| league:lol | 861 | +18.4% | 3.16 | 244 | -8.1% | -1.22 |
| league:mlb | 1657 | +0.8% | 0.26 | 313 | +2.4% | 0.59 |
| league:mls | 97 | +13.3% | 1.44 | 49 | -15.9% | -1.07 |
| league:nba | 0 | +0.0% | — | 85 | +4.3% | 0.48 |
| league:nfl | 164 | +19.5% | 1.7 | 180 | +29.8% | 2.65 |
| league:nhl | 0 | +0.0% | — | 44 | +32.1% | 2.06 |
| league:nwsl | 13 | -24.3% | -0.91 | 7 | +19.1% | 0.62 |
| league:sea | 98 | +25.0% | 2.69 | 57 | -31.3% | -2.88 |
| league:spl | 27 | +16.7% | 0.91 | 11 | +5.3% | 0.29 |
| league:swe2 | 4 | -27.3% | -0.36 | 7 | +26.2% | 0.92 |
| league:uel | 53 | -26.8% | -2.64 | 0 | +0.0% | — |
| league:uslc | 11 | +109.7% | 6.07 | 15 | +17.2% | 0.78 |
| league:uzb1 | 12 | -28.6% | -1.23 | 0 | +0.0% | — |
| league:wnba | 132 | +15.6% | 2.27 | 41 | -46.0% | -3.74 |
| league:wta | 1197 | +5.6% | 1.47 | 776 | +8.0% | 1.91 |
| price:30-70c | 5155 | +2.4% | 1.75 | 2703 | +1.4% | 0.96 |
| price:over 70c | 1127 | +4.3% | 3.23 | 509 | +1.4% | 0.58 |
| price:under 30c | 737 | +56.7% | 6.42 | 542 | -7.6% | -0.88 |
| timing:in-play | 1993 | +4.6% | 1.41 | 984 | -2.0% | -0.4 |
| timing:pre-game | 5026 | +10.3% | 6.45 | 2770 | +0.8% | 0.62 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 99565 | 50535 | $987,669 | -41,152.27 | -4.2% | -11.21 |
| consistency (winning weeks), top 16 | 8836 | 4830 | $86,949 | -1,311.80 | -1.5% | -1.20 |
| consistency (winning weeks), top 40 | 19387 | 10041 | $191,912 | -5,154.60 | -2.7% | -2.95 |
| copy return, average, top 16 | 4642 | 2360 | $46,083 | -1,215.05 | -2.6% | -1.31 |
| copy return, average, top 40 | 21256 | 10819 | $210,434 | -3,657.61 | -1.7% | -2.06 |
| copy return, lower bound, top 16 | 5688 | 3020 | $55,549 | -1,231.95 | -2.2% | -1.28 |
| copy return, lower bound, top 40 | 25529 | 13370 | $251,899 | -6,891.33 | -2.7% | -3.86 |
| most active, top 16 | 24197 | 12220 | $240,000 | -13,305.42 | -5.5% | -7.57 |
| most active, top 40 | 46107 | 23460 | $457,178 | -22,080.20 | -4.8% | -9.03 |
| win rate vs the odds, top 16 | 4441 | 2318 | $43,776 | -1,864.20 | -4.3% | -2.39 |
| win rate vs the odds, top 40 | 20628 | 10588 | $204,789 | -5,143.84 | -2.5% | -2.98 |

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
| tiger105 | 45 | 30 | +24.6% | 1.75 | +2.47 |
| yabanci | 25 | 17 | +22.8% | 1.58 | +2.91 |
| BreakTheBank | 350 | 181 | +10.5% | 1.96 | +1.31 |
| totoro3miyazaki | 39 | 29 | +28.0% | 1.96 | +2.76 |
| juice-fruit | 32 | 24 | +26.3% | 1.77 | +2.69 |
| eokho | 709 | 385 | +3.3% | 0.6 | +0.28 |
| THEHIGHLIFE | 519 | 226 | +12.2% | 1.64 | +1.24 |
| xxyx0xx | 209 | 109 | +17.3% | 1.35 | +1.62 |
| 0x16bb9951a36fce71e2ef57890b | 868 | 472 | +6.3% | 1.9 | +0.65 |
| KaneAnalytics | 91 | 54 | +12.3% | 0.88 | +1.21 |
| smithagent | 661 | 353 | +7.9% | 1.09 | +0.76 |
| monkeymashingkeyboard | 1956 | 1101 | +7.2% | 3.11 | +0.70 |
| GamblingOdyssey | 414 | 210 | +7.4% | 1.44 | +0.85 |
| Kkunn | 611 | 266 | +7.2% | 1.43 | +0.83 |
| cosmicsteaks | 1332 | 573 | -2.1% | -0.54 | -0.23 |
| Diabolical-Prize | 287 | 148 | +6.2% | 1.15 | +0.77 |
| PEYZ-BIGGEST-FAN | 360 | 182 | +4.7% | 0.72 | +0.54 |
| AmericaFirst1 | 497 | 312 | +6.8% | 1.65 | +0.69 |
| jiafan | 950 | 564 | +2.9% | 0.7 | +0.25 |
| slimjoe | 694 | 335 | -8.8% | -2.32 | -0.86 |
| shoemanhere | 379 | 157 | -8.4% | -1.17 | -0.84 |
| MurkSniper | 606 | 399 | -1.8% | -0.49 | -0.18 |
| 0xf12f7688A0bC8Cc744eF871f70 | 761 | 305 | +4.5% | 0.78 | +0.43 |
| TAIWANNUMBERONE | 1587 | 817 | -7.6% | -2.96 | -0.77 |
| UNEB3154s4f251 | 1886 | 1186 | +3.3% | 1.79 | +0.34 |
| mepawn | 592 | 258 | -5.2% | -0.76 | -0.53 |
| littlebay | 691 | 454 | +2.3% | 0.57 | +0.23 |
| TheRomanProcurator | 3334 | 1664 | +2.2% | 0.96 | +0.22 |
| n1ck10s | 907 | 486 | +2.2% | 0.6 | +0.22 |
| torta.tech | 1759 | 1047 | -1.7% | -0.72 | -0.16 |
| Sisyphus- | 114 | 68 | -0.9% | -0.1 | -0.09 |
| ic4cream | 799 | 463 | +2.2% | 0.56 | +0.20 |
| JustADonk | 720 | 432 | +2.9% | 0.61 | +0.24 |
| nightcity2077 | 1041 | 486 | -1.5% | -0.3 | -0.14 |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 299 | 130 | -4.0% | -0.64 | no |
| para-Vision | 210 | 103 | -15.0% | -2.25 | no |
| Kch-Temp | 133 | 60 | -4.3% | -0.36 | no |
| EdZachary | 76 | 36 | -3.5% | -0.3 | no |
| ColdBlooded | 219 | 158 | -11.0% | -2.5 | no |
| KaneAnalytics | 91 | 54 | +12.3% | 0.88 | yes |
| Jsram | 57 | 28 | -16.0% | -1.31 | no |
| Kkunn | 611 | 266 | +7.2% | 1.43 | yes |
| Sisyphus- | 114 | 68 | -0.9% | -0.1 | yes |
| PEYZ-BIGGEST-FAN | 360 | 182 | +4.7% | 0.72 | yes |
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
| GamblingOdyssey | 414 | 210 | +7.4% | 1.44 | yes |
| plonker2026 | 86 | 53 | +22.2% | 2.28 | yes |
| xxyx0xx | 209 | 109 | +17.3% | 1.35 | yes |
| monkeymashingkeyboard | 1956 | 1101 | +7.2% | 3.11 | yes |
| Tiger105 | 45 | 30 | +24.6% | 1.75 | yes |
