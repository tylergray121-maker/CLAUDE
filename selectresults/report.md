# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-13 09:00 UTC: 5600 candidates, 3866 with trades copytop could copy, 222 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3955 | 1924 | $39,018 | -1,043.47 | -2.7% | -1.31 |
| every wallet that qualified on the first part (test window) | 4690 | 2361 | $46,320 | -1,268.87 | -2.7% | -1.52 |
| currently copied (test window) | 3246 | 1660 | $31,692 | -574.85 | -1.8% | -0.65 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3955 | 1924 | $39,018 | -1,043.47 | -2.7% | -1.31 | 6478 | 3166 | $64,037 | +2,343.63 | +3.7% | 1.89 |
| copy their sells too | 3955 | 1921 | $39,018 | -1,079.01 | -2.8% | -1.35 | 6478 | 3158 | $64,037 | +2,252.35 | +3.5% | 1.82 |
| size by conviction (x0.5 / x1 / x1.5) | 3864 | 1877 | $42,650 | -775.19 | -1.8% | -1.3 | 6312 | 3087 | $72,528 | +2,523.10 | +3.5% | 1.78 |
| skip bets under 0.5x their usual | 3372 | 1711 | $33,334 | -419.85 | -1.3% | -0.6 | 5744 | 2876 | $56,907 | +2,452.87 | +4.3% | 2.28 |
| pre-game only | 1116 | 538 | $11,080 | -54.03 | -0.5% | 0.24 | 2819 | 1390 | $27,814 | +2,642.01 | +9.5% | 3.77 |
| skip prices under 30c | 3040 | 1751 | $29,840 | -985.34 | -3.3% | -1.99 | 4940 | 2816 | $48,588 | -223.07 | -0.5% | -0.31 |
| favorites only (50c+) | 1839 | 1288 | $17,871 | -236.23 | -1.3% | -0.66 | 2742 | 1921 | $26,698 | +235.01 | +0.9% | 0.81 |
| 15s delay | 4395 | 2185 | $43,224 | -1,379.38 | -3.2% | -1.28 | 7022 | 3484 | $69,267 | +1,958.25 | +2.8% | 1.85 |
| 60s delay | 3955 | 1924 | $39,018 | -1,043.47 | -2.7% | -1.31 | 6478 | 3166 | $64,037 | +2,343.63 | +3.7% | 1.89 |
| allow 2c over their price | 4351 | 2130 | $42,847 | -911.95 | -2.1% | -1.06 | 7049 | 3453 | $69,619 | +2,367.48 | +3.4% | 1.88 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 316 | +25.9% | 2.83 | 570 | +1.1% | 0.0 |
| conviction:1-2x | 503 | +12.0% | 1.96 | 669 | -5.2% | -1.22 |
| conviction:2x+ | 1453 | +8.3% | 2.04 | 1872 | +0.3% | 0.18 |
| conviction:under 0.5x | 251 | +31.4% | 2.64 | 844 | -9.8% | -1.79 |
| delay_move:flat | 1541 | +18.0% | 4.38 | 1411 | -0.0% | 0.15 |
| delay_move:price fell | 982 | +6.7% | 1.36 | 2544 | -4.1% | -1.66 |
| exit:settle | 2523 | +13.5% | 4.34 | 3955 | -2.7% | -1.31 |
| kind:moneyline | 2154 | +13.1% | 3.8 | 3358 | -1.6% | -0.76 |
| kind:result | 321 | +17.2% | 2.11 | 264 | -30.8% | -4.73 |
| kind:totals | 48 | +8.7% | 0.78 | 333 | +8.0% | 1.16 |
| league:atp | 899 | +13.8% | 2.92 | 2026 | +1.0% | 0.1 |
| league:bra | 36 | +36.0% | 1.2 | 70 | -48.1% | -5.0 |
| league:bun | 9 | +80.1% | 2.93 | 11 | -48.4% | -2.38 |
| league:cbb | 0 | +0.0% | — | 68 | -11.1% | -0.42 |
| league:cfb | 7 | -27.6% | -0.61 | 51 | +7.5% | 0.42 |
| league:cs2 | 200 | +7.1% | 0.6 | 148 | +14.5% | 1.12 |
| league:dota2 | 84 | -18.5% | -1.34 | 85 | +16.1% | 0.83 |
| league:lal | 11 | -5.3% | -0.14 | 118 | -1.2% | -0.0 |
| league:lol | 819 | +19.9% | 3.04 | 60 | -2.3% | 0.15 |
| league:nba | 10 | -27.6% | -0.75 | 403 | -6.6% | -0.89 |
| league:nfl | 1 | +29.3% | — | 18 | -39.6% | -1.35 |
| league:nhl | 89 | +28.0% | 3.3 | 79 | +1.5% | 0.26 |
| league:unl | 19 | +81.5% | 2.2 | 80 | -17.5% | -1.47 |
| league:wta | 339 | +0.5% | -0.02 | 733 | -9.7% | -2.65 |
| price:30-70c | 1599 | +3.9% | 1.51 | 2194 | -3.3% | -1.56 |
| price:over 70c | 295 | +4.6% | 1.78 | 817 | -2.7% | -1.6 |
| price:under 30c | 629 | +41.8% | 4.07 | 944 | -1.2% | -0.22 |
| timing:in-play | 820 | +8.3% | 1.39 | 2839 | -3.5% | -1.62 |
| timing:pre-game | 1703 | +16.1% | 4.39 | 1116 | -0.5% | 0.24 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 124763 | 64419 | $1,237,585 | -59,212.98 | -4.8% | -14.23 |
| consistency (winning weeks), top 16 | 9437 | 4783 | $93,980 | -5,105.70 | -5.4% | -4.59 |
| consistency (winning weeks), top 40 | 21677 | 11315 | $214,357 | -10,124.17 | -4.7% | -5.89 |
| copy return, average, top 16 | 10038 | 4945 | $98,626 | -6,959.46 | -7.1% | -6.08 |
| copy return, average, top 40 | 25878 | 12522 | $256,182 | -14,340.87 | -5.6% | -7.11 |
| copy return, lower bound, top 16 | 10413 | 5210 | $102,537 | -5,579.57 | -5.4% | -4.83 |
| copy return, lower bound, top 40 | 23888 | 12356 | $236,053 | -11,716.53 | -5.0% | -6.64 |
| copy return, shrunk, top 16 | 9015 | 4347 | $88,960 | -6,087.26 | -6.8% | -5.47 |
| copy return, shrunk, top 40 | 26207 | 12704 | $259,423 | -14,650.61 | -5.7% | -7.25 |
| markout 2h, average, top 16 | 10104 | 5040 | $100,518 | -5,549.97 | -5.5% | -4.35 |
| markout 2h, average, top 40 | 25395 | 13043 | $252,626 | -14,043.63 | -5.6% | -7.15 |
| markout 2h, lower bound, top 16 | 12162 | 6292 | $120,688 | -7,741.63 | -6.4% | -5.84 |
| markout 2h, lower bound, top 40 | 29347 | 14989 | $291,660 | -16,818.97 | -5.8% | -8.25 |
| markout 30m, average, top 16 | 8879 | 4727 | $88,745 | -4,567.89 | -5.1% | -4.11 |
| markout 30m, average, top 40 | 25631 | 13176 | $255,581 | -16,771.67 | -6.6% | -8.75 |
| most active, top 16 | 18894 | 10079 | $187,088 | -9,785.67 | -5.2% | -6.39 |
| most active, top 40 | 34502 | 17859 | $342,233 | -16,321.20 | -4.8% | -7.39 |
| win rate vs the odds, top 16 | 8233 | 4141 | $81,546 | -4,076.56 | -5.0% | -3.72 |
| win rate vs the odds, top 40 | 25604 | 12991 | $253,625 | -12,310.62 | -4.9% | -6.54 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| 0010001000001100 | 100 | 50 | +14.1% | 0.76 | +1.37 |
| Kch-Temp | 137 | 73 | +5.5% | 0.64 | +0.64 |
| nightcity2077 | 579 | 281 | +4.0% | 0.61 | +0.40 |
| 0x16bb9951a36fce71e2ef57890b | 62 | 22 | -13.7% | -0.92 | -1.44 |
| Car-c | 637 | 330 | -0.2% | -0.05 | -0.03 |
| NS13 | 1223 | 481 | -1.9% | -0.42 | -0.21 |
| Popeyesfriedchicken | 658 | 358 | -3.6% | -0.65 | -0.37 |
| cash-bundren | 383 | 150 | -5.5% | -0.82 | -0.54 |
| oxbus | 1234 | 636 | -1.0% | -0.35 | -0.12 |
| carelia | 1424 | 664 | -3.6% | -1.13 | -0.37 |
| Future-Tarot-Trader | 1538 | 771 | -2.5% | -0.77 | -0.29 |
| moreplatesmoredates | 934 | 471 | +2.0% | 0.7 | +0.30 |
| trapfive | 759 | 325 | -1.0% | -0.21 | -0.10 |
| SimpleTony | 999 | 323 | +10.1% | 1.8 | +1.06 |
| Bimboslaff | 540 | 259 | -0.6% | -0.08 | -0.04 |
| monkeymashingkeyboard | 1011 | 532 | +4.2% | 1.21 | +0.42 |
| smithagent | 1244 | 687 | +3.5% | 0.82 | +0.35 |
| 0x567212c82AAa6fe589bE5A2f4C | 537 | 281 | +4.9% | 1.11 | +0.68 |
| 636763 | 1386 | 446 | +1.2% | 0.38 | +0.20 |
| juice-fruit | 51 | 31 | +1.4% | 0.22 | +0.29 |
| arahbo | 1375 | 579 | +1.1% | 0.22 | +0.10 |
| TearsInTheRain | 593 | 400 | +0.2% | 0.09 | +0.03 |
| walnutz | 557 | 285 | -0.9% | -0.26 | -0.12 |
| cryptoqan0n | 1323 | 676 | +1.7% | 0.46 | +0.16 |
| 0x8g68hBa8tyH1946Bhjb674g3fu | 1519 | 851 | +1.1% | 0.42 | +0.11 |
| yuxkc0 | 331 | 113 | -4.7% | -0.55 | -0.46 |
| SharkVision | 731 | 347 | -1.2% | -0.19 | -0.10 |
| zuihouyici | 645 | 330 | -1.0% | -0.25 | -0.11 |
| 0x5fD2D9C60781D711721145Ff2b | 698 | 384 | +3.9% | 0.66 | +0.36 |
| oookkjjdd | 745 | 369 | -2.6% | -0.55 | -0.23 |
| dewey-dell-bundren | 437 | 200 | -6.1% | -1.11 | -0.60 |
| MIracle33 | 692 | 341 | +3.4% | 0.79 | +0.35 |
| -5rud | 966 | 645 | +0.9% | 0.42 | +0.11 |
| ludo-money | 839 | 467 | -3.2% | -0.85 | -0.31 |
| User7429 | 844 | 441 | -4.6% | -1.15 | -0.47 |
| WeBuyHighWeSelllow | 1100 | 580 | -7.4% | -2.1 | -0.65 |
| Kkunn | 907 | 383 | +0.4% | 0.33 | +0.15 |
| vardaman-bundren | 518 | 248 | +4.3% | 0.73 | +0.41 |
| darkumbreon88 | 2188 | 1429 | -1.1% | -0.51 | -0.09 |
| minji | 635 | 295 | -4.8% | -0.99 | -0.52 |

## Esports specialists (copies on esports markets only)

2963 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 169 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +48.6% (76) | +0.0% (0) | no |
| pltrkr111 | tag | 284 | 160 | +29.8% | 2.95 | +33.7% (266) | -30.3% (18) | yes |
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 21 | 13 | +52.4% | 1.53 | +55.8% (7) | +50.7% (14) | no |
| Tomahawkmaster | leaderboard | 22 | 10 | +66.3% | 1.38 | +0.0% (0) | +66.3% (22) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 290 | 176 | +25.7% | 2.69 | +24.8% (289) | +269.1% (1) | no |
| BunCaCham | tag | 19 | 19 | +17.4% | 4.91 | +14.7% (11) | +21.1% (8) | yes |
| TAIWANNUMBERONE | tag | 760 | 430 | +10.8% | 2.62 | +7.1% (709) | +62.4% (51) | yes |
| MIracle33 | tag | 428 | 221 | +10.5% | 1.85 | +12.0% (384) | -2.4% (44) | yes |
| SimpleTony | tag | 999 | 323 | +10.1% | 1.8 | +7.8% (735) | +16.3% (264) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1045 | 550 | +7.6% | 2.1 | +8.8% (979) | -9.6% (66) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 30 | 17 | +41.5% | 1.1 | +79.8% (16) | -2.4% (14) | yes |
| swaz13131313 | tag | 56 | 50 | +7.7% | 1.55 | +0.0% (0) | +7.7% (56) | yes |
| CUTJALENHURTS | tag | 145 | 79 | +13.0% | 1.14 | +21.4% (104) | -8.5% (41) | yes |
| ZEST011 | tag | 516 | 390 | +4.3% | 1.46 | +5.1% (455) | -1.1% (61) | no |
| vardaman-bundren | tag | 332 | 161 | +9.1% | 1.18 | +10.2% (258) | +5.5% (74) | yes |
| -5rud | tag | 476 | 325 | +5.1% | 1.29 | +6.3% (408) | -2.2% (68) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 537 | 281 | +4.9% | 1.11 | +6.9% (312) | +2.0% (225) | yes |
| RensPeters | tag | 107 | 64 | +10.1% | 1.04 | +12.6% (101) | -32.7% (6) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 67 | 45 | +10.1% | 0.94 | -23.5% (3) | +11.7% (64) | yes |
| carelia | tag | 200 | 115 | +7.9% | 0.92 | +6.6% (171) | +15.7% (29) | no |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 150 | 85 | +8.2% | 0.89 | +41.2% (10) | +5.9% (140) | yes |
| juice-fruit | current | 30 | 20 | +15.2% | 0.94 | +12.5% (20) | +20.3% (10) | yes |
| nightcity2077 | tag | 281 | 140 | +8.8% | 0.87 | +11.4% (269) | -52.0% (12) | yes |
| moreplatesmoredates | tag | 934 | 471 | +2.0% | 0.7 | +1.1% (685) | +4.5% (249) | yes |
| Gagalabu2 | tag | 346 | 154 | +8.1% | 0.85 | -1.4% (267) | +40.0% (79) | no |
| shaw | tag | 154 | 103 | +5.0% | 0.79 | +7.0% (100) | +1.2% (54) | yes |
| GC-C | tag | 787 | 547 | +1.0% | 0.34 | -3.8% (665) | +26.6% (122) | yes |
| returdmaxxer | tag | 333 | 302 | -0.2% | -0.12 | +0.8% (277) | -5.3% (56) | yes |
| ZTMZqClEsjMmwCDWXoG | tag | 986 | 567 | +0.9% | 0.28 | -1.2% (906) | +24.2% (80) | yes |
| 636763 | tag | 1350 | 433 | +2.1% | 0.52 | +0.4% (1061) | +8.3% (289) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 437 | 189 | -9.9% | -1.77 | no |
| Kch-Temp | 137 | 73 | +5.5% | 0.64 | yes |
| EdZachary | 140 | 56 | -7.9% | -0.73 | no |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | no |
| Jsram | 10 | 6 | -0.2% | -0.03 | no |
| Kkunn | 907 | 383 | +0.4% | 0.33 | yes |
| Sisyphus- | 126 | 71 | -2.0% | -0.2 | no |
| PEYZ-BIGGEST-FAN | 372 | 185 | -3.0% | -0.39 | no |
| theowalcott | 13 | 11 | +63.3% | 2.93 | no |
| HVAB | 381 | 231 | -1.6% | -0.31 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +5.3% | 1.01 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 31 | 28 | +14.2% | 1.22 | no |
| 0010001000001100 | 100 | 50 | +14.1% | 0.76 | yes |
| totoro3miyazaki | 26 | 14 | -21.6% | -1.41 | no |
| 1l2ihj34li12u34 | 37 | 17 | -8.3% | -0.51 | no |
| yabanci | 82 | 46 | -4.0% | -0.11 | no |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 51 | 31 | +1.4% | 0.22 | yes |
| 0x16bb9951a36fce71e2ef57890b | 62 | 22 | -13.7% | -0.92 | yes |
| GamblingOdyssey | 328 | 178 | +9.8% | 1.58 | no |
| plonker2026 | 17 | 14 | +72.5% | 1.83 | no |
| xxyx0xx | 201 | 91 | +23.0% | 1.21 | no |
| monkeymashingkeyboard | 1011 | 532 | +4.2% | 1.21 | yes |
| Tiger105 | 34 | 25 | +34.2% | 2.28 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 532 | 306 | +1.6% | 0.44 | no |
| UNEB3154s4f251 | 1904 | 1161 | +2.6% | 1.43 | no |
