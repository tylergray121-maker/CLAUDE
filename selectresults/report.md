# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-03 17:00 UTC: 5693 candidates, 3915 with trades copytop could copy, 221 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2843 | 1425 | $27,556 | +181.17 | +0.7% | +0.38 |
| every wallet that qualified on the first part (test window) | 4341 | 2279 | $42,477 | -500.46 | -1.2% | -0.62 |
| currently copied (test window) | 3980 | 2135 | $38,990 | +1,045.54 | +2.7% | +1.67 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2843 | 1425 | $27,556 | +181.17 | +0.7% | 0.38 | 6427 | 3257 | $62,380 | +5,020.63 | +8.1% | 4.88 |
| copy their sells too | 2849 | 1093 | $27,616 | -227.58 | -0.8% | -0.34 | 6433 | 2669 | $62,441 | +3,784.65 | +6.1% | 3.94 |
| size by conviction (x0.5 / x1 / x1.5) | 2705 | 1351 | $32,818 | +334.75 | +1.0% | 0.27 | 6106 | 3084 | $73,860 | +5,486.93 | +7.4% | 4.58 |
| skip bets under 0.5x their usual | 2686 | 1347 | $26,204 | +170.24 | +0.7% | 0.49 | 6032 | 3062 | $59,001 | +4,778.54 | +8.1% | 4.83 |
| pre-game only | 2717 | 1377 | $26,290 | +214.79 | +0.8% | 0.46 | 6052 | 3124 | $58,603 | +5,079.41 | +8.7% | 5.24 |
| skip prices under 30c | 2418 | 1310 | $23,368 | -392.61 | -1.7% | -0.87 | 5202 | 2875 | $50,200 | +163.79 | +0.3% | 0.34 |
| favorites only (50c+) | 1349 | 886 | $12,927 | +190.06 | +1.5% | 0.8 | 2753 | 1863 | $26,236 | +636.63 | +2.4% | 1.94 |
| 15s delay | 2860 | 1437 | $27,727 | +411.71 | +1.5% | 0.8 | 6475 | 3285 | $62,867 | +5,424.31 | +8.6% | 5.22 |
| 60s delay | 2843 | 1425 | $27,556 | +181.17 | +0.7% | 0.38 | 6427 | 3257 | $62,380 | +5,020.63 | +8.1% | 4.88 |
| allow 2c over their price | 2911 | 1462 | $28,182 | +436.79 | +1.6% | 0.77 | 6667 | 3376 | $64,687 | +5,360.13 | +8.3% | 5.05 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 416 | +20.5% | 2.75 | 323 | +9.2% | 1.16 |
| conviction:1-2x | 632 | +15.2% | 2.5 | 328 | +0.3% | 0.15 |
| conviction:2x+ | 2120 | +11.0% | 3.62 | 1852 | +0.5% | 0.33 |
| conviction:under 0.5x | 416 | +20.6% | 2.97 | 340 | -6.3% | -1.16 |
| delay_move:flat | 2404 | +15.8% | 5.28 | 2200 | +1.0% | 0.45 |
| delay_move:price fell | 1180 | +9.9% | 2.49 | 643 | -0.4% | -0.04 |
| exit:settle | 3584 | +13.9% | 5.8 | 2843 | +0.7% | 0.38 |
| kind:moneyline | 2742 | +10.6% | 3.67 | 2288 | -1.6% | -0.7 |
| kind:result | 767 | +24.9% | 5.4 | 353 | +14.7% | 2.54 |
| kind:totals | 75 | +21.6% | 2.46 | 202 | +1.8% | 0.36 |
| league:atp | 517 | +6.2% | 1.24 | 227 | +7.3% | 1.26 |
| league:bun | 9 | +80.1% | 2.93 | 4 | -100.0% | — |
| league:cfb | 189 | +4.1% | 0.49 | 240 | +24.5% | 2.33 |
| league:cs2 | 239 | +11.9% | 1.04 | 205 | -2.5% | -0.05 |
| league:dota2 | 70 | -12.6% | -0.8 | 89 | +23.0% | 1.21 |
| league:epl | 54 | +35.2% | 3.23 | 65 | +7.5% | 0.44 |
| league:ere | 4 | +97.0% | — | 34 | +25.8% | 1.03 |
| league:lal | 70 | +15.4% | 1.43 | 131 | +4.2% | 0.74 |
| league:lol | 1662 | +19.4% | 4.86 | 212 | +6.8% | 0.67 |
| league:nba | 0 | +0.0% | — | 471 | -5.7% | -1.11 |
| league:nfl | 316 | +8.7% | 1.25 | 208 | -9.1% | -1.47 |
| league:nhl | 120 | +8.7% | 0.78 | 691 | -10.3% | -2.73 |
| league:sea | 34 | +54.4% | 3.14 | 50 | +0.4% | 0.12 |
| league:ucl | 35 | -13.7% | -0.88 | 62 | +15.6% | 1.3 |
| league:uel | 0 | +0.0% | — | 12 | +17.4% | 0.79 |
| league:wta | 253 | +9.6% | 1.18 | 130 | +1.9% | 0.12 |
| price:30-70c | 2303 | +3.1% | 1.58 | 2069 | -2.0% | -0.9 |
| price:over 70c | 479 | -2.4% | -1.11 | 344 | -0.7% | -0.19 |
| price:under 30c | 802 | +53.2% | 6.4 | 430 | +14.3% | 1.66 |
| timing:in-play | 249 | -1.0% | -0.15 | 126 | -2.7% | -0.26 |
| timing:pre-game | 3335 | +15.0% | 6.25 | 2717 | +0.8% | 0.46 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 133367 | 69951 | $1,326,007 | -50,462.43 | -3.8% | -11.81 |
| consistency (winning weeks), top 16 | 10297 | 5201 | $102,156 | -3,434.79 | -3.4% | -2.71 |
| consistency (winning weeks), top 40 | 21236 | 10998 | $210,647 | -7,502.02 | -3.6% | -4.36 |
| copy return, average, top 16 | 6103 | 3011 | $60,481 | +579.22 | +1.0% | +0.43 |
| copy return, average, top 40 | 21335 | 11043 | $211,380 | -3,523.15 | -1.7% | -1.91 |
| copy return, lower bound, top 16 | 8089 | 4126 | $80,156 | -1,493.03 | -1.9% | -1.36 |
| copy return, lower bound, top 40 | 25195 | 13487 | $248,976 | -6,671.64 | -2.7% | -3.49 |
| copy return, shrunk, top 16 | 6791 | 3275 | $67,418 | -164.90 | -0.2% | -0.15 |
| copy return, shrunk, top 40 | 21747 | 11248 | $215,532 | -3,728.36 | -1.7% | -2.01 |
| markout 2h, average, top 16 | 7390 | 3992 | $73,915 | -1,246.83 | -1.7% | -0.91 |
| markout 2h, average, top 40 | 19819 | 10577 | $197,194 | -5,879.44 | -3.0% | -3.32 |
| markout 2h, lower bound, top 16 | 8187 | 4326 | $81,787 | -1,739.88 | -2.1% | -1.49 |
| markout 2h, lower bound, top 40 | 21717 | 11657 | $215,892 | -7,500.37 | -3.5% | -4.32 |
| markout 30m, average, top 16 | 9314 | 5107 | $93,318 | -2,620.75 | -2.8% | -2.08 |
| markout 30m, average, top 40 | 22138 | 12215 | $220,666 | -5,931.98 | -2.7% | -3.30 |
| most active, top 16 | 20808 | 10716 | $207,540 | -9,047.12 | -4.4% | -5.33 |
| most active, top 40 | 40070 | 20879 | $397,415 | -17,945.67 | -4.5% | -7.85 |
| win rate vs the odds, top 16 | 4600 | 2454 | $45,557 | +40.08 | +0.1% | +0.01 |
| win rate vs the odds, top 40 | 20810 | 10688 | $206,418 | -5,290.53 | -2.6% | -2.98 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 55 | 50 | +36.2% | 3.82 | +3.52 |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | +4.48 |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | +3.03 |
| xxyx0xx | 292 | 146 | +7.1% | 0.7 | +0.66 |
| gordonwrong | 903 | 329 | -0.4% | 0.24 | +0.12 |
| eokho | 811 | 454 | +4.1% | 0.91 | +0.38 |
| juice-fruit | 47 | 32 | +11.5% | 0.96 | +1.24 |
| AmericaFirst1 | 458 | 280 | +6.9% | 1.58 | +0.70 |
| Limousin | 863 | 471 | +11.2% | 1.97 | +1.03 |
| platarb | 490 | 199 | +0.9% | 0.13 | +0.08 |
| SimpleTony | 1120 | 373 | +13.1% | 2.43 | +1.34 |
| am100 | 857 | 515 | +15.3% | 3.85 | +1.55 |
| 1l2ihj34li12u34 | 118 | 68 | +14.6% | 1.81 | +1.71 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 807 | 359 | +4.0% | 0.66 | +0.39 |
| KaneAnalytics | 172 | 93 | +7.2% | 0.63 | +0.70 |
| pltrkr111 | 1120 | 635 | +13.4% | 3.44 | +1.30 |
| Jsram | 100 | 61 | +5.1% | 0.73 | +0.64 |
| yabanci | 77 | 47 | +3.7% | 0.62 | +0.64 |
| plonker2026 | 139 | 81 | +14.2% | 1.96 | +1.81 |
| moreplatesmoredates | 957 | 479 | +3.0% | 0.89 | +0.39 |
| Sisyphus- | 120 | 68 | -1.1% | -0.1 | -0.09 |
| Kch-Temp | 137 | 75 | +1.2% | 0.32 | +0.28 |
| capitalpiston2 | 1724 | 790 | +2.2% | 0.65 | +0.21 |
| blimp123 | 620 | 279 | -10.2% | -2.11 | -1.01 |
| smithagent | 1148 | 637 | +4.3% | 0.9 | +0.42 |
| monkeymashingkeyboard | 836 | 435 | +5.5% | 1.37 | +0.53 |
| darkumbreon88 | 1850 | 1265 | +3.9% | 1.84 | +0.39 |
| GamblingOdyssey | 348 | 179 | +7.3% | 1.37 | +0.87 |
| Manchester4ever | 867 | 506 | +1.2% | 0.4 | +0.13 |
| iseedota | 1324 | 590 | -1.0% | -0.25 | -0.09 |
| arahbo | 1503 | 626 | -2.8% | -0.67 | -0.29 |
| walnutz | 626 | 319 | -1.5% | -0.37 | -0.17 |
| yuxkc0 | 365 | 125 | -5.5% | -0.68 | -0.54 |
| igot50k | 1685 | 1045 | -0.6% | -0.26 | -0.07 |
| 0x1E3bB7DEf89B002D45FD86D37F | 1628 | 972 | +2.6% | 0.74 | +0.23 |
| EdZachary | 107 | 44 | +2.4% | 0.16 | +0.22 |
| 636763 | 1472 | 463 | +1.4% | 0.41 | +0.21 |
| UNEB3154s4f251 | 2224 | 1404 | +2.5% | 1.49 | +0.25 |
| assasin5002 | 635 | 321 | +2.1% | 0.39 | +0.20 |
| n1ck10s | 1144 | 604 | +2.0% | 0.54 | +0.19 |

## Esports specialists (copies on esports markets only)

3037 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 164 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +51.2% (72) | +0.4% (4) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +32.2% (242) | +37.1% (35) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 292 | 176 | +24.8% | 2.61 | +22.6% (237) | +34.6% (55) | no |
| am100 | tag | 857 | 515 | +15.3% | 3.85 | +14.3% (818) | +36.4% (39) | yes |
| SimpleTony | tag | 1098 | 361 | +12.3% | 2.27 | +15.1% (781) | +5.4% (317) | yes |
| CUTJALENHURTS | tag | 152 | 85 | +17.6% | 1.64 | +7.8% (106) | +40.6% (46) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1253 | 659 | +8.6% | 2.55 | +11.1% (1104) | -9.7% (149) | yes |
| -5rud | tag | 529 | 364 | +8.5% | 2.08 | +7.6% (437) | +12.8% (92) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 85 | 49 | +17.1% | 1.31 | +44.6% (9) | +13.8% (76) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +72.4% (7) | +5.0% (22) | yes |
| BunCaCham | tag | 21 | 20 | +7.9% | 1.41 | +4.9% (14) | +13.9% (7) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 596 | 313 | +6.0% | 1.39 | +11.8% (404) | -6.3% (192) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 28 | 16 | +41.6% | 1.04 | +69.2% (17) | -1.1% (11) | yes |
| shaw | tag | 251 | 156 | +7.6% | 1.18 | +12.0% (193) | -7.5% (58) | yes |
| Manchester4ever | tag | 237 | 144 | +7.0% | 1.15 | +6.3% (189) | +9.4% (48) | yes |
| AmericaFirst1 | current | 257 | 166 | +5.5% | 1.12 | +8.3% (222) | -11.4% (35) | yes |
| ZEST011 | tag | 632 | 474 | +3.1% | 1.18 | +3.1% (549) | +3.4% (83) | yes |
| TAIWANNUMBERONE | tag | 982 | 534 | +3.4% | 1.02 | +2.6% (893) | +11.2% (89) | yes |
| moreplatesmoredates | tag | 957 | 479 | +3.0% | 0.89 | +0.2% (629) | +8.6% (328) | yes |
| GC-C | tag | 763 | 538 | +2.2% | 0.82 | -3.9% (489) | +13.3% (274) | yes |
| berlinskies | tag | 1044 | 608 | +2.5% | 0.76 | +2.8% (883) | +1.1% (161) | yes |
| littlebay | tag | 100 | 73 | +5.1% | 0.75 | +10.2% (55) | -1.1% (45) | yes |
| 636763 | tag | 1443 | 456 | +2.5% | 0.62 | -1.6% (1096) | +15.6% (347) | yes |
| NS13 | tag | 324 | 137 | +5.3% | 0.81 | +1.4% (251) | +18.2% (73) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | +0.5% (141) | +4.2% (77) | no |
| nightcity2077 | tag | 407 | 198 | +4.9% | 0.62 | +6.0% (396) | -35.8% (11) | yes |
| HalleyChen | tag | 606 | 369 | +1.6% | 0.33 | +1.6% (472) | +1.6% (134) | yes |
| 0x1E3bB7DEf89B002D45FD86D37F | tag | 31 | 19 | +16.9% | 0.83 | +0.0% (0) | +16.9% (31) | yes |
| Diabolical-Prize | current | 224 | 118 | +2.1% | 0.47 | +3.9% (190) | -7.9% (34) | no |
| dddd123s | tag | 588 | 352 | -0.3% | -0.1 | +3.2% (408) | -8.1% (180) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 311 | 129 | -9.8% | -1.47 | no |
| Kch-Temp | 137 | 75 | +1.2% | 0.32 | yes |
| EdZachary | 107 | 44 | +2.4% | 0.16 | yes |
| KaneAnalytics | 172 | 93 | +7.2% | 0.63 | yes |
| Jsram | 100 | 61 | +5.1% | 0.73 | yes |
| Kkunn | 823 | 345 | +1.4% | 0.49 | no |
| Sisyphus- | 120 | 68 | -1.1% | -0.1 | yes |
| PEYZ-BIGGEST-FAN | 394 | 198 | +2.4% | 0.36 | no |
| theowalcott | 13 | 11 | +63.3% | 2.93 | no |
| HVAB | 348 | 210 | -2.2% | -0.4 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 282 | 147 | +6.5% | 1.18 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | yes |
| BunCaCham | 55 | 50 | +36.2% | 3.82 | yes |
| 0010001000001100 | 177 | 87 | -1.1% | -0.36 | no |
| totoro3miyazaki | 49 | 31 | +8.7% | 0.68 | no |
| 1l2ihj34li12u34 | 118 | 68 | +14.6% | 1.81 | yes |
| yabanci | 77 | 47 | +3.7% | 0.62 | yes |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | yes |
| juice-fruit | 47 | 32 | +11.5% | 0.96 | yes |
| 0x16bb9951a36fce71e2ef57890b | 61 | 23 | -7.3% | -0.5 | no |
| GamblingOdyssey | 348 | 179 | +7.3% | 1.37 | yes |
| plonker2026 | 139 | 81 | +14.2% | 1.96 | yes |
| xxyx0xx | 292 | 146 | +7.1% | 0.7 | yes |
| monkeymashingkeyboard | 836 | 435 | +5.5% | 1.37 | yes |
| Tiger105 | 38 | 25 | +20.5% | 1.37 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 458 | 280 | +6.9% | 1.58 | yes |
| UNEB3154s4f251 | 2224 | 1404 | +2.5% | 1.49 | yes |
