# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-05 09:00 UTC: 5650 candidates, 3859 with trades copytop could copy, 222 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 1688 | 911 | $16,646 | +729.80 | +4.4% | +1.72 |
| every wallet that qualified on the first part (test window) | 3246 | 1793 | $32,149 | +228.02 | +0.7% | +0.43 |
| currently copied (test window) | 3825 | 2035 | $37,469 | +1,092.58 | +2.9% | +1.77 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 1688 | 911 | $16,646 | +729.80 | +4.4% | 1.72 | 4698 | 2479 | $45,853 | +5,582.52 | +12.2% | 6.35 |
| copy their sells too | 1688 | 885 | $16,646 | +486.37 | +2.9% | 1.28 | 4698 | 2432 | $45,853 | +5,104.63 | +11.1% | 5.93 |
| size by conviction (x0.5 / x1 / x1.5) | 1630 | 884 | $20,337 | +912.54 | +4.5% | 1.66 | 4473 | 2352 | $55,707 | +6,216.49 | +11.2% | 5.79 |
| skip bets under 0.5x their usual | 1644 | 890 | $16,237 | +806.01 | +5.0% | 1.87 | 4505 | 2374 | $44,253 | +5,397.23 | +12.2% | 6.18 |
| pre-game only | 1135 | 602 | $11,102 | +770.05 | +6.9% | 2.23 | 3799 | 2025 | $36,805 | +5,507.51 | +15.0% | 7.12 |
| skip prices under 30c | 1413 | 836 | $13,902 | +276.75 | +2.0% | 0.9 | 3708 | 2177 | $36,018 | +1,744.13 | +4.8% | 3.4 |
| favorites only (50c+) | 902 | 621 | $8,807 | +377.07 | +4.3% | 1.85 | 1997 | 1428 | $19,190 | +1,370.43 | +7.1% | 4.79 |
| 15s delay | 1789 | 1002 | $17,644 | +1,172.36 | +6.6% | 2.48 | 4833 | 2587 | $47,195 | +6,110.45 | +13.0% | 6.77 |
| 60s delay | 1688 | 911 | $16,646 | +729.80 | +4.4% | 1.72 | 4698 | 2479 | $45,853 | +5,582.52 | +12.2% | 6.35 |
| allow 2c over their price | 1859 | 1011 | $18,323 | +798.74 | +4.4% | 1.71 | 5049 | 2665 | $49,286 | +5,669.72 | +11.5% | 6.18 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 308 | +19.0% | 2.72 | 176 | +23.6% | 1.83 |
| conviction:1-2x | 389 | +19.1% | 2.22 | 365 | -3.7% | -0.77 |
| conviction:2x+ | 1972 | +14.8% | 4.59 | 1033 | +4.1% | 1.47 |
| conviction:under 0.5x | 341 | +22.9% | 3.2 | 114 | +3.4% | 0.45 |
| delay_move:flat | 2033 | +17.3% | 5.37 | 1100 | +5.6% | 1.75 |
| delay_move:price fell | 977 | +15.2% | 3.5 | 588 | +2.1% | 0.51 |
| exit:settle | 3010 | +16.6% | 6.42 | 1688 | +4.4% | 1.72 |
| kind:moneyline | 2108 | +13.3% | 4.07 | 1178 | +3.3% | 1.13 |
| kind:result | 835 | +24.4% | 5.67 | 312 | +10.2% | 1.49 |
| kind:totals | 67 | +21.6% | 2.37 | 198 | +1.5% | 0.23 |
| league:atp | 434 | +10.4% | 1.78 | 452 | -2.5% | -0.56 |
| league:bra | 12 | +60.6% | 2.56 | 16 | +3.8% | 0.19 |
| league:bun | 11 | +66.2% | 2.38 | 6 | -100.0% | — |
| league:cbb | 0 | +0.0% | — | 13 | +6.4% | 0.15 |
| league:cfb | 6 | -17.8% | -0.31 | 17 | +37.1% | 1.23 |
| league:cs2 | 339 | +13.7% | 1.83 | 160 | +6.3% | 0.61 |
| league:dota2 | 110 | -7.9% | -0.71 | 95 | +17.0% | 0.94 |
| league:epl | 55 | +32.9% | 3.0 | 66 | +8.6% | 0.55 |
| league:ere | 4 | +97.0% | — | 34 | +25.8% | 1.03 |
| league:khl | 3 | +7.2% | 0.15 | 8 | -33.0% | -1.02 |
| league:lal | 34 | -1.7% | -0.02 | 21 | +67.2% | 1.17 |
| league:lol | 1597 | +18.8% | 4.71 | 147 | +7.7% | 0.74 |
| league:mls | 52 | +9.6% | 0.8 | 58 | -16.1% | -1.13 |
| league:nba | 0 | +0.0% | — | 98 | +2.3% | 0.49 |
| league:nfl | 51 | +38.9% | 1.78 | 12 | +81.4% | 2.8 |
| league:nhl | 34 | +57.2% | 4.23 | 107 | +14.8% | 1.94 |
| league:sea | 49 | +55.7% | 3.32 | 99 | -2.7% | -0.13 |
| league:spl | 5 | +32.3% | 2.84 | 5 | -52.4% | -1.75 |
| league:uel | 0 | +0.0% | — | 16 | +42.0% | 1.31 |
| league:wta | 210 | +4.4% | 0.55 | 250 | +2.0% | 0.27 |
| price:30-70c | 1898 | +7.4% | 3.39 | 1115 | +3.7% | 1.38 |
| price:over 70c | 392 | +3.0% | 1.33 | 294 | -5.5% | -1.73 |
| price:under 30c | 720 | +47.2% | 5.39 | 279 | +17.0% | 1.58 |
| timing:in-play | 346 | +3.3% | 0.24 | 553 | -0.7% | -0.16 |
| timing:pre-game | 2664 | +18.4% | 6.91 | 1135 | +6.9% | 2.23 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 129797 | 67964 | $1,290,742 | -49,151.37 | -3.8% | -11.76 |
| consistency (winning weeks), top 16 | 8251 | 4683 | $81,831 | -1,512.97 | -1.8% | -1.53 |
| consistency (winning weeks), top 40 | 20994 | 11256 | $208,197 | -6,155.47 | -3.0% | -3.62 |
| copy return, average, top 16 | 4822 | 2468 | $47,585 | +218.03 | +0.5% | +0.09 |
| copy return, average, top 40 | 19191 | 9930 | $190,160 | -4,167.02 | -2.2% | -2.45 |
| copy return, lower bound, top 16 | 6421 | 3223 | $63,371 | -1,369.22 | -2.2% | -1.55 |
| copy return, lower bound, top 40 | 22232 | 11599 | $220,306 | -5,618.13 | -2.5% | -3.13 |
| copy return, shrunk, top 16 | 4939 | 2426 | $48,911 | -539.06 | -1.1% | -0.66 |
| copy return, shrunk, top 40 | 19941 | 10288 | $197,804 | -4,578.40 | -2.3% | -2.61 |
| markout 2h, average, top 16 | 7799 | 4357 | $77,369 | -646.70 | -0.8% | -0.62 |
| markout 2h, average, top 40 | 22577 | 12352 | $224,313 | -7,840.06 | -3.5% | -4.36 |
| markout 2h, lower bound, top 16 | 8969 | 4717 | $89,164 | -2,402.18 | -2.7% | -2.11 |
| markout 2h, lower bound, top 40 | 23841 | 12746 | $236,626 | -8,981.50 | -3.8% | -5.13 |
| markout 30m, average, top 16 | 7898 | 4187 | $79,268 | -2,570.67 | -3.2% | -2.24 |
| markout 30m, average, top 40 | 23257 | 12858 | $231,569 | -10,030.03 | -4.3% | -5.73 |
| most active, top 16 | 17614 | 9191 | $175,630 | -6,045.94 | -3.4% | -3.89 |
| most active, top 40 | 40168 | 21127 | $398,275 | -17,172.57 | -4.3% | -7.61 |
| win rate vs the odds, top 16 | 4118 | 2279 | $40,670 | -895.74 | -2.2% | -1.30 |
| win rate vs the odds, top 40 | 18618 | 9886 | $184,533 | -5,104.21 | -2.8% | -3.11 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 53 | 48 | +37.4% | 3.81 | +3.64 |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | +4.48 |
| 1l2ihj34li12u34 | 78 | 56 | +42.6% | 4.16 | +4.43 |
| xxyx0xx | 242 | 124 | +16.3% | 1.37 | +1.52 |
| 0010001000001100 | 88 | 50 | +22.8% | 1.21 | +2.26 |
| WagerWizard | 637 | 339 | -3.2% | -0.65 | -0.31 |
| Kch-Temp | 142 | 80 | +6.7% | 1.03 | +0.89 |
| eokho | 821 | 463 | +5.6% | 1.24 | +0.53 |
| juice-fruit | 46 | 30 | +11.8% | 0.93 | +1.28 |
| am100 | 829 | 510 | +18.3% | 4.52 | +1.85 |
| AmericaFirst1 | 471 | 284 | +5.0% | 1.18 | +0.52 |
| moreplatesmoredates | 942 | 473 | +3.6% | 1.01 | +0.44 |
| nightcity2077 | 782 | 363 | -0.8% | -0.14 | -0.07 |
| monkeymashingkeyboard | 874 | 459 | +5.6% | 1.5 | +0.56 |
| 636763 | 1468 | 468 | +1.9% | 0.51 | +0.26 |
| 0x16bb9951a36fce71e2ef57890b | 61 | 23 | -7.3% | -0.5 | -0.80 |
| Manchester4ever | 965 | 554 | +1.4% | 0.45 | +0.14 |
| yabanci | 77 | 46 | +1.6% | 0.42 | +0.44 |
| capitalpiston2 | 1811 | 828 | +1.4% | 0.42 | +0.13 |
| SimpleTony | 1102 | 357 | +11.5% | 2.1 | +1.18 |
| smithagent | 1159 | 638 | +3.0% | 0.66 | +0.30 |
| 0x870a742f | 546 | 233 | -1.8% | -0.28 | -0.16 |
| GamblingAddict12345 | 751 | 317 | -3.3% | -0.68 | -0.33 |
| clownly | 2174 | 812 | -5.7% | -2.09 | -0.58 |
| Limousin | 1361 | 714 | +4.4% | 0.82 | +0.32 |
| iseedota | 1384 | 611 | -1.3% | -0.32 | -0.12 |
| Notradecopy | 798 | 346 | -0.8% | -0.2 | -0.10 |
| igot50k | 1667 | 1036 | -0.5% | -0.2 | -0.05 |
| Future-Tarot-Trader | 1828 | 929 | -0.4% | -0.22 | -0.08 |
| 0x1E3bB7DEf89B002D45FD86D37F | 1974 | 1178 | +3.1% | 0.94 | +0.27 |
| walnutz | 614 | 312 | -1.7% | -0.41 | -0.19 |
| johnbaster | 760 | 403 | -0.7% | -0.17 | -0.08 |
| EdZachary | 107 | 44 | +2.4% | 0.16 | +0.22 |
| arahbo | 1488 | 617 | -2.7% | -0.64 | -0.28 |
| oxbus | 1194 | 593 | -6.4% | -2.12 | -0.68 |
| carelia | 1828 | 849 | -4.8% | -1.71 | -0.48 |
| blimp123 | 632 | 287 | -8.7% | -1.81 | -0.87 |
| n1ck10s | 1146 | 605 | +1.9% | 0.52 | +0.18 |
| UNEB3154s4f251 | 2202 | 1375 | +2.3% | 1.4 | +0.24 |
| ludo-money | 855 | 480 | -2.7% | -0.74 | -0.27 |

## Esports specialists (copies on esports markets only)

2989 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 163 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +50.4% (75) | -100.0% (1) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +32.1% (249) | +39.3% (28) | no |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 291 | 176 | +25.3% | 2.65 | +23.6% (242) | +33.7% (49) | no |
| am100 | tag | 829 | 510 | +18.3% | 4.52 | +17.4% (798) | +39.6% (31) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1181 | 634 | +10.4% | 2.95 | +13.6% (1066) | -18.8% (115) | yes |
| CUTJALENHURTS | tag | 152 | 85 | +17.6% | 1.64 | +15.7% (117) | +24.2% (35) | yes |
| SimpleTony | tag | 1093 | 353 | +11.4% | 2.07 | +12.8% (781) | +7.8% (312) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 26 | 15 | +48.0% | 1.12 | +84.0% (15) | -1.1% (11) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 98 | 55 | +17.1% | 1.35 | +44.6% (9) | +14.3% (89) | yes |
| -5rud | tag | 511 | 351 | +8.5% | 2.04 | +8.2% (428) | +10.2% (83) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +7.0% (14) | +30.4% (15) | yes |
| Manchester4ever | tag | 242 | 148 | +8.6% | 1.4 | +7.2% (197) | +14.7% (45) | yes |
| MIracle33 | tag | 448 | 225 | +8.2% | 1.43 | +8.3% (369) | +7.8% (79) | yes |
| BunCaCham | tag | 21 | 20 | +7.9% | 1.41 | +4.9% (14) | +13.9% (7) | yes |
| TAIWANNUMBERONE | tag | 922 | 506 | +5.0% | 1.42 | +2.9% (851) | +29.8% (71) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 580 | 306 | +5.2% | 1.27 | +10.4% (388) | -5.2% (192) | yes |
| ZEST011 | tag | 621 | 465 | +3.0% | 1.12 | +3.0% (547) | +2.8% (74) | yes |
| moreplatesmoredates | tag | 942 | 473 | +3.6% | 1.01 | -0.3% (669) | +13.4% (273) | yes |
| AmericaFirst1 | current | 259 | 166 | +4.7% | 0.97 | +8.4% (225) | -19.3% (34) | yes |
| berlinskies | tag | 1046 | 610 | +2.7% | 0.81 | +2.7% (905) | +2.8% (141) | yes |
| GC-C | tag | 773 | 542 | +1.6% | 0.59 | -2.6% (549) | +12.2% (224) | yes |
| shaw | tag | 240 | 144 | +5.3% | 0.81 | +7.6% (192) | -4.3% (48) | yes |
| 636763 | tag | 1439 | 461 | +3.0% | 0.72 | +0.3% (1114) | +12.6% (325) | yes |
| carelia | tag | 214 | 123 | +5.9% | 0.73 | +3.4% (176) | +17.8% (38) | yes |
| NS13 | tag | 325 | 137 | +5.0% | 0.78 | -1.4% (261) | +30.1% (64) | yes |
| littlebay | tag | 104 | 75 | +4.3% | 0.64 | +9.4% (62) | -3.3% (42) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -0.2% (165) | +8.3% (53) | no |
| nightcity2077 | tag | 390 | 189 | +5.0% | 0.61 | +6.4% (378) | -41.4% (12) | yes |
| HalleyChen | tag | 605 | 367 | +1.4% | 0.29 | +2.8% (493) | -5.0% (112) | yes |
| Diabolical-Prize | current | 224 | 118 | +2.1% | 0.47 | +8.3% (200) | -49.7% (24) | no |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 329 | 137 | -8.4% | -1.34 | no |
| Kch-Temp | 142 | 80 | +6.7% | 1.03 | yes |
| EdZachary | 107 | 44 | +2.4% | 0.16 | yes |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | no |
| Jsram | 65 | 36 | -1.2% | -0.16 | no |
| Kkunn | 824 | 345 | +1.2% | 0.46 | no |
| Sisyphus- | 124 | 68 | -4.3% | -0.47 | no |
| PEYZ-BIGGEST-FAN | 401 | 202 | +1.9% | 0.31 | no |
| theowalcott | 75 | 44 | +9.8% | 1.05 | no |
| HVAB | 364 | 221 | -1.3% | -0.25 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 276 | 142 | +5.8% | 1.06 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | yes |
| BunCaCham | 53 | 48 | +37.4% | 3.81 | yes |
| 0010001000001100 | 88 | 50 | +22.8% | 1.21 | yes |
| totoro3miyazaki | 40 | 30 | +29.5% | 2.1 | no |
| 1l2ihj34li12u34 | 78 | 56 | +42.6% | 4.16 | yes |
| yabanci | 77 | 46 | +1.6% | 0.42 | yes |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 46 | 30 | +11.8% | 0.93 | yes |
| 0x16bb9951a36fce71e2ef57890b | 61 | 23 | -7.3% | -0.5 | yes |
| GamblingOdyssey | 368 | 183 | +2.7% | 0.67 | no |
| plonker2026 | 115 | 65 | +13.6% | 1.67 | no |
| xxyx0xx | 242 | 124 | +16.3% | 1.37 | yes |
| monkeymashingkeyboard | 874 | 459 | +5.6% | 1.5 | yes |
| Tiger105 | 38 | 25 | +21.8% | 1.43 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 471 | 284 | +5.0% | 1.18 | yes |
| UNEB3154s4f251 | 2202 | 1375 | +2.3% | 1.4 | yes |
