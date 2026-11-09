# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-09 09:00 UTC: 5695 candidates, 3901 with trades copytop could copy, 216 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2460 | 1282 | $24,178 | -153.59 | -0.6% | -0.47 |
| every wallet that qualified on the first part (test window) | 3092 | 1656 | $30,453 | -386.69 | -1.3% | -0.82 |
| currently copied (test window) | 3305 | 1707 | $32,337 | +469.75 | +1.5% | +0.96 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2460 | 1282 | $24,178 | -153.59 | -0.6% | -0.47 | 5088 | 2796 | $49,678 | +4,007.27 | +8.1% | 4.5 |
| copy their sells too | 2460 | 1277 | $24,178 | -182.42 | -0.8% | -0.52 | 5088 | 2790 | $49,678 | +3,966.25 | +8.0% | 4.47 |
| size by conviction (x0.5 / x1 / x1.5) | 2403 | 1251 | $26,474 | +111.09 | +0.4% | -0.37 | 4926 | 2692 | $55,863 | +3,916.96 | +7.0% | 4.11 |
| skip bets under 0.5x their usual | 2105 | 1142 | $20,738 | +153.28 | +0.7% | 0.11 | 4525 | 2536 | $44,419 | +3,521.80 | +7.9% | 4.37 |
| pre-game only | 782 | 444 | $7,745 | +498.98 | +6.4% | 1.77 | 2778 | 1610 | $26,884 | +3,964.11 | +14.8% | 6.61 |
| skip prices under 30c | 2043 | 1198 | $20,043 | -275.54 | -1.4% | -0.78 | 4321 | 2578 | $42,066 | +1,250.18 | +3.0% | 2.19 |
| favorites only (50c+) | 1310 | 912 | $12,752 | +158.04 | +1.2% | 0.76 | 2615 | 1850 | $25,271 | +1,103.74 | +4.4% | 3.39 |
| 15s delay | 2700 | 1436 | $26,532 | -31.67 | -0.1% | 0.15 | 5418 | 3002 | $52,915 | +4,128.56 | +7.8% | 4.84 |
| 60s delay | 2460 | 1282 | $24,178 | -153.59 | -0.6% | -0.47 | 5088 | 2796 | $49,678 | +4,007.27 | +8.1% | 4.5 |
| allow 2c over their price | 2659 | 1390 | $26,148 | -238.02 | -0.9% | -0.58 | 5464 | 3008 | $53,360 | +3,952.56 | +7.4% | 4.31 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 389 | +28.1% | 3.59 | 360 | -2.8% | -0.35 |
| conviction:1-2x | 479 | +17.5% | 2.97 | 439 | +3.9% | 0.57 |
| conviction:2x+ | 1381 | +9.2% | 3.2 | 1142 | +2.6% | 0.52 |
| conviction:under 0.5x | 379 | +29.5% | 3.65 | 519 | -10.1% | -1.59 |
| delay_move:flat | 1377 | +15.3% | 4.5 | 864 | +4.0% | 0.97 |
| delay_move:price fell | 1251 | +17.4% | 4.81 | 1596 | -3.1% | -1.23 |
| exit:settle | 2628 | +16.3% | 6.58 | 2460 | -0.6% | -0.47 |
| kind:moneyline | 2060 | +14.6% | 4.98 | 2243 | -1.6% | -0.84 |
| kind:result | 536 | +22.6% | 5.02 | 25 | +48.1% | 1.51 |
| kind:totals | 32 | +19.1% | 1.55 | 192 | +4.5% | 0.67 |
| league:atp | 852 | +12.8% | 2.65 | 1334 | +2.6% | 0.48 |
| league:cbb | 0 | +0.0% | — | 38 | -59.6% | -4.21 |
| league:cfb | 10 | -49.8% | -1.47 | 49 | +12.1% | 0.64 |
| league:cs2 | 139 | +17.7% | 2.1 | 12 | -19.7% | -0.63 |
| league:dota2 | 37 | +7.0% | 0.46 | 0 | +0.0% | — |
| league:lol | 1124 | +21.5% | 5.64 | 65 | +13.8% | 0.57 |
| league:nba | 9 | -19.5% | -0.5 | 252 | -1.3% | 0.17 |
| league:nfl | 44 | +33.9% | 1.64 | 23 | -27.1% | -0.99 |
| league:nhl | 71 | +33.6% | 4.2 | 79 | +6.2% | 0.69 |
| league:unl | 14 | +34.4% | 1.28 | 0 | +0.0% | — |
| league:wta | 326 | +4.9% | 0.72 | 606 | -6.0% | -1.49 |
| price:30-70c | 1825 | +7.5% | 3.34 | 1539 | -0.7% | -0.34 |
| price:over 70c | 448 | +3.6% | 1.63 | 489 | -3.5% | -1.68 |
| price:under 30c | 355 | +75.7% | 5.81 | 432 | +2.5% | 0.06 |
| timing:in-play | 632 | +10.9% | 1.93 | 1678 | -4.0% | -1.55 |
| timing:pre-game | 1996 | +18.1% | 6.56 | 782 | +6.4% | 1.77 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 117193 | 61407 | $1,162,476 | -50,162.37 | -4.3% | -12.58 |
| consistency (winning weeks), top 16 | 8321 | 4026 | $82,981 | -5,634.77 | -6.8% | -5.33 |
| consistency (winning weeks), top 40 | 25984 | 14086 | $256,493 | -11,727.82 | -4.6% | -6.68 |
| copy return, average, top 16 | 6110 | 2847 | $60,629 | -3,537.15 | -5.8% | -3.55 |
| copy return, average, top 40 | 23407 | 11576 | $231,727 | -12,596.76 | -5.4% | -6.98 |
| copy return, lower bound, top 16 | 8600 | 4215 | $85,240 | -4,008.01 | -4.7% | -3.66 |
| copy return, lower bound, top 40 | 23860 | 12699 | $236,073 | -10,132.96 | -4.3% | -5.93 |
| copy return, shrunk, top 16 | 7299 | 3465 | $72,460 | -3,847.49 | -5.3% | -3.63 |
| copy return, shrunk, top 40 | 23194 | 11363 | $229,748 | -12,078.70 | -5.3% | -6.56 |
| markout 2h, average, top 16 | 9512 | 4973 | $94,500 | -4,922.17 | -5.2% | -4.31 |
| markout 2h, average, top 40 | 23127 | 12393 | $229,877 | -12,764.49 | -5.5% | -7.44 |
| markout 2h, lower bound, top 16 | 12083 | 6356 | $119,950 | -6,419.80 | -5.3% | -5.08 |
| markout 2h, lower bound, top 40 | 24803 | 13073 | $246,380 | -12,418.28 | -5.0% | -7.03 |
| markout 30m, average, top 16 | 6975 | 3744 | $69,761 | -5,451.58 | -7.8% | -6.12 |
| markout 30m, average, top 40 | 24452 | 13035 | $243,777 | -11,812.11 | -4.9% | -6.46 |
| most active, top 16 | 18480 | 9816 | $183,726 | -7,883.14 | -4.3% | -5.09 |
| most active, top 40 | 33972 | 17950 | $337,440 | -13,885.69 | -4.1% | -6.36 |
| win rate vs the odds, top 16 | 7708 | 3976 | $76,514 | -4,298.78 | -5.6% | -4.14 |
| win rate vs the odds, top 40 | 23261 | 12283 | $230,960 | -9,863.82 | -4.3% | -5.60 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| xxyx0xx | 184 | 86 | +25.4% | 1.29 | +2.34 |
| am100 | 755 | 484 | +23.3% | 5.52 | +2.36 |
| Kch-Temp | 134 | 71 | +4.5% | 0.53 | +0.54 |
| cash-bundren | 386 | 155 | -4.0% | -0.59 | -0.39 |
| SimpleTony | 1047 | 336 | +10.5% | 1.86 | +1.08 |
| juice-fruit | 48 | 31 | +8.0% | 0.7 | +0.93 |
| oxbus | 1094 | 556 | -0.6% | -0.1 | -0.04 |
| 0x16bb9951a36fce71e2ef57890b | 64 | 24 | -9.3% | -0.65 | -1.00 |
| moreplatesmoredates | 967 | 487 | +3.5% | 1.01 | +0.43 |
| monkeymashingkeyboard | 951 | 512 | +7.4% | 2.09 | +0.74 |
| horaciorolinha | 569 | 261 | -4.0% | -0.75 | -0.41 |
| carelia | 1574 | 720 | -4.5% | -1.48 | -0.46 |
| Manchester4ever | 1031 | 598 | +3.0% | 1.0 | +0.30 |
| Future-Tarot-Trader | 1699 | 859 | -1.8% | -0.6 | -0.21 |
| 0x5fD2D9C60781D711721145Ff2b | 699 | 388 | +5.8% | 0.98 | +0.54 |
| 636763 | 1444 | 469 | +2.1% | 0.56 | +0.29 |
| igot50k | 1557 | 979 | -0.3% | -0.16 | -0.04 |
| TearsInTheRain | 559 | 374 | -0.8% | -0.2 | -0.07 |
| calvinoxieS | 678 | 304 | -4.3% | -0.91 | -0.42 |
| trapfive | 771 | 331 | -1.8% | -0.37 | -0.18 |
| 239393828 | 531 | 261 | -0.5% | -0.14 | -0.07 |
| walnutz | 591 | 304 | -0.6% | -0.18 | -0.08 |
| flatbarrel | 1517 | 764 | -6.9% | -2.07 | -0.68 |
| Popeyesfriedchicken | 664 | 363 | -3.7% | -0.68 | -0.38 |
| chrysos | 712 | 364 | -5.0% | -1.3 | -0.50 |
| ludo-money | 757 | 423 | -1.7% | -0.44 | -0.17 |
| 0x709179E7392e59922Ab2D73cb1 | 2670 | 1304 | -1.6% | -0.62 | -0.15 |
| 0x8g68hBa8tyH1946Bhjb674g3fu | 1223 | 678 | -0.1% | -0.04 | -0.01 |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | +0.58 |
| oookkjjdd | 783 | 388 | -2.6% | -0.58 | -0.23 |
| capitalpiston2 | 1579 | 712 | +1.3% | 0.39 | +0.13 |
| 0x1E3bB7DEf89B002D45FD86D37F | 2411 | 1427 | +1.3% | 0.42 | +0.11 |
| cryptoqan0n | 1280 | 650 | +0.9% | 0.21 | +0.07 |
| torta.tech | 887 | 555 | +0.6% | 0.2 | +0.06 |
| AmericaFirst1 | 495 | 286 | +2.4% | 0.61 | +0.26 |
| UNEB3154s4f251 | 1830 | 1114 | +3.5% | 1.86 | +0.35 |
| zuihouyici | 621 | 320 | -0.3% | -0.11 | -0.05 |
| CUTJALENHURTS | 1146 | 643 | -1.4% | -0.49 | -0.16 |
| pltrkr111 | 1115 | 636 | +12.6% | 3.22 | +1.21 |
| sweetcaroline | 651 | 537 | -0.6% | -0.35 | -0.06 |

## Esports specialists (copies on esports markets only)

3061 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 168 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +48.6% (76) | +0.0% (0) | no |
| am100 | tag | 755 | 484 | +23.3% | 5.52 | +23.0% (738) | +34.7% (17) | yes |
| pltrkr111 | tag | 284 | 160 | +29.8% | 2.95 | +30.0% (258) | +27.8% (26) | yes |
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 21 | 13 | +52.4% | 1.53 | +55.8% (7) | +50.7% (14) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 290 | 176 | +25.7% | 2.69 | +21.2% (257) | +61.9% (33) | no |
| BunCaCham | tag | 19 | 19 | +17.4% | 4.91 | +14.7% (11) | +21.1% (8) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 30 | 18 | +45.4% | 1.21 | +97.8% (14) | -0.4% (16) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1146 | 619 | +9.7% | 2.81 | +10.1% (1067) | +4.1% (79) | yes |
| SimpleTony | tag | 1047 | 336 | +10.5% | 1.86 | +7.9% (781) | +18.1% (266) | yes |
| -5rud | tag | 504 | 347 | +8.6% | 2.03 | +8.5% (418) | +8.8% (86) | yes |
| TAIWANNUMBERONE | tag | 838 | 464 | +6.8% | 1.79 | +2.5% (789) | +73.6% (49) | yes |
| Manchester4ever | tag | 251 | 153 | +8.3% | 1.38 | +4.6% (207) | +25.9% (44) | yes |
| ccwcc | tag | 329 | 169 | +11.3% | 1.26 | +12.4% (311) | -7.2% (18) | yes |
| CUTJALENHURTS | tag | 156 | 85 | +13.8% | 1.24 | +15.1% (117) | +9.8% (39) | yes |
| shaw | tag | 191 | 124 | +8.9% | 1.31 | +12.0% (139) | +0.6% (52) | yes |
| MIracle33 | tag | 447 | 226 | +7.8% | 1.37 | +7.4% (386) | +10.2% (61) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 123 | 69 | +12.3% | 1.13 | +44.6% (9) | +9.8% (114) | yes |
| littlebay | tag | 110 | 78 | +9.3% | 1.05 | +7.0% (79) | +14.8% (31) | yes |
| ZEST011 | tag | 554 | 415 | +3.3% | 1.13 | +3.6% (488) | +0.4% (66) | no |
| moreplatesmoredates | tag | 967 | 487 | +3.5% | 1.01 | +0.8% (663) | +9.4% (304) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 559 | 293 | +3.7% | 1.0 | +8.2% (358) | -4.5% (201) | yes |
| carelia | tag | 202 | 117 | +8.3% | 0.97 | +6.8% (169) | +16.0% (33) | yes |
| GC-C | tag | 779 | 547 | +2.0% | 0.72 | -2.7% (628) | +21.6% (151) | yes |
| ZTMZqClEsjMmwCDWXoG | tag | 1019 | 590 | +2.5% | 0.74 | +2.0% (914) | +6.7% (105) | yes |
| juice-fruit | current | 30 | 20 | +15.2% | 0.94 | +5.9% (17) | +26.7% (13) | yes |
| 636763 | tag | 1409 | 457 | +3.1% | 0.73 | +2.0% (1098) | +6.6% (311) | yes |
| RensPeters | tag | 109 | 64 | +8.1% | 0.83 | +7.1% (94) | +14.4% (15) | yes |
| returdmaxxer | tag | 318 | 289 | +0.1% | 0.04 | +0.6% (272) | -3.2% (46) | yes |
| AmericaFirst1 | tag | 285 | 181 | +2.4% | 0.57 | +6.3% (234) | -15.8% (51) | yes |
| nightcity2077 | tag | 350 | 169 | +6.6% | 0.73 | +8.5% (335) | -37.1% (15) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 415 | 183 | -9.7% | -1.74 | no |
| Kch-Temp | 134 | 71 | +4.5% | 0.53 | yes |
| EdZachary | 129 | 46 | -13.0% | -1.13 | no |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | yes |
| Jsram | 12 | 6 | -15.8% | -0.68 | no |
| Kkunn | 860 | 360 | +0.3% | 0.31 | no |
| Sisyphus- | 127 | 69 | -4.3% | -0.48 | no |
| PEYZ-BIGGEST-FAN | 397 | 197 | -2.7% | -0.36 | no |
| theowalcott | — | — | — | — | no copyable trades |
| HVAB | 364 | 221 | -0.7% | -0.15 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +5.3% | 1.01 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 32 | 29 | +14.1% | 1.25 | no |
| 0010001000001100 | 62 | 30 | +7.3% | 0.34 | no |
| totoro3miyazaki | 11 | 3 | -69.9% | -4.21 | no |
| 1l2ihj34li12u34 | 9 | 6 | +30.6% | 0.92 | no |
| yabanci | 80 | 45 | -4.0% | -0.1 | no |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 48 | 31 | +8.0% | 0.7 | yes |
| 0x16bb9951a36fce71e2ef57890b | 64 | 24 | -9.3% | -0.65 | yes |
| GamblingOdyssey | 336 | 173 | +7.6% | 1.4 | no |
| plonker2026 | 6 | 5 | +161.7% | 1.6 | no |
| xxyx0xx | 184 | 86 | +25.4% | 1.29 | yes |
| monkeymashingkeyboard | 951 | 512 | +7.4% | 2.09 | yes |
| Tiger105 | 31 | 23 | +36.2% | 2.3 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 495 | 286 | +2.4% | 0.61 | yes |
| UNEB3154s4f251 | 1830 | 1114 | +3.5% | 1.86 | yes |
