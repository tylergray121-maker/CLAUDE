# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-02 09:00 UTC: 5582 candidates, 3833 with trades copytop could copy, 217 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2780 | 1380 | $26,976 | -52.75 | -0.2% | -0.05 |
| every wallet that qualified on the first part (test window) | 2834 | 1402 | $27,524 | +17.19 | +0.1% | +0.05 |
| currently copied (test window) | 4028 | 2149 | $39,572 | +969.77 | +2.5% | +1.58 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2780 | 1380 | $26,976 | -52.75 | -0.2% | -0.05 | 6593 | 3329 | $64,010 | +5,140.82 | +8.0% | 4.9 |
| copy their sells too | 2791 | 1060 | $27,078 | -508.41 | -1.9% | -0.92 | 6604 | 2780 | $64,112 | +3,888.42 | +6.1% | 3.93 |
| size by conviction (x0.5 / x1 / x1.5) | 2655 | 1314 | $32,157 | +333.09 | +1.0% | -0.11 | 6274 | 3155 | $76,027 | +5,786.35 | +7.6% | 4.56 |
| skip bets under 0.5x their usual | 2605 | 1294 | $25,504 | -34.64 | -0.1% | 0.1 | 6182 | 3132 | $60,509 | +4,894.24 | +8.1% | 4.88 |
| pre-game only | 2617 | 1312 | $25,335 | -249.14 | -1.0% | -0.35 | 6085 | 3123 | $58,885 | +4,906.93 | +8.3% | 5.08 |
| skip prices under 30c | 2340 | 1272 | $22,608 | -380.31 | -1.7% | -0.92 | 5314 | 2941 | $51,274 | +338.68 | +0.7% | 0.62 |
| favorites only (50c+) | 1290 | 851 | $12,354 | +102.11 | +0.8% | 0.42 | 2745 | 1860 | $26,153 | +494.24 | +1.9% | 1.5 |
| 15s delay | 2796 | 1391 | $27,164 | +180.34 | +0.7% | 0.35 | 6648 | 3363 | $64,592 | +5,603.29 | +8.7% | 5.27 |
| 60s delay | 2780 | 1380 | $26,976 | -52.75 | -0.2% | -0.05 | 6593 | 3329 | $64,010 | +5,140.82 | +8.0% | 4.9 |
| allow 2c over their price | 2847 | 1414 | $27,609 | +160.65 | +0.6% | 0.24 | 6849 | 3454 | $66,494 | +5,447.74 | +8.2% | 5.01 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 427 | +23.8% | 3.38 | 310 | +1.9% | 0.23 |
| conviction:1-2x | 631 | +15.8% | 2.49 | 333 | -2.4% | -0.21 |
| conviction:2x+ | 2304 | +10.4% | 3.68 | 1791 | +2.0% | 0.68 |
| conviction:under 0.5x | 451 | +21.4% | 3.1 | 346 | -11.3% | -1.81 |
| delay_move:flat | 2535 | +16.3% | 5.61 | 2149 | -1.2% | -0.42 |
| delay_move:price fell | 1278 | +9.4% | 2.54 | 631 | +3.1% | 0.7 |
| exit:settle | 3813 | +14.0% | 6.1 | 2780 | -0.2% | -0.05 |
| kind:moneyline | 2909 | +11.4% | 4.14 | 2307 | -2.0% | -0.85 |
| kind:result | 831 | +22.7% | 5.17 | 313 | +12.0% | 2.12 |
| kind:totals | 73 | +20.4% | 2.3 | 160 | +1.5% | 0.18 |
| league:atp | 527 | +5.9% | 1.18 | 217 | +13.1% | 2.15 |
| league:bun | 9 | +80.1% | 2.93 | 4 | -100.0% | — |
| league:cfb | 204 | +3.0% | 0.44 | 298 | +17.7% | 1.94 |
| league:cs2 | 348 | +15.0% | 1.96 | 206 | +3.8% | 0.59 |
| league:dota2 | 111 | -4.8% | -0.43 | 88 | +22.4% | 1.17 |
| league:epl | 54 | +35.2% | 3.23 | 65 | +7.5% | 0.44 |
| league:lal | 70 | +15.4% | 1.43 | 125 | +8.4% | 1.1 |
| league:lol | 1760 | +17.3% | 4.46 | 228 | +1.8% | 0.18 |
| league:nba | 0 | +0.0% | — | 349 | -10.1% | -1.82 |
| league:nfl | 324 | +19.5% | 2.69 | 274 | -3.4% | -0.67 |
| league:nhl | 74 | +12.4% | 0.85 | 655 | -14.6% | -3.8 |
| league:sea | 34 | +54.4% | 3.14 | 44 | -23.7% | -1.35 |
| league:ucl | 41 | -4.3% | -0.32 | 64 | +16.9% | 1.42 |
| league:uel | 0 | +0.0% | — | 12 | +17.4% | 0.79 |
| league:wta | 244 | +8.4% | 0.98 | 139 | +4.5% | 0.44 |
| price:30-70c | 2470 | +3.1% | 1.72 | 1986 | -2.2% | -1.02 |
| price:over 70c | 499 | -1.1% | -0.46 | 348 | +0.8% | 0.23 |
| price:under 30c | 844 | +53.4% | 6.6 | 446 | +7.9% | 0.97 |
| timing:in-play | 345 | +1.1% | 0.06 | 163 | +12.0% | 0.77 |
| timing:pre-game | 3468 | +15.4% | 6.55 | 2617 | -1.0% | -0.35 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 128379 | 67015 | $1,276,663 | -50,965.62 | -4.0% | -12.10 |
| consistency (winning weeks), top 16 | 10317 | 5759 | $101,887 | -2,854.74 | -2.8% | -2.26 |
| consistency (winning weeks), top 40 | 22998 | 12529 | $227,336 | -7,706.56 | -3.4% | -4.45 |
| copy return, average, top 16 | 6348 | 3114 | $63,175 | -618.65 | -1.0% | -0.56 |
| copy return, average, top 40 | 22218 | 11632 | $220,355 | -5,629.48 | -2.5% | -2.95 |
| copy return, lower bound, top 16 | 7214 | 3657 | $71,253 | -2,527.09 | -3.5% | -2.58 |
| copy return, lower bound, top 40 | 23358 | 12305 | $230,606 | -7,921.52 | -3.4% | -4.29 |
| copy return, shrunk, top 16 | 7075 | 3421 | $70,244 | -1,499.34 | -2.1% | -1.39 |
| copy return, shrunk, top 40 | 21828 | 11449 | $216,304 | -5,351.66 | -2.5% | -2.81 |
| markout 2h, average, top 16 | 7666 | 4190 | $76,541 | -2,407.46 | -3.1% | -2.11 |
| markout 2h, average, top 40 | 21832 | 11762 | $217,444 | -8,202.66 | -3.8% | -4.64 |
| markout 2h, lower bound, top 16 | 7965 | 4294 | $79,204 | -5,172.68 | -6.5% | -5.00 |
| markout 2h, lower bound, top 40 | 23476 | 12691 | $232,721 | -9,450.02 | -4.1% | -5.25 |
| markout 30m, average, top 16 | 9656 | 5500 | $96,304 | -1,945.00 | -2.0% | -1.64 |
| markout 30m, average, top 40 | 24570 | 13562 | $245,128 | -6,449.67 | -2.6% | -3.53 |
| most active, top 16 | 20626 | 10732 | $205,540 | -9,249.45 | -4.5% | -5.53 |
| most active, top 40 | 38845 | 20231 | $385,080 | -16,604.30 | -4.3% | -7.32 |
| win rate vs the odds, top 16 | 4890 | 2610 | $48,302 | +248.56 | +0.5% | +0.31 |
| win rate vs the odds, top 40 | 20732 | 10897 | $205,661 | -7,555.06 | -3.7% | -4.41 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 55 | 50 | +36.2% | 3.82 | +3.52 |
| chillhouse123 | 849 | 459 | +0.3% | -0.1 | -0.05 |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | +4.48 |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | +3.03 |
| xxyx0xx | 285 | 141 | +6.1% | 0.58 | +0.56 |
| 1l2ihj34li12u34 | 102 | 64 | +24.6% | 2.73 | +2.73 |
| eokho | 798 | 444 | +3.8% | 0.81 | +0.35 |
| am100 | 916 | 549 | +13.9% | 3.6 | +1.38 |
| juice-fruit | 47 | 32 | +11.5% | 0.96 | +1.24 |
| AmericaFirst1 | 457 | 279 | +6.6% | 1.52 | +0.68 |
| 0x6918EA182D963b1Fb7888860b8 | 688 | 404 | +11.1% | 2.41 | +0.99 |
| yabanci | 73 | 46 | +7.4% | 0.95 | +1.01 |
| pltrkr111 | 1089 | 620 | +14.0% | 3.52 | +1.35 |
| moreplatesmoredates | 930 | 466 | +2.8% | 0.87 | +0.38 |
| platarb | 515 | 208 | +0.0% | -0.01 | -0.01 |
| SimpleTony | 1126 | 374 | +12.4% | 2.31 | +1.27 |
| KaneAnalytics | 172 | 93 | +7.2% | 0.63 | +0.70 |
| Jsram | 100 | 61 | +5.1% | 0.73 | +0.64 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 784 | 348 | +5.3% | 0.84 | +0.51 |
| monkeymashingkeyboard | 785 | 414 | +6.9% | 1.69 | +0.68 |
| GamblingOdyssey | 355 | 182 | +8.5% | 1.54 | +0.98 |
| Sisyphus- | 120 | 66 | -4.0% | -0.43 | -0.38 |
| arahbo | 1518 | 637 | -2.6% | -0.64 | -0.27 |
| cosmicsteaks | 1186 | 510 | -1.1% | -0.29 | -0.13 |
| smithagent | 1061 | 579 | +3.6% | 0.73 | +0.36 |
| Future-Tarot-Trader | 1946 | 992 | -1.5% | -0.54 | -0.18 |
| 636763 | 1461 | 459 | +1.7% | 0.47 | +0.24 |
| darkumbreon88 | 1762 | 1205 | +3.7% | 1.63 | +0.36 |
| igot50k | 1666 | 1024 | -0.6% | -0.24 | -0.06 |
| torta.tech | 1010 | 617 | +0.5% | 0.17 | +0.05 |
| iseedota | 1290 | 572 | -1.8% | -0.44 | -0.17 |
| n1ck10s | 1132 | 600 | +2.5% | 0.68 | +0.24 |
| 0x1E3bB7DEf89B002D45FD86D37F | 1360 | 807 | +2.6% | 0.65 | +0.23 |
| jiafan | 977 | 582 | +1.1% | 0.24 | +0.08 |
| UNEB3154s4f251 | 2130 | 1346 | +2.7% | 1.59 | +0.27 |
| assasin5002 | 598 | 297 | +2.1% | 0.35 | +0.19 |
| EdZachary | 104 | 42 | +2.1% | 0.14 | +0.19 |
| carelia | 1830 | 849 | -4.4% | -1.57 | -0.44 |
| walnutz | 626 | 319 | -2.4% | -0.56 | -0.25 |
| 0xffAaEFb5f6762Cc70cb575Da87 | 694 | 328 | +1.9% | 0.31 | +0.18 |

## Esports specialists (copies on esports markets only)

3006 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 167 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | tag | 76 | 43 | +48.6% | 2.16 | +42.4% (66) | +89.7% (10) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +32.2% (242) | +37.1% (35) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 298 | 182 | +25.5% | 2.74 | +20.6% (240) | +46.1% (58) | no |
| am100 | tag | 916 | 549 | +13.9% | 3.6 | +13.0% (876) | +32.8% (40) | yes |
| SimpleTony | tag | 1112 | 366 | +11.8% | 2.19 | +14.3% (791) | +5.6% (321) | yes |
| 0x6918EA182D963b1Fb7888860b8 | tag | 688 | 404 | +11.1% | 2.41 | +9.2% (639) | +35.8% (49) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1306 | 685 | +7.3% | 2.26 | +10.5% (1151) | -16.3% (155) | yes |
| -5rud | tag | 528 | 363 | +8.4% | 2.06 | +7.1% (437) | +14.8% (91) | yes |
| MIracle33 | tag | 449 | 229 | +9.6% | 1.68 | +9.5% (362) | +9.9% (87) | yes |
| Nooserac | tag | 150 | 83 | +14.6% | 1.38 | +5.9% (100) | +32.4% (50) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 78 | 46 | +15.9% | 1.22 | +44.6% (9) | +12.2% (69) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +0.0% (0) | +19.4% (29) | yes |
| BunCaCham | tag | 21 | 20 | +7.9% | 1.41 | +4.9% (14) | +13.9% (7) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 600 | 316 | +6.0% | 1.4 | +11.6% (410) | -6.0% (190) | yes |
| shaw | tag | 258 | 159 | +8.1% | 1.25 | +10.8% (205) | -2.8% (53) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 28 | 16 | +41.6% | 1.04 | +72.9% (16) | -0.5% (12) | yes |
| ZEST011 | tag | 645 | 484 | +3.1% | 1.19 | +3.0% (554) | +3.8% (91) | yes |
| AmericaFirst1 | current | 256 | 165 | +5.1% | 1.03 | +7.3% (220) | -8.2% (36) | no |
| littlebay | tag | 97 | 72 | +6.7% | 0.96 | +9.3% (52) | +3.7% (45) | yes |
| moreplatesmoredates | tag | 930 | 466 | +2.8% | 0.87 | -0.3% (584) | +8.2% (346) | yes |
| yakz | leaderboard | 191 | 92 | +12.8% | 0.9 | +27.2% (111) | -7.4% (80) | yes |
| berlinskies | tag | 1043 | 605 | +2.0% | 0.62 | +2.7% (875) | -1.5% (168) | yes |
| GC-C | tag | 747 | 523 | +1.2% | 0.5 | -4.0% (454) | +9.6% (293) | yes |
| 636763 | tag | 1438 | 452 | +2.4% | 0.59 | -1.7% (1079) | +14.8% (359) | yes |
| TAIWANNUMBERONE | tag | 1026 | 543 | +0.5% | 0.2 | -0.5% (938) | +11.1% (88) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -2.1% (123) | +7.1% (95) | no |
| HalleyChen | tag | 613 | 375 | +1.8% | 0.38 | +2.5% (472) | -0.4% (141) | yes |
| johnbaster | tag | 786 | 420 | +1.9% | 0.32 | +1.1% (732) | +12.8% (54) | yes |
| dddd123s | tag | 579 | 348 | +0.0% | -0.01 | +4.6% (398) | -10.0% (181) | yes |
| nightcity2077 | tag | 413 | 200 | +4.1% | 0.53 | +5.6% (399) | -41.1% (14) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 311 | 129 | -9.8% | -1.47 | no |
| Kch-Temp | 127 | 61 | -6.8% | -0.67 | no |
| EdZachary | 104 | 42 | +2.1% | 0.14 | yes |
| KaneAnalytics | 172 | 93 | +7.2% | 0.63 | yes |
| Jsram | 100 | 61 | +5.1% | 0.73 | yes |
| Kkunn | 804 | 341 | +0.9% | 0.43 | no |
| Sisyphus- | 120 | 66 | -4.0% | -0.43 | yes |
| PEYZ-BIGGEST-FAN | 400 | 199 | +1.1% | 0.2 | no |
| theowalcott | 13 | 11 | +63.3% | 2.93 | no |
| HVAB | 342 | 207 | -1.8% | -0.33 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 282 | 147 | +6.5% | 1.18 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | yes |
| BunCaCham | 55 | 50 | +36.2% | 3.82 | yes |
| 0010001000001100 | 173 | 85 | -0.5% | -0.31 | no |
| totoro3miyazaki | 49 | 31 | +8.7% | 0.68 | no |
| 1l2ihj34li12u34 | 102 | 64 | +24.6% | 2.73 | yes |
| yabanci | 73 | 46 | +7.4% | 0.95 | yes |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | yes |
| juice-fruit | 47 | 32 | +11.5% | 0.96 | yes |
| 0x16bb9951a36fce71e2ef57890b | 61 | 23 | -7.3% | -0.5 | no |
| GamblingOdyssey | 355 | 182 | +8.5% | 1.54 | yes |
| plonker2026 | 109 | 65 | +9.3% | 1.47 | no |
| xxyx0xx | 285 | 141 | +6.1% | 0.58 | yes |
| monkeymashingkeyboard | 785 | 414 | +6.9% | 1.69 | yes |
| Tiger105 | 38 | 25 | +20.5% | 1.37 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 457 | 279 | +6.6% | 1.52 | yes |
| UNEB3154s4f251 | 2130 | 1346 | +2.7% | 1.59 | yes |
