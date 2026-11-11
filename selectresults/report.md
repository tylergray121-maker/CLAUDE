# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-11 09:00 UTC: 5647 candidates, 3894 with trades copytop could copy, 220 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3983 | 2021 | $39,327 | -791.17 | -2.0% | -1.01 |
| every wallet that qualified on the first part (test window) | 5427 | 2769 | $53,863 | -995.01 | -1.8% | -1.14 |
| currently copied (test window) | 3189 | 1658 | $31,117 | +196.94 | +0.6% | +0.56 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3983 | 2021 | $39,327 | -791.17 | -2.0% | -1.01 | 7797 | 4058 | $77,083 | +3,173.05 | +4.1% | 2.73 |
| copy their sells too | 3983 | 2018 | $39,327 | -824.02 | -2.1% | -1.05 | 7797 | 4049 | $77,083 | +3,067.63 | +4.0% | 2.64 |
| size by conviction (x0.5 / x1 / x1.5) | 3898 | 1977 | $43,939 | -599.80 | -1.4% | -1.04 | 7628 | 3977 | $88,469 | +3,414.90 | +3.9% | 2.6 |
| skip bets under 0.5x their usual | 3472 | 1826 | $34,338 | -210.14 | -0.6% | -0.28 | 7093 | 3756 | $70,245 | +3,189.79 | +4.5% | 3.02 |
| pre-game only | 1513 | 804 | $15,014 | +485.62 | +3.2% | 1.47 | 4471 | 2425 | $44,129 | +3,715.75 | +8.4% | 4.82 |
| skip prices under 30c | 3196 | 1869 | $31,427 | -524.64 | -1.7% | -1.07 | 6300 | 3710 | $62,033 | +882.50 | +1.4% | 1.25 |
| favorites only (50c+) | 2075 | 1430 | $20,239 | +71.99 | +0.4% | 0.35 | 4018 | 2768 | $39,273 | +1,164.01 | +3.0% | 2.92 |
| 15s delay | 4347 | 2241 | $42,853 | -836.20 | -1.9% | -0.6 | 8282 | 4348 | $81,805 | +3,278.60 | +4.0% | 3.04 |
| 60s delay | 3983 | 2021 | $39,327 | -791.17 | -2.0% | -1.01 | 7797 | 4058 | $77,083 | +3,173.05 | +4.1% | 2.73 |
| allow 2c over their price | 4328 | 2196 | $42,689 | -827.93 | -1.9% | -0.95 | 8387 | 4358 | $82,879 | +3,146.52 | +3.8% | 2.63 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 857 | +17.7% | 4.28 | 680 | +0.1% | -0.13 |
| conviction:1-2x | 784 | +7.2% | 1.92 | 661 | +0.0% | -0.15 |
| conviction:2x+ | 1888 | +6.7% | 2.04 | 1914 | -0.2% | 0.06 |
| conviction:under 0.5x | 285 | +22.9% | 2.17 | 728 | -10.5% | -1.87 |
| delay_move:flat | 1784 | +15.7% | 4.28 | 1339 | +1.5% | 0.63 |
| delay_move:price fell | 2030 | +6.0% | 2.31 | 2644 | -3.8% | -1.68 |
| exit:settle | 3814 | +10.5% | 4.79 | 3983 | -2.0% | -1.01 |
| kind:moneyline | 3319 | +10.3% | 4.32 | 3547 | -1.5% | -0.74 |
| kind:result | 446 | +12.4% | 2.0 | 177 | -22.7% | -2.47 |
| kind:totals | 49 | +9.2% | 0.81 | 259 | +5.2% | 0.85 |
| league:atp | 1705 | +9.2% | 3.24 | 2124 | -0.5% | -0.36 |
| league:bra | 66 | +42.0% | 2.22 | 85 | -52.8% | -6.32 |
| league:cbb | 0 | +0.0% | — | 54 | -11.3% | -0.39 |
| league:cfb | 7 | -27.6% | -0.61 | 50 | +9.7% | 0.53 |
| league:cs2 | 199 | +12.1% | 1.03 | 148 | +17.0% | 1.27 |
| league:dota2 | 81 | -15.5% | -1.11 | 83 | +17.9% | 0.96 |
| league:lol | 841 | +17.4% | 2.69 | 72 | +1.2% | 0.29 |
| league:nba | 19 | +10.5% | 0.37 | 382 | -1.7% | 0.02 |
| league:nfl | 1 | +29.3% | — | 18 | -39.6% | -1.35 |
| league:nhl | 83 | +27.8% | 3.22 | 79 | +8.3% | 0.9 |
| league:nwsl | 13 | -27.0% | -1.12 | 3 | +9.2% | 0.15 |
| league:unl | 65 | +9.4% | 1.16 | 0 | +0.0% | — |
| league:uslc | 14 | +28.4% | 1.24 | 4 | +29.7% | 0.71 |
| league:uwcl | 12 | -4.0% | -0.16 | 43 | +7.0% | 0.29 |
| league:wsl | 9 | -6.8% | -0.31 | 2 | +42.5% | 1.21 |
| league:wta | 684 | +4.5% | 1.2 | 834 | -7.8% | -2.36 |
| price:30-70c | 2327 | +4.8% | 2.36 | 2330 | -1.8% | -0.96 |
| price:over 70c | 772 | +3.5% | 2.25 | 839 | -0.2% | -0.17 |
| price:under 30c | 715 | +35.9% | 3.89 | 814 | -4.3% | -0.51 |
| timing:in-play | 856 | +8.5% | 1.47 | 2470 | -5.2% | -2.18 |
| timing:pre-game | 2958 | +11.1% | 4.79 | 1513 | +3.2% | 1.47 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 120355 | 62656 | $1,194,593 | -56,675.37 | -4.7% | -13.88 |
| consistency (winning weeks), top 16 | 9646 | 4964 | $96,010 | -5,221.06 | -5.4% | -4.56 |
| consistency (winning weeks), top 40 | 23859 | 12593 | $235,670 | -12,791.22 | -5.4% | -7.46 |
| copy return, average, top 16 | 7887 | 3835 | $78,203 | -3,402.05 | -4.3% | -2.92 |
| copy return, average, top 40 | 22468 | 10987 | $223,267 | -10,978.17 | -4.9% | -5.87 |
| copy return, lower bound, top 16 | 9490 | 4642 | $94,207 | -4,628.73 | -4.9% | -3.85 |
| copy return, lower bound, top 40 | 23670 | 12247 | $234,206 | -11,357.52 | -4.9% | -6.36 |
| copy return, shrunk, top 16 | 8794 | 4248 | $87,028 | -4,181.32 | -4.8% | -3.51 |
| copy return, shrunk, top 40 | 22993 | 11248 | $228,547 | -11,522.34 | -5.0% | -6.09 |
| markout 2h, average, top 16 | 9915 | 4988 | $98,801 | -5,252.67 | -5.3% | -4.14 |
| markout 2h, average, top 40 | 23901 | 12113 | $238,248 | -14,655.48 | -6.2% | -7.78 |
| markout 2h, lower bound, top 16 | 12131 | 6009 | $120,905 | -8,128.35 | -6.7% | -5.91 |
| markout 2h, lower bound, top 40 | 28528 | 14828 | $282,999 | -15,229.51 | -5.4% | -7.72 |
| markout 30m, average, top 16 | 6296 | 3273 | $63,197 | -3,981.77 | -6.3% | -4.32 |
| markout 30m, average, top 40 | 23465 | 12248 | $234,112 | -14,667.13 | -6.3% | -8.14 |
| most active, top 16 | 18498 | 9967 | $183,302 | -8,581.07 | -4.7% | -5.57 |
| most active, top 40 | 34519 | 18055 | $342,428 | -15,678.78 | -4.6% | -7.12 |
| win rate vs the odds, top 16 | 8591 | 4374 | $85,154 | -3,724.61 | -4.4% | -3.34 |
| win rate vs the odds, top 40 | 22546 | 11599 | $224,009 | -8,377.80 | -3.7% | -4.74 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| Kch-Temp | 134 | 71 | +4.5% | 0.53 | +0.54 |
| 0010001000001100 | 62 | 30 | +7.3% | 0.34 | +0.70 |
| cash-bundren | 392 | 158 | -3.0% | -0.46 | -0.30 |
| juice-fruit | 48 | 31 | +8.0% | 0.7 | +0.93 |
| 0x16bb9951a36fce71e2ef57890b | 63 | 23 | -11.2% | -0.76 | -1.19 |
| Future-Tarot-Trader | 1615 | 817 | -1.6% | -0.53 | -0.19 |
| moreplatesmoredates | 944 | 476 | +2.5% | 0.85 | +0.36 |
| monkeymashingkeyboard | 984 | 523 | +6.0% | 1.73 | +0.60 |
| 636763 | 1422 | 462 | +2.4% | 0.59 | +0.31 |
| oxbus | 1044 | 534 | -1.5% | -0.39 | -0.14 |
| Popeyesfriedchicken | 663 | 362 | -3.8% | -0.68 | -0.38 |
| yuxkc0 | 340 | 116 | -5.9% | -0.7 | -0.58 |
| horaciorolinha | 599 | 278 | -3.7% | -0.71 | -0.37 |
| trapfive | 765 | 329 | -1.1% | -0.24 | -0.12 |
| Bimboslaff | 516 | 246 | -0.6% | -0.07 | -0.04 |
| pltrkr111 | 1139 | 654 | +13.5% | 3.48 | +1.30 |
| 239393828 | 472 | 234 | +0.9% | 0.12 | +0.07 |
| carelia | 1510 | 697 | -4.2% | -1.36 | -0.43 |
| 0x5fD2D9C60781D711721145Ff2b | 697 | 389 | +6.1% | 1.03 | +0.57 |
| walnutz | 566 | 291 | -0.3% | -0.13 | -0.06 |
| SimpleTony | 1026 | 331 | +10.3% | 1.85 | +1.08 |
| oookkjjdd | 768 | 385 | -1.5% | -0.29 | -0.12 |
| TearsInTheRain | 586 | 394 | -0.7% | -0.17 | -0.06 |
| 0xA55c1539adF5640951DA735c2f | 585 | 293 | -0.7% | -0.18 | -0.09 |
| ludo-money | 780 | 437 | -2.0% | -0.5 | -0.19 |
| calvinoxieS | 666 | 299 | -4.2% | -0.88 | -0.41 |
| 0x8g68hBa8tyH1946Bhjb674g3fu | 1348 | 759 | +1.1% | 0.38 | +0.11 |
| flatbarrel | 1450 | 731 | -6.1% | -1.77 | -0.61 |
| -5rud | 959 | 640 | +1.6% | 0.65 | +0.18 |
| dewey-dell-bundren | 435 | 196 | -6.4% | -1.14 | -0.63 |
| cryptoqan0n | 1294 | 656 | +0.3% | 0.07 | +0.03 |
| sweetcaroline | 666 | 548 | -0.7% | -0.4 | -0.07 |
| yabanci | 81 | 46 | -2.8% | 0.01 | +0.01 |
| 0x1E3bB7DEf89B002D45FD86D37F | 2784 | 1627 | +0.1% | 0.02 | +0.00 |
| CUTJALENHURTS | 1146 | 640 | -1.4% | -0.51 | -0.16 |
| ahmerde | 556 | 338 | -2.2% | -0.02 | -0.01 |
| capitalpiston2 | 1621 | 727 | +0.9% | 0.26 | +0.09 |
| WeBuyHighWeSelllow | 1008 | 540 | -7.6% | -2.12 | -0.69 |
| szy10010 | 592 | 323 | -1.4% | -0.3 | -0.14 |
| NS13 | 1234 | 486 | -0.6% | 0.05 | +0.03 |

## Esports specialists (copies on esports markets only)

3009 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 170 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | current | 76 | 43 | +48.6% | 2.16 | +48.6% (76) | +0.0% (0) | no |
| pltrkr111 | tag | 284 | 160 | +29.8% | 2.95 | +34.1% (263) | -25.0% (21) | yes |
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 21 | 13 | +52.4% | 1.53 | +55.8% (7) | +50.7% (14) | no |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 290 | 176 | +25.7% | 2.69 | +24.7% (283) | +64.6% (7) | no |
| BunCaCham | tag | 19 | 19 | +17.4% | 4.91 | +14.7% (11) | +21.1% (8) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 30 | 18 | +45.4% | 1.21 | +75.9% (17) | +5.3% (13) | yes |
| SimpleTony | tag | 1026 | 331 | +10.3% | 1.85 | +7.6% (758) | +17.9% (268) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1097 | 585 | +7.9% | 2.3 | +8.5% (1026) | -0.8% (71) | yes |
| MIracle33 | tag | 440 | 223 | +8.5% | 1.48 | +9.5% (398) | -1.2% (42) | yes |
| -5rud | tag | 487 | 333 | +6.7% | 1.64 | +8.4% (414) | -3.1% (73) | yes |
| shaw | tag | 176 | 115 | +9.2% | 1.29 | +11.9% (125) | +2.6% (51) | yes |
| CUTJALENHURTS | tag | 151 | 81 | +13.5% | 1.17 | +15.1% (113) | +8.7% (38) | yes |
| 0x4dDC7068ef679Dc7c34e2c2241 | tag | 137 | 77 | +10.7% | 1.07 | +44.6% (9) | +8.3% (128) | yes |
| TAIWANNUMBERONE | tag | 808 | 438 | +4.4% | 1.13 | +1.2% (764) | +58.0% (44) | yes |
| vardaman-bundren | tag | 337 | 163 | +8.2% | 1.07 | +9.1% (261) | +5.1% (76) | yes |
| littlebay | tag | 110 | 78 | +9.3% | 1.05 | +7.9% (82) | +13.1% (28) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 546 | 288 | +4.2% | 1.07 | +9.5% (337) | -4.5% (209) | yes |
| ZEST011 | tag | 536 | 401 | +3.2% | 1.08 | +3.6% (471) | +0.3% (65) | no |
| ccwcc | tag | 325 | 163 | +9.1% | 1.0 | +10.8% (305) | -16.6% (20) | yes |
| carelia | tag | 202 | 117 | +8.3% | 0.97 | +7.0% (173) | +15.7% (29) | no |
| moreplatesmoredates | tag | 944 | 476 | +2.5% | 0.85 | -0.5% (666) | +9.8% (278) | yes |
| GC-C | tag | 776 | 545 | +2.1% | 0.74 | -2.1% (645) | +22.2% (131) | yes |
| juice-fruit | current | 30 | 20 | +15.2% | 0.94 | +12.5% (20) | +20.3% (10) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 59 | 40 | +9.9% | 0.89 | -23.5% (3) | +11.7% (56) | yes |
| Gagalabu2 | tag | 346 | 154 | +8.1% | 0.85 | -0.5% (249) | +30.2% (97) | no |
| ZTMZqClEsjMmwCDWXoG | tag | 1005 | 581 | +2.0% | 0.6 | +0.9% (914) | +13.7% (91) | yes |
| 636763 | tag | 1386 | 449 | +3.2% | 0.73 | +2.6% (1085) | +5.3% (301) | yes |
| RensPeters | tag | 109 | 64 | +8.1% | 0.83 | +9.9% (99) | -10.1% (10) | yes |
| returdmaxxer | tag | 325 | 295 | -0.1% | -0.06 | +0.8% (277) | -5.4% (48) | yes |
| 0xffAaEFb5f6762Cc70cb575Da87 | tag | 665 | 316 | +3.4% | 0.54 | +3.2% (614) | +5.2% (51) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 425 | 188 | -7.6% | -1.35 | no |
| Kch-Temp | 134 | 71 | +4.5% | 0.53 | yes |
| EdZachary | 134 | 50 | -10.4% | -0.94 | no |
| KaneAnalytics | 174 | 93 | +6.0% | 0.52 | no |
| Jsram | 8 | 6 | +25.2% | 0.85 | no |
| Kkunn | 880 | 371 | +0.1% | 0.27 | no |
| Sisyphus- | 128 | 70 | -4.2% | -0.46 | no |
| PEYZ-BIGGEST-FAN | 392 | 197 | -1.3% | -0.13 | no |
| theowalcott | 13 | 11 | +63.3% | 2.93 | no |
| HVAB | 385 | 234 | -1.1% | -0.22 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +5.3% | 1.01 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 31 | 28 | +14.4% | 1.24 | no |
| 0010001000001100 | 62 | 30 | +7.3% | 0.34 | yes |
| totoro3miyazaki | 11 | 3 | -69.9% | -4.21 | no |
| 1l2ihj34li12u34 | 9 | 6 | +30.6% | 0.92 | no |
| yabanci | 81 | 46 | -2.8% | 0.01 | yes |
| 0x20D6436849F930584892730C7F | 123 | 69 | +30.4% | 1.83 | no |
| juice-fruit | 48 | 31 | +8.0% | 0.7 | yes |
| 0x16bb9951a36fce71e2ef57890b | 63 | 23 | -11.2% | -0.76 | yes |
| GamblingOdyssey | 339 | 179 | +8.8% | 1.6 | no |
| plonker2026 | 6 | 5 | +161.7% | 1.6 | no |
| xxyx0xx | 184 | 86 | +25.4% | 1.29 | no |
| monkeymashingkeyboard | 984 | 523 | +6.0% | 1.73 | yes |
| Tiger105 | 32 | 24 | +37.6% | 2.45 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 511 | 294 | +2.1% | 0.55 | no |
| UNEB3154s4f251 | 1864 | 1135 | +3.2% | 1.72 | no |
