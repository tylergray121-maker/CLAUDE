# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-22 22:00 UTC: 5491 candidates, 3844 with trades copytop could copy, 227 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2071 | 1010 | $20,228 | +304.00 | +1.5% | +0.79 |
| every wallet that qualified on the first part (test window) | 2155 | 1048 | $21,087 | +395.41 | +1.9% | +0.92 |
| currently copied (test window) | 4013 | 2147 | $39,454 | +1,916.04 | +4.9% | +2.95 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2071 | 1010 | $20,228 | +304.00 | +1.5% | 0.79 | 5095 | 2673 | $49,067 | +4,672.51 | +9.5% | 5.4 |
| copy their sells too | 2072 | 981 | $20,239 | -199.11 | -1.0% | -0.1 | 5096 | 2627 | $49,077 | +3,867.53 | +7.9% | 4.63 |
| size by conviction (x0.5 / x1 / x1.5) | 1983 | 957 | $24,444 | +381.42 | +1.6% | 0.52 | 4751 | 2470 | $57,888 | +4,790.35 | +8.3% | 5.03 |
| skip bets under 0.5x their usual | 1950 | 963 | $19,137 | +459.76 | +2.4% | 1.12 | 4860 | 2571 | $46,893 | +4,565.64 | +9.7% | 5.45 |
| pre-game only | 1512 | 783 | $14,559 | +427.69 | +2.9% | 1.28 | 4075 | 2225 | $38,710 | +4,011.95 | +10.4% | 5.52 |
| skip prices under 30c | 1689 | 928 | $16,337 | +616.05 | +3.8% | 1.77 | 4445 | 2480 | $42,477 | +2,137.97 | +5.0% | 3.52 |
| favorites only (50c+) | 849 | 561 | $8,121 | +521.11 | +6.4% | 2.47 | 2373 | 1533 | $22,476 | +1,081.87 | +4.8% | 3.08 |
| 15s delay | 2131 | 1034 | $20,826 | +133.85 | +0.6% | 0.54 | 5245 | 2756 | $50,564 | +4,958.94 | +9.8% | 5.66 |
| 60s delay | 2071 | 1010 | $20,228 | +304.00 | +1.5% | 0.79 | 5095 | 2673 | $49,067 | +4,672.51 | +9.5% | 5.4 |
| allow 2c over their price | 2163 | 1044 | $21,106 | +138.32 | +0.7% | 0.54 | 5313 | 2773 | $51,197 | +4,913.78 | +9.6% | 5.49 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 370 | +22.5% | 3.36 | 218 | +14.0% | 1.62 |
| conviction:1-2x | 486 | +12.3% | 1.64 | 215 | -19.0% | -2.29 |
| conviction:2x+ | 1898 | +12.0% | 4.25 | 1346 | +3.4% | 0.97 |
| conviction:under 0.5x | 270 | +33.0% | 3.14 | 292 | -1.8% | 0.15 |
| delay_move:flat | 2316 | +16.4% | 5.99 | 1416 | +3.9% | 1.5 |
| delay_move:price fell | 708 | +11.3% | 2.15 | 655 | -3.4% | -0.63 |
| exit:settle | 3024 | +15.2% | 6.26 | 2071 | +1.5% | 0.79 |
| kind:moneyline | 2446 | +14.0% | 5.07 | 1760 | +2.8% | 1.15 |
| kind:result | 182 | +43.1% | 5.19 | 151 | +2.4% | 0.42 |
| kind:totals | 396 | +8.8% | 1.45 | 160 | -14.2% | -1.87 |
| league:atp | 374 | +11.8% | 1.51 | 485 | -13.9% | -2.39 |
| league:bra | 8 | +102.8% | 3.0 | 2 | -24.5% | -0.31 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 2 | -100.0% | — | 115 | -5.0% | -0.29 |
| league:cs2 | 123 | +26.2% | 2.76 | 103 | +6.3% | 0.82 |
| league:dota2 | 63 | +41.1% | 2.18 | 94 | -11.2% | -0.91 |
| league:epl | 52 | +34.2% | 3.05 | 39 | -24.6% | -1.88 |
| league:ere | 8 | +106.7% | 28.83 | 12 | +166.2% | 6.87 |
| league:lal | 29 | +5.9% | 0.5 | 8 | +152.3% | 1.06 |
| league:lib | 8 | +106.3% | 6.95 | 7 | +76.9% | 46.14 |
| league:lol | 217 | +61.5% | 3.73 | 121 | -18.7% | -1.97 |
| league:mlb | 1524 | +2.6% | 0.82 | 266 | +14.7% | 2.7 |
| league:mls | 43 | +28.4% | 2.05 | 37 | -23.4% | -1.33 |
| league:nba | 0 | +0.0% | — | 67 | -0.1% | 0.06 |
| league:nfl | 125 | +25.9% | 1.71 | 93 | +47.5% | 2.4 |
| league:nhl | 0 | +0.0% | — | 28 | -11.6% | -1.06 |
| league:sea | 45 | +57.3% | 3.21 | 31 | -45.4% | -2.77 |
| league:wnba | 119 | +23.0% | 2.74 | 32 | -42.4% | -2.95 |
| league:wta | 275 | +10.5% | 1.42 | 525 | +13.1% | 2.28 |
| price:30-70c | 2580 | +5.1% | 2.56 | 1554 | +3.9% | 1.72 |
| price:over 70c | 172 | +14.5% | 5.67 | 127 | +4.4% | 0.9 |
| price:under 30c | 272 | +105.0% | 6.21 | 390 | -8.3% | -0.79 |
| timing:in-play | 461 | +16.7% | 2.38 | 559 | -2.2% | -0.28 |
| timing:pre-game | 2563 | +14.8% | 5.81 | 1512 | +2.9% | 1.28 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 139293 | 72621 | $1,384,171 | -53,694.02 | -3.9% | -12.64 |
| consistency (winning weeks), top 16 | 7715 | 3954 | $76,109 | -1,804.56 | -2.4% | -1.59 |
| consistency (winning weeks), top 40 | 20855 | 10877 | $207,154 | -4,635.27 | -2.2% | -2.55 |
| copy return, average, top 16 | 4495 | 2140 | $44,652 | +542.72 | +1.2% | +0.57 |
| copy return, average, top 40 | 20615 | 10355 | $204,528 | -1,976.71 | -1.0% | -1.05 |
| copy return, lower bound, top 16 | 5615 | 2847 | $55,232 | +283.09 | +0.5% | +0.43 |
| copy return, lower bound, top 40 | 25005 | 13504 | $247,203 | -4,959.78 | -2.0% | -2.67 |
| copy return, shrunk, top 16 | 5193 | 2419 | $51,298 | -53.01 | -0.1% | -0.04 |
| copy return, shrunk, top 40 | 21049 | 10625 | $208,873 | -2,326.25 | -1.1% | -1.23 |
| markout 2h, average, top 16 | 5608 | 2893 | $56,126 | +571.68 | +1.0% | +0.59 |
| markout 2h, average, top 40 | 19182 | 10216 | $191,394 | -2,647.34 | -1.4% | -1.53 |
| markout 2h, lower bound, top 16 | 5763 | 2825 | $57,611 | -409.81 | -0.7% | -0.35 |
| markout 2h, lower bound, top 40 | 21251 | 10911 | $211,235 | -3,392.70 | -1.6% | -1.92 |
| markout 30m, average, top 16 | 8004 | 4275 | $79,781 | -875.72 | -1.1% | -0.75 |
| markout 30m, average, top 40 | 21897 | 11652 | $218,418 | -7,376.80 | -3.4% | -4.13 |
| most active, top 16 | 24635 | 12427 | $244,584 | -14,900.30 | -6.1% | -8.61 |
| most active, top 40 | 48480 | 25020 | $481,133 | -23,362.09 | -4.9% | -9.40 |
| win rate vs the odds, top 16 | 3898 | 1996 | $38,439 | +820.12 | +2.1% | +1.07 |
| win rate vs the odds, top 40 | 18326 | 9390 | $181,879 | -391.07 | -0.2% | -0.23 |

Used for the final list: **win rate vs the odds, top 40** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 31 | 28 | +33.7% | 2.94 | +3.30 |
| juice-fruit | 30 | 22 | +22.7% | 1.46 | +2.34 |
| theowalcott | 71 | 50 | +38.1% | 3.46 | +3.94 |
| yabanci | 25 | 17 | +22.8% | 1.58 | +2.91 |
| plonker2026 | 82 | 57 | +39.6% | 3.69 | +4.49 |
| 1l2ihj34li12u34 | 31 | 22 | +42.7% | 2.53 | +4.47 |
| 0010001000001100 | 35 | 21 | +61.6% | 1.49 | +5.95 |
| tiger105 | 44 | 29 | +23.9% | 1.66 | +2.39 |
| 0x20D6436849F930584892730C7F | 148 | 86 | +30.1% | 2.16 | +3.05 |
| 0x16bb9951a36fce71e2ef57890b | 868 | 472 | +6.3% | 1.9 | +0.65 |
| PEYZ-BIGGEST-FAN | 196 | 109 | +7.5% | 1.14 | +0.90 |
| GamblingOdyssey | 416 | 211 | +7.3% | 1.42 | +0.83 |
| monkeymashingkeyboard | 1927 | 1098 | +8.5% | 3.65 | +0.83 |
| KaneAnalytics | 91 | 54 | +12.3% | 0.88 | +1.21 |
| AmericaFirst1 | 440 | 279 | +8.0% | 1.8 | +0.80 |
| Wiretransferxyz | 690 | 364 | -10.3% | -2.98 | -1.04 |
| EdZachary | 76 | 36 | -3.5% | -0.3 | -0.36 |
| oookkjjdd | 827 | 421 | -0.6% | -0.1 | -0.04 |
| AlphaPengu1n | 377 | 170 | -8.7% | -1.33 | -0.86 |
| Kkunn | 643 | 272 | +3.9% | 0.88 | +0.50 |
| RensPeters | 572 | 283 | +0.8% | 0.17 | +0.08 |
| jiafan | 808 | 493 | +7.1% | 1.66 | +0.65 |
| NeedForDead | 377 | 159 | +10.2% | 1.31 | +1.02 |
| nightcity2077 | 835 | 401 | +1.4% | 0.26 | +0.14 |
| 0x6daae04265d65cb2aae7fe6db4 | 608 | 326 | -5.3% | -1.23 | -0.51 |
| 0x567212c82AAa6fe589bE5A2f4C | 517 | 261 | +4.1% | 0.99 | +0.62 |
| Sisyphus- | 115 | 68 | -1.8% | -0.21 | -0.17 |
| walnutz | 620 | 322 | -1.8% | -0.42 | -0.18 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 960 | 422 | +2.5% | 0.49 | +0.24 |
| sinhtuycanh | 618 | 436 | +2.0% | 0.74 | +0.20 |
| Petal | 855 | 405 | -5.8% | -1.41 | -0.58 |
| HVAB | 315 | 197 | +0.7% | 0.13 | +0.07 |
| n1ck10s | 950 | 507 | +2.3% | 0.63 | +0.23 |
| TheRomanProcurator | 3422 | 1708 | +3.1% | 1.31 | +0.30 |
| smithagent | 671 | 355 | +7.1% | 0.98 | +0.68 |
| littlebay | 701 | 461 | +2.2% | 0.55 | +0.21 |
| smartcombo | 1019 | 596 | +0.2% | 0.05 | +0.02 |
| torta.tech | 1756 | 1047 | -1.6% | -0.64 | -0.15 |
| SimpleTony | 1054 | 332 | +5.1% | 1.01 | +0.56 |
| oneheadedlebron | 1165 | 634 | -1.9% | -0.53 | -0.15 |

## Esports specialists (copies on esports markets only)

2802 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 169 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| pltrkr111 | tag | 180 | 99 | +40.9% | 2.83 | +71.4% (111) | -8.7% (69) | yes |
| THEHIGHLIFE | tag | 248 | 127 | +32.5% | 2.64 | +53.2% (146) | +2.6% (102) | no |
| juice-fruit | current | 25 | 19 | +28.5% | 1.64 | +0.0% (0) | +28.5% (25) | yes |
| NeedForDead | tag | 40 | 22 | +31.0% | 1.54 | +44.1% (25) | +9.2% (15) | no |
| PT-S3 | leaderboard | 11 | 10 | +18.3% | 1.41 | +18.3% (11) | +0.0% (0) | no |
| yakz | leaderboard | 122 | 61 | +21.8% | 1.36 | +19.1% (73) | +25.8% (49) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 223 | 114 | +16.3% | 1.24 | +26.2% (150) | -4.2% (73) | yes |
| AmericaFirst1 | current | 193 | 130 | +8.1% | 1.44 | +0.3% (126) | +22.3% (67) | yes |
| ehl-rungs | tag | 197 | 149 | +6.4% | 1.38 | +6.4% (197) | +0.0% (0) | no |
| RensPeters | tag | 77 | 46 | +13.4% | 1.13 | +4.9% (43) | +24.1% (34) | no |
| newUser2025 | tag | 125 | 87 | +7.9% | 1.18 | +10.7% (80) | +2.9% (45) | yes |
| dddd123s | tag | 439 | 279 | +5.3% | 1.27 | +5.7% (182) | +5.0% (257) | yes |
| sinhtuycanh | tag | 152 | 112 | +6.1% | 1.11 | +1.3% (71) | +10.2% (81) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 517 | 261 | +4.1% | 0.99 | +8.6% (318) | -3.2% (199) | yes |
| SimpleTony | tag | 1045 | 328 | +5.0% | 0.98 | +7.8% (693) | -0.5% (352) | yes |
| littlebay | tag | 88 | 66 | +6.7% | 0.94 | +29.8% (8) | +4.3% (80) | no |
| smartcombo | tag | 186 | 107 | +8.4% | 0.94 | +12.1% (157) | -11.0% (29) | yes |
| returdmaxxer | tag | 277 | 253 | +0.8% | 0.41 | +1.4% (165) | -0.1% (112) | no |
| MIracle33 | tag | 303 | 153 | +5.1% | 0.81 | +16.5% (196) | -15.7% (107) | yes |
| superlxj | tag | 195 | 135 | +3.5% | 0.71 | -8.0% (91) | +14.1% (104) | yes |
| 0xcf279d52 | tag | 312 | 193 | +3.2% | 0.67 | +2.6% (153) | +3.8% (159) | yes |
| jiafan | tag | 415 | 248 | +2.8% | 0.56 | +4.9% (350) | -7.9% (65) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 138 | 94 | +4.0% | 0.66 | +1.8% (64) | +6.0% (74) | yes |
| nightcity2077 | tag | 297 | 151 | +7.2% | 0.75 | +7.7% (280) | -0.7% (17) | no |
| lll981kd | tag | 643 | 415 | +0.4% | 0.16 | -4.1% (164) | +1.9% (479) | yes |
| igot50k | tag | 679 | 351 | +2.8% | 0.45 | -0.1% (517) | +12.1% (162) | yes |
| 8dddj | tag | 696 | 451 | -0.2% | 0.01 | -4.1% (179) | +1.1% (517) | yes |
| darkumbreon88 | tag | 273 | 194 | +1.2% | 0.28 | +3.8% (98) | -0.2% (175) | yes |
| 0x09dAc7226f8df37eBFAF277252 | tag | 534 | 312 | +0.1% | 0.12 | +3.7% (450) | -18.8% (84) | yes |
| Saber-greed | leaderboard | 305 | 167 | +4.5% | 0.53 | +0.7% (260) | +26.7% (45) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 299 | 130 | -4.0% | -0.64 | no |
| Kch-Temp | 114 | 52 | -9.6% | -0.9 | no |
| EdZachary | 76 | 36 | -3.5% | -0.3 | yes |
| KaneAnalytics | 91 | 54 | +12.3% | 0.88 | yes |
| Jsram | 57 | 28 | -16.0% | -1.31 | no |
| Kkunn | 643 | 272 | +3.9% | 0.88 | yes |
| Sisyphus- | 115 | 68 | -1.8% | -0.21 | yes |
| PEYZ-BIGGEST-FAN | 196 | 109 | +7.5% | 1.14 | yes |
| theowalcott | 71 | 50 | +38.1% | 3.46 | yes |
| HVAB | 315 | 197 | +0.7% | 0.13 | yes |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +6.5% | 1.16 | no |
| Talvez10 | 581 | 309 | +2.6% | 0.33 | no |
| BunCaCham | 31 | 28 | +33.7% | 2.94 | yes |
| 0010001000001100 | 35 | 21 | +61.6% | 1.49 | yes |
| totoro3miyazaki | 39 | 29 | +28.0% | 1.96 | no |
| 1l2ihj34li12u34 | 31 | 22 | +42.7% | 2.53 | yes |
| yabanci | 25 | 17 | +22.8% | 1.58 | yes |
| 0x20D6436849F930584892730C7F | 148 | 86 | +30.1% | 2.16 | yes |
| juice-fruit | 30 | 22 | +22.7% | 1.46 | yes |
| 0x16bb9951a36fce71e2ef57890b | 868 | 472 | +6.3% | 1.9 | yes |
| GamblingOdyssey | 416 | 211 | +7.3% | 1.42 | yes |
| plonker2026 | 82 | 57 | +39.6% | 3.69 | yes |
| xxyx0xx | 173 | 86 | +1.8% | 0.1 | no |
| monkeymashingkeyboard | 1927 | 1098 | +8.5% | 3.65 | yes |
| Tiger105 | 44 | 29 | +23.9% | 1.66 | yes |
| THEHIGHLIFE | 278 | 133 | +24.2% | 2.13 | no |
| AmericaFirst1 | 440 | 279 | +8.0% | 1.8 | yes |
| UNEB3154s4f251 | 1859 | 1172 | +3.8% | 2.08 | no |
