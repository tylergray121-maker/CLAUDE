# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-29 09:00 UTC: 5513 candidates, 3779 with trades copytop could copy, 218 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3286 | 1631 | $31,750 | -62.89 | -0.2% | -0.05 |
| every wallet that qualified on the first part (test window) | 3360 | 1658 | $32,503 | -92.13 | -0.3% | -0.10 |
| currently copied (test window) | 4024 | 2138 | $39,465 | +764.77 | +1.9% | +1.26 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3286 | 1631 | $31,750 | -62.89 | -0.2% | -0.05 | 6959 | 3502 | $67,212 | +4,782.11 | +7.1% | 4.51 |
| copy their sells too | 3286 | 1336 | $31,750 | -878.47 | -2.8% | -1.48 | 6959 | 3020 | $67,212 | +3,296.67 | +4.9% | 3.25 |
| size by conviction (x0.5 / x1 / x1.5) | 3105 | 1537 | $36,991 | +166.65 | +0.4% | -0.18 | 6546 | 3285 | $78,642 | +5,364.68 | +6.8% | 4.27 |
| skip bets under 0.5x their usual | 3069 | 1520 | $29,862 | +65.04 | +0.2% | 0.21 | 6535 | 3295 | $63,590 | +4,748.61 | +7.5% | 4.6 |
| pre-game only | 3150 | 1579 | $30,401 | -59.19 | -0.2% | -0.06 | 6529 | 3346 | $62,897 | +4,985.14 | +7.9% | 4.99 |
| skip prices under 30c | 2819 | 1517 | $27,097 | -216.91 | -0.8% | -0.47 | 5652 | 3123 | $54,223 | +643.46 | +1.2% | 1.04 |
| favorites only (50c+) | 1565 | 988 | $14,923 | -125.44 | -0.8% | -0.34 | 3028 | 2001 | $28,719 | +305.86 | +1.1% | 0.99 |
| 15s delay | 3302 | 1642 | $31,931 | +174.33 | +0.5% | 0.33 | 7011 | 3530 | $67,770 | +5,177.06 | +7.6% | 4.81 |
| 60s delay | 3286 | 1631 | $31,750 | -62.89 | -0.2% | -0.05 | 6959 | 3502 | $67,212 | +4,782.11 | +7.1% | 4.51 |
| allow 2c over their price | 3363 | 1664 | $32,482 | +58.58 | +0.2% | 0.13 | 7213 | 3626 | $69,683 | +5,085.32 | +7.3% | 4.63 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 412 | +26.4% | 3.56 | 377 | +10.9% | 1.27 |
| conviction:1-2x | 630 | +11.3% | 1.79 | 418 | -7.0% | -1.14 |
| conviction:2x+ | 2223 | +10.4% | 3.39 | 2054 | +0.9% | 0.49 |
| conviction:under 0.5x | 408 | +23.4% | 3.33 | 437 | -8.5% | -1.73 |
| delay_move:flat | 2459 | +15.4% | 5.16 | 2593 | +0.1% | 0.02 |
| delay_move:price fell | 1214 | +10.0% | 2.57 | 693 | -1.3% | -0.15 |
| exit:settle | 3673 | +13.7% | 5.74 | 3286 | -0.2% | -0.05 |
| kind:moneyline | 2730 | +11.6% | 3.98 | 2535 | -0.0% | 0.0 |
| kind:result | 868 | +20.9% | 4.86 | 589 | +3.5% | 0.89 |
| kind:totals | 75 | +5.1% | 0.65 | 162 | -17.4% | -2.33 |
| league:atp | 370 | +10.4% | 1.54 | 178 | +4.6% | 0.79 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 131 | +3.4% | 0.33 | 271 | +20.4% | 2.11 |
| league:cs2 | 319 | +11.4% | 1.3 | 240 | +2.9% | 0.68 |
| league:dota2 | 86 | -9.0% | -0.68 | 108 | +25.4% | 1.48 |
| league:epl | 52 | +34.2% | 3.05 | 50 | -13.4% | -1.19 |
| league:ere | 4 | +97.0% | — | 32 | +34.7% | 1.3 |
| league:lal | 70 | +15.4% | 1.43 | 92 | -16.5% | -1.65 |
| league:lol | 1774 | +15.5% | 3.96 | 325 | +0.4% | 0.04 |
| league:mls | 49 | +23.1% | 1.67 | 236 | -4.9% | -0.67 |
| league:nba | 0 | +0.0% | — | 384 | -1.8% | -0.29 |
| league:nfl | 340 | +14.1% | 2.01 | 321 | -0.4% | -0.31 |
| league:nhl | 9 | -4.4% | -0.11 | 626 | -11.7% | -2.99 |
| league:sea | 33 | +59.4% | 3.41 | 39 | -29.2% | -1.58 |
| league:ucl | 40 | -8.0% | -0.57 | 61 | +15.9% | 1.3 |
| league:uel | 0 | +0.0% | — | 12 | +17.4% | 0.79 |
| league:wnba | 96 | +7.0% | 1.03 | 74 | -6.7% | -0.43 |
| league:wta | 284 | +11.6% | 1.41 | 223 | +2.0% | 0.26 |
| price:30-70c | 2343 | +3.4% | 1.73 | 2516 | -1.1% | -0.51 |
| price:over 70c | 486 | +2.3% | 1.27 | 297 | +0.5% | 0.03 |
| price:under 30c | 844 | +47.5% | 5.81 | 473 | +3.8% | 0.53 |
| timing:in-play | 294 | -6.7% | -0.8 | 136 | -0.3% | 0.0 |
| timing:pre-game | 3379 | +15.5% | 6.44 | 3150 | -0.2% | -0.06 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 137408 | 71426 | $1,368,104 | -53,374.00 | -3.9% | -12.21 |
| consistency (winning weeks), top 16 | 10062 | 5691 | $98,966 | -2,571.43 | -2.6% | -2.30 |
| consistency (winning weeks), top 40 | 21680 | 11665 | $214,253 | -6,329.76 | -2.9% | -3.66 |
| copy return, average, top 16 | 6641 | 3354 | $65,465 | -1,605.84 | -2.5% | -1.71 |
| copy return, average, top 40 | 24209 | 12913 | $238,855 | -7,145.05 | -3.0% | -3.94 |
| copy return, lower bound, top 16 | 6921 | 3702 | $68,075 | -2,279.09 | -3.4% | -2.72 |
| copy return, lower bound, top 40 | 24938 | 13814 | $246,475 | -7,522.63 | -3.0% | -4.24 |
| copy return, shrunk, top 16 | 7752 | 3855 | $76,118 | -3,041.88 | -4.0% | -3.03 |
| copy return, shrunk, top 40 | 23355 | 12450 | $230,732 | -6,605.30 | -2.9% | -3.60 |
| markout 2h, average, top 16 | 7755 | 4502 | $76,487 | -1,521.41 | -2.0% | -1.66 |
| markout 2h, average, top 40 | 22372 | 12193 | $221,951 | -5,501.57 | -2.5% | -3.23 |
| markout 2h, lower bound, top 16 | 7675 | 4290 | $76,240 | -1,898.41 | -2.5% | -1.91 |
| markout 2h, lower bound, top 40 | 23724 | 12886 | $235,305 | -4,747.82 | -2.0% | -2.81 |
| markout 30m, average, top 16 | 9412 | 5162 | $94,024 | -2,656.48 | -2.8% | -2.35 |
| markout 30m, average, top 40 | 23403 | 12579 | $233,819 | -7,798.55 | -3.3% | -4.19 |
| most active, top 16 | 25449 | 13222 | $254,474 | -9,604.24 | -3.8% | -4.94 |
| most active, top 40 | 42686 | 21890 | $426,074 | -19,771.70 | -4.6% | -7.96 |
| win rate vs the odds, top 16 | 5714 | 2953 | $55,975 | -2,350.91 | -4.2% | -2.95 |
| win rate vs the odds, top 40 | 23708 | 12892 | $233,598 | -6,577.27 | -2.8% | -3.98 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| Talvez10 | 106 | 89 | +50.5% | 7.2 | +4.98 |
| BunCaCham | 49 | 45 | +29.7% | 3.56 | +2.90 |
| 0x20D6436849F930584892730C7F | 126 | 70 | +28.3% | 1.74 | +2.82 |
| tiger105 | 40 | 26 | +20.4% | 1.37 | +2.04 |
| theowalcott | 66 | 41 | +16.6% | 1.57 | +1.83 |
| eokho | 784 | 435 | +4.2% | 0.88 | +0.38 |
| xxyx0xx | 276 | 138 | +7.1% | 0.67 | +0.65 |
| Sisyphus- | 126 | 74 | +3.4% | 0.39 | +0.34 |
| yabanci | 61 | 40 | +11.7% | 1.31 | +1.47 |
| juice-fruit | 47 | 32 | +11.5% | 0.96 | +1.24 |
| SimpleTony | 1203 | 383 | +8.1% | 1.53 | +0.80 |
| platarb | 599 | 237 | +0.1% | 0.0 | +0.00 |
| moreplatesmoredates | 964 | 484 | +1.5% | 0.59 | +0.25 |
| 0x6918EA182D963b1Fb7888860b8 | 732 | 430 | +9.1% | 2.07 | +0.81 |
| AmericaFirst1 | 464 | 284 | +5.5% | 1.3 | +0.57 |
| plonker2026 | 132 | 76 | +12.6% | 1.76 | +1.68 |
| smithagent | 965 | 535 | +7.0% | 1.22 | +0.68 |
| KaneAnalytics | 150 | 85 | +7.1% | 0.69 | +0.71 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 881 | 389 | +5.3% | 0.91 | +0.51 |
| am100 | 980 | 585 | +12.1% | 3.28 | +1.21 |
| monkeymashingkeyboard | 779 | 421 | +8.8% | 2.17 | +0.86 |
| 1l2ihj34li12u34 | 90 | 53 | +16.0% | 1.78 | +1.92 |
| eskk | 1023 | 258 | -0.0% | 0.04 | +0.03 |
| pltrkr111 | 1087 | 613 | +13.0% | 3.25 | +1.25 |
| arahbo | 1598 | 683 | +1.3% | 0.24 | +0.11 |
| cosmicsteaks | 1261 | 542 | -2.5% | -0.62 | -0.28 |
| torta.tech | 1130 | 707 | +2.9% | 0.98 | +0.29 |
| 0x16bb9951a36fce71e2ef57890b | 56 | 23 | +1.0% | 0.01 | +0.02 |
| 0xFd1df6a11eB52B2B1a1b6131E7 | 594 | 314 | -2.6% | -0.53 | -0.26 |
| 0xffAaEFb5f6762Cc70cb575Da87 | 691 | 327 | +2.1% | 0.34 | +0.20 |
| walnutz | 640 | 328 | -2.3% | -0.54 | -0.23 |
| UNEB3154s4f251 | 2197 | 1397 | +3.2% | 1.91 | +0.33 |
| 0x870a742f | 537 | 231 | +1.5% | 0.27 | +0.16 |
| Future-Tarot-Trader | 2056 | 1045 | -0.8% | -0.32 | -0.11 |
| jiafan | 1039 | 617 | +0.4% | 0.08 | +0.03 |
| yuxkc0 | 392 | 132 | -5.6% | -0.7 | -0.56 |
| iseedota | 1274 | 559 | -2.3% | -0.59 | -0.22 |
| ZEST011 | 700 | 524 | +3.2% | 1.25 | +0.31 |
| littlebay | 774 | 512 | +1.8% | 0.5 | +0.18 |
| n1ck10s | 1017 | 540 | +1.7% | 0.48 | +0.17 |

## Esports specialists (copies on esports markets only)

2941 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 167 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | tag | 76 | 43 | +48.6% | 2.16 | +72.2% (33) | +30.6% (43) | no |
| pltrkr111 | tag | 271 | 160 | +35.4% | 3.48 | +45.7% (194) | +9.3% (77) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 26 | 14 | +105.0% | 1.27 | +132.6% (21) | -12.0% (5) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 301 | 182 | +24.2% | 2.62 | +20.1% (235) | +39.0% (66) | no |
| am100 | tag | 980 | 585 | +12.1% | 3.28 | +11.6% (903) | +17.3% (77) | yes |
| juice-fruit | current | 28 | 20 | +24.0% | 1.39 | +0.0% (0) | +24.0% (28) | yes |
| MIracle33 | tag | 444 | 228 | +10.4% | 1.82 | +10.9% (351) | +8.7% (93) | yes |
| 0x6918EA182D963b1Fb7888860b8 | tag | 732 | 430 | +9.1% | 2.07 | +5.5% (621) | +29.3% (111) | yes |
| -5rud | tag | 542 | 369 | +7.8% | 1.92 | +8.2% (432) | +6.4% (110) | yes |
| yakz | leaderboard | 176 | 87 | +17.4% | 1.3 | +30.0% (85) | +5.4% (91) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1392 | 730 | +6.2% | 2.0 | +9.7% (1175) | -13.1% (217) | yes |
| SimpleTony | tag | 1181 | 371 | +7.3% | 1.37 | +7.7% (828) | +6.3% (353) | yes |
| BunCaCham | tag | 20 | 19 | +7.6% | 1.29 | +4.9% (14) | +13.9% (6) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 618 | 316 | +4.9% | 1.14 | +9.9% (411) | -5.0% (207) | yes |
| ZEST011 | tag | 697 | 522 | +3.3% | 1.29 | +2.5% (596) | +7.8% (101) | yes |
| AmericaFirst1 | current | 256 | 165 | +5.1% | 1.03 | +8.9% (201) | -8.5% (55) | yes |
| Nooserac | tag | 188 | 99 | +7.3% | 0.84 | -1.7% (138) | +32.4% (50) | yes |
| berlinskies | tag | 1037 | 604 | +1.8% | 0.55 | +5.5% (801) | -10.8% (236) | yes |
| GC-C | tag | 733 | 513 | +1.1% | 0.44 | -4.7% (323) | +5.8% (410) | yes |
| moreplatesmoredates | tag | 964 | 484 | +1.5% | 0.59 | -2.9% (629) | +9.8% (335) | yes |
| TheRomanProcurator | tag | 131 | 61 | +13.7% | 0.86 | -100.0% (3) | +16.3% (128) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -9.6% (101) | +12.1% (117) | no |
| littlebay | tag | 94 | 69 | +3.9% | 0.59 | +7.8% (37) | +1.4% (57) | yes |
| dddd123s | tag | 566 | 341 | +0.6% | 0.15 | +4.9% (357) | -6.7% (209) | yes |
| 0xcf279d52 | tag | 496 | 297 | +1.1% | 0.24 | +6.7% (342) | -11.3% (154) | yes |
| johnbaster | tag | 867 | 462 | +1.8% | 0.31 | +2.3% (793) | -3.9% (74) | no |
| HalleyChen | tag | 657 | 400 | +1.0% | 0.24 | -0.2% (498) | +4.7% (159) | yes |
| Diabolical-Prize | tag | 224 | 118 | +2.1% | 0.47 | +11.6% (155) | -19.2% (69) | no |
| 0xffAaEFb5f6762Cc70cb575Da87 | tag | 691 | 327 | +2.1% | 0.34 | +5.5% (555) | -11.8% (136) | yes |
| Future-Tarot-Trader | tag | 2056 | 1045 | -0.8% | -0.32 | -2.9% (1835) | +16.2% (221) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 290 | 120 | -8.9% | -1.28 | no |
| Kch-Temp | 124 | 59 | -7.5% | -0.73 | no |
| EdZachary | 82 | 28 | -13.1% | -0.99 | no |
| KaneAnalytics | 150 | 85 | +7.1% | 0.69 | yes |
| Jsram | 95 | 56 | +0.0% | 0.21 | no |
| Kkunn | 745 | 320 | +2.7% | 0.77 | no |
| Sisyphus- | 126 | 74 | +3.4% | 0.39 | yes |
| PEYZ-BIGGEST-FAN | 392 | 195 | +2.3% | 0.36 | no |
| theowalcott | 66 | 41 | +16.6% | 1.57 | yes |
| HVAB | 339 | 204 | -3.2% | -0.59 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 282 | 147 | +6.5% | 1.18 | no |
| Talvez10 | 106 | 89 | +50.5% | 7.2 | yes |
| BunCaCham | 49 | 45 | +29.7% | 3.56 | yes |
| 0010001000001100 | 155 | 73 | +0.6% | -0.24 | no |
| totoro3miyazaki | 49 | 31 | +8.7% | 0.68 | no |
| 1l2ihj34li12u34 | 90 | 53 | +16.0% | 1.78 | yes |
| yabanci | 61 | 40 | +11.7% | 1.31 | yes |
| 0x20D6436849F930584892730C7F | 126 | 70 | +28.3% | 1.74 | yes |
| juice-fruit | 47 | 32 | +11.5% | 0.96 | yes |
| 0x16bb9951a36fce71e2ef57890b | 56 | 23 | +1.0% | 0.01 | yes |
| GamblingOdyssey | 392 | 188 | +2.3% | 0.59 | no |
| plonker2026 | 132 | 76 | +12.6% | 1.76 | yes |
| xxyx0xx | 276 | 138 | +7.1% | 0.67 | yes |
| monkeymashingkeyboard | 779 | 421 | +8.8% | 2.17 | yes |
| Tiger105 | 40 | 26 | +20.4% | 1.37 | yes |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 464 | 284 | +5.5% | 1.3 | yes |
| UNEB3154s4f251 | 2197 | 1397 | +3.2% | 1.91 | yes |
