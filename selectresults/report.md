# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-14 09:00 UTC: 5580 candidates, 3871 with trades copytop could copy, 222 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 806 | 470 | $7,923 | +836.24 | +10.5% | +2.65 |
| every wallet that qualified on the first part (test window) | 1584 | 930 | $15,659 | +689.29 | +4.4% | +1.64 |
| currently copied (test window) | 3497 | 1829 | $34,191 | -78.84 | -0.2% | +0.10 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 806 | 470 | $7,923 | +836.24 | +10.5% | 2.65 | 2141 | 1262 | $20,993 | +2,979.67 | +14.2% | 5.5 |
| copy their sells too | 806 | 455 | $7,923 | +664.76 | +8.4% | 2.16 | 2141 | 1239 | $20,993 | +2,739.69 | +13.1% | 5.1 |
| size by conviction (x0.5 / x1 / x1.5) | 785 | 452 | $9,860 | +826.38 | +8.4% | 2.42 | 2080 | 1216 | $25,974 | +2,938.36 | +11.3% | 5.14 |
| skip bets under 0.5x their usual | 771 | 451 | $7,585 | +773.17 | +10.2% | 2.53 | 2036 | 1204 | $20,053 | +2,680.19 | +13.4% | 5.26 |
| pre-game only | 732 | 431 | $7,171 | +609.71 | +8.5% | 2.35 | 1976 | 1165 | $19,327 | +2,626.05 | +13.6% | 5.28 |
| skip prices under 30c | 753 | 450 | $7,380 | +415.45 | +5.6% | 1.83 | 1927 | 1184 | $18,818 | +1,452.93 | +7.7% | 3.89 |
| favorites only (50c+) | 456 | 310 | $4,448 | +279.81 | +6.3% | 1.97 | 1121 | 809 | $10,875 | +963.01 | +8.8% | 4.48 |
| 15s delay | 815 | 476 | $8,010 | +831.63 | +10.4% | 2.64 | 2154 | 1272 | $21,116 | +2,965.07 | +14.0% | 5.48 |
| 60s delay | 806 | 470 | $7,923 | +836.24 | +10.5% | 2.65 | 2141 | 1262 | $20,993 | +2,979.67 | +14.2% | 5.5 |
| allow 2c over their price | 830 | 484 | $8,166 | +820.37 | +10.1% | 2.59 | 2200 | 1295 | $21,581 | +2,886.51 | +13.4% | 5.3 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 121 | +42.7% | 3.69 | 73 | +21.1% | 1.68 |
| conviction:1-2x | 148 | +23.2% | 2.09 | 67 | +9.1% | 0.82 |
| conviction:2x+ | 894 | +9.3% | 2.57 | 554 | +7.6% | 1.69 |
| conviction:under 0.5x | 172 | +29.2% | 2.3 | 112 | +19.5% | 1.46 |
| delay_move:flat | 1056 | +18.4% | 4.73 | 613 | +15.6% | 3.3 |
| delay_move:price fell | 279 | +9.1% | 1.35 | 193 | -5.0% | -0.6 |
| exit:settle | 1335 | +16.4% | 4.87 | 806 | +10.5% | 2.65 |
| kind:moneyline | 1017 | +13.7% | 3.27 | 468 | +19.8% | 3.48 |
| kind:result | 189 | +34.9% | 4.77 | 117 | -7.4% | -0.57 |
| kind:totals | 129 | +10.6% | 1.65 | 221 | +0.5% | -0.0 |
| league:atp | 438 | +10.0% | 1.73 | 193 | +11.5% | 1.83 |
| league:bel1 | 2 | +18.2% | 0.17 | 13 | +20.9% | 0.73 |
| league:bra | 2 | +69.5% | 4.09 | 8 | -19.5% | -0.61 |
| league:bun | 9 | +80.1% | 2.93 | 4 | -100.0% | — |
| league:cfb | 78 | -3.5% | -0.12 | 32 | +56.3% | 2.06 |
| league:cs2 | 23 | +24.0% | 1.3 | 6 | +2.7% | 0.08 |
| league:epl | 70 | +19.9% | 2.15 | 68 | +10.7% | 0.49 |
| league:lal | 22 | +24.9% | 1.64 | 31 | -26.8% | -1.55 |
| league:lol | 277 | +33.0% | 3.36 | 26 | -18.7% | -0.97 |
| league:nba | 0 | +0.0% | — | 163 | +0.8% | 0.2 |
| league:nfl | 25 | +50.8% | 1.35 | 22 | +93.4% | 1.41 |
| league:nhl | 86 | +29.9% | 3.46 | 51 | +26.4% | 2.91 |
| league:sea | 52 | +37.8% | 2.75 | 66 | +22.4% | 1.98 |
| league:unl | 35 | +40.2% | 1.74 | 15 | -57.1% | -2.89 |
| league:wta | 216 | -8.9% | -1.37 | 105 | +12.1% | 1.21 |
| price:30-70c | 926 | +9.8% | 3.11 | 644 | +6.6% | 1.86 |
| price:over 70c | 247 | +5.5% | 1.99 | 109 | -0.2% | 0.04 |
| price:under 30c | 162 | +68.7% | 3.5 | 53 | +77.5% | 2.01 |
| timing:in-play | 91 | +13.9% | 1.05 | 74 | +30.1% | 1.24 |
| timing:pre-game | 1244 | +16.6% | 4.76 | 732 | +8.5% | 2.35 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 125906 | 65452 | $1,247,845 | -58,619.98 | -4.7% | -14.29 |
| consistency (winning weeks), top 16 | 7030 | 3382 | $70,180 | -4,716.00 | -6.7% | -4.79 |
| consistency (winning weeks), top 40 | 22188 | 11651 | $219,867 | -9,355.71 | -4.3% | -5.46 |
| copy return, average, top 16 | 4204 | 2145 | $41,457 | -2,530.35 | -6.1% | -3.41 |
| copy return, average, top 40 | 19706 | 9670 | $195,762 | -10,653.95 | -5.4% | -6.13 |
| copy return, lower bound, top 16 | 6748 | 3434 | $66,569 | -3,527.62 | -5.3% | -3.95 |
| copy return, lower bound, top 40 | 21783 | 11456 | $215,505 | -9,427.42 | -4.4% | -5.64 |
| copy return, shrunk, top 16 | 6076 | 2957 | $59,730 | -3,262.72 | -5.5% | -3.49 |
| copy return, shrunk, top 40 | 20277 | 9952 | $201,517 | -11,416.88 | -5.7% | -6.49 |
| markout 2h, average, top 16 | 8153 | 4089 | $81,458 | -4,945.23 | -6.1% | -4.25 |
| markout 2h, average, top 40 | 24505 | 12435 | $244,298 | -16,060.71 | -6.6% | -8.40 |
| markout 2h, lower bound, top 16 | 10086 | 5167 | $100,518 | -6,715.67 | -6.7% | -5.36 |
| markout 2h, lower bound, top 40 | 27756 | 14377 | $275,730 | -16,703.80 | -6.1% | -8.61 |
| markout 30m, average, top 16 | 6438 | 3452 | $64,440 | -3,104.64 | -4.8% | -3.20 |
| markout 30m, average, top 40 | 19973 | 10589 | $199,592 | -9,458.45 | -4.7% | -5.51 |
| most active, top 16 | 18691 | 10098 | $184,736 | -8,775.22 | -4.8% | -5.95 |
| most active, top 40 | 36160 | 18974 | $357,984 | -17,236.04 | -4.8% | -7.83 |
| win rate vs the odds, top 16 | 4008 | 2035 | $39,638 | -2,966.50 | -7.5% | -4.51 |
| win rate vs the odds, top 40 | 21295 | 10886 | $211,934 | -8,979.10 | -4.2% | -5.16 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 53 | 48 | +43.6% | 4.28 | +4.24 |
| 0x16bb9951a36fce71e2ef57890b | 64 | 24 | -9.3% | -0.65 | -1.01 |
| 1l2ihj34li12u34 | 87 | 52 | +17.8% | 1.85 | +1.99 |
| cash-bundren | 387 | 154 | -4.2% | -0.62 | -0.41 |
| Kch-Temp | 160 | 87 | +7.0% | 0.91 | +0.82 |
| 0010001000001100 | 170 | 86 | +7.8% | 0.65 | +0.79 |
| Car-c | 963 | 497 | +3.7% | 0.73 | +0.36 |
| nightcity2077 | 635 | 311 | +3.9% | 0.62 | +0.38 |
| Popeyesfriedchicken | 655 | 358 | -3.2% | -0.57 | -0.33 |
| NS13 | 1205 | 481 | -0.6% | -0.13 | -0.07 |
| nibbio3 | 314 | 139 | +7.7% | 0.73 | +0.74 |
| carelia | 1405 | 650 | -3.9% | -1.19 | -0.39 |
| moreplatesmoredates | 918 | 461 | +2.0% | 0.69 | +0.30 |
| monkeymashingkeyboard | 1016 | 539 | +4.0% | 1.21 | +0.41 |
| Manchester4ever | 1110 | 639 | +3.6% | 1.2 | +0.36 |
| arahbo | 1356 | 565 | +1.0% | 0.19 | +0.09 |
| 636763 | 1352 | 434 | +0.1% | 0.1 | +0.05 |
| oxbus | 1486 | 745 | -5.3% | -2.08 | -0.61 |
| trapfive | 773 | 330 | -1.4% | -0.29 | -0.14 |
| pltrkr111 | 1202 | 681 | +12.0% | 3.23 | +1.16 |
| TearsInTheRain | 603 | 406 | +0.3% | 0.12 | +0.04 |
| SlickRick123 | 1399 | 593 | +1.8% | 0.39 | +0.16 |
| Kkunn | 921 | 387 | +1.4% | 0.5 | +0.24 |
| juice-fruit | 54 | 33 | +1.2% | 0.2 | +0.25 |
| smithagent | 1376 | 754 | +2.5% | 0.61 | +0.26 |
| 0x567212c82AAa6fe589bE5A2f4C | 529 | 278 | +4.5% | 1.05 | +0.65 |
| 0x8g68hBa8tyH1946Bhjb674g3fu | 1642 | 913 | +0.7% | 0.29 | +0.08 |
| darkumbreon88 | 2542 | 1651 | -0.7% | -0.33 | -0.05 |
| CUTJALENHURTS | 1222 | 697 | -0.3% | -0.1 | -0.03 |
| JAMJAMJAM4 | 1513 | 782 | -2.5% | -0.94 | -0.25 |
| User7429 | 906 | 473 | -4.2% | -1.09 | -0.43 |
| walnutz | 552 | 283 | -0.9% | -0.24 | -0.11 |
| TAIWANNUMBERONE | 1161 | 680 | +4.7% | 1.56 | +0.49 |
| guyefwalkfvhujajeswdgfa | 863 | 453 | -4.9% | -1.13 | -0.44 |
| MIracle33 | 695 | 344 | +3.9% | 0.91 | +0.40 |
| zuihouyici | 651 | 332 | -1.3% | -0.32 | -0.14 |
| cryptoqan0n | 1379 | 699 | +0.6% | 0.15 | +0.05 |
| 0x5fD2D9C60781D711721145Ff2b | 687 | 376 | +2.1% | 0.34 | +0.18 |
| yuxkc0 | 327 | 110 | -5.9% | -0.69 | -0.59 |
| ahmerde | 579 | 353 | -2.2% | -0.04 | -0.02 |

## Esports specialists (copies on esports markets only)

2944 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 169 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 27 | 19 | +76.1% | 2.82 | +55.8% (7) | +83.6% (20) | yes |
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +48.6% (76) | +0.0% (0) | no |
| pltrkr111 | tag | 284 | 160 | +29.8% | 2.95 | +33.7% (266) | -30.3% (18) | yes |
| Tomahawkmaster | leaderboard | 22 | 10 | +66.3% | 1.38 | +0.0% (0) | +66.3% (22) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 290 | 176 | +25.7% | 2.69 | +24.8% (289) | +269.1% (1) | no |
| BunCaCham | tag | 19 | 19 | +17.4% | 4.91 | +14.7% (11) | +21.1% (8) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 27 | 16 | +52.5% | 1.27 | +111.4% (13) | -2.4% (14) | yes |
| TAIWANNUMBERONE | tag | 734 | 412 | +11.0% | 2.6 | +7.1% (683) | +62.4% (51) | yes |
| MIracle33 | tag | 424 | 220 | +11.2% | 1.96 | +13.5% (383) | -10.0% (41) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1005 | 514 | +6.7% | 1.82 | +8.3% (942) | -15.6% (63) | yes |
| carelia | tag | 184 | 108 | +11.1% | 1.21 | +9.6% (156) | +19.8% (28) | yes |
| Manchester4ever | tag | 256 | 155 | +7.8% | 1.31 | +6.7% (216) | +13.5% (40) | yes |
| CUTJALENHURTS | tag | 145 | 79 | +13.0% | 1.14 | +21.4% (104) | -8.5% (41) | yes |
| -5rud | tag | 472 | 323 | +5.3% | 1.31 | +7.1% (402) | -4.9% (70) | yes |
| nightcity2077 | tag | 269 | 136 | +11.4% | 1.09 | +14.3% (258) | -58.0% (11) | yes |
| swaz13131313 | tag | 59 | 52 | +5.9% | 1.15 | +0.0% (0) | +5.9% (59) | yes |
| vardaman-bundren | tag | 330 | 159 | +8.3% | 1.06 | +10.0% (258) | +2.2% (72) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 529 | 278 | +4.5% | 1.05 | +8.2% (350) | -2.6% (179) | yes |
| RensPeters | tag | 106 | 63 | +9.4% | 0.95 | +11.9% (100) | -32.7% (6) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 69 | 46 | +9.8% | 0.91 | -23.5% (3) | +11.3% (66) | yes |
| juice-fruit | current | 30 | 20 | +15.2% | 0.94 | +24.0% (23) | -12.2% (7) | yes |
| moreplatesmoredates | tag | 918 | 461 | +2.0% | 0.69 | +1.4% (676) | +3.7% (242) | yes |
| GC-C | tag | 782 | 543 | +1.1% | 0.34 | -1.9% (670) | +18.5% (112) | yes |
| returdmaxxer | tag | 335 | 304 | -0.2% | -0.08 | +0.8% (277) | -4.6% (58) | yes |
| ZTMZqClEsjMmwCDWXoG | tag | 975 | 561 | +1.2% | 0.37 | -1.2% (895) | +27.4% (80) | yes |
| 0xffAaEFb5f6762Cc70cb575Da87 | tag | 655 | 313 | +3.8% | 0.6 | +3.8% (604) | +4.6% (51) | yes |
| nibbio3 | tag | 70 | 34 | +16.8% | 0.86 | -0.6% (32) | +31.5% (38) | yes |
| shaw | tag | 149 | 98 | +3.9% | 0.63 | +6.5% (94) | -0.7% (55) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | +1.6% (205) | +4.5% (13) | no |
| AmericaFirst1 | current | 289 | 182 | +1.6% | 0.41 | +5.5% (243) | -19.0% (46) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 444 | 194 | -9.8% | -1.77 | no |
| Kch-Temp | 160 | 87 | +7.0% | 0.91 | yes |
| EdZachary | 140 | 56 | -7.9% | -0.73 | no |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | no |
| Jsram | 70 | 43 | +8.8% | 0.75 | no |
| Kkunn | 921 | 387 | +1.4% | 0.5 | yes |
| Sisyphus- | 126 | 71 | -2.4% | -0.24 | no |
| PEYZ-BIGGEST-FAN | 359 | 179 | -1.7% | -0.18 | no |
| theowalcott | 13 | 11 | +63.3% | 2.93 | no |
| HVAB | 381 | 232 | -4.2% | -0.91 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +5.3% | 1.01 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 53 | 48 | +43.6% | 4.28 | yes |
| 0010001000001100 | 170 | 86 | +7.8% | 0.65 | yes |
| totoro3miyazaki | 45 | 30 | +14.8% | 1.07 | no |
| 1l2ihj34li12u34 | 87 | 52 | +17.8% | 1.85 | yes |
| yabanci | 83 | 47 | -3.6% | -0.07 | no |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 54 | 33 | +1.2% | 0.2 | yes |
| 0x16bb9951a36fce71e2ef57890b | 64 | 24 | -9.3% | -0.65 | yes |
| GamblingOdyssey | 312 | 170 | +4.1% | 0.8 | no |
| plonker2026 | 84 | 46 | +9.6% | 0.92 | no |
| xxyx0xx | 269 | 133 | +24.4% | 1.66 | no |
| monkeymashingkeyboard | 1016 | 539 | +4.0% | 1.21 | yes |
| Tiger105 | 37 | 26 | +27.6% | 1.88 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 548 | 315 | +0.7% | 0.24 | no |
| UNEB3154s4f251 | 2072 | 1293 | +2.0% | 1.19 | no |
