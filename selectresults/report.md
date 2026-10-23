# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-23 09:00 UTC: 5483 candidates, 3838 with trades copytop could copy, 228 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2075 | 1019 | $20,249 | +419.21 | +2.1% | +0.98 |
| every wallet that qualified on the first part (test window) | 2156 | 1055 | $21,077 | +506.06 | +2.4% | +1.09 |
| currently copied (test window) | 4001 | 2124 | $39,301 | +1,627.08 | +4.1% | +2.48 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2075 | 1019 | $20,249 | +419.21 | +2.1% | 0.98 | 5111 | 2674 | $49,203 | +4,502.64 | +9.2% | 5.21 |
| copy their sells too | 2075 | 990 | $20,249 | -74.55 | -0.4% | 0.11 | 5111 | 2628 | $49,203 | +3,707.02 | +7.5% | 4.45 |
| size by conviction (x0.5 / x1 / x1.5) | 1985 | 965 | $24,440 | +556.06 | +2.3% | 0.73 | 4765 | 2470 | $58,053 | +4,626.23 | +8.0% | 4.85 |
| skip bets under 0.5x their usual | 1957 | 973 | $19,177 | +553.08 | +2.9% | 1.3 | 4878 | 2574 | $47,049 | +4,410.31 | +9.4% | 5.28 |
| pre-game only | 1527 | 796 | $14,700 | +481.50 | +3.3% | 1.37 | 4090 | 2226 | $38,844 | +3,815.45 | +9.8% | 5.26 |
| skip prices under 30c | 1692 | 935 | $16,348 | +663.86 | +4.1% | 1.88 | 4452 | 2479 | $42,518 | +1,984.05 | +4.7% | 3.3 |
| favorites only (50c+) | 862 | 575 | $8,233 | +601.73 | +7.3% | 2.87 | 2382 | 1541 | $22,547 | +1,096.59 | +4.9% | 3.15 |
| 15s delay | 2137 | 1045 | $20,867 | +266.16 | +1.3% | 0.75 | 5257 | 2756 | $50,660 | +4,808.58 | +9.5% | 5.49 |
| 60s delay | 2075 | 1019 | $20,249 | +419.21 | +2.1% | 0.98 | 5111 | 2674 | $49,203 | +4,502.64 | +9.2% | 5.21 |
| allow 2c over their price | 2167 | 1053 | $21,126 | +253.03 | +1.2% | 0.72 | 5329 | 2774 | $51,333 | +4,743.12 | +9.2% | 5.31 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 363 | +23.4% | 3.44 | 219 | +12.9% | 1.51 |
| conviction:1-2x | 492 | +11.7% | 1.58 | 221 | -18.1% | -2.21 |
| conviction:2x+ | 1909 | +10.6% | 3.8 | 1347 | +4.3% | 1.2 |
| conviction:under 0.5x | 272 | +31.1% | 2.99 | 288 | -1.3% | 0.24 |
| delay_move:flat | 2319 | +15.3% | 5.61 | 1424 | +4.3% | 1.6 |
| delay_move:price fell | 717 | +10.6% | 2.04 | 651 | -2.5% | -0.44 |
| exit:settle | 3036 | +14.1% | 5.87 | 2075 | +2.1% | 0.98 |
| kind:moneyline | 2458 | +13.3% | 4.84 | 1780 | +3.6% | 1.42 |
| kind:result | 188 | +37.0% | 4.54 | 134 | +1.3% | 0.28 |
| kind:totals | 390 | +7.9% | 1.29 | 161 | -14.9% | -1.97 |
| league:atp | 378 | +12.2% | 1.58 | 481 | -14.4% | -2.47 |
| league:bra | 8 | +102.8% | 3.0 | 2 | -24.5% | -0.31 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 2 | -100.0% | — | 115 | -5.0% | -0.29 |
| league:cs2 | 127 | +21.9% | 2.39 | 99 | +10.7% | 1.23 |
| league:dota2 | 74 | +36.0% | 2.14 | 83 | -13.6% | -1.03 |
| league:epl | 52 | +34.2% | 3.05 | 39 | -24.6% | -1.88 |
| league:ere | 8 | +106.7% | 28.83 | 12 | +166.2% | 6.87 |
| league:lal | 29 | +5.9% | 0.5 | 8 | +152.3% | 1.06 |
| league:lol | 222 | +57.7% | 3.57 | 116 | -14.9% | -1.56 |
| league:mlb | 1514 | +2.0% | 0.62 | 267 | +14.1% | 2.62 |
| league:mls | 45 | +22.4% | 1.66 | 35 | -18.9% | -1.0 |
| league:nba | 0 | +0.0% | — | 87 | -6.2% | -0.5 |
| league:nfl | 127 | +24.9% | 1.72 | 91 | +49.1% | 2.4 |
| league:nhl | 0 | +0.0% | — | 28 | -11.6% | -1.06 |
| league:sea | 45 | +57.3% | 3.21 | 31 | -45.4% | -2.77 |
| league:wnba | 119 | +23.0% | 2.74 | 32 | -42.4% | -2.95 |
| league:wta | 277 | +9.6% | 1.31 | 543 | +15.2% | 2.73 |
| price:30-70c | 2583 | +4.3% | 2.18 | 1557 | +4.2% | 1.82 |
| price:over 70c | 173 | +14.5% | 5.73 | 127 | +4.5% | 0.91 |
| price:under 30c | 280 | +98.9% | 5.99 | 391 | -6.6% | -0.61 |
| timing:in-play | 473 | +15.6% | 2.26 | 548 | -1.1% | -0.1 |
| timing:pre-game | 2563 | +13.8% | 5.44 | 1527 | +3.3% | 1.37 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 139352 | 72650 | $1,384,561 | -54,275.91 | -3.9% | -12.76 |
| consistency (winning weeks), top 16 | 8101 | 4195 | $79,924 | -2,174.26 | -2.7% | -1.95 |
| consistency (winning weeks), top 40 | 21105 | 10980 | $209,074 | -6,910.04 | -3.3% | -3.95 |
| copy return, average, top 16 | 4627 | 2174 | $45,936 | +360.65 | +0.8% | +0.39 |
| copy return, average, top 40 | 21714 | 11032 | $215,165 | -3,627.56 | -1.7% | -2.00 |
| copy return, lower bound, top 16 | 5179 | 2493 | $50,860 | -629.12 | -1.2% | -0.53 |
| copy return, lower bound, top 40 | 24019 | 12889 | $236,734 | -5,110.29 | -2.2% | -2.84 |
| copy return, shrunk, top 16 | 5121 | 2394 | $50,780 | -474.53 | -0.9% | -0.47 |
| copy return, shrunk, top 40 | 21460 | 10922 | $213,011 | -3,097.44 | -1.5% | -1.67 |
| markout 2h, average, top 16 | 5365 | 2596 | $53,809 | -167.43 | -0.3% | -0.10 |
| markout 2h, average, top 40 | 16976 | 9169 | $169,208 | -1,206.99 | -0.7% | -0.69 |
| markout 2h, lower bound, top 16 | 5473 | 2639 | $54,628 | -331.35 | -0.6% | -0.24 |
| markout 2h, lower bound, top 40 | 22289 | 11883 | $220,846 | -3,164.55 | -1.4% | -1.79 |
| markout 30m, average, top 16 | 7723 | 4073 | $76,979 | -1,822.89 | -2.4% | -1.68 |
| markout 30m, average, top 40 | 19909 | 10784 | $198,352 | -5,438.76 | -2.7% | -3.23 |
| most active, top 16 | 24616 | 12394 | $244,369 | -14,799.27 | -6.1% | -8.55 |
| most active, top 40 | 48472 | 24959 | $481,189 | -23,552.79 | -4.9% | -9.52 |
| win rate vs the odds, top 16 | 4056 | 2024 | $39,945 | -18.67 | -0.1% | -0.06 |
| win rate vs the odds, top 40 | 18910 | 9649 | $187,803 | -1,126.63 | -0.6% | -0.65 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| 0010001000001100 | 35 | 21 | +61.6% | 1.49 | +5.95 |
| BunCaCham | 31 | 28 | +33.7% | 2.94 | +3.30 |
| plonker2026 | 82 | 57 | +39.6% | 3.69 | +4.49 |
| yabanci | 27 | 19 | +28.0% | 1.94 | +3.35 |
| 0x20D6436849F930584892730C7F | 150 | 86 | +28.4% | 2.07 | +2.89 |
| 1l2ihj34li12u34 | 30 | 22 | +47.7% | 2.81 | +4.95 |
| tiger105 | 41 | 28 | +30.4% | 2.04 | +3.02 |
| juice-fruit | 30 | 22 | +22.7% | 1.46 | +2.34 |
| theowalcott | 57 | 36 | +24.8% | 1.96 | +2.64 |
| 0x16bb9951a36fce71e2ef57890b | 858 | 466 | +6.3% | 1.87 | +0.64 |
| KaneAnalytics | 93 | 55 | +15.7% | 1.08 | +1.53 |
| smithagent | 658 | 351 | +6.6% | 0.91 | +0.63 |
| monkeymashingkeyboard | 1938 | 1097 | +7.6% | 3.31 | +0.75 |
| GamblingOdyssey | 417 | 211 | +6.7% | 1.34 | +0.78 |
| eskk | 898 | 215 | -0.5% | -0.02 | -0.01 |
| AmericaFirst1 | 440 | 278 | +7.7% | 1.74 | +0.78 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 952 | 419 | +2.4% | 0.46 | +0.23 |
| arahbo | 1046 | 443 | +4.7% | 0.78 | +0.44 |
| polkals | 560 | 253 | +7.1% | 1.04 | +0.68 |
| RensPeters | 575 | 287 | +1.5% | 0.34 | +0.16 |
| NeedForDead | 376 | 158 | +10.4% | 1.34 | +1.04 |
| nightcity2077 | 837 | 402 | +2.0% | 0.35 | +0.20 |
| cosmicsteaks | 752 | 334 | -1.9% | -0.36 | -0.20 |
| Petal | 855 | 405 | -5.8% | -1.41 | -0.58 |
| jiafan | 845 | 511 | +5.3% | 1.29 | +0.49 |
| 0x567212c82AAa6fe589bE5A2f4C | 517 | 261 | +4.1% | 0.99 | +0.62 |
| walnutz | 620 | 322 | -1.8% | -0.42 | -0.18 |
| Kkunn | 655 | 283 | +5.2% | 1.14 | +0.63 |
| Wiretransferxyz | 687 | 362 | -10.4% | -2.95 | -1.03 |
| SimpleTony | 1054 | 334 | +5.5% | 1.1 | +0.61 |
| UNEB3154s4f251 | 1847 | 1160 | +3.7% | 1.97 | +0.37 |
| oookkjjdd | 836 | 428 | -0.2% | 0.01 | +0.00 |
| TheRomanProcurator | 3458 | 1717 | +2.6% | 1.13 | +0.26 |
| littlebay | 705 | 464 | +2.2% | 0.55 | +0.21 |
| n1ck10s | 976 | 520 | +2.0% | 0.55 | +0.20 |
| 0x7a3FB8C5aD2aF4C621B2138D95 | 463 | 190 | -9.0% | -1.25 | -0.89 |
| sinhtuycanh | 612 | 430 | +1.7% | 0.64 | +0.17 |
| SharkVision | 751 | 350 | -3.2% | -0.56 | -0.30 |
| sbsport | 890 | 481 | +1.7% | 0.48 | +0.15 |
| torta.tech | 1754 | 1041 | -1.9% | -0.78 | -0.18 |

## Esports specialists (copies on esports markets only)

2793 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 169 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| pltrkr111 | tag | 180 | 99 | +40.9% | 2.83 | +69.8% (112) | -7.2% (68) | no |
| THEHIGHLIFE | tag | 248 | 127 | +32.5% | 2.64 | +44.1% (155) | +12.8% (93) | no |
| juice-fruit | current | 25 | 19 | +28.5% | 1.64 | +0.0% (0) | +28.5% (25) | yes |
| NeedForDead | tag | 40 | 22 | +31.0% | 1.54 | +44.1% (25) | +9.2% (15) | no |
| yakz | leaderboard | 122 | 61 | +21.8% | 1.36 | +19.1% (73) | +25.8% (49) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 223 | 114 | +16.3% | 1.24 | +18.6% (159) | +10.3% (64) | no |
| AmericaFirst1 | current | 193 | 130 | +8.1% | 1.44 | +4.1% (132) | +16.5% (61) | yes |
| ehl-rungs | tag | 197 | 149 | +6.4% | 1.38 | +6.4% (197) | +0.0% (0) | no |
| RensPeters | tag | 77 | 46 | +13.4% | 1.13 | +10.1% (45) | +18.0% (32) | no |
| newUser2025 | tag | 125 | 87 | +7.9% | 1.18 | +10.0% (83) | +3.7% (42) | yes |
| dddd123s | tag | 439 | 279 | +5.3% | 1.27 | +6.7% (192) | +4.2% (247) | yes |
| mpoly | tag | 230 | 167 | +5.5% | 1.11 | +8.7% (150) | -0.3% (80) | yes |
| SimpleTony | tag | 1045 | 330 | +5.3% | 1.07 | +5.6% (714) | +4.9% (331) | yes |
| sinhtuycanh | tag | 150 | 110 | +5.7% | 1.04 | -1.0% (70) | +11.6% (80) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 517 | 261 | +4.1% | 0.99 | +9.9% (321) | -5.5% (196) | yes |
| littlebay | tag | 88 | 66 | +6.7% | 0.94 | +27.0% (15) | +2.5% (73) | no |
| smartcombo | tag | 186 | 107 | +8.4% | 0.94 | +13.8% (160) | -23.8% (26) | yes |
| returdmaxxer | tag | 277 | 253 | +0.8% | 0.41 | +1.6% (171) | -0.5% (106) | no |
| MIracle33 | tag | 303 | 153 | +5.1% | 0.81 | +14.5% (204) | -14.1% (99) | yes |
| superlxj | tag | 195 | 135 | +3.5% | 0.71 | -8.0% (91) | +14.1% (104) | yes |
| 0xcf279d52 | tag | 310 | 191 | +3.0% | 0.61 | +2.2% (155) | +3.8% (155) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 138 | 94 | +4.0% | 0.66 | +2.3% (68) | +5.7% (70) | yes |
| nightcity2077 | tag | 297 | 151 | +7.2% | 0.75 | +7.7% (280) | -0.7% (17) | no |
| jiafan | tag | 411 | 245 | +2.6% | 0.51 | +4.2% (354) | -7.4% (57) | yes |
| lll981kd | tag | 645 | 416 | +0.4% | 0.15 | -2.2% (189) | +1.5% (456) | yes |
| darkumbreon88 | tag | 273 | 194 | +1.2% | 0.28 | +2.6% (124) | +0.0% (149) | yes |
| 8dddj | tag | 698 | 452 | -0.2% | 0.01 | -4.3% (208) | +1.5% (490) | yes |
| igot50k | tag | 677 | 349 | +2.6% | 0.42 | -1.0% (522) | +14.7% (155) | yes |
| 0x09dAc7226f8df37eBFAF277252 | tag | 534 | 312 | +0.1% | 0.12 | +3.6% (454) | -19.4% (80) | yes |
| dfdeath | tag | 1102 | 584 | -0.1% | -0.04 | -0.1% (602) | -0.0% (500) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 302 | 130 | -5.0% | -0.77 | no |
| Kch-Temp | 114 | 52 | -9.6% | -0.9 | no |
| EdZachary | 82 | 36 | -10.2% | -0.94 | no |
| KaneAnalytics | 93 | 55 | +15.7% | 1.08 | yes |
| Jsram | 57 | 28 | -16.0% | -1.31 | no |
| Kkunn | 655 | 283 | +5.2% | 1.14 | yes |
| Sisyphus- | 115 | 68 | -1.8% | -0.21 | no |
| PEYZ-BIGGEST-FAN | 212 | 109 | +0.1% | 0.1 | no |
| theowalcott | 57 | 36 | +24.8% | 1.96 | yes |
| HVAB | 316 | 198 | +1.0% | 0.18 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +6.5% | 1.16 | no |
| Talvez10 | 593 | 321 | +3.6% | 0.61 | no |
| BunCaCham | 31 | 28 | +33.7% | 2.94 | yes |
| 0010001000001100 | 35 | 21 | +61.6% | 1.49 | yes |
| totoro3miyazaki | 39 | 29 | +28.0% | 1.96 | no |
| 1l2ihj34li12u34 | 30 | 22 | +47.7% | 2.81 | yes |
| yabanci | 27 | 19 | +28.0% | 1.94 | yes |
| 0x20D6436849F930584892730C7F | 150 | 86 | +28.4% | 2.07 | yes |
| juice-fruit | 30 | 22 | +22.7% | 1.46 | yes |
| 0x16bb9951a36fce71e2ef57890b | 858 | 466 | +6.3% | 1.87 | yes |
| GamblingOdyssey | 417 | 211 | +6.7% | 1.34 | yes |
| plonker2026 | 82 | 57 | +39.6% | 3.69 | yes |
| xxyx0xx | 173 | 86 | +1.8% | 0.1 | no |
| monkeymashingkeyboard | 1938 | 1097 | +7.6% | 3.31 | yes |
| Tiger105 | 41 | 28 | +30.4% | 2.04 | yes |
| THEHIGHLIFE | 278 | 133 | +24.2% | 2.13 | no |
| AmericaFirst1 | 440 | 278 | +7.7% | 1.74 | yes |
| UNEB3154s4f251 | 1847 | 1160 | +3.7% | 1.97 | yes |
