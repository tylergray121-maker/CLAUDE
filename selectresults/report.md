# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-01 09:00 UTC: 5576 candidates, 3835 with trades copytop could copy, 220 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2889 | 1408 | $28,007 | -353.57 | -1.3% | -0.53 |
| every wallet that qualified on the first part (test window) | 3484 | 1692 | $34,028 | -376.17 | -1.1% | -0.51 |
| currently copied (test window) | 4095 | 2191 | $40,181 | +900.03 | +2.2% | +1.55 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2889 | 1408 | $28,007 | -353.57 | -1.3% | -0.53 | 6414 | 3227 | $62,288 | +4,768.43 | +7.7% | 4.55 |
| copy their sells too | 2889 | 1062 | $28,007 | -921.18 | -3.3% | -1.63 | 6414 | 2672 | $62,288 | +3,473.23 | +5.6% | 3.5 |
| size by conviction (x0.5 / x1 / x1.5) | 2752 | 1338 | $32,818 | -46.00 | -0.1% | -0.62 | 6102 | 3061 | $73,247 | +5,271.21 | +7.2% | 4.28 |
| skip bets under 0.5x their usual | 2694 | 1314 | $26,314 | -218.45 | -0.8% | -0.16 | 5992 | 3019 | $58,629 | +4,513.19 | +7.7% | 4.51 |
| pre-game only | 2740 | 1345 | $26,526 | -637.00 | -2.4% | -1.02 | 5939 | 3034 | $57,499 | +4,499.84 | +7.8% | 4.65 |
| skip prices under 30c | 2423 | 1299 | $23,365 | -441.83 | -1.9% | -1.07 | 5162 | 2856 | $49,784 | +352.64 | +0.7% | 0.61 |
| favorites only (50c+) | 1322 | 857 | $12,655 | -59.00 | -0.5% | -0.21 | 2709 | 1828 | $25,796 | +418.31 | +1.6% | 1.29 |
| 15s delay | 2904 | 1418 | $28,197 | -142.80 | -0.5% | -0.14 | 6463 | 3259 | $62,820 | +5,243.11 | +8.3% | 4.94 |
| 60s delay | 2889 | 1408 | $28,007 | -353.57 | -1.3% | -0.53 | 6414 | 3227 | $62,288 | +4,768.43 | +7.7% | 4.55 |
| allow 2c over their price | 2954 | 1437 | $28,619 | -212.35 | -0.7% | -0.35 | 6663 | 3349 | $64,708 | +5,080.20 | +7.8% | 4.68 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 395 | +26.5% | 3.51 | 337 | +0.8% | -0.06 |
| conviction:1-2x | 601 | +15.6% | 2.48 | 387 | +0.5% | 0.03 |
| conviction:2x+ | 2097 | +10.8% | 3.48 | 1787 | +0.2% | 0.19 |
| conviction:under 0.5x | 432 | +24.8% | 3.49 | 378 | -11.7% | -2.11 |
| delay_move:flat | 2287 | +17.1% | 5.46 | 2227 | -1.1% | -0.42 |
| delay_move:price fell | 1238 | +10.8% | 2.87 | 662 | -1.7% | -0.35 |
| exit:settle | 3525 | +14.9% | 6.14 | 2889 | -1.3% | -0.53 |
| kind:moneyline | 2601 | +12.7% | 4.23 | 2284 | -2.9% | -1.14 |
| kind:result | 855 | +20.8% | 4.85 | 522 | +7.3% | 1.57 |
| kind:totals | 69 | +26.4% | 2.69 | 83 | -11.7% | -1.06 |
| league:atp | 387 | +6.5% | 1.0 | 182 | +16.5% | 2.54 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 165 | +8.9% | 0.9 | 337 | +13.2% | 1.61 |
| league:cs2 | 324 | +13.2% | 1.55 | 234 | +5.4% | 0.93 |
| league:dota2 | 112 | -5.6% | -0.5 | 90 | +19.6% | 1.04 |
| league:epl | 52 | +34.2% | 3.05 | 56 | -4.5% | -0.51 |
| league:ere | 8 | +106.7% | 28.83 | 35 | +28.4% | 1.15 |
| league:lal | 70 | +15.4% | 1.43 | 105 | -1.5% | -0.11 |
| league:lol | 1748 | +18.2% | 4.7 | 260 | -5.6% | -0.71 |
| league:mls | 32 | -3.9% | -0.2 | 202 | +0.1% | -0.01 |
| league:nba | 0 | +0.0% | — | 266 | -11.3% | -1.73 |
| league:nfl | 305 | +22.4% | 2.96 | 247 | -8.1% | -1.2 |
| league:nhl | 46 | +15.7% | 0.94 | 636 | -14.8% | -3.76 |
| league:sea | 33 | +59.4% | 3.41 | 39 | -29.2% | -1.58 |
| league:ucl | 40 | -8.0% | -0.57 | 62 | +16.1% | 1.33 |
| league:uel | 0 | +0.0% | — | 12 | +17.4% | 0.79 |
| league:wta | 194 | +2.2% | 0.17 | 117 | +8.9% | 0.8 |
| price:30-70c | 2252 | +3.7% | 1.88 | 2086 | -2.6% | -1.22 |
| price:over 70c | 482 | -0.6% | -0.15 | 331 | +1.9% | 0.51 |
| price:under 30c | 791 | +54.9% | 6.44 | 472 | +2.4% | 0.43 |
| timing:in-play | 326 | -0.4% | -0.14 | 149 | +19.1% | 1.2 |
| timing:pre-game | 3199 | +16.6% | 6.68 | 2740 | -2.4% | -1.02 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 132501 | 69004 | $1,318,477 | -50,252.32 | -3.8% | -11.73 |
| consistency (winning weeks), top 16 | 10699 | 5883 | $105,952 | -5,725.40 | -5.4% | -4.97 |
| consistency (winning weeks), top 40 | 23646 | 12796 | $234,151 | -8,808.96 | -3.8% | -5.10 |
| copy return, average, top 16 | 6868 | 3446 | $67,887 | -1,332.57 | -2.0% | -1.39 |
| copy return, average, top 40 | 20877 | 10740 | $207,189 | -6,821.24 | -3.3% | -3.71 |
| copy return, lower bound, top 16 | 7897 | 4110 | $77,946 | -4,472.35 | -5.7% | -4.64 |
| copy return, lower bound, top 40 | 23760 | 12787 | $235,369 | -8,560.41 | -3.6% | -4.71 |
| copy return, shrunk, top 16 | 6683 | 3131 | $66,355 | -3,905.92 | -5.9% | -3.65 |
| copy return, shrunk, top 40 | 21244 | 10876 | $210,955 | -6,308.47 | -3.0% | -3.34 |
| markout 2h, average, top 16 | 7520 | 4133 | $75,039 | -1,799.24 | -2.4% | -1.61 |
| markout 2h, average, top 40 | 20009 | 10870 | $198,982 | -7,201.12 | -3.6% | -4.46 |
| markout 2h, lower bound, top 16 | 8313 | 4619 | $82,514 | -4,551.98 | -5.5% | -4.55 |
| markout 2h, lower bound, top 40 | 24773 | 13443 | $246,437 | -9,957.40 | -4.0% | -5.53 |
| markout 30m, average, top 16 | 11164 | 6295 | $110,908 | -1,664.90 | -1.5% | -1.45 |
| markout 30m, average, top 40 | 26400 | 14451 | $263,260 | -7,765.06 | -2.9% | -4.01 |
| most active, top 16 | 21436 | 11274 | $213,607 | -9,319.15 | -4.4% | -5.47 |
| most active, top 40 | 38973 | 20098 | $387,138 | -16,265.35 | -4.2% | -7.11 |
| win rate vs the odds, top 16 | 5361 | 2845 | $53,081 | -1,064.32 | -2.0% | -1.14 |
| win rate vs the odds, top 40 | 20751 | 10916 | $205,429 | -6,733.55 | -3.3% | -4.07 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| chillhouse123 | 855 | 462 | +1.2% | 0.08 | +0.04 |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | +4.48 |
| BunCaCham | 51 | 46 | +26.7% | 3.19 | +2.62 |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | +3.03 |
| xxyx0xx | 280 | 139 | +6.8% | 0.64 | +0.62 |
| plonker2026 | 141 | 85 | +19.4% | 2.5 | +2.29 |
| eokho | 801 | 447 | +4.0% | 0.86 | +0.37 |
| yabanci | 69 | 45 | +10.8% | 1.25 | +1.35 |
| am100 | 926 | 556 | +13.5% | 3.54 | +1.35 |
| 1l2ihj34li12u34 | 95 | 56 | +16.9% | 1.89 | +1.98 |
| juice-fruit | 48 | 32 | +9.0% | 0.79 | +1.00 |
| moreplatesmoredates | 945 | 474 | +2.5% | 0.83 | +0.36 |
| AmericaFirst1 | 467 | 284 | +5.0% | 1.18 | +0.51 |
| 0xffAaEFb5f6762Cc70cb575Da87 | 694 | 328 | +1.9% | 0.31 | +0.18 |
| SimpleTony | 1151 | 381 | +11.6% | 2.2 | +1.18 |
| platarb | 567 | 227 | +0.2% | 0.02 | +0.01 |
| pltrkr111 | 1103 | 627 | +13.7% | 3.47 | +1.32 |
| monkeymashingkeyboard | 759 | 406 | +8.6% | 2.11 | +0.86 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 950 | 430 | +7.1% | 1.27 | +0.69 |
| arahbo | 1525 | 644 | -2.0% | -0.49 | -0.21 |
| eskk | 1003 | 255 | +0.7% | 0.14 | +0.10 |
| Sisyphus- | 125 | 69 | -3.0% | -0.33 | -0.29 |
| smithagent | 1124 | 622 | +4.0% | 0.85 | +0.40 |
| Future-Tarot-Trader | 1976 | 1005 | -1.0% | -0.37 | -0.12 |
| User7429 | 918 | 488 | -1.9% | -0.52 | -0.20 |
| GamblingOdyssey | 386 | 190 | +6.0% | 1.15 | +0.71 |
| igot50k | 1663 | 1017 | +0.3% | 0.06 | +0.02 |
| cosmicsteaks | 1221 | 533 | -0.8% | -0.23 | -0.10 |
| iseedota | 1377 | 609 | -1.3% | -0.34 | -0.13 |
| torta.tech | 1117 | 689 | -0.0% | 0.01 | +0.00 |
| UNEB3154s4f251 | 2196 | 1394 | +3.3% | 1.94 | +0.33 |
| KaneAnalytics | 167 | 91 | +2.5% | 0.27 | +0.25 |
| n1ck10s | 1132 | 600 | +2.5% | 0.68 | +0.24 |
| 636763 | 1466 | 459 | +1.4% | 0.4 | +0.21 |
| theowalcott | 108 | 58 | +0.8% | 0.25 | +0.23 |
| walnutz | 637 | 323 | -2.9% | -0.69 | -0.30 |
| assasin5002 | 623 | 316 | +2.1% | 0.37 | +0.19 |
| jiafan | 978 | 579 | +0.5% | 0.09 | +0.03 |
| 0x1E3bB7DEf89B002D45FD86D37F | 1341 | 797 | +2.0% | 0.52 | +0.18 |
| Jsram | 95 | 56 | +0.0% | 0.21 | +0.19 |

## Esports specialists (copies on esports markets only)

3002 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 168 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | tag | 76 | 43 | +48.6% | 2.16 | +52.3% (58) | +36.7% (18) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +40.9% (226) | -3.7% (51) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 31 | 17 | +91.9% | 1.31 | +150.0% (19) | -0.5% (12) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 301 | 182 | +24.2% | 2.62 | +19.1% (243) | +46.1% (58) | no |
| am100 | tag | 926 | 556 | +13.5% | 3.54 | +13.0% (880) | +22.7% (46) | yes |
| SimpleTony | tag | 1129 | 369 | +10.8% | 2.04 | +13.4% (797) | +4.6% (332) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1314 | 691 | +7.5% | 2.32 | +10.9% (1152) | -16.2% (162) | yes |
| -5rud | tag | 528 | 363 | +8.4% | 2.06 | +7.2% (435) | +14.2% (93) | yes |
| MIracle33 | tag | 449 | 229 | +9.6% | 1.68 | +9.5% (362) | +9.9% (87) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 612 | 321 | +7.8% | 1.62 | +13.7% (425) | -6.0% (187) | yes |
| Nooserac | tag | 151 | 83 | +13.8% | 1.31 | +5.8% (100) | +29.8% (51) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +0.0% (0) | +19.4% (29) | yes |
| BunCaCham | tag | 21 | 20 | +7.9% | 1.41 | +4.9% (14) | +13.9% (7) | yes |
| shaw | tag | 270 | 163 | +7.1% | 1.11 | +10.3% (209) | -4.6% (61) | yes |
| ZEST011 | tag | 656 | 490 | +2.9% | 1.1 | +2.4% (558) | +5.7% (98) | yes |
| AmericaFirst1 | current | 256 | 165 | +5.1% | 1.03 | +7.1% (217) | -6.2% (39) | no |
| littlebay | tag | 97 | 72 | +6.7% | 0.96 | +9.3% (51) | +3.9% (46) | yes |
| moreplatesmoredates | tag | 945 | 474 | +2.5% | 0.83 | -1.0% (584) | +8.2% (361) | yes |
| yakz | leaderboard | 191 | 92 | +12.8% | 0.9 | +31.2% (89) | -4.0% (102) | yes |
| berlinskies | tag | 1044 | 606 | +2.1% | 0.63 | +3.1% (858) | -2.8% (186) | yes |
| GC-C | tag | 747 | 523 | +1.2% | 0.5 | -4.9% (410) | +8.9% (337) | yes |
| TAIWANNUMBERONE | tag | 1049 | 557 | +1.4% | 0.45 | +0.2% (957) | +13.7% (92) | yes |
| 636763 | tag | 1444 | 452 | +2.0% | 0.53 | -0.3% (1068) | +8.7% (376) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -6.9% (113) | +11.7% (105) | no |
| igot50k | tag | 997 | 499 | +1.2% | 0.26 | -0.4% (868) | +12.1% (129) | yes |
| HalleyChen | tag | 632 | 387 | +1.6% | 0.35 | +2.2% (482) | -0.2% (150) | yes |
| 0x85264d29Fa7279946D15105C17 | tag | 128 | 67 | +7.1% | 0.67 | +10.6% (101) | -5.8% (27) | yes |
| dddd123s | tag | 579 | 348 | +0.0% | -0.01 | +5.2% (392) | -10.9% (187) | yes |
| johnbaster | tag | 794 | 424 | +1.7% | 0.29 | +0.9% (740) | +12.8% (54) | yes |
| Diabolical-Prize | tag | 224 | 118 | +2.1% | 0.47 | +5.8% (178) | -12.3% (46) | no |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 307 | 125 | -10.8% | -1.6 | no |
| Kch-Temp | 127 | 61 | -6.8% | -0.66 | no |
| EdZachary | 88 | 33 | -7.5% | -0.67 | no |
| KaneAnalytics | 167 | 91 | +2.5% | 0.27 | yes |
| Jsram | 95 | 56 | +0.0% | 0.21 | yes |
| Kkunn | 792 | 338 | +1.4% | 0.53 | no |
| Sisyphus- | 125 | 69 | -3.0% | -0.33 | yes |
| PEYZ-BIGGEST-FAN | 395 | 201 | +3.8% | 0.6 | no |
| theowalcott | 108 | 58 | +0.8% | 0.25 | yes |
| HVAB | 340 | 205 | -3.3% | -0.6 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 282 | 147 | +6.5% | 1.18 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | yes |
| BunCaCham | 51 | 46 | +26.7% | 3.19 | yes |
| 0010001000001100 | 164 | 79 | -0.1% | -0.29 | no |
| totoro3miyazaki | 49 | 31 | +8.7% | 0.68 | no |
| 1l2ihj34li12u34 | 95 | 56 | +16.9% | 1.89 | yes |
| yabanci | 69 | 45 | +10.8% | 1.25 | yes |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | yes |
| juice-fruit | 48 | 32 | +9.0% | 0.79 | yes |
| 0x16bb9951a36fce71e2ef57890b | 58 | 23 | -2.5% | -0.2 | no |
| GamblingOdyssey | 386 | 190 | +6.0% | 1.15 | yes |
| plonker2026 | 141 | 85 | +19.4% | 2.5 | yes |
| xxyx0xx | 280 | 139 | +6.8% | 0.64 | yes |
| monkeymashingkeyboard | 759 | 406 | +8.6% | 2.11 | yes |
| Tiger105 | 43 | 28 | +19.1% | 1.34 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 467 | 284 | +5.0% | 1.18 | yes |
| UNEB3154s4f251 | 2196 | 1394 | +3.3% | 1.94 | yes |
