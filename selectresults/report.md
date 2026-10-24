# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-24 09:00 UTC: 5492 candidates, 3865 with trades copytop could copy, 227 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 1455 | 661 | $14,455 | -465.76 | -3.2% | -0.89 |
| every wallet that qualified on the first part (test window) | 1721 | 795 | $17,127 | -810.69 | -4.7% | -1.50 |
| currently copied (test window) | 4157 | 2194 | $40,790 | +915.16 | +2.2% | +1.46 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 1455 | 661 | $14,455 | -465.76 | -3.2% | -0.89 | 3373 | 1680 | $33,477 | +2,177.67 | +6.5% | 3.11 |
| copy their sells too | 1455 | 649 | $14,455 | -680.47 | -4.7% | -1.39 | 3373 | 1667 | $33,477 | +1,955.30 | +5.8% | 2.83 |
| size by conviction (x0.5 / x1 / x1.5) | 1438 | 652 | $17,823 | -500.69 | -2.8% | -1.01 | 3338 | 1660 | $40,723 | +2,272.90 | +5.6% | 3.03 |
| skip bets under 0.5x their usual | 1334 | 611 | $13,321 | -346.20 | -2.6% | -0.57 | 3015 | 1507 | $30,065 | +1,953.02 | +6.5% | 3.0 |
| pre-game only | 1051 | 515 | $10,361 | -24.61 | -0.2% | -0.05 | 2657 | 1384 | $26,196 | +2,019.89 | +7.7% | 3.36 |
| skip prices under 30c | 1168 | 601 | $11,529 | -108.58 | -0.9% | -0.23 | 2885 | 1536 | $28,523 | +700.82 | +2.5% | 1.41 |
| favorites only (50c+) | 550 | 349 | $5,369 | +70.77 | +1.3% | 0.43 | 1371 | 876 | $13,461 | +445.94 | +3.3% | 1.6 |
| 15s delay | 1511 | 685 | $15,012 | -583.40 | -3.9% | -1.07 | 3503 | 1747 | $34,785 | +2,386.10 | +6.9% | 3.34 |
| 60s delay | 1455 | 661 | $14,455 | -465.76 | -3.2% | -0.89 | 3373 | 1680 | $33,477 | +2,177.67 | +6.5% | 3.11 |
| allow 2c over their price | 1522 | 687 | $15,097 | -546.56 | -3.6% | -1.0 | 3535 | 1748 | $35,076 | +2,020.88 | +5.8% | 2.87 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 160 | +42.3% | 3.3 | 140 | +9.3% | 0.9 |
| conviction:1-2x | 255 | +18.1% | 2.09 | 148 | -18.9% | -1.78 |
| conviction:2x+ | 1171 | +8.8% | 2.51 | 940 | -1.6% | -0.56 |
| conviction:under 0.5x | 332 | +15.0% | 2.12 | 227 | -7.2% | -0.59 |
| delay_move:flat | 1124 | +14.1% | 3.81 | 887 | -1.4% | -0.26 |
| delay_move:price fell | 794 | +13.6% | 2.9 | 568 | -5.9% | -1.04 |
| exit:settle | 1918 | +13.9% | 4.78 | 1455 | -3.2% | -0.89 |
| kind:moneyline | 1389 | +15.6% | 4.4 | 1274 | +0.4% | 0.24 |
| kind:result | 75 | +49.6% | 4.79 | 64 | -40.5% | -3.64 |
| kind:totals | 454 | +3.0% | 0.49 | 117 | -21.4% | -2.46 |
| league:atp | 378 | +13.4% | 1.75 | 460 | -11.6% | -1.81 |
| league:cfb | 13 | -100.0% | — | 32 | +53.7% | 2.1 |
| league:cs2 | 118 | +20.3% | 2.13 | 70 | -4.4% | -0.21 |
| league:dota2 | 32 | +59.1% | 3.04 | 33 | -34.8% | -2.05 |
| league:epl | 13 | +126.8% | 4.8 | 6 | -10.4% | -0.24 |
| league:lal | 15 | +26.4% | 1.49 | 2 | -0.4% | -0.03 |
| league:lol | 121 | +59.0% | 3.02 | 96 | -14.0% | -1.37 |
| league:mlb | 967 | +5.8% | 1.56 | 188 | -13.6% | -1.87 |
| league:mls | 13 | +26.7% | 1.1 | 16 | -32.2% | -1.39 |
| league:nba | 0 | +0.0% | — | 23 | -11.9% | -0.47 |
| league:nfl | 33 | +32.8% | 1.27 | 32 | +19.1% | 1.01 |
| league:sea | 17 | +56.2% | 2.51 | 20 | -28.2% | -1.23 |
| league:wnba | 11 | -1.8% | -0.03 | 13 | -55.0% | -2.6 |
| league:wta | 185 | +8.8% | 1.19 | 458 | +13.9% | 2.24 |
| price:30-70c | 1599 | +4.1% | 1.64 | 1065 | -1.1% | -0.24 |
| price:over 70c | 116 | +12.8% | 4.15 | 96 | +1.8% | 0.2 |
| price:under 30c | 203 | +90.5% | 5.21 | 294 | -12.2% | -1.1 |
| timing:in-play | 312 | +18.8% | 2.22 | 404 | -10.8% | -1.4 |
| timing:pre-game | 1606 | +12.9% | 4.23 | 1051 | -0.2% | -0.05 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 142478 | 73712 | $1,415,867 | -59,057.12 | -4.2% | -13.76 |
| consistency (winning weeks), top 16 | 7893 | 3964 | $77,966 | -4,330.25 | -5.5% | -4.14 |
| consistency (winning weeks), top 40 | 24128 | 12823 | $237,943 | -7,077.77 | -3.0% | -4.25 |
| copy return, average, top 16 | 6475 | 3169 | $64,171 | -1,484.87 | -2.3% | -1.45 |
| copy return, average, top 40 | 22821 | 12027 | $225,604 | -6,019.28 | -2.7% | -3.45 |
| copy return, lower bound, top 16 | 7464 | 3777 | $73,540 | -2,046.56 | -2.8% | -1.93 |
| copy return, lower bound, top 40 | 29373 | 15798 | $290,353 | -8,656.69 | -3.0% | -4.59 |
| copy return, shrunk, top 16 | 7035 | 3411 | $69,564 | -1,692.83 | -2.4% | -1.57 |
| copy return, shrunk, top 40 | 26157 | 13742 | $258,836 | -5,713.94 | -2.2% | -3.04 |
| markout 2h, average, top 16 | 5589 | 2966 | $55,950 | -433.28 | -0.8% | -0.34 |
| markout 2h, average, top 40 | 18471 | 9850 | $184,396 | -5,340.99 | -2.9% | -3.20 |
| markout 2h, lower bound, top 16 | 6709 | 3503 | $66,958 | -1,425.63 | -2.1% | -1.31 |
| markout 2h, lower bound, top 40 | 25367 | 13340 | $252,249 | -6,421.56 | -2.5% | -3.38 |
| markout 30m, average, top 16 | 7582 | 4011 | $75,595 | -2,522.45 | -3.3% | -2.53 |
| markout 30m, average, top 40 | 25601 | 13420 | $255,978 | -7,643.46 | -3.0% | -3.97 |
| most active, top 16 | 25230 | 12818 | $250,163 | -14,849.40 | -5.9% | -8.63 |
| most active, top 40 | 49846 | 25522 | $494,961 | -24,671.88 | -5.0% | -9.84 |
| win rate vs the odds, top 16 | 5146 | 2639 | $50,873 | -210.61 | -0.4% | -0.20 |
| win rate vs the odds, top 40 | 22402 | 11684 | $221,952 | -5,236.70 | -2.4% | -3.06 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| yabanci | 30 | 21 | +28.5% | 2.03 | +3.35 |
| 0x20D6436849F930584892730C7F | 149 | 84 | +26.9% | 1.94 | +2.74 |
| tiger105 | 47 | 32 | +27.2% | 1.97 | +2.71 |
| juice-fruit | 31 | 23 | +27.5% | 1.73 | +2.80 |
| 1l2ihj34li12u34 | 31 | 23 | +49.0% | 2.97 | +5.07 |
| 0x16bb9951a36fce71e2ef57890b | 837 | 458 | +7.0% | 2.1 | +0.73 |
| theowalcott | 79 | 45 | +8.1% | 0.89 | +0.98 |
| SimpleTony | 1067 | 351 | +10.7% | 2.04 | +1.14 |
| KaneAnalytics | 98 | 57 | +12.7% | 0.9 | +1.23 |
| AmericaFirst1 | 450 | 286 | +8.2% | 1.87 | +0.83 |
| smithagent | 697 | 374 | +5.6% | 0.82 | +0.54 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 1056 | 466 | +2.1% | 0.43 | +0.20 |
| platarb | 920 | 357 | +0.6% | 0.12 | +0.05 |
| arahbo | 1053 | 441 | +3.7% | 0.6 | +0.34 |
| eskk | 884 | 208 | -0.8% | -0.05 | -0.04 |
| polkals | 561 | 253 | +6.9% | 1.01 | +0.66 |
| NeedForDead | 375 | 158 | +11.0% | 1.41 | +1.10 |
| nightcity2077 | 858 | 416 | +2.2% | 0.41 | +0.22 |
| Sisyphus- | 118 | 71 | +1.7% | 0.21 | +0.17 |
| clement21 | 656 | 344 | +0.6% | 0.17 | +0.07 |
| totoro3miyazaki | 46 | 34 | +35.8% | 2.44 | +3.50 |
| 0x567212c82AAa6fe589bE5A2f4C | 515 | 262 | +5.0% | 1.13 | +0.71 |
| RensPeters | 595 | 296 | +0.8% | 0.19 | +0.08 |
| cosmicsteaks | 781 | 347 | -2.8% | -0.54 | -0.29 |
| monkeymashingkeyboard | 1964 | 1099 | +5.8% | 2.51 | +0.56 |
| GamblingOdyssey | 422 | 213 | +6.5% | 1.31 | +0.76 |
| walnutz | 634 | 328 | -1.5% | -0.37 | -0.16 |
| Petal | 861 | 406 | -6.2% | -1.52 | -0.62 |
| 0x7a3FB8C5aD2aF4C621B2138D95 | 472 | 193 | -9.1% | -1.28 | -0.90 |
| plonker2026 | 179 | 89 | +0.5% | 0.36 | +0.30 |
| PEYZ-BIGGEST-FAN | 229 | 117 | +2.3% | 0.37 | +0.28 |
| UNEB3154s4f251 | 1942 | 1222 | +3.2% | 1.78 | +0.33 |
| jiafan | 926 | 552 | +3.0% | 0.77 | +0.27 |
| n1ck10s | 1001 | 534 | +2.4% | 0.67 | +0.24 |
| littlebay | 711 | 468 | +2.1% | 0.53 | +0.20 |
| igot50k | 1345 | 824 | -2.0% | -0.72 | -0.21 |
| Future-Tarot-Trader | 1110 | 558 | -2.9% | -0.75 | -0.33 |
| Kkunn | 667 | 284 | +3.4% | 0.83 | +0.45 |
| TheRomanProcurator | 3728 | 1844 | +1.7% | 0.77 | +0.17 |
| cm2897 | 929 | 452 | +0.6% | 0.02 | +0.01 |

## Esports specialists (copies on esports markets only)

2800 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 168 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| pltrkr111 | tag | 184 | 101 | +41.9% | 2.93 | +68.2% (113) | -0.1% (71) | yes |
| juice-fruit | current | 25 | 19 | +28.5% | 1.64 | +0.0% (0) | +28.5% (25) | yes |
| NeedForDead | tag | 40 | 22 | +31.0% | 1.54 | +44.1% (25) | +9.2% (15) | no |
| yakz | leaderboard | 152 | 75 | +23.7% | 1.56 | +19.1% (73) | +28.0% (79) | yes |
| SimpleTony | tag | 1056 | 347 | +10.8% | 2.05 | +6.0% (722) | +21.1% (334) | yes |
| -5rud | tag | 364 | 262 | +8.6% | 1.91 | +12.6% (221) | +2.5% (143) | yes |
| AmericaFirst1 | current | 196 | 132 | +8.5% | 1.52 | +8.1% (146) | +9.8% (50) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 223 | 114 | +16.3% | 1.24 | +17.1% (161) | +14.2% (62) | no |
| ehl-rungs | tag | 197 | 149 | +6.4% | 1.38 | +6.4% (197) | +0.0% (0) | no |
| smartcombo | tag | 182 | 106 | +10.1% | 1.1 | +17.4% (158) | -37.8% (24) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 515 | 262 | +5.0% | 1.13 | +10.5% (322) | -4.2% (193) | yes |
| newUser2025 | tag | 128 | 88 | +6.4% | 0.97 | +11.0% (85) | -2.7% (43) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 141 | 97 | +6.0% | 0.96 | +9.7% (73) | +2.0% (68) | yes |
| mpoly | tag | 238 | 172 | +4.6% | 0.93 | +7.9% (151) | -1.3% (87) | yes |
| dddd123s | tag | 452 | 283 | +3.8% | 0.91 | +11.0% (209) | -2.4% (243) | yes |
| sinhtuycanh | tag | 148 | 108 | +5.2% | 0.93 | +1.3% (71) | +8.9% (77) | yes |
| RensPeters | tag | 78 | 46 | +11.4% | 0.97 | +10.9% (43) | +12.0% (35) | yes |
| littlebay | tag | 88 | 66 | +6.7% | 0.94 | +16.8% (24) | +2.9% (64) | no |
| nightcity2077 | tag | 294 | 151 | +8.4% | 0.86 | +8.9% (277) | -0.1% (17) | yes |
| MIracle33 | tag | 309 | 156 | +4.9% | 0.78 | +8.9% (216) | -4.5% (93) | yes |
| superlxj | tag | 195 | 135 | +3.5% | 0.71 | -8.6% (93) | +15.2% (102) | yes |
| GC-C | tag | 727 | 507 | +0.9% | 0.37 | +5.1% (194) | -0.7% (533) | yes |
| igot50k | tag | 674 | 348 | +3.9% | 0.65 | -1.5% (522) | +22.6% (152) | yes |
| 0x09dAc7226f8df37eBFAF277252 | tag | 533 | 314 | +0.9% | 0.32 | +3.9% (451) | -15.7% (82) | yes |
| dfdeath | tag | 1133 | 602 | +0.4% | 0.1 | -0.8% (639) | +1.9% (494) | yes |
| jiafan | tag | 396 | 235 | +1.9% | 0.38 | +3.4% (345) | -7.4% (51) | yes |
| 8dddj | tag | 730 | 469 | -0.7% | -0.15 | +0.0% (240) | -1.0% (490) | yes |
| lll981kd | tag | 671 | 428 | -0.6% | -0.15 | +1.0% (215) | -1.3% (456) | yes |
| Diabolical-Prize | tag | 214 | 112 | +2.2% | 0.48 | +19.9% (129) | -23.8% (85) | no |
| BOB6633 | tag | 369 | 209 | +1.2% | 0.26 | +18.8% (20) | +0.2% (349) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 305 | 133 | -3.9% | -0.62 | no |
| Kch-Temp | 106 | 48 | -11.4% | -1.14 | no |
| EdZachary | 83 | 36 | -11.4% | -1.04 | no |
| KaneAnalytics | 98 | 57 | +12.7% | 0.9 | yes |
| Jsram | 100 | 62 | +3.4% | 0.4 | no |
| Kkunn | 667 | 284 | +3.4% | 0.83 | yes |
| Sisyphus- | 118 | 71 | +1.7% | 0.21 | yes |
| PEYZ-BIGGEST-FAN | 229 | 117 | +2.3% | 0.37 | yes |
| theowalcott | 79 | 45 | +8.1% | 0.89 | yes |
| HVAB | 307 | 191 | -0.2% | -0.03 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 278 | 142 | +6.1% | 1.11 | no |
| Talvez10 | 580 | 317 | +4.4% | 0.78 | no |
| BunCaCham | 25 | 22 | +12.3% | 1.14 | no |
| 0010001000001100 | 148 | 71 | -8.8% | -0.71 | no |
| totoro3miyazaki | 46 | 34 | +35.8% | 2.44 | yes |
| 1l2ihj34li12u34 | 31 | 23 | +49.0% | 2.97 | yes |
| yabanci | 30 | 21 | +28.5% | 2.03 | yes |
| 0x20D6436849F930584892730C7F | 149 | 84 | +26.9% | 1.94 | yes |
| juice-fruit | 31 | 23 | +27.5% | 1.73 | yes |
| 0x16bb9951a36fce71e2ef57890b | 837 | 458 | +7.0% | 2.1 | yes |
| GamblingOdyssey | 422 | 213 | +6.5% | 1.31 | yes |
| plonker2026 | 179 | 89 | +0.5% | 0.36 | yes |
| xxyx0xx | 217 | 107 | -4.9% | -0.55 | no |
| monkeymashingkeyboard | 1964 | 1099 | +5.8% | 2.51 | yes |
| Tiger105 | 47 | 32 | +27.2% | 1.97 | yes |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 450 | 286 | +8.2% | 1.87 | yes |
| UNEB3154s4f251 | 1942 | 1222 | +3.2% | 1.78 | yes |
