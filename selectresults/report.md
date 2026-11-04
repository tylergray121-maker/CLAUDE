# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-04 09:00 UTC: 5674 candidates, 3896 with trades copytop could copy, 222 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2345 | 1315 | $23,096 | +391.35 | +1.7% | +0.91 |
| every wallet that qualified on the first part (test window) | 3061 | 1700 | $30,281 | +306.63 | +1.0% | +0.62 |
| currently copied (test window) | 4084 | 2187 | $40,026 | +1,013.47 | +2.5% | +1.62 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2345 | 1315 | $23,096 | +391.35 | +1.7% | 0.91 | 5353 | 2900 | $52,296 | +4,860.14 | +9.3% | 5.36 |
| copy their sells too | 2345 | 1257 | $23,096 | +217.80 | +0.9% | 0.66 | 5353 | 2818 | $52,296 | +4,512.66 | +8.6% | 5.14 |
| size by conviction (x0.5 / x1 / x1.5) | 2281 | 1280 | $25,925 | +569.44 | +2.2% | 0.68 | 5132 | 2772 | $60,839 | +5,333.03 | +8.8% | 4.8 |
| skip bets under 0.5x their usual | 2184 | 1248 | $21,501 | +932.64 | +4.3% | 1.85 | 5031 | 2742 | $49,388 | +5,055.56 | +10.2% | 5.57 |
| pre-game only | 1041 | 559 | $10,121 | +923.94 | +9.1% | 2.74 | 3585 | 1910 | $34,663 | +5,274.98 | +15.2% | 6.95 |
| skip prices under 30c | 1965 | 1227 | $19,261 | +325.52 | +1.7% | 0.88 | 4283 | 2596 | $41,602 | +1,619.43 | +3.9% | 2.99 |
| favorites only (50c+) | 1319 | 944 | $12,804 | +77.60 | +0.6% | 0.41 | 2511 | 1817 | $24,118 | +937.87 | +3.9% | 3.14 |
| 15s delay | 2555 | 1472 | $25,168 | +617.77 | +2.5% | 1.28 | 5612 | 3083 | $54,858 | +5,214.74 | +9.5% | 5.61 |
| 60s delay | 2345 | 1315 | $23,096 | +391.35 | +1.7% | 0.91 | 5353 | 2900 | $52,296 | +4,860.14 | +9.3% | 5.36 |
| allow 2c over their price | 2641 | 1496 | $26,015 | +723.69 | +2.8% | 1.34 | 5841 | 3183 | $57,091 | +5,295.47 | +9.3% | 5.51 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 335 | +17.4% | 2.72 | 486 | +4.4% | 0.64 |
| conviction:1-2x | 459 | +15.3% | 2.14 | 520 | +1.3% | 0.22 |
| conviction:2x+ | 1865 | +13.3% | 3.93 | 1053 | +3.4% | 1.35 |
| conviction:under 0.5x | 349 | +24.7% | 3.33 | 286 | -8.5% | -1.09 |
| delay_move:flat | 1935 | +16.8% | 5.05 | 1332 | +4.8% | 1.71 |
| delay_move:price fell | 1073 | +12.7% | 3.11 | 1013 | -2.4% | -0.64 |
| exit:settle | 3008 | +15.3% | 5.93 | 2345 | +1.7% | 0.91 |
| kind:moneyline | 2134 | +11.9% | 3.66 | 1763 | +0.6% | 0.32 |
| kind:result | 808 | +23.8% | 5.42 | 458 | +5.7% | 1.18 |
| kind:totals | 66 | +21.6% | 2.24 | 124 | +2.4% | 0.39 |
| league:atp | 430 | +13.2% | 2.13 | 830 | -2.8% | -0.82 |
| league:bra | 6 | +109.4% | — | 9 | +12.9% | 0.44 |
| league:bun | 8 | +50.3% | 14.89 | 10 | -37.1% | -1.34 |
| league:cfb | 10 | -15.9% | -0.45 | 37 | +18.2% | 1.09 |
| league:cs2 | 333 | +12.3% | 1.63 | 163 | -0.4% | 0.19 |
| league:dota2 | 105 | -8.5% | -0.73 | 93 | +19.6% | 1.06 |
| league:epl | 52 | +34.2% | 3.05 | 64 | +9.2% | 0.58 |
| league:ere | 4 | +97.0% | — | 46 | +15.1% | 0.81 |
| league:lal | 20 | +17.4% | 1.12 | 27 | +5.7% | 0.15 |
| league:lol | 1614 | +18.7% | 4.66 | 163 | +4.4% | 0.52 |
| league:mls | 48 | +13.2% | 1.05 | 115 | -5.3% | -0.4 |
| league:nba | 0 | +0.0% | — | 50 | +26.4% | 2.77 |
| league:nfl | 48 | +28.4% | 1.49 | 23 | +50.1% | 2.52 |
| league:nhl | 17 | +80.5% | 15.3 | 103 | +12.6% | 1.59 |
| league:sea | 33 | +59.4% | 3.41 | 73 | -8.1% | -0.55 |
| league:spl | 1 | +64.8% | — | 25 | -4.0% | -0.16 |
| league:ucl | 40 | -8.0% | -0.57 | 82 | -2.2% | 0.09 |
| league:uel | 0 | +0.0% | — | 18 | +6.3% | 0.51 |
| league:wta | 239 | -5.1% | -0.88 | 413 | -0.5% | -0.23 |
| price:30-70c | 1866 | +7.0% | 3.16 | 1315 | +5.1% | 1.92 |
| price:over 70c | 447 | +1.0% | 0.5 | 645 | -5.7% | -2.95 |
| price:under 30c | 695 | +45.8% | 5.07 | 385 | +1.9% | 0.42 |
| timing:in-play | 464 | +2.5% | 0.25 | 1303 | -4.0% | -1.43 |
| timing:pre-game | 2544 | +17.7% | 6.42 | 1041 | +9.1% | 2.74 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 138233 | 72321 | $1,374,452 | -57,605.82 | -4.2% | -13.27 |
| consistency (winning weeks), top 16 | 9174 | 4885 | $90,553 | -1,755.13 | -1.9% | -1.58 |
| consistency (winning weeks), top 40 | 21504 | 11200 | $213,306 | -7,570.66 | -3.5% | -4.31 |
| copy return, average, top 16 | 6352 | 3058 | $62,883 | -1,208.68 | -1.9% | -1.17 |
| copy return, average, top 40 | 19552 | 9827 | $193,895 | -6,431.23 | -3.3% | -3.54 |
| copy return, lower bound, top 16 | 7873 | 3989 | $77,487 | -1,845.81 | -2.4% | -1.65 |
| copy return, lower bound, top 40 | 24050 | 12613 | $237,472 | -8,887.83 | -3.7% | -4.66 |
| copy return, shrunk, top 16 | 6644 | 3169 | $65,842 | -2,531.60 | -3.8% | -2.20 |
| copy return, shrunk, top 40 | 20003 | 10066 | $198,449 | -6,511.48 | -3.3% | -3.53 |
| markout 2h, average, top 16 | 6995 | 3603 | $69,816 | -1,589.10 | -2.3% | -1.26 |
| markout 2h, average, top 40 | 19841 | 10540 | $197,569 | -8,114.23 | -4.1% | -4.60 |
| markout 2h, lower bound, top 16 | 7749 | 3895 | $77,104 | -2,806.12 | -3.6% | -2.44 |
| markout 2h, lower bound, top 40 | 22628 | 12177 | $224,649 | -9,281.06 | -4.1% | -5.32 |
| markout 30m, average, top 16 | 9323 | 4952 | $93,597 | -2,972.31 | -3.2% | -2.34 |
| markout 30m, average, top 40 | 23503 | 12800 | $234,602 | -9,390.16 | -4.0% | -5.15 |
| most active, top 16 | 21569 | 11119 | $215,247 | -9,102.81 | -4.2% | -5.29 |
| most active, top 40 | 44210 | 23230 | $437,973 | -21,039.71 | -4.8% | -8.89 |
| win rate vs the odds, top 16 | 3874 | 2129 | $38,204 | -482.00 | -1.3% | -0.64 |
| win rate vs the odds, top 40 | 18666 | 9707 | $185,384 | -4,753.35 | -2.6% | -2.66 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 55 | 50 | +36.2% | 3.82 | +3.52 |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | +4.48 |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | +3.03 |
| xxyx0xx | 300 | 150 | +6.1% | 0.61 | +0.56 |
| Kch-Temp | 149 | 86 | +9.6% | 1.36 | +1.15 |
| eokho | 812 | 453 | +3.8% | 0.84 | +0.35 |
| yabanci | 86 | 53 | +9.9% | 1.16 | +1.19 |
| AmericaFirst1 | 469 | 286 | +6.1% | 1.42 | +0.62 |
| platarb | 494 | 197 | -0.8% | -0.15 | -0.09 |
| juice-fruit | 48 | 32 | +9.0% | 0.79 | +1.00 |
| WagerWizard | 705 | 384 | -2.6% | -0.56 | -0.25 |
| am100 | 847 | 511 | +15.9% | 3.99 | +1.61 |
| plonker2026 | 139 | 81 | +14.2% | 1.96 | +1.81 |
| moreplatesmoredates | 958 | 480 | +3.0% | 0.9 | +0.39 |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | +0.58 |
| 1l2ihj34li12u34 | 122 | 69 | +12.7% | 1.62 | +1.52 |
| Jsram | 100 | 61 | +5.1% | 0.73 | +0.64 |
| monkeymashingkeyboard | 837 | 435 | +5.3% | 1.34 | +0.52 |
| 0x16bb9951a36fce71e2ef57890b | 61 | 23 | -7.3% | -0.5 | -0.80 |
| capitalpiston2 | 2009 | 954 | +1.7% | 0.55 | +0.16 |
| Car-c | 1393 | 696 | -1.2% | -0.32 | -0.13 |
| iseedota | 1402 | 622 | -0.3% | -0.07 | -0.03 |
| Sisyphus- | 121 | 68 | -1.9% | -0.19 | -0.17 |
| darkumbreon88 | 1934 | 1311 | +3.0% | 1.47 | +0.30 |
| walnutz | 621 | 315 | -2.0% | -0.47 | -0.21 |
| nightcity2077 | 828 | 385 | -1.1% | -0.19 | -0.10 |
| GamblingOdyssey | 361 | 184 | +5.2% | 1.07 | +0.66 |
| blimp123 | 620 | 281 | -9.7% | -2.0 | -0.96 |
| smithagent | 1221 | 673 | +2.6% | 0.57 | +0.26 |
| SimpleTony | 1125 | 371 | +11.9% | 2.24 | +1.23 |
| igot50k | 1681 | 1044 | -0.4% | -0.2 | -0.05 |
| arahbo | 1499 | 625 | -2.5% | -0.6 | -0.26 |
| yuxkc0 | 359 | 122 | -7.2% | -0.9 | -0.71 |
| cm2897 | 985 | 450 | +3.2% | 0.42 | +0.25 |
| 0x870a742f | 548 | 235 | -1.0% | -0.15 | -0.09 |
| EdZachary | 107 | 44 | +2.4% | 0.16 | +0.22 |
| UNEB3154s4f251 | 2289 | 1444 | +2.5% | 1.54 | +0.26 |
| Limousin | 1199 | 620 | +3.3% | 0.48 | +0.20 |
| shiifoo | 498 | 196 | -3.0% | -0.49 | -0.32 |
| n1ck10s | 1146 | 605 | +1.9% | 0.52 | +0.18 |

## Esports specialists (copies on esports markets only)

3015 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 163 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +51.7% (73) | -29.5% (3) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +32.3% (245) | +36.8% (32) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 292 | 176 | +24.8% | 2.61 | +22.7% (240) | +35.0% (52) | no |
| am100 | tag | 847 | 511 | +15.9% | 3.99 | +14.9% (813) | +37.6% (34) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1218 | 646 | +9.6% | 2.78 | +12.3% (1078) | -10.6% (140) | yes |
| CUTJALENHURTS | tag | 152 | 85 | +17.6% | 1.64 | +7.6% (109) | +43.3% (43) | yes |
| SimpleTony | tag | 1102 | 359 | +11.2% | 2.09 | +14.8% (784) | +2.4% (318) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 89 | 52 | +17.3% | 1.38 | +44.6% (9) | +14.2% (80) | yes |
| -5rud | tag | 530 | 364 | +8.3% | 2.04 | +7.7% (440) | +11.2% (90) | yes |
| MIracle33 | tag | 446 | 226 | +9.1% | 1.58 | +9.1% (363) | +9.3% (83) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 590 | 313 | +6.6% | 1.49 | +12.5% (396) | -5.7% (194) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +7.0% (14) | +30.4% (15) | yes |
| BunCaCham | tag | 21 | 20 | +7.9% | 1.41 | +4.9% (14) | +13.9% (7) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 28 | 16 | +41.6% | 1.04 | +69.2% (17) | -1.1% (11) | yes |
| shaw | tag | 247 | 152 | +7.7% | 1.17 | +10.5% (196) | -3.3% (51) | yes |
| Manchester4ever | tag | 238 | 145 | +7.1% | 1.17 | +6.3% (193) | +10.1% (45) | yes |
| TAIWANNUMBERONE | tag | 949 | 520 | +4.2% | 1.24 | +2.8% (871) | +19.1% (78) | yes |
| AmericaFirst1 | current | 257 | 166 | +5.5% | 1.12 | +8.3% (222) | -11.4% (35) | yes |
| ZEST011 | tag | 629 | 472 | +3.2% | 1.21 | +3.3% (548) | +2.7% (81) | yes |
| GC-C | tag | 767 | 542 | +2.3% | 0.87 | -2.7% (521) | +13.1% (246) | yes |
| moreplatesmoredates | tag | 958 | 480 | +3.0% | 0.9 | -0.6% (663) | +11.2% (295) | yes |
| berlinskies | tag | 1045 | 609 | +2.6% | 0.78 | +2.7% (894) | +1.7% (151) | yes |
| 636763 | tag | 1439 | 456 | +2.8% | 0.67 | -1.3% (1101) | +16.1% (338) | yes |
| littlebay | tag | 100 | 73 | +5.1% | 0.75 | +13.3% (58) | -6.1% (42) | yes |
| NS13 | tag | 324 | 137 | +5.3% | 0.81 | +1.4% (253) | +18.8% (71) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -0.2% (165) | +8.3% (53) | no |
| nightcity2077 | tag | 399 | 194 | +4.8% | 0.6 | +6.0% (388) | -35.8% (11) | yes |
| HalleyChen | tag | 606 | 369 | +1.6% | 0.33 | +2.6% (478) | -2.0% (128) | yes |
| Diabolical-Prize | current | 224 | 118 | +2.1% | 0.47 | +7.0% (196) | -32.5% (28) | no |
| dddd123s | tag | 588 | 352 | -0.3% | -0.1 | +3.2% (413) | -8.6% (175) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 320 | 136 | -6.5% | -1.01 | no |
| Kch-Temp | 149 | 86 | +9.6% | 1.36 | yes |
| EdZachary | 107 | 44 | +2.4% | 0.16 | yes |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | yes |
| Jsram | 100 | 61 | +5.1% | 0.73 | yes |
| Kkunn | 824 | 345 | +1.2% | 0.46 | no |
| Sisyphus- | 121 | 68 | -1.9% | -0.19 | yes |
| PEYZ-BIGGEST-FAN | 398 | 202 | +2.6% | 0.42 | no |
| theowalcott | 75 | 44 | +9.8% | 1.05 | no |
| HVAB | 354 | 212 | -3.1% | -0.57 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 282 | 147 | +6.5% | 1.18 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | yes |
| BunCaCham | 55 | 50 | +36.2% | 3.82 | yes |
| 0010001000001100 | 197 | 96 | -3.9% | -0.64 | no |
| totoro3miyazaki | 49 | 31 | +8.7% | 0.68 | no |
| 1l2ihj34li12u34 | 122 | 69 | +12.7% | 1.62 | yes |
| yabanci | 86 | 53 | +9.9% | 1.16 | yes |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | yes |
| juice-fruit | 48 | 32 | +9.0% | 0.79 | yes |
| 0x16bb9951a36fce71e2ef57890b | 61 | 23 | -7.3% | -0.5 | yes |
| GamblingOdyssey | 361 | 184 | +5.2% | 1.07 | yes |
| plonker2026 | 139 | 81 | +14.2% | 1.96 | yes |
| xxyx0xx | 300 | 150 | +6.1% | 0.61 | yes |
| monkeymashingkeyboard | 837 | 435 | +5.3% | 1.34 | yes |
| Tiger105 | 40 | 26 | +20.4% | 1.37 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 469 | 286 | +6.1% | 1.42 | yes |
| UNEB3154s4f251 | 2289 | 1444 | +2.5% | 1.54 | yes |
