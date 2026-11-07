# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-07 09:00 UTC: 5653 candidates, 3874 with trades copytop could copy, 224 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 1161 | 650 | $11,472 | +731.53 | +6.4% | +2.16 |
| every wallet that qualified on the first part (test window) | 1464 | 812 | $14,530 | +884.02 | +6.1% | +2.09 |
| currently copied (test window) | 3780 | 1993 | $37,014 | +834.25 | +2.2% | +1.40 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 1161 | 650 | $11,472 | +731.53 | +6.4% | 2.16 | 3696 | 2146 | $36,003 | +5,064.96 | +14.1% | 7.54 |
| copy their sells too | 1161 | 633 | $11,472 | +544.01 | +4.7% | 1.67 | 3696 | 2116 | $36,003 | +4,758.70 | +13.2% | 7.16 |
| size by conviction (x0.5 / x1 / x1.5) | 1130 | 630 | $13,710 | +818.29 | +6.0% | 2.06 | 3543 | 2042 | $42,569 | +5,139.87 | +12.1% | 6.93 |
| skip bets under 0.5x their usual | 1098 | 621 | $10,855 | +847.77 | +7.8% | 2.51 | 3491 | 2028 | $34,245 | +4,747.47 | +13.9% | 7.23 |
| pre-game only | 908 | 538 | $8,906 | +871.41 | +9.8% | 3.04 | 3056 | 1825 | $29,537 | +5,055.09 | +17.1% | 8.26 |
| skip prices under 30c | 1079 | 620 | $10,647 | +363.62 | +3.4% | 1.34 | 3316 | 1995 | $32,246 | +2,389.24 | +7.4% | 4.83 |
| favorites only (50c+) | 659 | 430 | $6,450 | +267.84 | +4.2% | 1.52 | 1917 | 1345 | $18,488 | +1,471.76 | +8.0% | 5.04 |
| 15s delay | 1195 | 669 | $11,808 | +785.66 | +6.7% | 2.25 | 3785 | 2199 | $36,890 | +5,220.48 | +14.1% | 7.67 |
| 60s delay | 1161 | 650 | $11,472 | +731.53 | +6.4% | 2.16 | 3696 | 2146 | $36,003 | +5,064.96 | +14.1% | 7.54 |
| allow 2c over their price | 1206 | 672 | $11,926 | +659.33 | +5.5% | 1.94 | 3879 | 2250 | $37,791 | +5,055.71 | +13.4% | 7.35 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 337 | +21.9% | 3.5 | 160 | +5.8% | 0.52 |
| conviction:1-2x | 421 | +22.9% | 3.44 | 186 | +10.9% | 1.48 |
| conviction:2x+ | 1456 | +12.7% | 4.37 | 675 | +5.2% | 1.48 |
| conviction:under 0.5x | 321 | +30.1% | 3.93 | 140 | +6.5% | 0.74 |
| delay_move:flat | 1465 | +17.9% | 5.62 | 721 | +11.0% | 2.97 |
| delay_move:price fell | 1070 | +17.3% | 4.96 | 440 | -1.0% | -0.22 |
| exit:settle | 2535 | +17.7% | 7.49 | 1161 | +6.4% | 2.16 |
| kind:moneyline | 1782 | +13.5% | 4.57 | 774 | +5.9% | 1.56 |
| kind:result | 659 | +26.0% | 6.37 | 168 | +14.9% | 1.85 |
| kind:totals | 94 | +37.0% | 4.7 | 219 | +1.6% | 0.27 |
| league:atp | 632 | +8.1% | 1.68 | 419 | +5.3% | 1.07 |
| league:bel1 | 0 | +0.0% | — | 13 | +5.5% | 0.21 |
| league:bun | 9 | +80.1% | 2.93 | 4 | -100.0% | — |
| league:cfb | 6 | -17.8% | -0.31 | 19 | +35.5% | 1.31 |
| league:cs2 | 132 | +21.4% | 2.5 | 14 | -49.1% | -2.48 |
| league:dota2 | 36 | +4.8% | 0.31 | 2 | +51.0% | 1.38 |
| league:epl | 54 | +35.2% | 3.23 | 71 | +13.9% | 1.01 |
| league:ere | 8 | +106.7% | 28.83 | 40 | +1.0% | 0.16 |
| league:lal | 22 | +26.1% | 1.67 | 26 | -12.8% | -0.64 |
| league:lol | 1140 | +20.8% | 5.5 | 75 | +32.2% | 2.26 |
| league:mls | 27 | +5.9% | 0.34 | 22 | -21.5% | -1.07 |
| league:nba | 0 | +0.0% | — | 106 | +2.4% | 0.49 |
| league:nfl | 47 | +28.6% | 1.47 | 12 | +81.4% | 2.8 |
| league:nhl | 52 | +35.6% | 3.59 | 69 | +21.4% | 2.35 |
| league:sea | 39 | +59.6% | 3.86 | 73 | +13.2% | 1.31 |
| league:spl | 9 | +68.6% | 3.06 | 4 | -39.9% | -1.14 |
| league:unl | 40 | +40.5% | 1.89 | 0 | +0.0% | — |
| league:wta | 280 | +4.8% | 0.72 | 191 | -4.0% | -0.55 |
| price:30-70c | 1847 | +10.2% | 4.57 | 956 | +5.0% | 1.77 |
| price:over 70c | 387 | +5.2% | 2.35 | 123 | -9.2% | -1.86 |
| price:under 30c | 301 | +78.2% | 5.9 | 82 | +44.6% | 2.0 |
| timing:in-play | 387 | +3.8% | 0.69 | 253 | -5.5% | -0.78 |
| timing:pre-game | 2148 | +20.3% | 7.75 | 908 | +9.8% | 3.04 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 133575 | 69948 | $1,327,346 | -47,383.73 | -3.6% | -11.13 |
| consistency (winning weeks), top 16 | 6968 | 3766 | $69,436 | -1,609.07 | -2.3% | -1.62 |
| consistency (winning weeks), top 40 | 21400 | 11279 | $212,883 | -7,493.14 | -3.5% | -4.40 |
| copy return, average, top 16 | 5321 | 2522 | $53,053 | -1,120.52 | -2.1% | -1.11 |
| copy return, average, top 40 | 20075 | 10156 | $198,998 | -5,410.60 | -2.7% | -3.13 |
| copy return, lower bound, top 16 | 6781 | 3312 | $67,156 | -1,205.86 | -1.8% | -1.21 |
| copy return, lower bound, top 40 | 22448 | 11668 | $223,093 | -7,300.85 | -3.3% | -4.09 |
| copy return, shrunk, top 16 | 6746 | 3191 | $67,040 | -1,411.28 | -2.1% | -1.32 |
| copy return, shrunk, top 40 | 20075 | 10156 | $198,998 | -5,410.60 | -2.7% | -3.13 |
| markout 2h, average, top 16 | 9279 | 5015 | $91,749 | -1,435.52 | -1.6% | -1.44 |
| markout 2h, average, top 40 | 19197 | 9896 | $191,128 | -4,258.40 | -2.2% | -2.61 |
| markout 2h, lower bound, top 16 | 8688 | 4555 | $86,146 | -2,370.60 | -2.8% | -2.29 |
| markout 2h, lower bound, top 40 | 25137 | 13490 | $249,053 | -8,062.55 | -3.2% | -4.67 |
| markout 30m, average, top 16 | 8581 | 4756 | $85,205 | -3,288.32 | -3.9% | -3.26 |
| markout 30m, average, top 40 | 23250 | 12830 | $231,028 | -6,923.50 | -3.0% | -3.99 |
| most active, top 16 | 20936 | 11096 | $207,415 | -5,414.80 | -2.6% | -3.33 |
| most active, top 40 | 40740 | 21395 | $403,995 | -15,424.24 | -3.8% | -6.69 |
| win rate vs the odds, top 16 | 4187 | 2222 | $41,783 | -542.80 | -1.3% | -0.57 |
| win rate vs the odds, top 40 | 19927 | 10432 | $197,116 | -5,799.80 | -2.9% | -3.52 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 50 | 46 | +41.4% | 4.17 | +4.03 |
| xxyx0xx | 274 | 135 | +23.0% | 1.59 | +2.16 |
| 1l2ihj34li12u34 | 85 | 56 | +30.9% | 3.05 | +3.26 |
| plonker2026 | 114 | 68 | +26.2% | 2.43 | +2.85 |
| eokho | 841 | 477 | +5.8% | 1.31 | +0.55 |
| platarb | 490 | 190 | -2.6% | -0.46 | -0.27 |
| juice-fruit | 47 | 30 | +8.0% | 0.67 | +0.90 |
| oxbus | 1394 | 701 | -3.6% | -1.19 | -0.37 |
| moreplatesmoredates | 942 | 472 | +3.2% | 0.92 | +0.40 |
| Kch-Temp | 148 | 80 | +2.8% | 0.53 | +0.45 |
| WagerWizard | 636 | 345 | -4.8% | -1.0 | -0.46 |
| Notradecopy | 776 | 342 | +1.2% | 0.21 | +0.11 |
| SimpleTony | 1085 | 347 | +10.5% | 1.89 | +1.07 |
| carelia | 1812 | 849 | -3.8% | -1.35 | -0.38 |
| Future-Tarot-Trader | 1740 | 884 | -0.9% | -0.35 | -0.12 |
| 0x16bb9951a36fce71e2ef57890b | 60 | 22 | -8.7% | -0.58 | -0.94 |
| monkeymashingkeyboard | 901 | 474 | +5.3% | 1.44 | +0.53 |
| AmericaFirst1 | 504 | 300 | +3.1% | 0.8 | +0.34 |
| ludo-money | 866 | 490 | -1.2% | -0.35 | -0.13 |
| nightcity2077 | 781 | 366 | +0.2% | 0.04 | +0.02 |
| walnutz | 604 | 309 | -1.4% | -0.35 | -0.16 |
| yabanci | 78 | 46 | +0.4% | 0.3 | +0.32 |
| Manchester4ever | 1024 | 589 | +1.7% | 0.56 | +0.17 |
| Limousin | 1641 | 864 | +3.9% | 0.86 | +0.30 |
| oookkjjdd | 880 | 442 | -2.9% | -0.7 | -0.26 |
| igot50k | 1601 | 1000 | -0.8% | -0.34 | -0.09 |
| flatbarrel | 1539 | 774 | -7.0% | -2.13 | -0.70 |
| 0010001000001100 | 143 | 75 | +9.1% | 0.67 | +0.92 |
| smithagent | 1237 | 685 | +2.1% | 0.53 | +0.21 |
| dv-pm | 1069 | 493 | -2.9% | -0.67 | -0.28 |
| pltrkr111 | 1171 | 668 | +13.0% | 3.49 | +1.27 |
| 0x5fD2D9C60781D711721145Ff2b | 696 | 385 | +5.3% | 0.89 | +0.49 |
| yuxkc0 | 347 | 118 | -6.5% | -0.79 | -0.65 |
| clownly | 2159 | 806 | -6.1% | -2.24 | -0.62 |
| 0x1E3bB7DEf89B002D45FD86D37F | 2272 | 1347 | +1.8% | 0.61 | +0.16 |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | +0.58 |
| User7429 | 938 | 490 | -3.7% | -0.98 | -0.38 |
| n1ck10s | 1230 | 647 | +1.4% | 0.39 | +0.13 |
| torta.tech | 1197 | 720 | -2.0% | -0.67 | -0.19 |
| trapfive | 804 | 347 | -1.3% | -0.28 | -0.13 |

## Esports specialists (copies on esports markets only)

2991 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 164 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +48.6% (76) | +0.0% (0) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +30.4% (253) | +57.3% (24) | no |
| am100 | tag | 771 | 495 | +22.8% | 5.47 | +21.8% (747) | +52.2% (24) | no |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 291 | 176 | +25.3% | 2.65 | +21.2% (256) | +56.2% (35) | no |
| BunCaCham | tag | 18 | 18 | +14.4% | 7.11 | +14.7% (11) | +13.9% (7) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 25 | 15 | +54.2% | 1.23 | +97.8% (14) | -1.1% (11) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1151 | 624 | +11.2% | 3.12 | +11.5% (1076) | +6.7% (75) | yes |
| CUTJALENHURTS | tag | 152 | 85 | +17.6% | 1.64 | +17.7% (120) | +17.3% (32) | yes |
| SimpleTony | tag | 1076 | 343 | +10.4% | 1.86 | +7.5% (801) | +19.0% (275) | yes |
| -5rud | tag | 505 | 347 | +8.3% | 1.97 | +8.5% (422) | +7.3% (83) | yes |
| MIracle33 | tag | 448 | 227 | +9.1% | 1.58 | +10.4% (385) | +0.9% (63) | yes |
| Manchester4ever | tag | 249 | 153 | +9.3% | 1.52 | +5.6% (205) | +26.1% (44) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +2.1% (16) | +39.4% (13) | no |
| ccwcc | tag | 328 | 169 | +11.7% | 1.3 | +13.5% (308) | -16.7% (20) | yes |
| TAIWANNUMBERONE | tag | 854 | 470 | +5.7% | 1.57 | +1.6% (806) | +72.4% (48) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 582 | 306 | +5.3% | 1.27 | +10.1% (378) | -3.6% (204) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 108 | 60 | +12.9% | 1.1 | +44.6% (9) | +10.1% (99) | yes |
| ZEST011 | tag | 588 | 441 | +3.4% | 1.23 | +3.8% (522) | +0.4% (66) | no |
| littlebay | tag | 110 | 78 | +9.3% | 1.05 | +9.4% (74) | +9.2% (36) | yes |
| RensPeters | tag | 109 | 65 | +9.8% | 1.01 | +8.0% (95) | +22.7% (14) | no |
| moreplatesmoredates | tag | 942 | 472 | +3.2% | 0.92 | +0.4% (668) | +10.1% (274) | yes |
| 636763 | tag | 1412 | 456 | +4.0% | 0.89 | +1.8% (1119) | +12.5% (293) | yes |
| carelia | tag | 206 | 119 | +7.5% | 0.9 | +5.7% (171) | +16.3% (35) | yes |
| GC-C | tag | 778 | 546 | +1.9% | 0.69 | -2.2% (606) | +16.4% (172) | yes |
| berlinskies | tag | 1029 | 598 | +2.5% | 0.74 | +2.1% (920) | +6.0% (109) | yes |
| AmericaFirst1 | tag | 279 | 177 | +2.8% | 0.64 | +6.8% (233) | -17.7% (46) | yes |
| nightcity2077 | tag | 360 | 174 | +6.2% | 0.71 | +7.8% (349) | -46.4% (11) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | +0.6% (181) | +7.6% (37) | no |
| 0ooo0o0o0oo0o0 | tag | 167 | 100 | +3.8% | 0.53 | +3.7% (130) | +4.0% (37) | yes |
| Diabolical-Prize | current | 224 | 118 | +2.1% | 0.47 | +8.6% (202) | -58.0% (22) | no |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 347 | 144 | -9.0% | -1.46 | no |
| Kch-Temp | 148 | 80 | +2.8% | 0.53 | yes |
| EdZachary | 107 | 44 | +2.4% | 0.16 | no |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | yes |
| Jsram | 71 | 42 | +4.8% | 0.37 | no |
| Kkunn | 848 | 356 | +1.5% | 0.52 | no |
| Sisyphus- | 127 | 70 | -4.0% | -0.44 | no |
| PEYZ-BIGGEST-FAN | 382 | 194 | -0.2% | 0.04 | no |
| theowalcott | 98 | 47 | -10.8% | -0.92 | no |
| HVAB | 366 | 223 | -0.4% | -0.1 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +5.3% | 1.01 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 50 | 46 | +41.4% | 4.17 | yes |
| 0010001000001100 | 143 | 75 | +9.1% | 0.67 | yes |
| totoro3miyazaki | 45 | 30 | +14.8% | 1.07 | no |
| 1l2ihj34li12u34 | 85 | 56 | +30.9% | 3.05 | yes |
| yabanci | 78 | 46 | +0.4% | 0.3 | yes |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 47 | 30 | +8.0% | 0.67 | yes |
| 0x16bb9951a36fce71e2ef57890b | 60 | 22 | -8.7% | -0.58 | yes |
| GamblingOdyssey | 370 | 191 | +6.7% | 1.32 | no |
| plonker2026 | 114 | 68 | +26.2% | 2.43 | yes |
| xxyx0xx | 274 | 135 | +23.0% | 1.59 | yes |
| monkeymashingkeyboard | 901 | 474 | +5.3% | 1.44 | yes |
| Tiger105 | 41 | 28 | +23.9% | 1.68 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 504 | 300 | +3.1% | 0.8 | yes |
| UNEB3154s4f251 | 2216 | 1388 | +2.1% | 1.29 | no |
