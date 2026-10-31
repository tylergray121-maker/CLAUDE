# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-31 09:00 UTC: 5509 candidates, 3778 with trades copytop could copy, 219 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3318 | 1653 | $31,983 | +211.79 | +0.7% | +0.48 |
| every wallet that qualified on the first part (test window) | 3911 | 1938 | $37,982 | +221.29 | +0.6% | +0.42 |
| currently copied (test window) | 4068 | 2186 | $39,896 | +1,228.02 | +3.1% | +2.02 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3318 | 1653 | $31,983 | +211.79 | +0.7% | 0.48 | 7069 | 3592 | $68,187 | +5,391.32 | +7.9% | 5.12 |
| copy their sells too | 3329 | 1341 | $32,086 | -534.51 | -1.7% | -0.77 | 7080 | 3069 | $68,290 | +3,872.95 | +5.7% | 3.88 |
| size by conviction (x0.5 / x1 / x1.5) | 3117 | 1544 | $37,128 | +478.56 | +1.3% | 0.25 | 6646 | 3363 | $79,441 | +5,951.56 | +7.5% | 4.79 |
| skip bets under 0.5x their usual | 3119 | 1553 | $30,239 | +337.90 | +1.1% | 0.78 | 6644 | 3376 | $64,537 | +5,253.96 | +8.1% | 5.14 |
| pre-game only | 3186 | 1604 | $30,666 | +257.31 | +0.8% | 0.54 | 6654 | 3437 | $63,999 | +5,555.03 | +8.7% | 5.56 |
| skip prices under 30c | 2833 | 1532 | $27,164 | +78.36 | +0.3% | 0.17 | 5779 | 3204 | $55,367 | +881.63 | +1.6% | 1.39 |
| favorites only (50c+) | 1580 | 996 | $15,013 | -195.53 | -1.3% | -0.53 | 3103 | 2061 | $29,383 | +430.66 | +1.5% | 1.32 |
| 15s delay | 3331 | 1661 | $32,142 | +406.17 | +1.3% | 0.8 | 7120 | 3620 | $68,731 | +5,795.76 | +8.4% | 5.43 |
| 60s delay | 3318 | 1653 | $31,983 | +211.79 | +0.7% | 0.48 | 7069 | 3592 | $68,187 | +5,391.32 | +7.9% | 5.12 |
| allow 2c over their price | 3385 | 1682 | $32,608 | +342.34 | +1.1% | 0.65 | 7319 | 3715 | $70,607 | +5,732.03 | +8.1% | 5.26 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 422 | +26.2% | 3.58 | 384 | +11.2% | 1.31 |
| conviction:1-2x | 647 | +12.9% | 2.14 | 448 | -6.1% | -0.95 |
| conviction:2x+ | 2232 | +11.0% | 3.6 | 2068 | +1.9% | 0.96 |
| conviction:under 0.5x | 450 | +22.6% | 3.51 | 418 | -8.0% | -1.44 |
| delay_move:flat | 2525 | +15.7% | 5.35 | 2646 | +1.4% | 0.7 |
| delay_move:price fell | 1226 | +11.4% | 3.0 | 672 | -2.1% | -0.32 |
| exit:settle | 3751 | +14.3% | 6.13 | 3318 | +0.7% | 0.48 |
| kind:moneyline | 2828 | +12.6% | 4.47 | 2604 | +0.7% | 0.4 |
| kind:result | 840 | +20.7% | 4.8 | 532 | +6.8% | 1.5 |
| kind:totals | 83 | +6.7% | 0.69 | 182 | -17.8% | -2.5 |
| league:atp | 384 | +7.9% | 1.2 | 184 | +13.3% | 2.07 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 132 | +2.6% | 0.27 | 270 | +20.8% | 2.15 |
| league:cs2 | 322 | +12.9% | 1.47 | 239 | +4.9% | 0.89 |
| league:dota2 | 98 | -12.2% | -1.06 | 103 | +22.5% | 1.29 |
| league:epl | 52 | +34.2% | 3.05 | 50 | -13.4% | -1.19 |
| league:ere | 8 | +106.7% | 28.83 | 32 | +34.7% | 1.3 |
| league:lal | 70 | +15.4% | 1.43 | 99 | -5.3% | -0.44 |
| league:lol | 1760 | +18.2% | 4.71 | 277 | -5.0% | -0.57 |
| league:mls | 26 | +12.6% | 0.62 | 200 | -3.6% | -0.49 |
| league:nba | 0 | +0.0% | — | 528 | +2.5% | 0.68 |
| league:nfl | 370 | +15.3% | 2.33 | 291 | -3.5% | -0.83 |
| league:nhl | 34 | +14.4% | 0.72 | 642 | -14.1% | -3.6 |
| league:sea | 33 | +59.4% | 3.41 | 39 | -29.2% | -1.58 |
| league:ucl | 40 | -8.0% | -0.57 | 61 | +15.9% | 1.3 |
| league:uel | 0 | +0.0% | — | 12 | +17.4% | 0.79 |
| league:wnba | 126 | +6.1% | 0.88 | 51 | -1.5% | 0.16 |
| league:wta | 286 | +9.2% | 1.09 | 227 | +8.6% | 1.19 |
| price:30-70c | 2431 | +3.1% | 1.63 | 2504 | -0.4% | -0.08 |
| price:over 70c | 511 | +1.8% | 1.03 | 318 | +0.9% | 0.1 |
| price:under 30c | 809 | +54.4% | 6.47 | 496 | +5.5% | 0.84 |
| timing:in-play | 283 | -4.1% | -0.48 | 132 | -3.5% | -0.19 |
| timing:pre-game | 3468 | +15.9% | 6.71 | 3186 | +0.8% | 0.54 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 133526 | 69536 | $1,328,756 | -51,150.68 | -3.9% | -11.91 |
| consistency (winning weeks), top 16 | 8968 | 5093 | $88,067 | -2,536.23 | -2.9% | -2.06 |
| consistency (winning weeks), top 40 | 23079 | 12470 | $228,364 | -7,673.12 | -3.4% | -4.34 |
| copy return, average, top 16 | 6862 | 3434 | $67,981 | -670.44 | -1.0% | -0.79 |
| copy return, average, top 40 | 22513 | 11521 | $222,935 | -7,146.10 | -3.2% | -3.78 |
| copy return, lower bound, top 16 | 7265 | 3771 | $71,644 | -4,611.21 | -6.4% | -5.05 |
| copy return, lower bound, top 40 | 24740 | 13679 | $244,890 | -10,423.46 | -4.3% | -5.90 |
| copy return, shrunk, top 16 | 6449 | 3066 | $64,010 | -2,186.75 | -3.4% | -2.08 |
| copy return, shrunk, top 40 | 22806 | 11662 | $226,215 | -8,427.31 | -3.7% | -4.53 |
| markout 2h, average, top 16 | 8310 | 4660 | $82,323 | -2,533.57 | -3.1% | -2.52 |
| markout 2h, average, top 40 | 22349 | 12069 | $222,379 | -7,300.09 | -3.3% | -4.22 |
| markout 2h, lower bound, top 16 | 8822 | 4853 | $87,577 | -5,206.85 | -5.9% | -5.17 |
| markout 2h, lower bound, top 40 | 27320 | 14836 | $271,292 | -10,359.52 | -3.8% | -5.50 |
| markout 30m, average, top 16 | 11068 | 6478 | $110,121 | -1,661.77 | -1.5% | -1.42 |
| markout 30m, average, top 40 | 27177 | 14858 | $271,223 | -8,781.01 | -3.2% | -4.46 |
| most active, top 16 | 22127 | 11681 | $220,548 | -9,720.45 | -4.4% | -5.63 |
| most active, top 40 | 38836 | 20152 | $386,498 | -15,935.14 | -4.1% | -6.94 |
| win rate vs the odds, top 16 | 4397 | 2264 | $43,371 | -1,122.55 | -2.6% | -1.39 |
| win rate vs the odds, top 40 | 22983 | 12037 | $227,745 | -8,287.51 | -3.6% | -4.74 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 49 | 45 | +29.7% | 3.56 | +2.90 |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | +4.48 |
| 0x20D6436849F930584892730C7F | 126 | 70 | +28.3% | 1.74 | +2.82 |
| xxyx0xx | 280 | 139 | +6.8% | 0.64 | +0.62 |
| yabanci | 63 | 42 | +16.0% | 1.63 | +1.87 |
| eokho | 791 | 443 | +4.8% | 1.03 | +0.44 |
| theowalcott | 101 | 58 | +7.9% | 0.98 | +0.94 |
| am100 | 957 | 581 | +13.8% | 3.71 | +1.38 |
| monkeymashingkeyboard | 848 | 472 | +12.1% | 3.22 | +1.23 |
| SimpleTony | 1163 | 381 | +10.5% | 2.0 | +1.07 |
| Sisyphus- | 123 | 71 | +0.7% | 0.08 | +0.07 |
| AmericaFirst1 | 468 | 288 | +5.5% | 1.31 | +0.57 |
| moreplatesmoredates | 937 | 471 | +2.7% | 0.87 | +0.38 |
| juice-fruit | 48 | 32 | +9.0% | 0.79 | +1.00 |
| plonker2026 | 136 | 80 | +15.9% | 2.1 | +1.97 |
| platarb | 601 | 238 | -0.3% | -0.08 | -0.04 |
| smithagent | 1087 | 604 | +6.7% | 1.27 | +0.65 |
| pltrkr111 | 1115 | 629 | +12.9% | 3.26 | +1.23 |
| 0xffAaEFb5f6762Cc70cb575Da87 | 693 | 327 | +1.8% | 0.29 | +0.17 |
| eskk | 1009 | 255 | +0.1% | 0.05 | +0.04 |
| arahbo | 1559 | 660 | -2.0% | -0.51 | -0.21 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 989 | 438 | +4.0% | 0.74 | +0.39 |
| Future-Tarot-Trader | 1998 | 1016 | -1.3% | -0.46 | -0.15 |
| torta.tech | 1172 | 725 | +1.8% | 0.63 | +0.18 |
| 0x16bb9951a36fce71e2ef57890b | 56 | 23 | +1.0% | 0.01 | +0.02 |
| KaneAnalytics | 164 | 90 | +3.7% | 0.38 | +0.37 |
| igot50k | 1680 | 1020 | -0.0% | -0.04 | -0.01 |
| walnutz | 636 | 323 | -2.8% | -0.65 | -0.29 |
| 636763 | 1485 | 463 | +0.8% | 0.31 | +0.16 |
| cosmicsteaks | 1243 | 537 | -1.9% | -0.47 | -0.21 |
| n1ck10s | 1104 | 585 | +2.6% | 0.68 | +0.24 |
| 0x870a742f | 546 | 234 | +1.0% | 0.18 | +0.11 |
| 1l2ihj34li12u34 | 92 | 53 | +13.4% | 1.55 | +1.66 |
| UNEB3154s4f251 | 2232 | 1417 | +3.0% | 1.77 | +0.30 |
| assasin5002 | 610 | 309 | +2.4% | 0.43 | +0.23 |
| User7429 | 932 | 496 | -3.0% | -0.79 | -0.30 |
| jiafan | 995 | 591 | +0.6% | 0.13 | +0.04 |
| littlebay | 799 | 528 | +2.0% | 0.57 | +0.20 |
| yuxkc0 | 383 | 129 | -7.0% | -0.89 | -0.69 |
| Jsram | 95 | 56 | +0.0% | 0.21 | +0.19 |

## Esports specialists (copies on esports markets only)

2933 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 167 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | tag | 76 | 43 | +48.6% | 2.16 | +61.7% (43) | +31.6% (33) | no |
| pltrkr111 | tag | 277 | 160 | +32.8% | 3.24 | +41.8% (214) | +2.1% (63) | yes |
| 0x5fD2D9C60781D711721145Ff2b | tag | 32 | 18 | +90.0% | 1.33 | +132.6% (21) | +8.5% (11) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 301 | 182 | +24.2% | 2.62 | +19.1% (243) | +46.1% (58) | no |
| am100 | tag | 957 | 581 | +13.8% | 3.71 | +13.5% (902) | +17.6% (55) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1339 | 711 | +7.8% | 2.41 | +11.7% (1148) | -16.3% (191) | yes |
| SimpleTony | tag | 1141 | 369 | +9.7% | 1.84 | +11.7% (791) | +5.4% (350) | yes |
| -5rud | tag | 529 | 364 | +8.5% | 2.08 | +7.8% (431) | +11.5% (98) | yes |
| MIracle33 | tag | 447 | 229 | +10.1% | 1.77 | +10.2% (360) | +9.9% (87) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 617 | 323 | +7.3% | 1.55 | +13.2% (416) | -5.2% (201) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +0.0% (0) | +19.4% (29) | yes |
| 0x1E3bB7DEf89B002D45FD86D37F | tag | 25 | 16 | +26.3% | 1.09 | +0.0% (0) | +26.3% (25) | yes |
| yakz | leaderboard | 180 | 88 | +15.3% | 1.15 | +29.3% (87) | +1.9% (93) | yes |
| BunCaCham | tag | 20 | 19 | +7.6% | 1.29 | +4.9% (14) | +13.9% (6) | no |
| ZEST011 | tag | 666 | 497 | +3.0% | 1.13 | +2.4% (565) | +6.6% (101) | yes |
| AmericaFirst1 | current | 256 | 165 | +5.1% | 1.03 | +8.2% (212) | -9.5% (44) | no |
| littlebay | tag | 97 | 72 | +6.7% | 0.96 | +7.7% (44) | +5.9% (53) | yes |
| moreplatesmoredates | tag | 937 | 471 | +2.7% | 0.87 | -1.1% (588) | +9.1% (349) | yes |
| Nooserac | tag | 162 | 87 | +9.2% | 0.9 | -0.1% (111) | +29.8% (51) | yes |
| berlinskies | tag | 1044 | 608 | +2.3% | 0.69 | +4.6% (827) | -6.5% (217) | yes |
| GC-C | tag | 742 | 518 | +0.9% | 0.38 | -5.1% (371) | +7.1% (371) | yes |
| shaw | tag | 279 | 163 | +3.5% | 0.6 | +5.5% (217) | -3.9% (62) | yes |
| 0x85264d29Fa7279946D15105C17 | tag | 130 | 68 | +7.7% | 0.73 | +11.0% (99) | -2.6% (31) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -9.4% (108) | +13.4% (110) | no |
| 636763 | tag | 1463 | 456 | +1.5% | 0.43 | -0.8% (1051) | +7.2% (412) | yes |
| HalleyChen | tag | 633 | 388 | +1.7% | 0.37 | +2.4% (484) | -0.4% (149) | yes |
| dddd123s | tag | 576 | 347 | +0.3% | 0.07 | +4.3% (384) | -7.6% (192) | yes |
| nightcity2077 | tag | 423 | 206 | +4.3% | 0.56 | +5.5% (406) | -27.0% (17) | yes |
| igot50k | tag | 1028 | 515 | +0.9% | 0.19 | -0.3% (889) | +8.7% (139) | yes |
| Diabolical-Prize | tag | 224 | 118 | +2.1% | 0.47 | +9.8% (172) | -23.3% (52) | no |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 292 | 120 | -9.5% | -1.37 | no |
| Kch-Temp | 125 | 60 | -7.2% | -0.7 | no |
| EdZachary | 84 | 30 | -9.2% | -0.76 | no |
| KaneAnalytics | 164 | 90 | +3.7% | 0.38 | yes |
| Jsram | 95 | 56 | +0.0% | 0.21 | yes |
| Kkunn | 777 | 334 | +2.4% | 0.72 | no |
| Sisyphus- | 123 | 71 | +0.7% | 0.08 | yes |
| PEYZ-BIGGEST-FAN | 386 | 192 | +2.3% | 0.36 | no |
| theowalcott | 101 | 58 | +7.9% | 0.98 | yes |
| HVAB | 344 | 205 | -4.4% | -0.8 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 282 | 147 | +6.5% | 1.18 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | yes |
| BunCaCham | 49 | 45 | +29.7% | 3.56 | yes |
| 0010001000001100 | 164 | 79 | -0.1% | -0.29 | no |
| totoro3miyazaki | 49 | 31 | +8.7% | 0.68 | no |
| 1l2ihj34li12u34 | 92 | 53 | +13.4% | 1.55 | yes |
| yabanci | 63 | 42 | +16.0% | 1.63 | yes |
| 0x20D6436849F930584892730C7F | 126 | 70 | +28.3% | 1.74 | yes |
| juice-fruit | 48 | 32 | +9.0% | 0.79 | yes |
| 0x16bb9951a36fce71e2ef57890b | 56 | 23 | +1.0% | 0.01 | yes |
| GamblingOdyssey | 387 | 188 | +2.9% | 0.68 | no |
| plonker2026 | 136 | 80 | +15.9% | 2.1 | yes |
| xxyx0xx | 280 | 139 | +6.8% | 0.64 | yes |
| monkeymashingkeyboard | 848 | 472 | +12.1% | 3.22 | yes |
| Tiger105 | 43 | 28 | +19.1% | 1.34 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 468 | 288 | +5.5% | 1.31 | yes |
| UNEB3154s4f251 | 2232 | 1417 | +3.0% | 1.77 | yes |
