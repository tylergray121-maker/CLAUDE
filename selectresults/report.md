# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-22 09:00 UTC: 5746 candidates, 3784 with trades copytop could copy, 242 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 668 | 347 | $6,626 | -214.40 | -3.2% | -0.71 |
| every wallet that qualified on the first part (test window) | 1215 | 624 | $12,133 | -686.40 | -5.7% | -1.65 |
| currently copied (test window) | 3353 | 1688 | $32,804 | -949.70 | -2.9% | -1.19 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 668 | 347 | $6,626 | -214.40 | -3.2% | -0.71 | 1698 | 1010 | $16,642 | +2,078.73 | +12.5% | 4.96 |
| copy their sells too | 668 | 296 | $6,626 | -360.96 | -5.5% | -1.33 | 1698 | 872 | $16,642 | +1,557.80 | +9.4% | 4.18 |
| size by conviction (x0.5 / x1 / x1.5) | 657 | 339 | $8,621 | -311.18 | -3.6% | -0.88 | 1654 | 969 | $21,250 | +2,224.20 | +10.5% | 4.17 |
| skip bets under 0.5x their usual | 647 | 336 | $6,421 | -207.08 | -3.2% | -0.71 | 1645 | 982 | $16,155 | +2,034.34 | +12.6% | 4.86 |
| pre-game only | 479 | 246 | $4,729 | -123.16 | -2.6% | -0.51 | 1220 | 722 | $11,856 | +1,566.63 | +13.2% | 5.1 |
| skip prices under 30c | 630 | 340 | $6,228 | -239.00 | -3.8% | -0.95 | 1555 | 974 | $15,176 | +1,745.34 | +11.5% | 5.36 |
| favorites only (50c+) | 365 | 231 | $3,587 | -9.69 | -0.3% | -0.04 | 867 | 614 | $8,400 | +714.48 | +8.5% | 3.58 |
| 15s delay | 672 | 353 | $6,667 | -207.79 | -3.1% | -0.72 | 1704 | 1018 | $16,699 | +1,995.18 | +11.9% | 4.94 |
| 60s delay | 668 | 347 | $6,626 | -214.40 | -3.2% | -0.71 | 1698 | 1010 | $16,642 | +2,078.73 | +12.5% | 4.96 |
| allow 2c over their price | 699 | 364 | $6,940 | -225.54 | -3.2% | -0.73 | 1760 | 1044 | $17,263 | +2,003.13 | +11.6% | 4.76 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 87 | +31.6% | 3.29 | 46 | -16.0% | -1.5 |
| conviction:1-2x | 79 | +50.9% | 3.06 | 51 | +6.0% | 0.36 |
| conviction:2x+ | 744 | +19.0% | 4.86 | 495 | -2.6% | -0.41 |
| conviction:under 0.5x | 120 | +22.7% | 2.67 | 76 | -6.2% | -0.34 |
| delay_move:flat | 705 | +27.6% | 6.67 | 436 | +1.0% | 0.28 |
| delay_move:price fell | 325 | +13.1% | 2.31 | 232 | -11.2% | -1.31 |
| exit:settle | 1030 | +22.9% | 6.85 | 668 | -3.2% | -0.71 |
| kind:moneyline | 543 | +26.1% | 5.08 | 178 | -0.3% | -0.09 |
| kind:result | 281 | +20.0% | 3.88 | 236 | +3.0% | 0.54 |
| kind:totals | 206 | +18.6% | 2.62 | 254 | -11.0% | -1.8 |
| league:acle | 1 | +73.1% | — | 15 | -100.0% | — |
| league:atp | 70 | +22.6% | 2.16 | 31 | +28.2% | 1.49 |
| league:bel1 | 2 | +18.2% | 0.17 | 17 | -7.8% | -0.31 |
| league:bra | 12 | +51.3% | 2.17 | 22 | -26.1% | -1.34 |
| league:bun | 7 | +87.0% | 2.42 | 5 | +86.1% | — |
| league:cfb | 86 | +3.0% | 0.33 | 9 | +64.4% | 1.8 |
| league:cs2 | 183 | +15.4% | 2.26 | 21 | -5.9% | -0.22 |
| league:dota2 | 37 | +7.0% | 0.46 | 3 | -2.6% | -0.02 |
| league:epl | 31 | +56.5% | 2.76 | 50 | +2.0% | -0.02 |
| league:ere | 25 | +96.3% | 4.55 | 45 | +16.4% | 0.97 |
| league:lal | 27 | -13.2% | -0.85 | 45 | +1.3% | 0.12 |
| league:mls | 148 | +12.5% | 1.46 | 61 | -25.9% | -2.36 |
| league:nba | 26 | -7.0% | -0.2 | 158 | -9.3% | -1.08 |
| league:nfl | 74 | +63.8% | 2.49 | 12 | +4.0% | 0.12 |
| league:nhl | 122 | +40.1% | 6.17 | 58 | -4.5% | -0.23 |
| league:sea | 56 | +28.8% | 2.53 | 44 | +1.7% | 0.35 |
| league:ucl | 78 | +2.3% | 0.53 | 41 | +8.9% | 0.23 |
| league:uel | 20 | +47.2% | 2.51 | 12 | +43.2% | 1.75 |
| league:wta | 24 | -16.1% | -0.78 | 17 | -1.9% | -0.08 |
| price:30-70c | 768 | +25.1% | 7.67 | 539 | -5.0% | -1.09 |
| price:over 70c | 153 | +5.7% | 1.71 | 91 | +3.3% | 0.66 |
| price:under 30c | 109 | +30.6% | 1.47 | 38 | +6.2% | 0.14 |
| timing:in-play | 289 | +20.9% | 2.47 | 189 | -4.8% | -0.49 |
| timing:pre-game | 741 | +23.7% | 6.91 | 479 | -2.6% | -0.51 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 133048 | 69942 | $1,318,944 | -50,070.06 | -3.8% | -11.90 |
| consistency (winning weeks), top 16 | 6286 | 3197 | $62,846 | -3,679.92 | -5.9% | -3.86 |
| consistency (winning weeks), top 40 | 19457 | 10554 | $193,780 | -6,140.89 | -3.2% | -3.75 |
| copy return, average, top 16 | 3500 | 1752 | $34,719 | -1,210.86 | -3.5% | -1.48 |
| copy return, average, top 40 | 17714 | 8916 | $175,772 | -7,803.88 | -4.4% | -4.96 |
| copy return, lower bound, top 16 | 5428 | 2905 | $53,612 | -2,065.74 | -3.9% | -2.46 |
| copy return, lower bound, top 40 | 21047 | 11640 | $208,413 | -8,764.95 | -4.2% | -5.64 |
| copy return, shrunk, top 16 | 4074 | 2042 | $40,314 | -1,769.34 | -4.4% | -2.17 |
| copy return, shrunk, top 40 | 18312 | 9169 | $181,866 | -8,095.89 | -4.5% | -5.03 |
| markout 2h, average, top 16 | 4633 | 2716 | $46,180 | -901.08 | -1.9% | -0.96 |
| markout 2h, average, top 40 | 14417 | 7700 | $144,053 | -2,902.48 | -2.0% | -1.90 |
| markout 2h, lower bound, top 16 | 6027 | 3418 | $60,137 | -1,640.20 | -2.7% | -1.79 |
| markout 2h, lower bound, top 40 | 19293 | 10492 | $192,245 | -5,320.80 | -2.8% | -3.27 |
| markout 30m, average, top 16 | 4776 | 2740 | $47,756 | +426.79 | +0.9% | +0.41 |
| markout 30m, average, top 40 | 19507 | 10840 | $194,586 | -5,055.82 | -2.6% | -3.05 |
| most active, top 16 | 23803 | 12655 | $235,764 | -12,770.95 | -5.4% | -7.29 |
| most active, top 40 | 43098 | 22584 | $426,744 | -20,794.80 | -4.9% | -8.84 |
| win rate vs the odds, top 16 | 4024 | 2108 | $39,568 | -842.09 | -2.1% | -1.10 |
| win rate vs the odds, top 40 | 15926 | 8381 | $157,801 | -5,126.32 | -3.2% | -3.29 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 36 | 30 | +51.5% | 3.44 | +5.07 |
| Kch-Temp | 184 | 107 | +15.1% | 1.97 | +1.63 |
| l..messi | 379 | 182 | +10.3% | 1.15 | +1.02 |
| NS13 | 1150 | 449 | -1.4% | -0.34 | -0.18 |
| strawberrycreek | 1032 | 623 | +12.2% | 3.82 | +1.16 |
| cosmicsteaks | 570 | 279 | +8.6% | 1.29 | +0.85 |
| Maizuqiu | 479 | 235 | +12.6% | 1.6 | +1.22 |
| 1l2ihj34li12u34 | 167 | 95 | +10.4% | 1.69 | +1.31 |
| KaneAnalytics | 185 | 101 | +6.9% | 0.63 | +0.67 |
| Car-c | 1094 | 563 | +4.9% | 0.98 | +0.47 |
| pltrkr111 | 968 | 546 | +5.0% | 1.42 | +0.50 |
| whosay | 603 | 326 | -2.8% | -0.63 | -0.29 |
| yabanci | 136 | 76 | +6.2% | 0.65 | +0.73 |
| Lisanal-Gaib | 480 | 281 | +1.8% | 0.32 | +0.15 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 774 | 349 | +5.8% | 0.87 | +0.52 |
| User7429 | 928 | 499 | +0.9% | 0.19 | +0.08 |
| 0xf9B5e9803Ea977b7111c9B7728 | 540 | 221 | +1.4% | 0.26 | +0.18 |
| carelia | 1217 | 583 | -2.5% | -0.76 | -0.26 |
| arahbo | 857 | 339 | +7.5% | 1.21 | +0.74 |
| juice-fruit | 73 | 48 | +5.4% | 0.63 | +0.64 |
| 0xE16D3F2A5807999b358aFfD944 | 613 | 343 | -2.0% | -0.71 | -0.28 |
| anontrader11 | 537 | 305 | +4.5% | 0.93 | +0.46 |
| redvinny | 518 | 408 | +3.9% | 1.43 | +0.38 |
| timurdrevoz | 507 | 248 | +1.5% | 0.22 | +0.13 |
| 0x567212c82AAa6fe589bE5A2f4C | 417 | 218 | -0.9% | 0.27 | +0.18 |
| WagerWizard | 444 | 282 | +4.1% | 0.79 | +0.41 |
| latvian.demon | 495 | 284 | +2.2% | 0.45 | +0.19 |
| TearsInTheRain | 558 | 372 | +1.3% | 0.36 | +0.14 |
| Bimboslaff | 601 | 285 | -1.4% | -0.25 | -0.13 |
| vardaman-bundren | 430 | 206 | +1.2% | 0.21 | +0.12 |
| OVER955 | 654 | 584 | +1.8% | 0.98 | +0.17 |
| dfdeath | 2126 | 1086 | -1.2% | -0.44 | -0.12 |
| 0xB8B95F31906f509d2a73eFF3d0 | 368 | 190 | -0.1% | -0.02 | -0.01 |
| rossoftw | 686 | 348 | +2.2% | 0.44 | +0.21 |
| _test_i075_CAND_11b7 | 591 | 351 | +1.6% | 0.32 | +0.14 |
| nibbio3 | 363 | 152 | +3.0% | 0.34 | +0.29 |
| TRCM | 2124 | 1089 | -6.5% | -2.32 | -0.63 |
| 0x5fD2D9C60781D711721145Ff2b | 707 | 389 | -4.5% | -0.98 | -0.44 |
| LonnieHawkinss | 233 | 151 | +6.1% | 0.78 | +0.59 |
| Petal | 804 | 402 | -1.6% | -0.41 | -0.17 |

## Esports specialists (copies on esports markets only)

3124 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 162 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| Tomahawkmaster | leaderboard | 12 | 5 | +86.1% | 1.23 | +0.0% (0) | +86.1% (12) | yes |
| CUTJALENHURTS | tag | 43 | 26 | +27.7% | 1.45 | +36.5% (32) | +3.6% (11) | no |
| Diabolical-Prize | current | 183 | 104 | +12.9% | 1.88 | +12.9% (183) | +0.0% (0) | no |
| Manchester4ever | tag | 153 | 98 | +13.8% | 1.92 | +19.4% (107) | +1.1% (46) | yes |
| anontrader11 | tag | 198 | 116 | +14.4% | 1.83 | +58.6% (53) | -1.5% (145) | yes |
| OVER955 | tag | 120 | 115 | +8.4% | 3.77 | +8.1% (96) | +9.6% (24) | yes |
| GoingStraightAhead | tag | 82 | 50 | +23.2% | 1.32 | +31.0% (51) | +10.2% (31) | yes |
| growzizi | tag | 120 | 77 | +13.9% | 1.36 | +17.6% (61) | +10.1% (59) | yes |
| THEHIGHLIFE | tag | 117 | 61 | +14.2% | 1.31 | +14.3% (98) | +13.9% (19) | no |
| redvinny | tag | 59 | 52 | +8.9% | 1.49 | +1.9% (32) | +17.2% (27) | yes |
| sara341 | tag | 104 | 49 | +18.1% | 1.1 | +47.7% (36) | +2.4% (68) | yes |
| juice-fruit | current | 31 | 21 | +17.4% | 1.08 | +28.5% (25) | -26.7% (6) | yes |
| .d-.-b. | tag | 42 | 23 | +21.9% | 1.03 | -35.3% (10) | +39.6% (32) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 118 | 82 | +7.4% | 1.06 | +5.8% (105) | +20.4% (13) | yes |
| returdmaxxer | tag | 307 | 282 | +1.4% | 0.79 | +3.4% (218) | -3.3% (89) | yes |
| arahbo | tag | 210 | 111 | +8.8% | 0.95 | +3.8% (141) | +19.1% (69) | yes |
| asdfasdf333 | tag | 373 | 238 | +3.6% | 0.86 | +3.6% (373) | +0.0% (0) | no |
| swaz13131313 | tag | 72 | 62 | +3.4% | 0.68 | +0.0% (0) | +3.4% (72) | yes |
| superlxj | tag | 144 | 98 | +4.7% | 0.74 | +4.7% (144) | +0.0% (0) | no |
| igot50k | tag | 233 | 124 | +9.3% | 0.83 | +11.9% (213) | -18.5% (20) | no |
| 0xf9B5e9803Ea977b7111c9B7728 | tag | 288 | 149 | +4.2% | 0.73 | +20.6% (94) | -3.9% (194) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 79 | 53 | +7.5% | 0.79 | +3.6% (15) | +8.4% (64) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 243 | 129 | +4.3% | 0.71 | +9.8% (207) | -26.6% (36) | no |
| Zzzz87 | tag | 107 | 72 | +6.5% | 0.74 | -11.4% (63) | +31.9% (44) | yes |
| vardaman-bundren | tag | 211 | 104 | +6.3% | 0.72 | +7.0% (152) | +4.4% (59) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 12 | 7 | +39.8% | 0.94 | +39.8% (12) | +0.0% (0) | no |
| chux.cc | leaderboard | 164 | 120 | +3.1% | 0.5 | +2.0% (139) | +8.8% (25) | no |
| manvsrice42 | tag | 54 | 31 | +11.3% | 0.81 | +14.8% (34) | +5.5% (20) | yes |
| dfdeath | tag | 1150 | 594 | +1.2% | 0.28 | +2.4% (597) | -0.2% (553) | yes |
| latvian.demon | tag | 94 | 55 | +6.8% | 0.67 | +7.9% (62) | +4.4% (32) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 623 | 270 | -5.1% | -0.85 | no |
| Kch-Temp | 184 | 107 | +15.1% | 1.97 | yes |
| EdZachary | 156 | 57 | -13.9% | -1.41 | no |
| KaneAnalytics | 185 | 101 | +6.9% | 0.63 | yes |
| Jsram | 96 | 61 | +9.7% | 1.21 | no |
| Kkunn | 920 | 386 | +1.4% | 0.5 | no |
| Sisyphus- | 140 | 77 | -3.5% | -0.39 | no |
| PEYZ-BIGGEST-FAN | 298 | 146 | -9.8% | -1.47 | no |
| theowalcott | 95 | 51 | -0.3% | 0.16 | no |
| HVAB | 409 | 251 | -1.2% | -0.27 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 241 | 133 | +15.3% | 2.36 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 36 | 30 | +51.5% | 3.44 | yes |
| 0010001000001100 | 245 | 119 | -1.0% | -0.31 | no |
| totoro3miyazaki | 50 | 31 | +6.5% | 0.52 | no |
| 1l2ihj34li12u34 | 167 | 95 | +10.4% | 1.69 | yes |
| yabanci | 136 | 76 | +6.2% | 0.65 | yes |
| 0x20D6436849F930584892730C7F | 123 | 70 | +31.4% | 1.89 | no |
| juice-fruit | 73 | 48 | +5.4% | 0.63 | yes |
| 0x16bb9951a36fce71e2ef57890b | 73 | 25 | -17.5% | -1.28 | no |
| GamblingOdyssey | 323 | 180 | +2.9% | 0.71 | no |
| plonker2026 | 160 | 86 | +10.0% | 1.43 | no |
| xxyx0xx | 243 | 117 | -6.1% | -0.69 | no |
| monkeymashingkeyboard | 1134 | 589 | +1.3% | 0.45 | no |
| Tiger105 | 41 | 27 | +20.8% | 1.42 | no |
| THEHIGHLIFE | 146 | 66 | -0.2% | -0.06 | no |
| AmericaFirst1 | 483 | 250 | +0.7% | 0.12 | no |
| UNEB3154s4f251 | 2124 | 1321 | +1.9% | 1.15 | no |
