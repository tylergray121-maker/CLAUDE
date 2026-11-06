# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-06 09:00 UTC: 5595 candidates, 3816 with trades copytop could copy, 225 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 1253 | 656 | $12,316 | +1,124.13 | +9.1% | +2.81 |
| every wallet that qualified on the first part (test window) | 1396 | 723 | $13,735 | +1,104.62 | +8.0% | +2.57 |
| currently copied (test window) | 3768 | 2006 | $36,906 | +1,202.22 | +3.3% | +1.92 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 1253 | 656 | $12,316 | +1,124.13 | +9.1% | 2.81 | 4259 | 2231 | $41,497 | +6,065.18 | +14.6% | 7.08 |
| copy their sells too | 1253 | 644 | $12,316 | +967.15 | +7.8% | 2.48 | 4259 | 2207 | $41,497 | +5,803.97 | +14.0% | 6.81 |
| size by conviction (x0.5 / x1 / x1.5) | 1198 | 629 | $15,289 | +1,354.42 | +8.9% | 2.7 | 4033 | 2104 | $50,676 | +6,746.79 | +13.3% | 6.56 |
| skip bets under 0.5x their usual | 1214 | 634 | $11,967 | +1,137.55 | +9.5% | 2.83 | 4079 | 2124 | $40,003 | +5,781.46 | +14.4% | 6.76 |
| pre-game only | 1143 | 615 | $11,185 | +1,061.26 | +9.5% | 2.96 | 3851 | 2080 | $37,342 | +6,131.01 | +16.4% | 7.83 |
| skip prices under 30c | 1024 | 587 | $10,044 | +536.57 | +5.3% | 1.85 | 3328 | 1946 | $32,269 | +2,344.76 | +7.3% | 4.59 |
| favorites only (50c+) | 553 | 375 | $5,367 | +354.73 | +6.6% | 2.15 | 1642 | 1187 | $15,697 | +1,563.69 | +10.0% | 5.95 |
| 15s delay | 1271 | 667 | $12,498 | +1,361.19 | +10.9% | 3.12 | 4308 | 2254 | $41,994 | +6,337.58 | +15.1% | 7.22 |
| 60s delay | 1253 | 656 | $12,316 | +1,124.13 | +9.1% | 2.81 | 4259 | 2231 | $41,497 | +6,065.18 | +14.6% | 7.08 |
| allow 2c over their price | 1313 | 684 | $12,900 | +1,328.45 | +10.3% | 3.03 | 4491 | 2342 | $43,756 | +6,307.31 | +14.4% | 7.06 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 302 | +22.5% | 3.0 | 127 | +13.3% | 0.94 |
| conviction:1-2x | 386 | +19.8% | 2.33 | 126 | +5.9% | 0.5 |
| conviction:2x+ | 1985 | +14.3% | 4.46 | 885 | +8.6% | 2.36 |
| conviction:under 0.5x | 333 | +25.1% | 3.58 | 115 | +12.7% | 1.29 |
| delay_move:flat | 2057 | +16.9% | 5.28 | 992 | +9.7% | 2.63 |
| delay_move:price fell | 949 | +17.1% | 3.9 | 261 | +7.2% | 1.04 |
| exit:settle | 3006 | +16.9% | 6.54 | 1253 | +9.1% | 2.81 |
| kind:moneyline | 2089 | +12.2% | 3.74 | 775 | +10.2% | 2.28 |
| kind:result | 827 | +26.6% | 6.08 | 262 | +11.4% | 1.74 |
| kind:totals | 90 | +36.3% | 4.42 | 216 | +2.6% | 0.41 |
| league:atp | 437 | +9.4% | 1.63 | 222 | +8.3% | 1.39 |
| league:bra | 12 | +60.6% | 2.56 | 16 | +3.8% | 0.19 |
| league:bun | 9 | +80.1% | 2.93 | 4 | -100.0% | — |
| league:cfb | 6 | -17.8% | -0.31 | 18 | +36.1% | 1.26 |
| league:cs2 | 340 | +14.2% | 1.91 | 158 | +8.2% | 0.72 |
| league:dota2 | 106 | -9.4% | -0.81 | 97 | +14.4% | 0.81 |
| league:epl | 54 | +35.2% | 3.23 | 71 | +13.9% | 1.01 |
| league:ere | 8 | +106.7% | 28.83 | 45 | +8.0% | 0.44 |
| league:lal | 22 | +26.1% | 1.67 | 24 | -5.4% | -0.26 |
| league:lol | 1585 | +18.7% | 4.64 | 124 | +19.5% | 1.53 |
| league:mls | 52 | +10.5% | 0.86 | 56 | -17.8% | -1.27 |
| league:nba | 0 | +0.0% | — | 98 | +2.3% | 0.49 |
| league:nfl | 47 | +28.6% | 1.47 | 12 | +81.4% | 2.8 |
| league:nhl | 32 | +54.3% | 5.31 | 88 | +17.2% | 2.06 |
| league:sea | 39 | +59.6% | 3.86 | 74 | +11.7% | 1.19 |
| league:spl | 9 | +68.6% | 3.06 | 4 | -39.9% | -1.14 |
| league:unl | 36 | +36.4% | 1.59 | 0 | +0.0% | — |
| league:wta | 211 | +3.8% | 0.48 | 132 | +0.2% | -0.05 |
| price:30-70c | 1922 | +9.0% | 4.07 | 888 | +6.9% | 2.15 |
| price:over 70c | 377 | +3.8% | 1.66 | 132 | -6.8% | -1.42 |
| price:under 30c | 707 | +44.5% | 4.99 | 233 | +26.3% | 2.17 |
| timing:in-play | 298 | -4.3% | -0.52 | 110 | +5.6% | 0.3 |
| timing:pre-game | 2708 | +19.4% | 7.32 | 1143 | +9.5% | 2.96 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 136427 | 71469 | $1,354,727 | -48,497.60 | -3.6% | -11.24 |
| consistency (winning weeks), top 16 | 8745 | 5055 | $86,267 | -2,326.51 | -2.7% | -2.27 |
| consistency (winning weeks), top 40 | 22398 | 11790 | $221,926 | -9,078.75 | -4.1% | -5.13 |
| copy return, average, top 16 | 6775 | 3448 | $66,759 | -603.07 | -0.9% | -0.59 |
| copy return, average, top 40 | 20193 | 10265 | $199,349 | -4,753.85 | -2.4% | -2.60 |
| copy return, lower bound, top 16 | 7223 | 3756 | $71,092 | -805.46 | -1.1% | -0.81 |
| copy return, lower bound, top 40 | 26655 | 14241 | $262,925 | -7,478.88 | -2.8% | -3.88 |
| copy return, shrunk, top 16 | 7450 | 3722 | $73,609 | -902.26 | -1.2% | -0.81 |
| copy return, shrunk, top 40 | 19653 | 9835 | $194,143 | -4,778.37 | -2.5% | -2.55 |
| markout 2h, average, top 16 | 7269 | 3941 | $72,095 | -310.95 | -0.4% | -0.46 |
| markout 2h, average, top 40 | 20442 | 10856 | $203,421 | -5,428.54 | -2.7% | -3.02 |
| markout 2h, lower bound, top 16 | 8654 | 4563 | $85,938 | -1,339.09 | -1.6% | -1.31 |
| markout 2h, lower bound, top 40 | 23038 | 12380 | $228,584 | -8,206.61 | -3.6% | -4.79 |
| markout 30m, average, top 16 | 6999 | 3812 | $70,055 | -1,445.61 | -2.1% | -1.29 |
| markout 30m, average, top 40 | 23169 | 12595 | $230,734 | -6,101.07 | -2.6% | -3.33 |
| most active, top 16 | 21366 | 11260 | $211,687 | -5,776.70 | -2.7% | -3.52 |
| most active, top 40 | 42112 | 22149 | $416,936 | -15,569.97 | -3.7% | -6.67 |
| win rate vs the odds, top 16 | 4551 | 2464 | $44,903 | -660.19 | -1.5% | -0.74 |
| win rate vs the odds, top 40 | 20057 | 10689 | $198,361 | -3,311.53 | -1.7% | -1.92 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 52 | 47 | +38.0% | 3.81 | +3.69 |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | +4.48 |
| xxyx0xx | 273 | 135 | +23.4% | 1.62 | +2.20 |
| 1l2ihj34li12u34 | 81 | 56 | +37.5% | 3.66 | +3.91 |
| plonker2026 | 114 | 68 | +26.2% | 2.43 | +2.85 |
| Kch-Temp | 142 | 80 | +6.7% | 1.03 | +0.89 |
| eokho | 828 | 465 | +5.2% | 1.15 | +0.49 |
| WagerWizard | 658 | 359 | -3.6% | -0.76 | -0.35 |
| GamblingAddict12345 | 745 | 322 | -0.5% | -0.11 | -0.06 |
| Notradecopy | 793 | 351 | +1.8% | 0.35 | +0.17 |
| platarb | 476 | 186 | -2.5% | -0.43 | -0.26 |
| moreplatesmoredates | 935 | 469 | +3.5% | 0.99 | +0.43 |
| juice-fruit | 45 | 28 | +6.2% | 0.52 | +0.73 |
| oxbus | 1394 | 701 | -3.6% | -1.19 | -0.37 |
| Future-Tarot-Trader | 1781 | 904 | -0.5% | -0.25 | -0.09 |
| AmericaFirst1 | 485 | 290 | +4.4% | 1.05 | +0.45 |
| monkeymashingkeyboard | 880 | 465 | +5.9% | 1.6 | +0.60 |
| yabanci | 78 | 47 | +2.9% | 0.54 | +0.56 |
| 0x16bb9951a36fce71e2ef57890b | 61 | 23 | -7.3% | -0.5 | -0.80 |
| nightcity2077 | 782 | 366 | +0.1% | 0.02 | +0.01 |
| 0010001000001100 | 141 | 75 | +10.7% | 0.78 | +1.07 |
| smithagent | 1244 | 688 | +3.4% | 0.8 | +0.35 |
| 636763 | 1454 | 467 | +2.6% | 0.63 | +0.33 |
| ludo-money | 866 | 489 | -1.9% | -0.53 | -0.19 |
| iseedota | 1410 | 620 | -2.0% | -0.52 | -0.19 |
| carelia | 1796 | 840 | -3.8% | -1.33 | -0.38 |
| clownly | 2160 | 807 | -5.8% | -2.11 | -0.59 |
| walnutz | 608 | 310 | -1.1% | -0.29 | -0.13 |
| Manchester4ever | 1002 | 571 | +0.8% | 0.28 | +0.09 |
| arahbo | 1463 | 605 | -2.8% | -0.66 | -0.29 |
| igot50k | 1626 | 1011 | -1.3% | -0.5 | -0.13 |
| flatbarrel | 1555 | 785 | -6.7% | -2.04 | -0.66 |
| EdZachary | 107 | 44 | +2.4% | 0.16 | +0.22 |
| 0x870a742f | 547 | 233 | -2.0% | -0.31 | -0.18 |
| Limousin | 1530 | 805 | +3.3% | 0.59 | +0.21 |
| n1ck10s | 1168 | 617 | +2.1% | 0.58 | +0.20 |
| oookkjjdd | 884 | 442 | -3.6% | -0.88 | -0.33 |
| ZEST011 | 611 | 456 | +2.7% | 0.97 | +0.26 |
| trapfive | 810 | 353 | -0.6% | -0.14 | -0.07 |
| yuxkc0 | 355 | 121 | -6.6% | -0.8 | -0.64 |

## Esports specialists (copies on esports markets only)

2923 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 165 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +48.6% (76) | +0.0% (0) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +30.4% (253) | +57.3% (24) | no |
| am100 | tag | 806 | 509 | +21.6% | 5.23 | +20.6% (780) | +50.4% (26) | no |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 291 | 176 | +25.3% | 2.65 | +21.6% (248) | +47.3% (43) | no |
| 0x5fD2D9C60781D711721145Ff2b | tag | 25 | 15 | +54.2% | 1.23 | +97.8% (14) | -1.1% (11) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1164 | 627 | +10.3% | 2.91 | +11.4% (1074) | -2.4% (90) | yes |
| CUTJALENHURTS | tag | 152 | 85 | +17.6% | 1.64 | +17.6% (119) | +17.8% (33) | yes |
| SimpleTony | tag | 1083 | 346 | +10.5% | 1.88 | +10.1% (784) | +11.6% (299) | yes |
| -5rud | tag | 510 | 350 | +8.2% | 1.96 | +7.9% (424) | +9.5% (86) | yes |
| littlebay | tag | 106 | 77 | +12.3% | 1.35 | +8.6% (66) | +18.3% (40) | yes |
| Manchester4ever | tag | 247 | 152 | +8.9% | 1.47 | +5.5% (204) | +25.1% (43) | yes |
| MIracle33 | tag | 450 | 227 | +8.6% | 1.5 | +8.5% (379) | +9.2% (71) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +2.1% (16) | +39.4% (13) | no |
| ccwcc | tag | 328 | 169 | +11.7% | 1.3 | +13.2% (306) | -10.7% (22) | yes |
| TAIWANNUMBERONE | tag | 876 | 486 | +5.9% | 1.67 | +2.8% (812) | +45.1% (64) | yes |
| BunCaCham | tag | 20 | 19 | +7.9% | 1.35 | +4.7% (13) | +13.9% (7) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 582 | 306 | +5.2% | 1.26 | +10.8% (379) | -5.2% (203) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 108 | 60 | +12.9% | 1.1 | +44.6% (9) | +10.1% (99) | yes |
| ZEST011 | tag | 606 | 453 | +2.9% | 1.07 | +3.2% (539) | +0.5% (67) | yes |
| moreplatesmoredates | tag | 935 | 469 | +3.5% | 0.99 | +0.9% (669) | +10.5% (266) | yes |
| berlinskies | tag | 1039 | 605 | +2.6% | 0.8 | +2.5% (909) | +3.9% (130) | yes |
| 636763 | tag | 1424 | 460 | +3.8% | 0.85 | +2.4% (1112) | +8.7% (312) | yes |
| carelia | tag | 206 | 119 | +7.5% | 0.9 | +6.4% (170) | +12.9% (36) | yes |
| GC-C | tag | 776 | 545 | +1.8% | 0.64 | -3.1% (588) | +17.0% (188) | yes |
| AmericaFirst1 | current | 271 | 170 | +2.4% | 0.55 | +7.6% (228) | -24.6% (43) | yes |
| nightcity2077 | tag | 366 | 177 | +6.1% | 0.7 | +8.0% (353) | -46.0% (13) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -0.7% (170) | +11.2% (48) | no |
| shaw | tag | 227 | 139 | +3.5% | 0.57 | +4.9% (173) | -0.9% (54) | yes |
| NS13 | leaderboard | 325 | 132 | +4.6% | 0.7 | +2.4% (255) | +12.4% (70) | yes |
| smartcombo | tag | 325 | 192 | +2.7% | 0.44 | +2.4% (314) | +12.7% (11) | no |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 333 | 140 | -7.8% | -1.25 | no |
| Kch-Temp | 142 | 80 | +6.7% | 1.03 | yes |
| EdZachary | 107 | 44 | +2.4% | 0.16 | yes |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | no |
| Jsram | 71 | 42 | +4.8% | 0.37 | no |
| Kkunn | 833 | 353 | +2.5% | 0.7 | no |
| Sisyphus- | 128 | 70 | -4.7% | -0.53 | no |
| PEYZ-BIGGEST-FAN | 389 | 196 | -1.4% | -0.15 | no |
| theowalcott | 75 | 44 | +9.8% | 1.05 | no |
| HVAB | 360 | 218 | -1.1% | -0.22 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +5.3% | 1.01 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | yes |
| BunCaCham | 52 | 47 | +38.0% | 3.81 | yes |
| 0010001000001100 | 141 | 75 | +10.7% | 0.78 | yes |
| totoro3miyazaki | 45 | 30 | +14.8% | 1.07 | no |
| 1l2ihj34li12u34 | 81 | 56 | +37.5% | 3.66 | yes |
| yabanci | 78 | 47 | +2.9% | 0.54 | yes |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 45 | 28 | +6.2% | 0.52 | yes |
| 0x16bb9951a36fce71e2ef57890b | 61 | 23 | -7.3% | -0.5 | yes |
| GamblingOdyssey | 378 | 193 | +4.9% | 1.03 | no |
| plonker2026 | 114 | 68 | +26.2% | 2.43 | yes |
| xxyx0xx | 273 | 135 | +23.4% | 1.62 | yes |
| monkeymashingkeyboard | 880 | 465 | +5.9% | 1.6 | yes |
| Tiger105 | 41 | 28 | +25.0% | 1.76 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 485 | 290 | +4.4% | 1.05 | yes |
| UNEB3154s4f251 | 2231 | 1404 | +2.5% | 1.54 | no |
