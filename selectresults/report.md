# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-08 15:00 UTC: 5657 candidates, 3925 with trades copytop could copy, 220 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3114 | 1590 | $30,678 | +1,126.77 | +3.7% | +1.53 |
| every wallet that qualified on the first part (test window) | 3960 | 2075 | $39,111 | +1,107.14 | +2.8% | +1.31 |
| currently copied (test window) | 3740 | 1970 | $36,622 | +1,096.33 | +3.0% | +1.75 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3114 | 1590 | $30,678 | +1,126.77 | +3.7% | 1.53 | 6710 | 3482 | $65,783 | +6,580.64 | +10.0% | 5.97 |
| copy their sells too | 3114 | 1571 | $30,678 | +889.84 | +2.9% | 1.21 | 6710 | 3450 | $65,783 | +6,223.09 | +9.5% | 5.67 |
| size by conviction (x0.5 / x1 / x1.5) | 3019 | 1538 | $34,525 | +1,604.98 | +4.7% | 1.43 | 6449 | 3334 | $76,060 | +7,321.88 | +9.6% | 5.49 |
| skip bets under 0.5x their usual | 2754 | 1448 | $27,188 | +1,403.54 | +5.2% | 2.12 | 6135 | 3222 | $60,402 | +6,260.71 | +10.4% | 6.02 |
| pre-game only | 1315 | 699 | $12,987 | +1,232.37 | +9.5% | 3.11 | 4060 | 2172 | $39,506 | +6,018.58 | +15.2% | 7.48 |
| skip prices under 30c | 2482 | 1438 | $24,394 | +225.20 | +0.9% | 0.43 | 5298 | 3095 | $51,728 | +2,189.90 | +4.2% | 3.35 |
| favorites only (50c+) | 1485 | 1020 | $14,482 | +110.00 | +0.8% | 0.58 | 2910 | 2045 | $28,155 | +1,166.41 | +4.1% | 3.41 |
| 15s delay | 3388 | 1775 | $33,333 | +1,646.80 | +4.9% | 2.46 | 7091 | 3725 | $69,497 | +7,144.51 | +10.3% | 6.53 |
| 60s delay | 3114 | 1590 | $30,678 | +1,126.77 | +3.7% | 1.53 | 6710 | 3482 | $65,783 | +6,580.64 | +10.0% | 5.97 |
| allow 2c over their price | 3398 | 1744 | $33,446 | +1,278.98 | +3.8% | 1.67 | 7241 | 3762 | $70,970 | +6,750.76 | +9.5% | 5.91 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 449 | +25.6% | 3.69 | 437 | +4.3% | 0.46 |
| conviction:1-2x | 614 | +13.3% | 2.32 | 508 | +3.6% | 0.56 |
| conviction:2x+ | 2118 | +12.4% | 4.01 | 1616 | +7.3% | 2.45 |
| conviction:under 0.5x | 415 | +24.8% | 3.37 | 553 | -7.4% | -1.25 |
| delay_move:flat | 2137 | +15.3% | 4.87 | 1413 | +9.8% | 2.9 |
| delay_move:price fell | 1459 | +15.9% | 4.39 | 1701 | -1.4% | -0.62 |
| exit:settle | 3596 | +15.5% | 6.54 | 3114 | +3.7% | 1.53 |
| kind:moneyline | 2720 | +12.1% | 4.2 | 2336 | +2.3% | 0.77 |
| kind:result | 773 | +25.1% | 5.59 | 380 | +4.7% | 0.92 |
| kind:totals | 103 | +33.7% | 4.48 | 398 | +10.6% | 1.53 |
| league:atp | 863 | +11.4% | 2.38 | 1237 | +3.0% | 0.59 |
| league:bel1 | 0 | +0.0% | — | 15 | +9.2% | 0.33 |
| league:bun | 9 | +80.1% | 2.93 | 4 | -100.0% | — |
| league:cbb | 0 | +0.0% | — | 28 | -54.4% | -3.23 |
| league:cfb | 10 | -49.8% | -1.47 | 49 | +12.1% | 0.64 |
| league:cs2 | 349 | +11.8% | 1.64 | 152 | +14.7% | 1.16 |
| league:dota2 | 120 | -10.0% | -0.96 | 83 | +19.3% | 1.04 |
| league:epl | 54 | +35.2% | 3.23 | 141 | +7.9% | 0.61 |
| league:ere | 8 | +106.7% | 28.83 | 78 | +16.0% | 0.85 |
| league:lal | 22 | +26.1% | 1.67 | 91 | +4.2% | 0.34 |
| league:lol | 1623 | +19.1% | 4.85 | 125 | +27.0% | 2.08 |
| league:nba | 9 | -19.5% | -0.5 | 211 | +3.7% | 0.83 |
| league:nfl | 47 | +28.6% | 1.47 | 12 | +81.4% | 2.8 |
| league:nhl | 69 | +33.4% | 4.06 | 73 | +13.5% | 1.39 |
| league:sea | 39 | +59.6% | 3.86 | 232 | -1.6% | 0.0 |
| league:unl | 40 | +40.5% | 1.89 | 0 | +0.0% | — |
| league:wta | 332 | +4.3% | 0.64 | 581 | -6.0% | -1.45 |
| price:30-70c | 2338 | +7.7% | 3.81 | 1943 | +2.1% | 0.86 |
| price:over 70c | 470 | +3.7% | 1.72 | 520 | -3.4% | -1.68 |
| price:under 30c | 788 | +44.9% | 5.17 | 651 | +13.7% | 1.63 |
| timing:in-play | 851 | +7.8% | 1.35 | 1799 | -0.6% | -0.46 |
| timing:pre-game | 2745 | +18.1% | 6.87 | 1315 | +9.5% | 3.11 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 128033 | 67080 | $1,270,740 | -46,449.50 | -3.7% | -11.06 |
| consistency (winning weeks), top 16 | 7345 | 3722 | $73,511 | -2,717.95 | -3.7% | -2.57 |
| consistency (winning weeks), top 40 | 23033 | 12066 | $228,869 | -8,412.37 | -3.7% | -4.85 |
| copy return, average, top 16 | 7214 | 3391 | $71,205 | -2,772.18 | -3.9% | -2.57 |
| copy return, average, top 40 | 21659 | 11080 | $214,207 | -5,542.32 | -2.6% | -3.32 |
| copy return, lower bound, top 16 | 7753 | 3790 | $76,536 | -2,323.27 | -3.0% | -2.22 |
| copy return, lower bound, top 40 | 24476 | 12749 | $242,230 | -8,825.21 | -3.6% | -4.87 |
| copy return, shrunk, top 16 | 7786 | 3651 | $76,878 | -3,373.90 | -4.4% | -3.02 |
| copy return, shrunk, top 40 | 20898 | 10515 | $206,836 | -5,268.65 | -2.5% | -3.14 |
| markout 2h, average, top 16 | 10653 | 5798 | $105,857 | -4,237.33 | -4.0% | -3.63 |
| markout 2h, average, top 40 | 22367 | 11999 | $222,433 | -8,945.07 | -4.0% | -5.10 |
| markout 2h, lower bound, top 16 | 11527 | 6049 | $114,557 | -4,993.62 | -4.4% | -3.92 |
| markout 2h, lower bound, top 40 | 25526 | 13606 | $253,679 | -10,515.27 | -4.2% | -5.89 |
| markout 30m, average, top 16 | 9271 | 5145 | $92,654 | -2,536.77 | -2.7% | -2.24 |
| markout 30m, average, top 40 | 23320 | 12662 | $232,533 | -5,567.38 | -2.4% | -3.13 |
| most active, top 16 | 20883 | 11254 | $207,198 | -6,396.53 | -3.1% | -3.84 |
| most active, top 40 | 36800 | 19533 | $365,027 | -13,471.13 | -3.7% | -5.93 |
| win rate vs the odds, top 16 | 4217 | 2313 | $41,905 | -1,168.29 | -2.8% | -1.46 |
| win rate vs the odds, top 40 | 19937 | 10475 | $198,225 | -6,259.57 | -3.2% | -3.76 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 52 | 48 | +45.2% | 4.53 | +4.40 |
| xxyx0xx | 274 | 135 | +23.0% | 1.59 | +2.16 |
| am100 | 763 | 488 | +22.8% | 5.43 | +2.30 |
| 1l2ihj34li12u34 | 83 | 52 | +24.0% | 2.38 | +2.59 |
| Kch-Temp | 156 | 85 | +7.8% | 0.97 | +0.89 |
| juice-fruit | 48 | 32 | +11.9% | 0.98 | +1.28 |
| 0x16bb9951a36fce71e2ef57890b | 63 | 24 | -7.9% | -0.55 | -0.86 |
| SimpleTony | 1065 | 345 | +12.1% | 2.14 | +1.23 |
| oxbus | 1404 | 704 | -3.8% | -1.26 | -0.39 |
| cash-bundren | 385 | 154 | -4.1% | -0.61 | -0.40 |
| moreplatesmoredates | 935 | 471 | +3.6% | 1.01 | +0.44 |
| carelia | 1676 | 780 | -3.1% | -1.06 | -0.32 |
| monkeymashingkeyboard | 929 | 497 | +7.4% | 2.03 | +0.73 |
| Future-Tarot-Trader | 1701 | 861 | -0.5% | -0.26 | -0.09 |
| Manchester4ever | 1031 | 599 | +3.3% | 1.07 | +0.32 |
| plonker2026 | 119 | 67 | +20.0% | 1.89 | +2.17 |
| 0x8g68hBa8tyH1946Bhjb674g3fu | 1315 | 728 | +0.5% | 0.19 | +0.06 |
| 0x5fD2D9C60781D711721145Ff2b | 697 | 386 | +5.5% | 0.92 | +0.51 |
| pltrkr111 | 1156 | 661 | +12.9% | 3.42 | +1.26 |
| igot50k | 1569 | 983 | -0.7% | -0.29 | -0.08 |
| flatbarrel | 1522 | 765 | -7.2% | -2.16 | -0.71 |
| ludo-money | 844 | 475 | -2.0% | -0.55 | -0.20 |
| yuxkc0 | 344 | 116 | -7.4% | -0.9 | -0.73 |
| zuihouyici | 614 | 317 | -0.1% | -0.06 | -0.03 |
| Car-c | 774 | 389 | +2.9% | 0.52 | +0.28 |
| 636763 | 1421 | 452 | +1.1% | 0.36 | +0.19 |
| 239393828 | 532 | 258 | -1.6% | -0.34 | -0.18 |
| nightcity2077 | 714 | 338 | +1.3% | 0.23 | +0.13 |
| CUTJALENHURTS | 1182 | 673 | +0.3% | 0.1 | +0.03 |
| 0010001000001100 | 146 | 77 | +8.5% | 0.64 | +0.86 |
| trapfive | 803 | 346 | -1.7% | -0.37 | -0.18 |
| Popeyesfriedchicken | 658 | 360 | -3.4% | -0.61 | -0.34 |
| capitalpiston2 | 2028 | 945 | +0.6% | 0.19 | +0.05 |
| GamblingOdyssey | 350 | 180 | +7.9% | 1.45 | +0.92 |
| AmericaFirst1 | 504 | 297 | +3.5% | 0.88 | +0.38 |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | +0.58 |
| smithagent | 1188 | 650 | +1.4% | 0.36 | +0.15 |
| torta.tech | 1068 | 638 | -1.5% | -0.47 | -0.14 |
| 0x709179E7392e59922Ab2D73cb1 | 3204 | 1573 | -1.4% | -0.58 | -0.13 |
| JAMJAMJAM4 | 1680 | 890 | -1.5% | -0.43 | -0.11 |

## Esports specialists (copies on esports markets only)

3023 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 167 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +48.6% (76) | +0.0% (0) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +30.4% (253) | +57.3% (24) | yes |
| am100 | tag | 763 | 488 | +22.8% | 5.43 | +21.8% (739) | +52.2% (24) | yes |
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 21 | 13 | +52.4% | 1.53 | +55.8% (7) | +50.7% (14) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 291 | 176 | +25.3% | 2.65 | +21.2% (256) | +56.2% (35) | no |
| BunCaCham | tag | 18 | 18 | +14.4% | 7.11 | +14.7% (11) | +13.9% (7) | no |
| 0x5fD2D9C60781D711721145Ff2b | tag | 25 | 15 | +54.2% | 1.23 | +97.8% (14) | -1.1% (11) | no |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1142 | 621 | +11.6% | 3.22 | +11.7% (1070) | +11.2% (72) | yes |
| CUTJALENHURTS | tag | 150 | 85 | +19.3% | 1.78 | +18.8% (119) | +21.3% (31) | yes |
| SimpleTony | tag | 1056 | 341 | +12.0% | 2.11 | +9.8% (784) | +18.4% (272) | yes |
| -5rud | tag | 501 | 345 | +8.6% | 2.04 | +8.2% (419) | +10.7% (82) | yes |
| MIracle33 | tag | 447 | 227 | +9.3% | 1.62 | +9.2% (389) | +9.6% (58) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +5.9% (17) | +37.4% (12) | no |
| ccwcc | tag | 328 | 169 | +11.7% | 1.3 | +12.4% (311) | -1.8% (17) | yes |
| TAIWANNUMBERONE | tag | 842 | 463 | +5.9% | 1.6 | +1.8% (794) | +72.4% (48) | yes |
| Manchester4ever | tag | 251 | 153 | +8.3% | 1.38 | +5.6% (205) | +20.4% (46) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 114 | 64 | +13.4% | 1.18 | +44.6% (9) | +10.7% (105) | yes |
| ZEST011 | tag | 563 | 422 | +3.4% | 1.18 | +3.8% (497) | +0.4% (66) | no |
| littlebay | tag | 110 | 78 | +9.3% | 1.05 | +7.0% (79) | +14.8% (31) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 562 | 294 | +4.0% | 1.04 | +7.5% (362) | -2.5% (200) | yes |
| RensPeters | tag | 109 | 65 | +9.8% | 1.01 | +8.0% (95) | +22.7% (14) | no |
| moreplatesmoredates | tag | 935 | 471 | +3.6% | 1.01 | +0.4% (668) | +11.7% (267) | yes |
| carelia | tag | 202 | 117 | +8.3% | 0.97 | +6.8% (169) | +16.0% (33) | yes |
| ZTMZqClEsjMmwCDWXoG | tag | 1027 | 597 | +2.5% | 0.75 | +2.1% (924) | +6.5% (103) | yes |
| GC-C | tag | 778 | 546 | +1.9% | 0.69 | -2.1% (617) | +17.0% (161) | yes |
| shaw | tag | 197 | 124 | +5.2% | 0.82 | +7.3% (146) | -0.9% (51) | yes |
| AmericaFirst1 | tag | 283 | 181 | +3.1% | 0.71 | +6.3% (234) | -12.4% (49) | yes |
| returdmaxxer | tag | 314 | 285 | -0.1% | -0.04 | +0.6% (271) | -4.2% (43) | yes |
| 636763 | tag | 1390 | 444 | +2.2% | 0.57 | +0.1% (1093) | +10.2% (297) | yes |
| smartcombo | tag | 294 | 174 | +4.1% | 0.63 | +3.7% (289) | +32.3% (5) | no |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 397 | 171 | -9.3% | -1.63 | no |
| Kch-Temp | 156 | 85 | +7.8% | 0.97 | yes |
| EdZachary | 116 | 46 | -3.0% | -0.27 | no |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | yes |
| Jsram | 71 | 42 | +4.8% | 0.37 | no |
| Kkunn | 868 | 364 | +1.7% | 0.56 | no |
| Sisyphus- | 128 | 70 | -3.9% | -0.42 | no |
| PEYZ-BIGGEST-FAN | 385 | 193 | -1.4% | -0.14 | no |
| theowalcott | — | — | — | — | no copyable trades |
| HVAB | 362 | 220 | -0.4% | -0.1 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +5.3% | 1.01 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 52 | 48 | +45.2% | 4.53 | yes |
| 0010001000001100 | 146 | 77 | +8.5% | 0.64 | yes |
| totoro3miyazaki | 45 | 30 | +14.8% | 1.07 | no |
| 1l2ihj34li12u34 | 83 | 52 | +24.0% | 2.38 | yes |
| yabanci | 81 | 46 | -3.5% | -0.06 | no |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 48 | 32 | +11.9% | 0.98 | yes |
| 0x16bb9951a36fce71e2ef57890b | 63 | 24 | -7.9% | -0.55 | yes |
| GamblingOdyssey | 350 | 180 | +7.9% | 1.45 | yes |
| plonker2026 | 119 | 67 | +20.0% | 1.89 | yes |
| xxyx0xx | 274 | 135 | +23.0% | 1.59 | yes |
| monkeymashingkeyboard | 929 | 497 | +7.4% | 2.03 | yes |
| Tiger105 | 36 | 25 | +26.1% | 1.75 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 504 | 297 | +3.5% | 0.88 | yes |
| UNEB3154s4f251 | 2077 | 1295 | +1.8% | 1.1 | no |
