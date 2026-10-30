# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-30 09:00 UTC: 5489 candidates, 3759 with trades copytop could copy, 220 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3841 | 1907 | $37,320 | -0.77 | -0.0% | +0.14 |
| every wallet that qualified on the first part (test window) | 4593 | 2253 | $44,949 | -72.72 | -0.2% | +0.03 |
| currently copied (test window) | 4010 | 2146 | $39,315 | +1,090.11 | +2.8% | +1.78 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3841 | 1907 | $37,320 | -0.77 | +0.0% | 0.14 | 7625 | 3852 | $73,887 | +5,094.10 | +6.9% | 4.65 |
| copy their sells too | 3841 | 1609 | $37,320 | -789.80 | -2.1% | -1.12 | 7625 | 3350 | $73,887 | +3,549.94 | +4.8% | 3.38 |
| size by conviction (x0.5 / x1 / x1.5) | 3649 | 1804 | $42,489 | +135.32 | +0.3% | -0.08 | 7203 | 3626 | $85,439 | +5,591.82 | +6.5% | 4.34 |
| skip bets under 0.5x their usual | 3559 | 1782 | $34,742 | +89.29 | +0.3% | 0.33 | 7126 | 3622 | $69,475 | +4,978.09 | +7.2% | 4.72 |
| pre-game only | 3164 | 1593 | $30,511 | +59.01 | +0.2% | 0.23 | 6608 | 3401 | $63,630 | +5,198.28 | +8.2% | 5.22 |
| skip prices under 30c | 3246 | 1755 | $31,341 | -510.86 | -1.6% | -0.91 | 6201 | 3430 | $59,656 | +308.92 | +0.5% | 0.58 |
| favorites only (50c+) | 1843 | 1179 | $17,632 | -103.60 | -0.6% | -0.19 | 3384 | 2247 | $32,186 | +401.95 | +1.2% | 1.2 |
| 15s delay | 3956 | 1985 | $38,476 | +171.53 | +0.4% | 0.38 | 7784 | 3954 | $75,490 | +5,444.56 | +7.2% | 4.85 |
| 60s delay | 3841 | 1907 | $37,320 | -0.77 | +0.0% | 0.14 | 7625 | 3852 | $73,887 | +5,094.10 | +6.9% | 4.65 |
| allow 2c over their price | 3967 | 1974 | $38,543 | +253.59 | +0.7% | 0.46 | 7939 | 4016 | $76,957 | +5,566.36 | +7.2% | 4.89 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 420 | +26.9% | 3.7 | 556 | +6.7% | 0.99 |
| conviction:1-2x | 656 | +12.7% | 2.03 | 664 | -6.3% | -1.33 |
| conviction:2x+ | 2278 | +10.5% | 3.5 | 2125 | +1.2% | 0.7 |
| conviction:under 0.5x | 430 | +22.4% | 3.36 | 496 | -4.5% | -0.77 |
| delay_move:flat | 2504 | +15.3% | 5.15 | 2711 | +0.2% | 0.2 |
| delay_move:price fell | 1280 | +11.3% | 3.05 | 1130 | -0.5% | -0.06 |
| exit:settle | 3784 | +13.9% | 5.98 | 3841 | +0.0% | 0.14 |
| kind:moneyline | 2817 | +12.4% | 4.36 | 2932 | -0.5% | -0.11 |
| kind:result | 888 | +19.9% | 4.76 | 720 | +3.4% | 0.87 |
| kind:totals | 79 | +0.7% | 0.15 | 189 | -4.7% | -0.55 |
| league:atp | 404 | +10.5% | 1.62 | 373 | +4.0% | 0.83 |
| league:bra | 6 | +109.4% | — | 19 | +15.5% | 0.63 |
| league:bun | 8 | +50.3% | 14.89 | 6 | -73.2% | -2.67 |
| league:cfb | 131 | +3.4% | 0.33 | 271 | +20.4% | 2.11 |
| league:cs2 | 321 | +11.4% | 1.3 | 272 | +3.0% | 0.7 |
| league:dota2 | 99 | -3.6% | -0.32 | 160 | +7.4% | 0.58 |
| league:epl | 52 | +34.2% | 3.05 | 51 | -15.2% | -1.33 |
| league:ere | 4 | +97.0% | — | 33 | +34.7% | 1.34 |
| league:lal | 70 | +15.4% | 1.43 | 97 | +2.8% | 0.03 |
| league:lol | 1788 | +15.8% | 4.14 | 324 | -1.4% | -0.16 |
| league:mls | 49 | +23.1% | 1.67 | 251 | -3.9% | -0.54 |
| league:nba | 0 | +0.0% | — | 445 | +2.6% | 0.62 |
| league:nfl | 355 | +14.4% | 2.13 | 306 | -1.6% | -0.51 |
| league:nhl | 15 | +33.9% | 1.08 | 672 | -14.1% | -3.66 |
| league:sea | 33 | +59.4% | 3.41 | 54 | -13.3% | -0.6 |
| league:ucl | 40 | -8.0% | -0.57 | 70 | +10.7% | 1.02 |
| league:uel | 0 | +0.0% | — | 13 | +34.3% | 1.22 |
| league:uslc | 0 | +0.0% | — | 11 | -6.1% | -0.32 |
| league:wnba | 113 | +2.9% | 0.45 | 64 | +5.4% | 0.78 |
| league:wta | 294 | +12.3% | 1.54 | 325 | +0.3% | 0.05 |
| price:30-70c | 2430 | +3.1% | 1.59 | 2822 | -1.9% | -0.89 |
| price:over 70c | 521 | +2.2% | 1.21 | 412 | -2.9% | -1.3 |
| price:under 30c | 833 | +51.5% | 6.27 | 607 | +10.4% | 1.47 |
| timing:in-play | 340 | -1.3% | -0.21 | 664 | -2.2% | -0.4 |
| timing:pre-game | 3444 | +15.5% | 6.5 | 3164 | +0.2% | 0.23 |
| timing:unknown | 0 | +0.0% | — | 13 | +71.8% | 2.32 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 132613 | 68961 | $1,320,012 | -51,157.50 | -3.9% | -11.95 |
| consistency (winning weeks), top 16 | 9960 | 5319 | $98,486 | -5,200.23 | -5.3% | -4.56 |
| consistency (winning weeks), top 40 | 23269 | 12638 | $230,019 | -6,470.19 | -2.8% | -3.54 |
| copy return, average, top 16 | 5443 | 2810 | $53,879 | -1,090.61 | -2.0% | -1.15 |
| copy return, average, top 40 | 20586 | 10737 | $203,502 | -6,955.25 | -3.4% | -4.02 |
| copy return, lower bound, top 16 | 7472 | 3870 | $73,808 | -4,946.75 | -6.7% | -5.25 |
| copy return, lower bound, top 40 | 22202 | 12040 | $219,867 | -9,069.47 | -4.1% | -5.36 |
| copy return, shrunk, top 16 | 7292 | 3579 | $72,295 | -4,441.24 | -6.1% | -4.04 |
| copy return, shrunk, top 40 | 20251 | 10611 | $200,534 | -6,344.30 | -3.2% | -3.61 |
| markout 2h, average, top 16 | 6291 | 3505 | $62,604 | -1,902.43 | -3.0% | -1.97 |
| markout 2h, average, top 40 | 21807 | 11691 | $216,822 | -6,490.73 | -3.0% | -3.69 |
| markout 2h, lower bound, top 16 | 7708 | 4223 | $76,547 | -2,544.89 | -3.3% | -2.49 |
| markout 2h, lower bound, top 40 | 24306 | 13372 | $240,949 | -6,700.62 | -2.8% | -3.89 |
| markout 30m, average, top 16 | 6988 | 3792 | $69,977 | -1,003.41 | -1.4% | -1.07 |
| markout 30m, average, top 40 | 21821 | 12030 | $217,729 | -6,500.28 | -3.0% | -3.67 |
| most active, top 16 | 22337 | 11818 | $222,668 | -10,085.70 | -4.5% | -5.82 |
| most active, top 40 | 40074 | 20606 | $399,433 | -18,465.24 | -4.6% | -7.85 |
| win rate vs the odds, top 16 | 4861 | 2575 | $47,797 | -1,439.97 | -3.0% | -1.88 |
| win rate vs the odds, top 40 | 22012 | 11679 | $217,726 | -7,601.15 | -3.5% | -4.61 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| Talvez10 | 110 | 90 | +46.7% | 6.52 | +4.61 |
| BunCaCham | 49 | 45 | +29.7% | 3.56 | +2.90 |
| 0x20D6436849F930584892730C7F | 126 | 70 | +28.3% | 1.74 | +2.82 |
| tiger105 | 40 | 26 | +20.4% | 1.37 | +2.04 |
| theowalcott | 72 | 45 | +16.8% | 1.66 | +1.84 |
| xxyx0xx | 279 | 139 | +7.2% | 0.68 | +0.66 |
| eokho | 794 | 442 | +4.3% | 0.93 | +0.40 |
| yabanci | 62 | 41 | +12.1% | 1.37 | +1.51 |
| Sisyphus- | 123 | 72 | +1.6% | 0.18 | +0.15 |
| am100 | 972 | 584 | +12.5% | 3.39 | +1.25 |
| 0x6918EA182D963b1Fb7888860b8 | 726 | 430 | +10.0% | 2.27 | +0.89 |
| platarb | 590 | 235 | +0.8% | 0.13 | +0.07 |
| SimpleTony | 1179 | 379 | +8.8% | 1.71 | +0.91 |
| moreplatesmoredates | 958 | 481 | +2.2% | 0.76 | +0.33 |
| AmericaFirst1 | 464 | 284 | +5.5% | 1.3 | +0.57 |
| juice-fruit | 48 | 32 | +9.0% | 0.79 | +1.00 |
| monkeymashingkeyboard | 799 | 438 | +10.6% | 2.67 | +1.06 |
| plonker2026 | 132 | 76 | +12.6% | 1.76 | +1.68 |
| pltrkr111 | 1115 | 629 | +12.9% | 3.26 | +1.23 |
| smithagent | 1001 | 553 | +6.1% | 1.09 | +0.59 |
| eskk | 1017 | 257 | +0.0% | 0.05 | +0.04 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 879 | 387 | +4.7% | 0.81 | +0.46 |
| arahbo | 1574 | 668 | -1.7% | -0.44 | -0.18 |
| torta.tech | 1148 | 719 | +3.5% | 1.17 | +0.35 |
| cosmicsteaks | 1254 | 541 | -2.2% | -0.55 | -0.24 |
| 0x16bb9951a36fce71e2ef57890b | 56 | 23 | +1.0% | 0.01 | +0.02 |
| KaneAnalytics | 156 | 86 | +4.3% | 0.43 | +0.42 |
| 0xffAaEFb5f6762Cc70cb575Da87 | 691 | 327 | +2.1% | 0.34 | +0.20 |
| 0xFd1df6a11eB52B2B1a1b6131E7 | 583 | 310 | -2.2% | -0.43 | -0.21 |
| shiifoo | 474 | 189 | -0.3% | -0.08 | -0.06 |
| n1ck10s | 1073 | 573 | +3.5% | 0.93 | +0.34 |
| walnutz | 636 | 325 | -2.2% | -0.52 | -0.23 |
| iseedota | 1302 | 575 | -2.3% | -0.59 | -0.22 |
| Kkunn | 761 | 332 | +4.1% | 1.04 | +0.53 |
| jiafan | 1014 | 601 | +0.2% | 0.02 | +0.01 |
| Future-Tarot-Trader | 2034 | 1029 | -1.9% | -0.64 | -0.21 |
| yuxkc0 | 388 | 131 | -7.2% | -0.92 | -0.70 |
| Petal | 927 | 437 | -6.7% | -1.7 | -0.67 |
| 1l2ihj34li12u34 | 92 | 53 | +13.4% | 1.55 | +1.66 |
| NS13 | 1110 | 433 | -1.8% | -0.05 | -0.03 |

## Esports specialists (copies on esports markets only)

2911 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 169 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | tag | 76 | 43 | +48.6% | 2.16 | +60.8% (42) | +33.6% (34) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +41.6% (206) | +6.8% (71) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 32 | 18 | +90.0% | 1.33 | +132.6% (21) | +8.5% (11) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 301 | 182 | +24.2% | 2.62 | +19.0% (242) | +45.8% (59) | no |
| am100 | tag | 972 | 584 | +12.5% | 3.39 | +11.6% (910) | +23.9% (62) | yes |
| 0x6918EA182D963b1Fb7888860b8 | tag | 726 | 430 | +10.0% | 2.27 | +6.2% (627) | +33.6% (99) | yes |
| MIracle33 | tag | 447 | 229 | +10.1% | 1.77 | +10.2% (356) | +9.7% (91) | yes |
| -5rud | tag | 538 | 367 | +8.2% | 2.0 | +8.4% (437) | +7.6% (101) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1358 | 715 | +6.7% | 2.14 | +10.0% (1163) | -12.5% (195) | yes |
| SimpleTony | tag | 1157 | 367 | +7.9% | 1.55 | +9.6% (812) | +4.0% (345) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +0.0% (0) | +19.4% (29) | yes |
| yakz | leaderboard | 179 | 88 | +16.0% | 1.2 | +28.4% (86) | +4.3% (93) | yes |
| BunCaCham | tag | 20 | 19 | +7.6% | 1.29 | +4.9% (14) | +13.9% (6) | yes |
| Nooserac | tag | 179 | 97 | +10.4% | 1.17 | +1.9% (129) | +32.4% (50) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 627 | 323 | +5.3% | 1.23 | +10.6% (417) | -5.3% (210) | yes |
| ZEST011 | tag | 680 | 509 | +3.2% | 1.25 | +2.4% (578) | +7.7% (102) | yes |
| AmericaFirst1 | current | 256 | 165 | +5.1% | 1.03 | +8.0% (210) | -7.7% (46) | yes |
| moreplatesmoredates | tag | 958 | 481 | +2.2% | 0.76 | -1.6% (613) | +9.0% (345) | yes |
| berlinskies | tag | 1043 | 607 | +2.1% | 0.65 | +4.9% (821) | -7.9% (222) | yes |
| GC-C | tag | 739 | 517 | +1.0% | 0.41 | -6.4% (351) | +7.9% (388) | yes |
| littlebay | tag | 95 | 70 | +4.9% | 0.73 | +12.2% (41) | -0.7% (54) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -9.4% (108) | +13.4% (110) | no |
| shaw | tag | 289 | 165 | +3.2% | 0.55 | +5.1% (225) | -4.0% (64) | yes |
| dddd123s | tag | 573 | 345 | +0.4% | 0.09 | +4.5% (371) | -7.1% (202) | yes |
| HalleyChen | tag | 649 | 396 | +1.2% | 0.28 | +1.5% (501) | +0.2% (148) | yes |
| 0xcf279d52 | tag | 499 | 298 | +0.9% | 0.19 | +5.6% (349) | -10.1% (150) | yes |
| Diabolical-Prize | tag | 224 | 118 | +2.1% | 0.47 | +9.0% (168) | -18.4% (56) | no |
| 0xffAaEFb5f6762Cc70cb575Da87 | tag | 691 | 327 | +2.1% | 0.34 | +5.7% (560) | -13.1% (131) | yes |
| johnbaster | tag | 854 | 456 | +1.1% | 0.19 | -0.4% (793) | +21.4% (61) | yes |
| 0x85264d29Fa7279946D15105C17 | tag | 132 | 68 | +6.4% | 0.61 | +10.5% (101) | -7.1% (31) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 291 | 120 | -9.2% | -1.33 | no |
| Kch-Temp | 124 | 59 | -7.5% | -0.73 | no |
| EdZachary | 82 | 28 | -13.1% | -0.99 | no |
| KaneAnalytics | 156 | 86 | +4.3% | 0.43 | yes |
| Jsram | 95 | 56 | +0.0% | 0.21 | no |
| Kkunn | 761 | 332 | +4.1% | 1.04 | yes |
| Sisyphus- | 123 | 72 | +1.6% | 0.18 | yes |
| PEYZ-BIGGEST-FAN | 392 | 196 | +2.5% | 0.4 | no |
| theowalcott | 72 | 45 | +16.8% | 1.66 | yes |
| HVAB | 339 | 204 | -3.2% | -0.59 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 282 | 147 | +6.5% | 1.18 | no |
| Talvez10 | 110 | 90 | +46.7% | 6.52 | yes |
| BunCaCham | 49 | 45 | +29.7% | 3.56 | yes |
| 0010001000001100 | 160 | 77 | +0.8% | -0.22 | no |
| totoro3miyazaki | 49 | 31 | +8.7% | 0.68 | no |
| 1l2ihj34li12u34 | 92 | 53 | +13.4% | 1.55 | yes |
| yabanci | 62 | 41 | +12.1% | 1.37 | yes |
| 0x20D6436849F930584892730C7F | 126 | 70 | +28.3% | 1.74 | yes |
| juice-fruit | 48 | 32 | +9.0% | 0.79 | yes |
| 0x16bb9951a36fce71e2ef57890b | 56 | 23 | +1.0% | 0.01 | yes |
| GamblingOdyssey | 389 | 185 | +1.2% | 0.41 | no |
| plonker2026 | 132 | 76 | +12.6% | 1.76 | yes |
| xxyx0xx | 279 | 139 | +7.2% | 0.68 | yes |
| monkeymashingkeyboard | 799 | 438 | +10.6% | 2.67 | yes |
| Tiger105 | 40 | 26 | +20.4% | 1.37 | yes |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 464 | 284 | +5.5% | 1.3 | yes |
| UNEB3154s4f251 | 2198 | 1395 | +2.9% | 1.71 | no |
