# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-28 09:00 UTC: 5512 candidates, 3819 with trades copytop could copy, 217 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 1218 | 575 | $11,961 | +74.41 | +0.6% | +0.37 |
| every wallet that qualified on the first part (test window) | 1826 | 881 | $18,104 | +216.30 | +1.2% | +0.50 |
| currently copied (test window) | 4323 | 2307 | $42,325 | +1,187.18 | +2.8% | +1.84 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 1218 | 575 | $11,961 | +74.41 | +0.6% | 0.37 | 4138 | 2024 | $40,220 | +3,207.76 | +8.0% | 3.77 |
| copy their sells too | 1218 | 566 | $11,961 | -34.67 | -0.3% | 0.13 | 4138 | 2003 | $40,220 | +2,994.58 | +7.4% | 3.54 |
| size by conviction (x0.5 / x1 / x1.5) | 1167 | 551 | $14,682 | +84.59 | +0.6% | 0.06 | 3917 | 1909 | $48,923 | +3,630.27 | +7.4% | 3.41 |
| skip bets under 0.5x their usual | 1157 | 539 | $11,400 | +93.49 | +0.8% | 0.41 | 3918 | 1907 | $38,375 | +3,075.64 | +8.0% | 3.66 |
| pre-game only | 1096 | 527 | $10,717 | +12.97 | +0.1% | 0.28 | 3725 | 1874 | $36,038 | +3,316.88 | +9.2% | 4.29 |
| skip prices under 30c | 940 | 499 | $9,197 | -301.02 | -3.3% | -0.98 | 3150 | 1744 | $30,437 | +333.47 | +1.1% | 0.83 |
| favorites only (50c+) | 458 | 321 | $4,421 | +300.63 | +6.8% | 2.2 | 1546 | 1084 | $14,693 | +719.68 | +4.9% | 2.9 |
| 15s delay | 1234 | 585 | $12,123 | +320.52 | +2.6% | 0.85 | 4192 | 2050 | $40,780 | +3,572.95 | +8.8% | 4.08 |
| 60s delay | 1218 | 575 | $11,961 | +74.41 | +0.6% | 0.37 | 4138 | 2024 | $40,220 | +3,207.76 | +8.0% | 3.77 |
| allow 2c over their price | 1283 | 604 | $12,581 | +231.90 | +1.8% | 0.68 | 4366 | 2136 | $42,447 | +3,578.09 | +8.4% | 4.0 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 310 | +8.1% | 1.2 | 114 | +10.9% | 0.81 |
| conviction:1-2x | 383 | +13.2% | 1.5 | 120 | -4.3% | -0.58 |
| conviction:2x+ | 1904 | +10.2% | 2.99 | 845 | +1.4% | 0.62 |
| conviction:under 0.5x | 323 | +17.4% | 2.37 | 139 | -8.5% | -0.87 |
| delay_move:flat | 1835 | +11.2% | 3.22 | 957 | +0.5% | 0.28 |
| delay_move:price fell | 1085 | +10.8% | 2.6 | 261 | +1.1% | 0.28 |
| exit:settle | 2920 | +11.1% | 4.13 | 1218 | +0.6% | 0.37 |
| kind:moneyline | 1972 | +8.6% | 2.46 | 831 | +0.4% | 0.24 |
| kind:result | 787 | +19.5% | 4.22 | 283 | +11.5% | 1.81 |
| kind:totals | 161 | +0.1% | 0.05 | 104 | -27.6% | -2.97 |
| league:atp | 282 | +18.5% | 2.24 | 175 | +3.3% | 0.6 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 2 | -100.0% | — | 12 | -2.9% | -0.05 |
| league:cs2 | 303 | +7.7% | 0.94 | 191 | +2.6% | 0.5 |
| league:dota2 | 78 | -9.1% | -0.64 | 110 | +29.0% | 1.79 |
| league:epl | 52 | +34.2% | 3.05 | 50 | -13.4% | -1.19 |
| league:ere | 4 | +97.0% | — | 32 | +34.7% | 1.3 |
| league:lal | 20 | +17.4% | 1.12 | 3 | -37.5% | -0.61 |
| league:lol | 1699 | +15.2% | 3.86 | 315 | -0.0% | 0.02 |
| league:mlb | 190 | -25.3% | -3.82 | 53 | -32.6% | -2.49 |
| league:mls | 17 | +29.2% | 1.38 | 15 | -34.4% | -1.33 |
| league:nfl | 45 | +34.7% | 1.7 | 7 | -17.3% | -0.39 |
| league:sea | 33 | +59.4% | 3.41 | 33 | -52.1% | -3.39 |
| league:ucl | 40 | -8.0% | -0.57 | 61 | +15.9% | 1.3 |
| league:uel | 8 | -100.0% | — | 12 | +17.4% | 0.79 |
| league:wnba | 0 | +0.0% | — | 11 | -63.8% | -3.0 |
| league:wta | 136 | -6.6% | -0.89 | 130 | +4.6% | 0.43 |
| price:30-70c | 1837 | +2.8% | 1.29 | 808 | -4.1% | -1.06 |
| price:over 70c | 369 | +4.1% | 1.93 | 127 | +1.0% | 0.16 |
| price:under 30c | 714 | +35.4% | 3.98 | 283 | +13.7% | 1.42 |
| timing:in-play | 291 | -5.8% | -0.7 | 122 | +4.9% | 0.3 |
| timing:pre-game | 2629 | +13.1% | 4.8 | 1096 | +0.1% | 0.28 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 154365 | 79838 | $1,533,457 | -65,595.58 | -4.3% | -14.44 |
| consistency (winning weeks), top 16 | 9781 | 5340 | $95,496 | -3,346.69 | -3.5% | -3.31 |
| consistency (winning weeks), top 40 | 22975 | 12031 | $226,559 | -7,957.59 | -3.5% | -4.44 |
| copy return, average, top 16 | 8352 | 4147 | $82,465 | -3,434.94 | -4.2% | -3.02 |
| copy return, average, top 40 | 24187 | 12555 | $239,095 | -9,908.22 | -4.1% | -5.41 |
| copy return, lower bound, top 16 | 8803 | 4674 | $86,857 | -3,530.65 | -4.1% | -3.21 |
| copy return, lower bound, top 40 | 26753 | 14512 | $264,181 | -10,496.23 | -4.0% | -5.73 |
| copy return, shrunk, top 16 | 8830 | 4433 | $87,021 | -5,043.37 | -5.8% | -4.34 |
| copy return, shrunk, top 40 | 24295 | 12606 | $240,186 | -10,073.18 | -4.2% | -5.49 |
| markout 2h, average, top 16 | 6213 | 3300 | $61,667 | -2,911.93 | -4.7% | -3.38 |
| markout 2h, average, top 40 | 20347 | 10652 | $202,467 | -5,543.76 | -2.7% | -3.22 |
| markout 2h, lower bound, top 16 | 8850 | 4681 | $88,115 | -3,765.76 | -4.3% | -3.33 |
| markout 2h, lower bound, top 40 | 25365 | 13136 | $250,492 | -7,093.31 | -2.8% | -3.97 |
| markout 30m, average, top 16 | 9355 | 4761 | $93,539 | -3,827.14 | -4.1% | -3.37 |
| markout 30m, average, top 40 | 23360 | 11886 | $233,078 | -10,497.53 | -4.5% | -5.62 |
| most active, top 16 | 28880 | 14603 | $286,461 | -14,345.22 | -5.0% | -7.38 |
| most active, top 40 | 50831 | 26185 | $503,950 | -24,359.79 | -4.8% | -9.63 |
| win rate vs the odds, top 16 | 7102 | 3564 | $69,363 | -2,541.03 | -3.7% | -2.93 |
| win rate vs the odds, top 40 | 22250 | 11521 | $219,542 | -8,730.97 | -4.0% | -5.13 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 49 | 45 | +29.7% | 3.56 | +2.90 |
| 0x20D6436849F930584892730C7F | 151 | 88 | +30.9% | 2.25 | +3.13 |
| tiger105 | 43 | 28 | +19.1% | 1.34 | +1.89 |
| xxyx0xx | 270 | 135 | +7.8% | 0.71 | +0.71 |
| 0x16bb9951a36fce71e2ef57890b | 805 | 437 | +6.0% | 1.76 | +0.63 |
| yabanci | 57 | 38 | +12.6% | 1.38 | +1.58 |
| platarb | 860 | 346 | +2.9% | 0.63 | +0.29 |
| juice-fruit | 45 | 31 | +13.6% | 1.09 | +1.43 |
| Sisyphus- | 126 | 74 | +2.3% | 0.27 | +0.23 |
| SimpleTony | 1215 | 389 | +8.6% | 1.66 | +0.86 |
| moreplatesmoredates | 973 | 489 | +1.3% | 0.55 | +0.23 |
| theowalcott | 92 | 51 | +4.3% | 0.58 | +0.59 |
| AmericaFirst1 | 515 | 321 | +5.5% | 1.36 | +0.56 |
| am100 | 988 | 587 | +11.4% | 3.13 | +1.15 |
| smithagent | 966 | 528 | +6.0% | 1.05 | +0.59 |
| plonker2026 | 142 | 78 | +7.6% | 1.27 | +1.17 |
| monkeymashingkeyboard | 1940 | 1077 | +5.0% | 2.17 | +0.49 |
| KaneAnalytics | 140 | 78 | +6.2% | 0.56 | +0.61 |
| 0xffAaEFb5f6762Cc70cb575Da87 | 688 | 326 | +2.4% | 0.38 | +0.22 |
| cosmicsteaks | 1318 | 570 | -2.3% | -0.57 | -0.25 |
| arahbo | 1626 | 696 | +1.3% | 0.24 | +0.11 |
| eskk | 1042 | 262 | -0.3% | 0.0 | +0.00 |
| walnutz | 632 | 326 | -1.7% | -0.41 | -0.18 |
| torta.tech | 1885 | 1122 | -1.4% | -0.58 | -0.13 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 1141 | 501 | +2.0% | 0.4 | +0.19 |
| GamblingOdyssey | 435 | 220 | +7.2% | 1.45 | +0.82 |
| UNEB3154s4f251 | 2179 | 1385 | +3.4% | 1.99 | +0.35 |
| jiafan | 1098 | 655 | +0.5% | 0.19 | +0.06 |
| ZEST011 | 712 | 532 | +2.8% | 1.1 | +0.27 |
| Talvez10 | 554 | 306 | +5.4% | 1.03 | +0.42 |
| MIracle33 | 903 | 454 | +5.2% | 1.35 | +0.51 |
| 1l2ihj34li12u34 | 87 | 50 | +14.2% | 1.5 | +1.66 |
| 0010001000001100 | 153 | 72 | -0.8% | -0.35 | -0.43 |
| n1ck10s | 1055 | 562 | +1.7% | 0.49 | +0.17 |
| Future-Tarot-Trader | 2113 | 1073 | -0.8% | -0.33 | -0.11 |
| iseedota | 1277 | 560 | -1.5% | -0.38 | -0.15 |
| Jsram | 95 | 56 | +0.0% | 0.21 | +0.19 |
| Petal | 927 | 437 | -6.7% | -1.7 | -0.67 |
| yuxkc0 | 435 | 143 | -7.3% | -0.94 | -0.72 |
| littlebay | 771 | 510 | +1.3% | 0.36 | +0.13 |

## Esports specialists (copies on esports markets only)

2947 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 164 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | tag | 76 | 43 | +48.6% | 2.16 | +76.2% (29) | +31.7% (47) | no |
| pltrkr111 | tag | 271 | 160 | +35.4% | 3.48 | +49.0% (185) | +6.0% (86) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 26 | 14 | +105.0% | 1.27 | +132.6% (21) | -12.0% (5) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 311 | 188 | +22.4% | 2.5 | +19.4% (236) | +32.1% (75) | no |
| juice-fruit | current | 27 | 20 | +28.8% | 1.65 | +0.0% (0) | +28.8% (27) | yes |
| am100 | tag | 988 | 587 | +11.4% | 3.13 | +11.0% (909) | +15.9% (79) | yes |
| MIracle33 | tag | 441 | 227 | +10.6% | 1.84 | +11.2% (345) | +8.3% (96) | yes |
| yakz | leaderboard | 176 | 87 | +17.4% | 1.3 | +31.6% (84) | +4.1% (92) | yes |
| -5rud | tag | 546 | 371 | +7.1% | 1.77 | +7.0% (422) | +7.5% (124) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1434 | 755 | +5.7% | 1.92 | +9.8% (1196) | -14.9% (238) | yes |
| SimpleTony | tag | 1193 | 377 | +7.8% | 1.5 | +7.4% (824) | +8.8% (369) | yes |
| BunCaCham | tag | 20 | 19 | +7.6% | 1.29 | +4.9% (14) | +13.9% (6) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 630 | 323 | +4.5% | 1.08 | +8.6% (425) | -4.1% (205) | yes |
| ZEST011 | tag | 710 | 530 | +2.8% | 1.08 | +2.3% (612) | +5.9% (98) | yes |
| AmericaFirst1 | current | 256 | 165 | +5.1% | 1.03 | +7.7% (197) | -3.3% (59) | yes |
| Nooserac | tag | 200 | 108 | +8.0% | 0.96 | -0.1% (150) | +32.4% (50) | yes |
| berlinskies | tag | 1032 | 600 | +1.5% | 0.46 | +6.3% (788) | -13.8% (244) | yes |
| GC-C | tag | 727 | 507 | +0.9% | 0.37 | -2.2% (292) | +3.0% (435) | yes |
| moreplatesmoredates | tag | 973 | 489 | +1.3% | 0.55 | -3.7% (635) | +10.8% (338) | yes |
| TheRomanProcurator | tag | 131 | 61 | +13.7% | 0.86 | -100.0% (2) | +15.4% (129) | yes |
| TAIWANNUMBERONE | tag | 1173 | 621 | +0.5% | 0.18 | -0.3% (1090) | +11.5% (83) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -9.2% (95) | +10.7% (123) | no |
| littlebay | tag | 94 | 69 | +3.9% | 0.59 | +7.0% (36) | +2.0% (58) | yes |
| 0x09dAc7226f8df37eBFAF277252 | tag | 510 | 297 | +0.8% | 0.25 | +4.3% (438) | -20.4% (72) | yes |
| vardaman-bundren | tag | 396 | 183 | +3.6% | 0.51 | +2.0% (300) | +8.8% (96) | yes |
| 0xcf279d52 | tag | 495 | 297 | +1.1% | 0.24 | +5.7% (341) | -9.0% (154) | yes |
| shaw | tag | 307 | 171 | +2.8% | 0.49 | +3.1% (236) | +1.9% (71) | yes |
| 636763 | tag | 1519 | 473 | +0.8% | 0.3 | +0.5% (1100) | +1.3% (419) | yes |
| dddd123s | tag | 561 | 337 | +0.2% | 0.03 | +4.3% (339) | -6.0% (222) | yes |
| 0xffAaEFb5f6762Cc70cb575Da87 | tag | 688 | 326 | +2.4% | 0.38 | +4.4% (543) | -5.3% (145) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 324 | 137 | -6.6% | -1.01 | no |
| Kch-Temp | 121 | 58 | -6.9% | -0.66 | no |
| EdZachary | 107 | 45 | -0.7% | -0.15 | no |
| KaneAnalytics | 140 | 78 | +6.2% | 0.56 | yes |
| Jsram | 95 | 56 | +0.0% | 0.21 | yes |
| Kkunn | 723 | 302 | +1.6% | 0.49 | no |
| Sisyphus- | 126 | 74 | +2.3% | 0.27 | yes |
| PEYZ-BIGGEST-FAN | 397 | 197 | +1.9% | 0.31 | no |
| theowalcott | 92 | 51 | +4.3% | 0.58 | yes |
| HVAB | 338 | 204 | -2.7% | -0.5 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 293 | 153 | +6.9% | 1.26 | no |
| Talvez10 | 554 | 306 | +5.4% | 1.03 | yes |
| BunCaCham | 49 | 45 | +29.7% | 3.56 | yes |
| 0010001000001100 | 153 | 72 | -0.8% | -0.35 | yes |
| totoro3miyazaki | 49 | 31 | +8.7% | 0.68 | no |
| 1l2ihj34li12u34 | 87 | 50 | +14.2% | 1.5 | yes |
| yabanci | 57 | 38 | +12.6% | 1.38 | yes |
| 0x20D6436849F930584892730C7F | 151 | 88 | +30.9% | 2.25 | yes |
| juice-fruit | 45 | 31 | +13.6% | 1.09 | yes |
| 0x16bb9951a36fce71e2ef57890b | 805 | 437 | +6.0% | 1.76 | yes |
| GamblingOdyssey | 435 | 220 | +7.2% | 1.45 | yes |
| plonker2026 | 142 | 78 | +7.6% | 1.27 | yes |
| xxyx0xx | 270 | 135 | +7.8% | 0.71 | yes |
| monkeymashingkeyboard | 1940 | 1077 | +5.0% | 2.17 | yes |
| Tiger105 | 43 | 28 | +19.1% | 1.34 | yes |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 515 | 321 | +5.5% | 1.36 | yes |
| UNEB3154s4f251 | 2179 | 1385 | +3.4% | 1.99 | yes |
