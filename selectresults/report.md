# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-21 09:00 UTC: 5708 candidates, 3746 with trades copytop could copy, 238 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2429 | 1366 | $23,423 | -705.88 | -3.0% | -1.46 |
| every wallet that qualified on the first part (test window) | 3306 | 1802 | $32,255 | -1,541.15 | -4.8% | -2.54 |
| currently copied (test window) | 3315 | 1673 | $32,361 | -1,234.14 | -3.8% | -1.70 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2429 | 1366 | $23,423 | -705.88 | -3.0% | -1.46 | 3992 | 2335 | $38,516 | +2,315.04 | +6.0% | 3.84 |
| copy their sells too | 2429 | 1295 | $23,423 | -917.17 | -3.9% | -2.02 | 3992 | 2164 | $38,516 | +1,553.73 | +4.0% | 2.87 |
| size by conviction (x0.5 / x1 / x1.5) | 2306 | 1301 | $27,537 | -852.30 | -3.1% | -1.5 | 3787 | 2214 | $46,095 | +2,669.24 | +5.8% | 3.51 |
| skip bets under 0.5x their usual | 2401 | 1353 | $23,165 | -667.64 | -2.9% | -1.4 | 3923 | 2302 | $37,912 | +2,362.58 | +6.2% | 3.84 |
| pre-game only | 1275 | 657 | $12,081 | -236.08 | -1.9% | -0.63 | 2389 | 1335 | $22,695 | +1,815.11 | +8.0% | 4.08 |
| skip prices under 30c | 2289 | 1345 | $22,022 | -322.79 | -1.5% | -0.72 | 3679 | 2262 | $35,384 | +2,090.39 | +5.9% | 4.15 |
| favorites only (50c+) | 1701 | 1072 | $16,314 | -746.11 | -4.6% | -2.47 | 2486 | 1658 | $23,824 | +311.52 | +1.3% | 0.92 |
| 15s delay | 2533 | 1454 | $24,424 | -520.39 | -2.1% | -1.08 | 4109 | 2428 | $39,643 | +2,266.97 | +5.7% | 3.77 |
| 60s delay | 2429 | 1366 | $23,423 | -705.88 | -3.0% | -1.46 | 3992 | 2335 | $38,516 | +2,315.04 | +6.0% | 3.84 |
| allow 2c over their price | 2577 | 1468 | $24,858 | -670.64 | -2.7% | -1.31 | 4186 | 2466 | $40,395 | +2,310.61 | +5.7% | 3.81 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 148 | +20.1% | 2.9 | 160 | +0.3% | -0.28 |
| conviction:1-2x | 193 | +35.5% | 3.36 | 865 | -4.2% | -1.3 |
| conviction:2x+ | 1077 | +17.2% | 5.11 | 1282 | -2.9% | -0.99 |
| conviction:under 0.5x | 145 | +20.2% | 2.6 | 122 | +0.3% | 0.25 |
| delay_move:flat | 1065 | +22.4% | 6.53 | 1336 | -0.0% | -0.06 |
| delay_move:price fell | 498 | +15.0% | 3.1 | 1093 | -6.5% | -2.1 |
| exit:settle | 1563 | +20.0% | 7.15 | 2429 | -3.0% | -1.46 |
| kind:moneyline | 1040 | +18.3% | 5.05 | 1468 | +0.5% | 0.28 |
| kind:result | 298 | +25.9% | 4.67 | 407 | -3.4% | -0.63 |
| kind:totals | 225 | +20.2% | 2.96 | 554 | -11.9% | -3.19 |
| league:acle | 1 | +73.1% | — | 15 | -100.0% | — |
| league:atp | 159 | +14.7% | 2.02 | 396 | +5.0% | 1.0 |
| league:bel1 | 2 | +18.2% | 0.17 | 13 | +20.9% | 0.73 |
| league:bra | 13 | +54.1% | 2.46 | 31 | -1.2% | -0.03 |
| league:bun | 7 | +87.0% | 2.42 | 14 | -22.0% | -1.16 |
| league:cbb | 0 | +0.0% | — | 12 | -9.0% | -0.39 |
| league:cfb | 114 | -4.2% | -0.22 | 62 | +0.1% | -0.1 |
| league:cs2 | 214 | +26.1% | 3.61 | 115 | -5.7% | -0.57 |
| league:dota2 | 56 | +25.5% | 1.53 | 110 | -12.2% | -1.44 |
| league:epl | 36 | +60.1% | 3.36 | 48 | +1.4% | -0.05 |
| league:ere | 25 | +96.3% | 4.55 | 58 | +10.7% | 0.73 |
| league:lal | 27 | -13.2% | -0.85 | 54 | -17.4% | -1.52 |
| league:mls | 149 | +12.5% | 1.47 | 96 | -10.4% | -1.19 |
| league:nba | 63 | -3.3% | -0.31 | 822 | -4.3% | -1.19 |
| league:nfl | 196 | +39.4% | 3.04 | 64 | +11.2% | 0.95 |
| league:nhl | 137 | +26.9% | 3.74 | 123 | -2.9% | -0.35 |
| league:sea | 55 | +27.7% | 2.42 | 104 | +8.2% | 1.4 |
| league:ucl | 79 | +2.4% | 0.54 | 41 | +8.9% | 0.23 |
| league:uel | 17 | +61.4% | 3.33 | 35 | -20.3% | -1.16 |
| league:wta | 204 | +2.2% | 0.53 | 210 | -4.9% | -0.5 |
| price:30-70c | 1178 | +19.8% | 7.17 | 1795 | -2.4% | -0.99 |
| price:over 70c | 206 | +5.9% | 2.08 | 489 | -0.5% | -0.11 |
| price:under 30c | 179 | +37.0% | 2.41 | 145 | -18.6% | -1.24 |
| timing:in-play | 449 | +21.6% | 3.38 | 1154 | -4.1% | -1.48 |
| timing:pre-game | 1114 | +19.3% | 6.46 | 1275 | -1.9% | -0.63 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 135635 | 71469 | $1,343,763 | -53,219.71 | -4.0% | -12.66 |
| consistency (winning weeks), top 16 | 5605 | 2937 | $56,125 | -2,151.12 | -3.8% | -2.17 |
| consistency (winning weeks), top 40 | 21161 | 10980 | $211,420 | -8,332.06 | -3.9% | -4.78 |
| copy return, average, top 16 | 5203 | 2893 | $51,083 | -1,274.25 | -2.5% | -1.49 |
| copy return, average, top 40 | 17262 | 9083 | $170,796 | -6,778.21 | -4.0% | -4.46 |
| copy return, lower bound, top 16 | 8076 | 4417 | $78,985 | -2,696.29 | -3.4% | -2.87 |
| copy return, lower bound, top 40 | 22143 | 12397 | $218,839 | -9,095.55 | -4.2% | -5.71 |
| copy return, shrunk, top 16 | 5866 | 3177 | $57,512 | -2,165.15 | -3.8% | -2.54 |
| copy return, shrunk, top 40 | 17908 | 9461 | $177,247 | -6,753.91 | -3.8% | -4.39 |
| markout 2h, average, top 16 | 4397 | 2548 | $43,862 | -709.65 | -1.6% | -0.86 |
| markout 2h, average, top 40 | 14870 | 8065 | $146,621 | -4,826.25 | -3.3% | -3.35 |
| markout 2h, lower bound, top 16 | 4956 | 2746 | $49,580 | -1,427.50 | -2.9% | -1.69 |
| markout 2h, lower bound, top 40 | 19748 | 10724 | $195,417 | -7,005.06 | -3.6% | -4.31 |
| markout 30m, average, top 16 | 5632 | 3057 | $56,521 | -1,144.64 | -2.0% | -1.28 |
| markout 30m, average, top 40 | 19824 | 11133 | $197,788 | -4,369.56 | -2.2% | -2.65 |
| most active, top 16 | 27030 | 14639 | $267,302 | -12,751.71 | -4.8% | -7.03 |
| most active, top 40 | 45745 | 24161 | $452,129 | -20,335.21 | -4.5% | -8.51 |
| win rate vs the odds, top 16 | 5019 | 2870 | $48,927 | -437.01 | -0.9% | -0.66 |
| win rate vs the odds, top 40 | 15730 | 8317 | $155,826 | -6,810.02 | -4.4% | -4.49 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 35 | 30 | +55.8% | 3.79 | +5.50 |
| Kch-Temp | 184 | 107 | +15.1% | 1.97 | +1.63 |
| l..messi | 387 | 189 | +11.6% | 1.31 | +1.14 |
| NS13 | 1150 | 449 | -1.4% | -0.34 | -0.18 |
| yabanci | 127 | 74 | +11.2% | 1.03 | +1.22 |
| cosmicsteaks | 559 | 273 | +8.1% | 1.22 | +0.81 |
| strawberrycreek | 981 | 583 | +10.7% | 3.22 | +1.01 |
| Car-c | 1115 | 581 | +5.2% | 1.07 | +0.50 |
| seeyouanymore | 450 | 229 | -3.4% | -0.43 | -0.33 |
| whosay | 595 | 319 | -4.4% | -1.0 | -0.45 |
| KaneAnalytics | 183 | 99 | +5.2% | 0.48 | +0.51 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 830 | 376 | +5.7% | 0.91 | +0.52 |
| 0xE16D3F2A5807999b358aFfD944 | 596 | 335 | -1.7% | -0.63 | -0.25 |
| pltrkr111 | 976 | 550 | +5.2% | 1.48 | +0.52 |
| arahbo | 830 | 328 | +7.8% | 1.22 | +0.77 |
| carelia | 1209 | 579 | -2.3% | -0.7 | -0.24 |
| Lisanal-Gaib | 471 | 274 | +1.0% | 0.17 | +0.08 |
| skywalkerxx | 876 | 329 | -9.0% | -1.83 | -0.91 |
| yoooogo | 602 | 334 | -2.3% | -0.47 | -0.20 |
| timurdrevoz | 494 | 241 | +2.5% | 0.36 | +0.22 |
| anontrader11 | 522 | 296 | +4.9% | 1.0 | +0.50 |
| User7429 | 930 | 498 | -0.5% | -0.14 | -0.05 |
| latvian.demon | 477 | 273 | +2.5% | 0.52 | +0.23 |
| TearsInTheRain | 568 | 380 | +1.5% | 0.41 | +0.15 |
| 0x567212c82AAa6fe589bE5A2f4C | 411 | 215 | -0.3% | 0.35 | +0.24 |
| redvinny | 504 | 398 | +4.0% | 1.45 | +0.39 |
| 0xB8B95F31906f509d2a73eFF3d0 | 364 | 190 | +0.9% | 0.21 | +0.10 |
| rossoftw | 627 | 320 | +2.3% | 0.42 | +0.21 |
| 0xf9B5e9803Ea977b7111c9B7728 | 532 | 216 | +1.2% | 0.24 | +0.17 |
| Bimboslaff | 594 | 284 | -1.3% | -0.23 | -0.12 |
| Kkunn | 920 | 386 | +1.4% | 0.5 | +0.24 |
| TRCM | 2140 | 1098 | -5.5% | -1.97 | -0.54 |
| WagerWizard | 470 | 290 | +1.1% | 0.24 | +0.12 |
| LonnieHawkinss | 227 | 148 | +6.6% | 0.83 | +0.63 |
| juice-fruit | 72 | 47 | +4.3% | 0.52 | +0.54 |
| Petal | 844 | 420 | -2.0% | -0.52 | -0.21 |
| 0x5fD2D9C60781D711721145Ff2b | 709 | 389 | -4.8% | -1.05 | -0.46 |
| chrysos | 526 | 275 | -5.2% | -1.21 | -0.51 |
| dfdeath | 2059 | 1050 | -1.7% | -0.59 | -0.17 |
| plonker2026 | 155 | 86 | +13.7% | 1.8 | +1.64 |

## Esports specialists (copies on esports markets only)

3087 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 159 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| oxbus | leaderboard | 42 | 24 | +96.3% | 2.8 | +18.1% (16) | +143.7% (26) | yes |
| Tomahawkmaster | leaderboard | 12 | 5 | +86.1% | 1.23 | +0.0% (0) | +86.1% (12) | no |
| Manchester4ever | tag | 151 | 98 | +15.4% | 2.11 | +19.4% (107) | +5.8% (44) | yes |
| CUTJALENHURTS | tag | 43 | 26 | +27.7% | 1.45 | +36.5% (32) | +3.6% (11) | no |
| anontrader11 | tag | 184 | 107 | +15.7% | 1.87 | +81.1% (43) | -3.9% (141) | yes |
| Diabolical-Prize | current | 183 | 104 | +12.9% | 1.88 | +12.9% (183) | +0.0% (0) | no |
| redvinny | tag | 55 | 50 | +12.8% | 2.2 | +1.9% (32) | +28.0% (23) | yes |
| hydra1248 | tag | 51 | 43 | +11.8% | 1.61 | +0.0% (0) | +11.8% (51) | yes |
| THEHIGHLIFE | tag | 117 | 61 | +14.2% | 1.31 | +14.3% (98) | +13.9% (19) | no |
| growzizi | tag | 118 | 75 | +12.9% | 1.25 | +19.8% (57) | +6.6% (61) | yes |
| sara341 | tag | 104 | 49 | +18.1% | 1.1 | +33.0% (31) | +11.8% (73) | yes |
| juice-fruit | current | 31 | 21 | +17.4% | 1.08 | +28.5% (25) | -26.7% (6) | yes |
| arahbo | tag | 206 | 110 | +10.3% | 1.08 | +3.8% (141) | +24.3% (65) | yes |
| igot50k | tag | 235 | 126 | +11.5% | 1.03 | +14.3% (215) | -18.5% (20) | no |
| 0x5974813b27CdE970e736AE3b55 | tag | 117 | 81 | +7.1% | 1.01 | +4.2% (102) | +27.1% (15) | yes |
| returdmaxxer | tag | 304 | 279 | +1.3% | 0.73 | +3.4% (218) | -3.8% (86) | yes |
| asdfasdf333 | tag | 377 | 240 | +3.6% | 0.87 | +3.6% (377) | +0.0% (0) | no |
| manvsrice42 | tag | 55 | 32 | +12.4% | 0.89 | +16.4% (35) | +5.5% (20) | yes |
| superlxj | tag | 144 | 98 | +4.7% | 0.74 | +4.7% (144) | +0.0% (0) | no |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 243 | 129 | +4.3% | 0.71 | +9.2% (206) | -22.2% (37) | no |
| swaz13131313 | tag | 70 | 60 | +2.8% | 0.56 | +0.0% (0) | +2.8% (70) | yes |
| dfdeath | tag | 1114 | 578 | +1.8% | 0.44 | +2.7% (576) | +0.9% (538) | yes |
| 0xf9B5e9803Ea977b7111c9B7728 | tag | 280 | 144 | +4.0% | 0.68 | +21.4% (92) | -4.7% (188) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 12 | 7 | +39.8% | 0.94 | +39.8% (12) | +0.0% (0) | no |
| carelia | tag | 127 | 76 | +6.4% | 0.72 | +8.6% (86) | +1.6% (41) | yes |
| chux.cc | tag | 164 | 120 | +3.1% | 0.5 | +2.0% (139) | +8.8% (25) | no |
| 0x6bfC64cb52307DeE90011412C6 | tag | 75 | 50 | +6.8% | 0.69 | +23.7% (11) | +3.9% (64) | yes |
| .d-.-b. | tag | 40 | 21 | +19.3% | 0.86 | -28.0% (9) | +32.8% (31) | yes |
| Zzzz87 | tag | 106 | 71 | +5.9% | 0.67 | -11.4% (63) | +31.0% (43) | yes |
| vardaman-bundren | tag | 209 | 102 | +5.7% | 0.64 | +7.2% (150) | +1.8% (59) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 551 | 242 | -5.9% | -0.95 | no |
| Kch-Temp | 184 | 107 | +15.1% | 1.97 | yes |
| EdZachary | 155 | 56 | -16.5% | -1.67 | no |
| KaneAnalytics | 183 | 99 | +5.2% | 0.48 | yes |
| Jsram | 96 | 61 | +9.7% | 1.21 | no |
| Kkunn | 920 | 386 | +1.4% | 0.5 | yes |
| Sisyphus- | 138 | 76 | -3.4% | -0.37 | no |
| PEYZ-BIGGEST-FAN | 295 | 146 | -8.8% | -1.3 | no |
| theowalcott | 98 | 54 | +4.5% | 0.61 | no |
| HVAB | 411 | 253 | -1.3% | -0.27 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 241 | 133 | +15.3% | 2.36 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 35 | 30 | +55.8% | 3.79 | yes |
| 0010001000001100 | 245 | 119 | -1.0% | -0.31 | no |
| totoro3miyazaki | 50 | 31 | +6.5% | 0.52 | no |
| 1l2ihj34li12u34 | 147 | 79 | +5.6% | 1.0 | no |
| yabanci | 127 | 74 | +11.2% | 1.03 | yes |
| 0x20D6436849F930584892730C7F | 123 | 70 | +31.4% | 1.89 | no |
| juice-fruit | 72 | 47 | +4.3% | 0.52 | yes |
| 0x16bb9951a36fce71e2ef57890b | 69 | 24 | -16.0% | -1.14 | no |
| GamblingOdyssey | 318 | 178 | +4.0% | 0.88 | no |
| plonker2026 | 155 | 86 | +13.7% | 1.8 | yes |
| xxyx0xx | 244 | 118 | -6.0% | -0.68 | no |
| monkeymashingkeyboard | 1128 | 585 | +1.2% | 0.39 | no |
| Tiger105 | 43 | 27 | +15.2% | 1.05 | no |
| THEHIGHLIFE | 152 | 72 | +3.1% | 0.34 | no |
| AmericaFirst1 | 444 | 238 | -0.2% | -0.04 | no |
| UNEB3154s4f251 | 2174 | 1354 | +2.0% | 1.21 | no |
