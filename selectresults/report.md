# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-15 09:00 UTC: 5602 candidates, 3655 with trades copytop could copy, 235 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 692 | 389 | $6,706 | +280.86 | +4.2% | +0.89 |
| every wallet that qualified on the first part (test window) | 3259 | 1833 | $32,447 | -414.60 | -1.3% | -0.68 |
| currently copied (test window) | 3750 | 1930 | $36,662 | -700.99 | -1.9% | -0.84 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 692 | 389 | $6,706 | +280.86 | +4.2% | 0.89 | 1931 | 1131 | $18,518 | +2,041.43 | +11.0% | 4.85 |
| copy their sells too | 692 | 368 | $6,706 | +94.62 | +1.4% | 0.26 | 1931 | 1082 | $18,518 | +1,664.30 | +9.0% | 4.11 |
| size by conviction (x0.5 / x1 / x1.5) | 658 | 369 | $8,092 | +233.42 | +2.9% | 0.97 | 1812 | 1051 | $21,922 | +1,988.11 | +9.1% | 4.21 |
| skip bets under 0.5x their usual | 661 | 370 | $6,409 | +169.66 | +2.6% | 0.5 | 1851 | 1083 | $17,849 | +1,772.67 | +9.9% | 4.33 |
| pre-game only | 619 | 347 | $5,964 | +2.52 | +0.0% | -0.05 | 1728 | 1014 | $16,474 | +1,697.14 | +10.3% | 4.66 |
| skip prices under 30c | 664 | 382 | $6,423 | +129.75 | +2.0% | 0.52 | 1797 | 1104 | $17,177 | +2,075.13 | +12.1% | 5.84 |
| favorites only (50c+) | 420 | 297 | $4,031 | +611.63 | +15.2% | 4.12 | 990 | 708 | $9,440 | +1,356.94 | +14.4% | 6.24 |
| 15s delay | 694 | 391 | $6,724 | +286.16 | +4.3% | 0.91 | 1939 | 1138 | $18,593 | +2,053.79 | +11.1% | 4.88 |
| 60s delay | 692 | 389 | $6,706 | +280.86 | +4.2% | 0.89 | 1931 | 1131 | $18,518 | +2,041.43 | +11.0% | 4.85 |
| allow 2c over their price | 707 | 394 | $6,859 | +210.97 | +3.1% | 0.65 | 1979 | 1154 | $19,001 | +1,952.51 | +10.3% | 4.62 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 149 | +14.0% | 2.0 | 75 | -3.1% | -0.82 |
| conviction:1-2x | 135 | +27.5% | 2.96 | 77 | -2.8% | -0.14 |
| conviction:2x+ | 793 | +11.7% | 3.61 | 458 | +2.3% | 0.45 |
| conviction:under 0.5x | 162 | +20.9% | 2.43 | 82 | +26.7% | 2.06 |
| delay_move:flat | 953 | +16.7% | 5.23 | 505 | +3.9% | 0.71 |
| delay_move:price fell | 286 | +9.1% | 1.8 | 187 | +4.9% | 0.56 |
| exit:settle | 1239 | +14.9% | 5.45 | 692 | +4.2% | 0.89 |
| kind:moneyline | 802 | +15.1% | 4.23 | 474 | +7.3% | 1.3 |
| kind:result | 109 | +37.3% | 3.92 | 34 | +8.3% | 0.55 |
| kind:totals | 328 | +7.1% | 1.7 | 184 | -4.4% | -0.77 |
| league:atp | 78 | +25.6% | 2.34 | 33 | -2.4% | -0.14 |
| league:cfb | 81 | -7.2% | -0.42 | 15 | +89.7% | 1.91 |
| league:cs2 | 176 | +10.8% | 1.63 | 6 | +2.7% | 0.08 |
| league:dota2 | 54 | +2.7% | 0.09 | 7 | -82.3% | -5.15 |
| league:epl | 69 | +18.9% | 2.04 | 59 | +9.2% | 0.31 |
| league:lal | 6 | +10.4% | 0.32 | 5 | -75.9% | -3.01 |
| league:nba | 0 | +0.0% | — | 132 | -6.7% | -0.61 |
| league:nfl | 79 | +32.6% | 1.95 | 14 | +116.1% | 1.12 |
| league:nhl | 561 | +12.0% | 3.07 | 348 | +5.6% | 1.26 |
| league:sea | 26 | +10.7% | 0.76 | 7 | +40.8% | 0.89 |
| league:ucl | 66 | +28.8% | 3.37 | 23 | -46.3% | -3.39 |
| league:unl | 20 | +86.9% | 2.72 | 6 | -3.2% | -0.08 |
| league:wta | 15 | -15.2% | -0.44 | 25 | +3.1% | 0.15 |
| price:30-70c | 1031 | +18.6% | 6.53 | 612 | +0.4% | 0.05 |
| price:over 70c | 98 | +10.4% | 2.65 | 52 | +21.6% | 5.05 |
| price:under 30c | 110 | -14.0% | -0.88 | 28 | +53.4% | 0.8 |
| timing:in-play | 130 | +5.1% | 0.53 | 73 | +37.5% | 1.56 |
| timing:pre-game | 1109 | +16.1% | 5.65 | 619 | +0.0% | -0.05 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 125554 | 65790 | $1,243,917 | -50,290.66 | -4.0% | -12.23 |
| consistency (winning weeks), top 16 | 8138 | 4386 | $80,956 | -2,634.18 | -3.2% | -2.21 |
| consistency (winning weeks), top 40 | 19624 | 10263 | $195,350 | -8,554.26 | -4.4% | -5.14 |
| copy return, average, top 16 | 4329 | 2044 | $42,962 | -1,598.56 | -3.7% | -1.79 |
| copy return, average, top 40 | 18442 | 9105 | $182,529 | -8,397.44 | -4.6% | -5.02 |
| copy return, lower bound, top 16 | 7541 | 3763 | $74,624 | -4,515.54 | -6.0% | -4.44 |
| copy return, lower bound, top 40 | 20563 | 11223 | $203,778 | -8,840.57 | -4.3% | -5.56 |
| copy return, shrunk, top 16 | 5575 | 2665 | $55,260 | -2,304.55 | -4.2% | -2.34 |
| copy return, shrunk, top 40 | 18869 | 9291 | $186,828 | -8,798.36 | -4.7% | -5.19 |
| markout 2h, average, top 16 | 5519 | 2850 | $55,420 | -627.44 | -1.1% | -0.49 |
| markout 2h, average, top 40 | 17409 | 9218 | $173,858 | -6,618.52 | -3.8% | -4.04 |
| markout 2h, lower bound, top 16 | 6386 | 3500 | $63,670 | -666.88 | -1.1% | -0.61 |
| markout 2h, lower bound, top 40 | 19132 | 10412 | $190,727 | -7,245.57 | -3.8% | -4.47 |
| markout 30m, average, top 16 | 6777 | 3808 | $67,842 | -684.79 | -1.0% | -0.60 |
| markout 30m, average, top 40 | 19876 | 10905 | $198,668 | -6,818.46 | -3.4% | -4.07 |
| most active, top 16 | 20126 | 10916 | $198,267 | -6,753.85 | -3.4% | -4.14 |
| most active, top 40 | 43754 | 23662 | $431,325 | -17,741.15 | -4.1% | -7.58 |
| win rate vs the odds, top 16 | 3200 | 1581 | $31,492 | -1,648.61 | -5.2% | -2.30 |
| win rate vs the odds, top 40 | 18256 | 9125 | $182,045 | -7,551.46 | -4.2% | -4.40 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 38 | 33 | +52.9% | 3.84 | +5.18 |
| l..messi | 321 | 162 | +24.4% | 2.14 | +2.37 |
| Kch-Temp | 178 | 102 | +13.1% | 1.72 | +1.46 |
| yoooogo | 520 | 294 | +0.1% | 0.09 | +0.04 |
| Car-c | 1185 | 627 | +5.7% | 1.26 | +0.55 |
| 0xE16D3F2A5807999b358aFfD944 | 603 | 334 | -3.1% | -0.96 | -0.38 |
| Lisanal-Gaib | 475 | 273 | +0.2% | -0.01 | -0.00 |
| NS13 | 1174 | 464 | -1.2% | -0.25 | -0.13 |
| Wiretransferxyz | 552 | 325 | -1.3% | -0.2 | -0.07 |
| nightcity2077 | 478 | 234 | +1.7% | 0.26 | +0.18 |
| yabanci | 104 | 57 | +7.8% | 0.65 | +0.91 |
| 1l2ihj34li12u34 | 122 | 68 | +10.4% | 1.4 | +1.30 |
| seeyouanymore | 362 | 188 | -3.8% | -0.43 | -0.37 |
| darkumbreon88 | 2648 | 1747 | +2.6% | 1.44 | +0.25 |
| arahbo | 766 | 306 | +6.7% | 1.04 | +0.66 |
| nibbio3 | 336 | 148 | +6.9% | 0.7 | +0.68 |
| Kuntro2 | 471 | 167 | -3.9% | -0.53 | -0.40 |
| juice-fruit | 61 | 41 | +5.6% | 0.61 | +0.67 |
| carelia | 1276 | 580 | -5.2% | -1.53 | -0.53 |
| Manchester4ever | 1026 | 591 | +4.0% | 1.3 | +0.40 |
| anontrader11 | 470 | 262 | +4.9% | 0.91 | +0.49 |
| cocococococo | 819 | 458 | +3.5% | 1.29 | +0.44 |
| TearsInTheRain | 530 | 354 | +0.7% | 0.2 | +0.07 |
| trapfive | 547 | 222 | +1.8% | 0.26 | +0.16 |
| cosmicsteaks | 515 | 247 | +4.5% | 0.65 | +0.45 |
| 0x16bb9951a36fce71e2ef57890b | 69 | 24 | -16.0% | -1.14 | -1.66 |
| Kkunn | 920 | 386 | +1.4% | 0.5 | +0.24 |
| shiifoo | 367 | 151 | -3.0% | -0.45 | -0.32 |
| timurdrevoz | 476 | 235 | +3.3% | 0.48 | +0.31 |
| walnutz | 414 | 217 | +0.8% | 0.06 | +0.03 |
| monkeymashingkeyboard | 1026 | 540 | +2.8% | 0.9 | +0.30 |
| pltrkr111 | 940 | 525 | +4.9% | 1.34 | +0.48 |
| KaneAnalytics | 178 | 96 | +5.8% | 0.52 | +0.57 |
| skywalkerxx | 837 | 312 | -10.8% | -2.17 | -1.09 |
| User7429 | 864 | 454 | -3.2% | -0.82 | -0.33 |
| 0x567212c82AAa6fe589bE5A2f4C | 392 | 203 | -0.3% | 0.36 | +0.26 |
| Zzzz87 | 1207 | 677 | +0.0% | 0.23 | +0.07 |
| smithagent | 1472 | 803 | +2.4% | 0.61 | +0.25 |
| F-812 | 735 | 405 | -0.1% | -0.04 | -0.02 |
| 0x842c81e145739b68a20192c619 | 522 | 279 | +1.7% | 0.38 | +0.18 |

## Esports specialists (copies on esports markets only)

2980 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 160 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| oxbus | leaderboard | 52 | 29 | +79.1% | 2.62 | -0.7% (23) | +137.1% (29) | yes |
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 19 | 12 | +55.9% | 2.02 | +55.8% (7) | +56.0% (12) | yes |
| Tomahawkmaster | leaderboard | 12 | 5 | +86.1% | 1.23 | +0.0% (0) | +86.1% (12) | yes |
| manvsrice42 | tag | 62 | 38 | +25.5% | 1.79 | +32.3% (45) | +7.3% (17) | yes |
| anontrader11 | tag | 158 | 91 | +17.4% | 1.87 | +66.8% (17) | +11.2% (141) | yes |
| Diabolical-Prize | current | 183 | 104 | +12.9% | 1.88 | +12.9% (183) | +0.0% (0) | no |
| Manchester4ever | tag | 159 | 101 | +13.1% | 1.83 | +14.1% (116) | +10.6% (43) | yes |
| 0x765e6a480ae3f05c3f2e6c50f4 | tag | 45 | 25 | +29.8% | 1.14 | +0.0% (0) | +29.8% (45) | yes |
| CUTJALENHURTS | tag | 60 | 35 | +17.6% | 1.19 | +19.2% (47) | +12.1% (13) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +24.0% (23) | +2.7% (6) | no |
| nightcity2077 | tag | 80 | 43 | +22.9% | 1.09 | +27.9% (76) | -72.5% (4) | no |
| sara341 | tag | 92 | 43 | +19.4% | 1.09 | +29.4% (14) | +17.5% (78) | yes |
| igot50k | tag | 286 | 154 | +10.3% | 1.08 | +11.7% (255) | -1.4% (31) | no |
| carelia | tag | 105 | 64 | +10.8% | 1.07 | +9.0% (73) | +15.0% (32) | yes |
| nibbio3 | tag | 66 | 33 | +20.3% | 1.01 | +14.5% (32) | +25.8% (34) | yes |
| arahbo | tag | 210 | 111 | +9.7% | 1.02 | -0.4% (143) | +31.0% (67) | yes |
| returdmaxxer | tag | 276 | 255 | +1.7% | 0.92 | +3.4% (218) | -4.6% (58) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 68 | 46 | +8.6% | 0.84 | +0.0% (0) | +8.6% (68) | yes |
| superlxj | tag | 144 | 98 | +4.7% | 0.74 | +5.6% (139) | -21.3% (5) | no |
| forsenxd | tag | 351 | 194 | +4.2% | 0.69 | -0.2% (317) | +45.4% (34) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 12 | 7 | +39.8% | 0.94 | +39.8% (12) | +0.0% (0) | no |
| swaz13131313 | tag | 63 | 54 | +2.6% | 0.49 | +0.0% (0) | +2.6% (63) | yes |
| chux.cc | tag | 164 | 120 | +3.1% | 0.5 | +4.6% (132) | -3.3% (32) | yes |
| NS13 | leaderboard | 215 | 93 | +11.4% | 0.76 | -10.5% (159) | +75.2% (56) | yes |
| dfdeath | tag | 1031 | 537 | +0.6% | 0.15 | +2.9% (478) | -1.5% (553) | yes |
| BOB6633 | tag | 329 | 190 | +1.6% | 0.32 | +6.0% (244) | -10.9% (85) | no |
| ZTMZqClEsjMmwCDWXoG | tag | 412 | 237 | +1.0% | 0.23 | -4.4% (344) | +28.2% (68) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 136 | 75 | +5.7% | 0.61 | +33.2% (11) | +3.2% (125) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 248 | 129 | +2.2% | 0.42 | +8.9% (205) | -29.3% (43) | yes |
| vardaman-bundren | tag | 203 | 100 | +4.2% | 0.48 | +3.8% (137) | +4.8% (66) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 511 | 223 | -7.8% | -1.48 | no |
| Kch-Temp | 178 | 102 | +13.1% | 1.72 | yes |
| EdZachary | 147 | 56 | -12.0% | -1.17 | no |
| KaneAnalytics | 178 | 96 | +5.8% | 0.52 | yes |
| Jsram | 105 | 68 | +11.6% | 1.48 | no |
| Kkunn | 920 | 386 | +1.4% | 0.5 | yes |
| Sisyphus- | 132 | 73 | -3.0% | -0.33 | no |
| PEYZ-BIGGEST-FAN | 273 | 135 | -8.7% | -1.25 | no |
| theowalcott | 13 | 11 | +63.3% | 2.93 | no |
| HVAB | 379 | 231 | -4.1% | -0.89 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 242 | 133 | +14.8% | 2.3 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 38 | 33 | +52.9% | 3.84 | yes |
| 0010001000001100 | 310 | 149 | -1.1% | -0.31 | no |
| totoro3miyazaki | 54 | 31 | -1.5% | -0.09 | no |
| 1l2ihj34li12u34 | 122 | 68 | +10.4% | 1.4 | yes |
| yabanci | 104 | 57 | +7.8% | 0.65 | yes |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | no |
| juice-fruit | 61 | 41 | +5.6% | 0.61 | yes |
| 0x16bb9951a36fce71e2ef57890b | 69 | 24 | -16.0% | -1.14 | yes |
| GamblingOdyssey | 314 | 176 | +6.1% | 1.16 | no |
| plonker2026 | 117 | 62 | +3.1% | 0.5 | no |
| xxyx0xx | 281 | 131 | +3.9% | 0.26 | no |
| monkeymashingkeyboard | 1026 | 540 | +2.8% | 0.9 | yes |
| Tiger105 | 39 | 27 | +25.9% | 1.81 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 448 | 251 | +0.9% | 0.2 | no |
| UNEB3154s4f251 | 2157 | 1356 | +1.8% | 1.08 | no |
