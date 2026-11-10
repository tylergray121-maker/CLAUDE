# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-10 09:00 UTC: 5679 candidates, 3888 with trades copytop could copy, 217 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2978 | 1500 | $29,346 | +223.91 | +0.8% | +0.23 |
| every wallet that qualified on the first part (test window) | 4296 | 2177 | $42,615 | +75.44 | +0.2% | +0.01 |
| currently copied (test window) | 3168 | 1633 | $30,946 | +41.34 | +0.1% | +0.32 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2978 | 1500 | $29,346 | +223.91 | +0.8% | 0.23 | 5408 | 2665 | $53,408 | +3,286.54 | +6.2% | 3.03 |
| copy their sells too | 2978 | 1495 | $29,346 | +175.47 | +0.6% | 0.17 | 5408 | 2658 | $53,408 | +3,201.16 | +6.0% | 2.95 |
| size by conviction (x0.5 / x1 / x1.5) | 2902 | 1462 | $32,413 | +664.00 | +2.1% | 0.2 | 5255 | 2596 | $61,143 | +3,720.98 | +6.1% | 2.9 |
| skip bets under 0.5x their usual | 2569 | 1344 | $25,363 | +775.23 | +3.1% | 1.15 | 4859 | 2438 | $48,100 | +3,353.45 | +7.0% | 3.39 |
| pre-game only | 976 | 510 | $9,658 | +805.91 | +8.3% | 2.43 | 2627 | 1304 | $25,848 | +3,121.37 | +12.1% | 4.52 |
| skip prices under 30c | 2353 | 1365 | $23,104 | -278.36 | -1.2% | -0.76 | 4145 | 2353 | $40,768 | +360.24 | +0.9% | 0.5 |
| favorites only (50c+) | 1431 | 1002 | $13,915 | +76.29 | +0.5% | 0.41 | 2233 | 1562 | $21,750 | +419.26 | +1.9% | 1.41 |
| 15s delay | 3283 | 1688 | $32,340 | +259.06 | +0.8% | 0.64 | 5808 | 2904 | $57,338 | +3,295.04 | +5.8% | 3.24 |
| 60s delay | 2978 | 1500 | $29,346 | +223.91 | +0.8% | 0.23 | 5408 | 2665 | $53,408 | +3,286.54 | +6.2% | 3.03 |
| allow 2c over their price | 3256 | 1645 | $32,092 | +286.84 | +0.9% | 0.3 | 5861 | 2889 | $57,892 | +3,196.18 | +5.5% | 2.85 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 317 | +31.2% | 3.17 | 425 | +8.3% | 0.8 |
| conviction:1-2x | 472 | +9.5% | 1.64 | 516 | -1.1% | -0.42 |
| conviction:2x+ | 1408 | +7.6% | 1.83 | 1441 | +4.4% | 1.47 |
| conviction:under 0.5x | 233 | +24.8% | 2.06 | 596 | -11.7% | -1.94 |
| delay_move:flat | 1527 | +15.2% | 3.72 | 1092 | +8.3% | 2.2 |
| delay_move:price fell | 903 | +8.6% | 1.63 | 1886 | -3.6% | -1.34 |
| exit:settle | 2430 | +12.7% | 3.98 | 2978 | +0.8% | 0.23 |
| kind:moneyline | 2120 | +13.6% | 3.88 | 2720 | +0.3% | 0.03 |
| kind:result | 273 | +7.0% | 0.85 | 45 | +23.8% | 0.94 |
| kind:totals | 37 | +6.3% | 0.52 | 213 | +1.8% | 0.34 |
| league:atp | 859 | +14.0% | 2.91 | 1541 | +0.8% | -0.0 |
| league:cbb | 0 | +0.0% | — | 42 | -14.1% | -0.41 |
| league:cfb | 7 | -27.6% | -0.61 | 48 | +14.5% | 0.76 |
| league:cs2 | 203 | +11.1% | 0.94 | 149 | +16.1% | 1.22 |
| league:dota2 | 83 | -17.5% | -1.26 | 82 | +19.4% | 1.03 |
| league:lol | 842 | +17.0% | 2.6 | 79 | +20.4% | 1.24 |
| league:nba | 10 | -27.6% | -0.75 | 304 | +0.5% | 0.39 |
| league:nfl | 1 | +29.3% | — | 18 | -39.6% | -1.35 |
| league:nhl | 83 | +27.8% | 3.22 | 71 | +4.7% | 0.57 |
| league:unl | 13 | +44.6% | 1.67 | 0 | +0.0% | — |
| league:wta | 327 | +4.1% | 0.6 | 642 | -7.2% | -1.84 |
| price:30-70c | 1516 | +3.2% | 1.16 | 1760 | -1.0% | -0.54 |
| price:over 70c | 271 | +5.1% | 1.9 | 571 | -1.5% | -0.83 |
| price:under 30c | 643 | +38.0% | 3.85 | 647 | +7.3% | 0.86 |
| timing:in-play | 779 | +9.5% | 1.53 | 2002 | -3.0% | -1.27 |
| timing:pre-game | 1651 | +14.3% | 3.82 | 976 | +8.3% | 2.43 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 116721 | 60991 | $1,158,154 | -50,789.82 | -4.4% | -12.69 |
| consistency (winning weeks), top 16 | 9563 | 4575 | $95,360 | -5,736.39 | -6.0% | -4.99 |
| consistency (winning weeks), top 40 | 24726 | 13055 | $244,501 | -11,174.13 | -4.6% | -6.25 |
| copy return, average, top 16 | 7721 | 3788 | $76,656 | -3,380.64 | -4.4% | -3.12 |
| copy return, average, top 40 | 22988 | 11369 | $228,095 | -9,108.14 | -4.0% | -4.94 |
| copy return, lower bound, top 16 | 10521 | 5200 | $104,193 | -5,087.14 | -4.9% | -4.33 |
| copy return, lower bound, top 40 | 24885 | 13037 | $245,979 | -10,972.00 | -4.5% | -6.20 |
| copy return, shrunk, top 16 | 8615 | 4199 | $85,622 | -4,875.33 | -5.7% | -4.35 |
| copy return, shrunk, top 40 | 22965 | 11354 | $227,870 | -9,221.98 | -4.0% | -5.00 |
| markout 2h, average, top 16 | 9926 | 5180 | $98,624 | -4,277.83 | -4.3% | -3.63 |
| markout 2h, average, top 40 | 23026 | 12266 | $228,989 | -10,858.13 | -4.7% | -6.21 |
| markout 2h, lower bound, top 16 | 12606 | 6616 | $125,037 | -6,462.33 | -5.2% | -5.00 |
| markout 2h, lower bound, top 40 | 25511 | 13438 | $253,191 | -11,852.83 | -4.7% | -6.55 |
| markout 30m, average, top 16 | 6430 | 3358 | $64,457 | -4,417.97 | -6.9% | -4.90 |
| markout 30m, average, top 40 | 22385 | 11799 | $223,312 | -12,243.21 | -5.5% | -7.11 |
| most active, top 16 | 18372 | 9774 | $182,151 | -8,606.60 | -4.7% | -5.58 |
| most active, top 40 | 33406 | 17542 | $331,473 | -13,662.57 | -4.1% | -6.30 |
| win rate vs the odds, top 16 | 8649 | 4285 | $85,885 | -3,595.62 | -4.2% | -3.10 |
| win rate vs the odds, top 40 | 21737 | 11036 | $216,491 | -9,374.74 | -4.3% | -5.35 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| Kch-Temp | 134 | 71 | +4.5% | 0.53 | +0.54 |
| cash-bundren | 387 | 156 | -3.2% | -0.48 | -0.32 |
| juice-fruit | 48 | 31 | +8.0% | 0.7 | +0.93 |
| 0x16bb9951a36fce71e2ef57890b | 63 | 23 | -11.2% | -0.76 | -1.19 |
| SimpleTony | 1040 | 336 | +10.8% | 1.95 | +1.13 |
| monkeymashingkeyboard | 951 | 512 | +7.4% | 2.09 | +0.74 |
| oxbus | 1100 | 560 | -0.6% | -0.05 | -0.02 |
| horaciorolinha | 571 | 263 | -3.8% | -0.7 | -0.38 |
| 636763 | 1442 | 471 | +2.6% | 0.64 | +0.33 |
| moreplatesmoredates | 967 | 487 | +3.5% | 1.01 | +0.43 |
| Popeyesfriedchicken | 664 | 363 | -3.7% | -0.68 | -0.38 |
| carelia | 1530 | 703 | -4.4% | -1.43 | -0.45 |
| Manchester4ever | 1052 | 609 | +2.9% | 0.97 | +0.29 |
| igot50k | 1551 | 977 | -0.1% | -0.07 | -0.02 |
| Future-Tarot-Trader | 1663 | 843 | -2.4% | -0.75 | -0.27 |
| 239393828 | 515 | 254 | -1.3% | -0.27 | -0.14 |
| trapfive | 772 | 333 | -1.2% | -0.25 | -0.12 |
| 0x5fD2D9C60781D711721145Ff2b | 696 | 385 | +5.8% | 0.98 | +0.54 |
| TearsInTheRain | 561 | 374 | -1.2% | -0.3 | -0.11 |
| ludo-money | 763 | 426 | -1.7% | -0.44 | -0.17 |
| pltrkr111 | 1132 | 651 | +13.8% | 3.54 | +1.33 |
| oookkjjdd | 772 | 385 | -1.9% | -0.41 | -0.17 |
| flatbarrel | 1488 | 750 | -6.2% | -1.85 | -0.62 |
| walnutz | 585 | 301 | -0.6% | -0.18 | -0.09 |
| 0x8g68hBa8tyH1946Bhjb674g3fu | 1265 | 702 | -0.0% | 0.0 | +0.00 |
| calvinoxieS | 676 | 303 | -4.5% | -0.96 | -0.44 |
| torta.tech | 887 | 555 | +0.6% | 0.2 | +0.06 |
| cryptoqan0n | 1269 | 643 | +0.8% | 0.2 | +0.07 |
| Bimboslaff | 494 | 235 | -2.1% | -0.34 | -0.19 |
| yuxkc0 | 342 | 116 | -6.4% | -0.77 | -0.64 |
| sweetcaroline | 659 | 543 | -0.6% | -0.35 | -0.06 |
| WeBuyHighWeSelllow | 888 | 459 | -8.2% | -2.1 | -0.74 |
| 0010001000001100 | 62 | 30 | +7.3% | 0.34 | +0.70 |
| fvckjumpjanestreet | 1606 | 905 | -3.9% | -1.59 | -0.38 |
| n1ck10s | 1285 | 668 | +0.1% | 0.01 | +0.00 |
| vardaman-bundren | 513 | 245 | +3.9% | 0.66 | +0.37 |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | +0.58 |
| -5rud | 962 | 641 | +2.1% | 0.8 | +0.22 |
| 0x1E3bB7DEf89B002D45FD86D37F | 2592 | 1515 | +0.0% | -0.06 | -0.01 |
| CUTJALENHURTS | 1146 | 643 | -1.5% | -0.51 | -0.17 |

## Esports specialists (copies on esports markets only)

3044 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 168 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +48.6% (76) | +0.0% (0) | no |
| pltrkr111 | tag | 284 | 160 | +29.8% | 2.95 | +30.0% (258) | +27.8% (26) | yes |
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 21 | 13 | +52.4% | 1.53 | +55.8% (7) | +50.7% (14) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 290 | 176 | +25.7% | 2.69 | +22.9% (271) | +67.2% (19) | no |
| BunCaCham | tag | 19 | 19 | +17.4% | 4.91 | +14.7% (11) | +21.1% (8) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 30 | 18 | +45.4% | 1.21 | +97.8% (14) | -0.4% (16) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1140 | 614 | +9.2% | 2.68 | +9.8% (1059) | +1.5% (81) | yes |
| SimpleTony | tag | 1040 | 336 | +10.8% | 1.95 | +8.4% (772) | +17.8% (268) | yes |
| -5rud | tag | 499 | 341 | +8.2% | 1.93 | +8.8% (421) | +5.3% (78) | yes |
| shaw | tag | 189 | 124 | +10.1% | 1.46 | +12.8% (138) | +2.6% (51) | yes |
| CUTJALENHURTS | tag | 156 | 85 | +13.8% | 1.24 | +15.4% (118) | +8.7% (38) | yes |
| Manchester4ever | tag | 253 | 154 | +8.1% | 1.36 | +5.4% (209) | +21.1% (44) | yes |
| MIracle33 | tag | 447 | 226 | +7.8% | 1.37 | +7.9% (398) | +6.5% (49) | yes |
| TAIWANNUMBERONE | tag | 834 | 460 | +5.5% | 1.44 | +1.1% (785) | +73.6% (49) | yes |
| ccwcc | tag | 331 | 169 | +10.6% | 1.19 | +12.4% (311) | -16.6% (20) | yes |
| ZEST011 | tag | 551 | 414 | +3.6% | 1.24 | +4.0% (485) | +0.4% (66) | no |
| littlebay | tag | 110 | 78 | +9.3% | 1.05 | +7.0% (79) | +14.8% (31) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 134 | 74 | +10.3% | 1.01 | +44.6% (9) | +7.9% (125) | yes |
| moreplatesmoredates | tag | 967 | 487 | +3.5% | 1.01 | +0.3% (676) | +10.8% (291) | yes |
| vardaman-bundren | tag | 339 | 163 | +7.5% | 0.98 | +8.5% (264) | +4.0% (75) | yes |
| carelia | tag | 202 | 117 | +8.3% | 0.97 | +7.0% (172) | +15.6% (30) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 548 | 287 | +3.4% | 0.95 | +8.9% (343) | -5.8% (205) | yes |
| ZTMZqClEsjMmwCDWXoG | tag | 1013 | 587 | +2.7% | 0.79 | +1.3% (921) | +16.4% (92) | yes |
| GC-C | tag | 779 | 547 | +2.0% | 0.72 | -2.5% (638) | +22.0% (141) | yes |
| 636763 | tag | 1407 | 459 | +3.5% | 0.81 | +2.4% (1097) | +7.2% (310) | yes |
| juice-fruit | current | 30 | 20 | +15.2% | 0.94 | +12.5% (20) | +20.3% (10) | yes |
| Gagalabu2 | tag | 346 | 154 | +8.1% | 0.85 | -1.4% (245) | +31.0% (101) | no |
| RensPeters | tag | 109 | 64 | +8.1% | 0.83 | +7.0% (97) | +17.0% (12) | yes |
| returdmaxxer | tag | 322 | 292 | -0.2% | -0.1 | +0.7% (276) | -5.9% (46) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 58 | 39 | +9.2% | 0.81 | -23.5% (3) | +11.0% (55) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 415 | 183 | -9.7% | -1.74 | no |
| Kch-Temp | 134 | 71 | +4.5% | 0.53 | yes |
| EdZachary | 133 | 49 | -10.9% | -0.98 | no |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | yes |
| Jsram | 12 | 6 | -15.8% | -0.68 | no |
| Kkunn | 868 | 366 | +0.5% | 0.36 | no |
| Sisyphus- | 128 | 69 | -5.1% | -0.57 | no |
| PEYZ-BIGGEST-FAN | 398 | 197 | -2.9% | -0.4 | no |
| theowalcott | — | — | — | — | no copyable trades |
| HVAB | 372 | 225 | -1.5% | -0.29 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +5.3% | 1.01 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 32 | 29 | +14.1% | 1.25 | no |
| 0010001000001100 | 62 | 30 | +7.3% | 0.34 | yes |
| totoro3miyazaki | 11 | 3 | -69.9% | -4.21 | no |
| 1l2ihj34li12u34 | 9 | 6 | +30.6% | 0.92 | no |
| yabanci | 80 | 45 | -4.0% | -0.1 | no |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 48 | 31 | +8.0% | 0.7 | yes |
| 0x16bb9951a36fce71e2ef57890b | 63 | 23 | -11.2% | -0.76 | yes |
| GamblingOdyssey | 333 | 172 | +8.0% | 1.46 | no |
| plonker2026 | 6 | 5 | +161.7% | 1.6 | no |
| xxyx0xx | 184 | 86 | +25.4% | 1.29 | no |
| monkeymashingkeyboard | 951 | 512 | +7.4% | 2.09 | yes |
| Tiger105 | 29 | 22 | +39.9% | 2.47 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 498 | 287 | +2.1% | 0.55 | no |
| UNEB3154s4f251 | 1803 | 1096 | +3.3% | 1.77 | no |
