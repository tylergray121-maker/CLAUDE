# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-25 09:00 UTC: 5519 candidates, 3904 with trades copytop could copy, 220 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 1975 | 977 | $19,155 | -99.36 | -0.5% | +0.04 |
| every wallet that qualified on the first part (test window) | 2681 | 1333 | $26,268 | -41.92 | -0.2% | +0.11 |
| currently copied (test window) | 4367 | 2317 | $42,885 | +1,146.26 | +2.7% | +1.72 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 1975 | 977 | $19,155 | -99.36 | -0.5% | 0.04 | 5351 | 2863 | $51,393 | +3,156.69 | +6.1% | 4.15 |
| copy their sells too | 1975 | 951 | $19,155 | -463.89 | -2.4% | -0.72 | 5351 | 2824 | $51,393 | +2,675.36 | +5.2% | 3.58 |
| size by conviction (x0.5 / x1 / x1.5) | 1880 | 919 | $23,100 | -52.12 | -0.2% | -0.32 | 5015 | 2665 | $61,244 | +3,181.28 | +5.2% | 3.75 |
| skip bets under 0.5x their usual | 1860 | 927 | $18,128 | +78.46 | +0.4% | 0.4 | 5026 | 2687 | $48,384 | +2,832.18 | +5.9% | 3.84 |
| pre-game only | 1674 | 872 | $16,115 | +284.07 | +1.8% | 0.83 | 4938 | 2682 | $47,234 | +3,410.44 | +7.2% | 4.68 |
| skip prices under 30c | 1673 | 912 | $16,111 | +243.82 | +1.5% | 0.85 | 4871 | 2719 | $46,592 | +1,756.69 | +3.8% | 2.86 |
| favorites only (50c+) | 913 | 601 | $8,692 | +519.38 | +6.0% | 2.52 | 2725 | 1761 | $25,883 | +1,276.32 | +4.9% | 3.47 |
| 15s delay | 2017 | 996 | $19,572 | -173.13 | -0.9% | -0.05 | 5417 | 2894 | $52,051 | +3,142.85 | +6.0% | 4.14 |
| 60s delay | 1975 | 977 | $19,155 | -99.36 | -0.5% | 0.04 | 5351 | 2863 | $51,393 | +3,156.69 | +6.1% | 4.15 |
| allow 2c over their price | 2033 | 1005 | $19,698 | -170.22 | -0.9% | -0.06 | 5476 | 2925 | $52,591 | +3,004.59 | +5.7% | 3.95 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 367 | +2.8% | 0.91 | 219 | +5.8% | 0.88 |
| conviction:1-2x | 419 | +9.6% | 1.16 | 172 | -19.0% | -1.98 |
| conviction:2x+ | 2209 | +8.9% | 3.9 | 1307 | +1.5% | 0.41 |
| conviction:under 0.5x | 381 | +24.4% | 3.8 | 277 | -4.1% | -0.13 |
| delay_move:flat | 2667 | +9.8% | 4.53 | 1465 | +1.9% | 0.91 |
| delay_move:price fell | 709 | +11.3% | 2.68 | 510 | -7.2% | -1.25 |
| exit:settle | 3376 | +10.1% | 5.25 | 1975 | -0.5% | 0.04 |
| kind:moneyline | 2509 | +11.6% | 4.84 | 1604 | +1.1% | 0.52 |
| kind:result | 189 | +25.4% | 4.18 | 156 | +2.6% | 0.63 |
| kind:totals | 678 | +0.6% | 0.3 | 215 | -15.2% | -2.27 |
| league:atp | 301 | +19.9% | 2.41 | 411 | -11.3% | -1.62 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 13 | -100.0% | — | 65 | +13.2% | 0.83 |
| league:cs2 | 112 | +16.5% | 1.76 | 58 | -3.3% | -0.08 |
| league:dota2 | 22 | +30.2% | 1.54 | 23 | -42.7% | -2.36 |
| league:epl | 52 | +34.2% | 3.05 | 49 | -15.2% | -1.31 |
| league:ere | 8 | +106.7% | 28.83 | 12 | +166.2% | 6.87 |
| league:lal | 20 | +17.4% | 1.12 | 2 | -0.4% | -0.03 |
| league:lol | 198 | +44.5% | 3.48 | 136 | -6.9% | -0.95 |
| league:mlb | 2029 | +1.9% | 0.84 | 313 | +4.0% | 1.14 |
| league:mls | 13 | +26.7% | 1.1 | 19 | -19.5% | -0.84 |
| league:nba | 0 | +0.0% | — | 130 | -13.8% | -1.88 |
| league:nfl | 126 | +5.1% | 0.55 | 70 | +47.1% | 3.07 |
| league:nhl | 0 | +0.0% | — | 25 | -23.4% | -1.73 |
| league:sea | 33 | +59.4% | 3.41 | 32 | -50.6% | -3.21 |
| league:ucl | 38 | -7.2% | -0.5 | 50 | -1.7% | 0.32 |
| league:wnba | 108 | +27.5% | 3.21 | 34 | -9.8% | -0.43 |
| league:wta | 292 | +15.4% | 2.13 | 536 | +8.8% | 1.62 |
| price:30-70c | 2999 | +4.2% | 2.35 | 1536 | +1.3% | 0.73 |
| price:over 70c | 197 | +15.0% | 6.68 | 130 | +5.0% | 1.12 |
| price:under 30c | 180 | +99.1% | 5.59 | 309 | -11.2% | -1.05 |
| timing:in-play | 112 | +11.6% | 1.3 | 301 | -12.6% | -1.35 |
| timing:pre-game | 3264 | +10.1% | 5.11 | 1674 | +1.8% | 0.83 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 150379 | 77492 | $1,495,154 | -61,385.17 | -4.1% | -13.65 |
| consistency (winning weeks), top 16 | 11388 | 5809 | $112,578 | -5,860.51 | -5.2% | -4.68 |
| consistency (winning weeks), top 40 | 27729 | 14489 | $273,403 | -11,366.14 | -4.2% | -6.13 |
| copy return, average, top 16 | 6426 | 3086 | $63,447 | -263.16 | -0.4% | -0.35 |
| copy return, average, top 40 | 22112 | 11335 | $218,455 | -5,504.43 | -2.5% | -3.25 |
| copy return, lower bound, top 16 | 7967 | 4007 | $78,450 | -2,043.30 | -2.6% | -1.75 |
| copy return, lower bound, top 40 | 28507 | 15132 | $282,109 | -6,996.14 | -2.5% | -3.70 |
| copy return, shrunk, top 16 | 6734 | 3239 | $66,437 | -746.08 | -1.1% | -0.71 |
| copy return, shrunk, top 40 | 22925 | 11974 | $226,262 | -5,657.58 | -2.5% | -3.28 |
| markout 2h, average, top 16 | 7444 | 3774 | $74,596 | -1,007.83 | -1.4% | -0.83 |
| markout 2h, average, top 40 | 21274 | 10898 | $213,010 | -5,456.47 | -2.6% | -2.84 |
| markout 2h, lower bound, top 16 | 9212 | 4704 | $91,893 | -3,318.28 | -3.6% | -2.66 |
| markout 2h, lower bound, top 40 | 29770 | 15326 | $295,776 | -8,455.70 | -2.9% | -4.13 |
| markout 30m, average, top 16 | 7514 | 3814 | $75,174 | -2,479.21 | -3.3% | -2.31 |
| markout 30m, average, top 40 | 25600 | 13285 | $255,995 | -6,790.49 | -2.6% | -3.38 |
| most active, top 16 | 27233 | 14085 | $269,808 | -14,191.31 | -5.3% | -7.80 |
| most active, top 40 | 52301 | 26775 | $519,621 | -24,926.27 | -4.8% | -9.56 |
| win rate vs the odds, top 16 | 5466 | 2697 | $53,555 | +236.96 | +0.4% | +0.21 |
| win rate vs the odds, top 40 | 23372 | 11934 | $231,434 | -4,995.22 | -2.2% | -2.76 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 48 | 44 | +28.8% | 3.4 | +2.81 |
| 0x20D6436849F930584892730C7F | 151 | 85 | +26.1% | 1.91 | +2.66 |
| yabanci | 38 | 26 | +23.5% | 1.89 | +2.76 |
| tiger105 | 44 | 29 | +23.0% | 1.61 | +2.29 |
| xxyx0xx | 260 | 131 | +6.8% | 0.63 | +0.63 |
| plonker2026 | 114 | 75 | +28.8% | 3.32 | +3.36 |
| KaneAnalytics | 110 | 66 | +17.2% | 1.32 | +1.68 |
| juice-fruit | 35 | 25 | +15.2% | 1.1 | +1.60 |
| 0x16bb9951a36fce71e2ef57890b | 834 | 454 | +6.5% | 1.94 | +0.68 |
| 0x6918EA182D963b1Fb7888860b8 | 804 | 471 | +6.4% | 1.43 | +0.52 |
| smithagent | 810 | 435 | +7.4% | 1.1 | +0.71 |
| am100 | 1016 | 607 | +11.1% | 3.12 | +1.11 |
| platarb | 918 | 362 | +1.6% | 0.35 | +0.15 |
| 1l2ihj34li12u34 | 57 | 35 | +25.0% | 2.01 | +2.81 |
| SimpleTony | 1244 | 403 | +9.8% | 1.93 | +0.99 |
| theowalcott | 92 | 51 | +4.3% | 0.58 | +0.59 |
| moreplatesmoredates | 956 | 481 | +0.3% | 0.27 | +0.11 |
| AmericaFirst1 | 509 | 317 | +5.7% | 1.4 | +0.58 |
| monkeymashingkeyboard | 1957 | 1097 | +6.4% | 2.78 | +0.63 |
| polkals | 566 | 255 | +7.2% | 1.06 | +0.69 |
| Sisyphus- | 121 | 72 | +0.8% | 0.1 | +0.08 |
| eskk | 1074 | 268 | -0.6% | -0.05 | -0.03 |
| cosmicsteaks | 1345 | 579 | -2.6% | -0.65 | -0.28 |
| arahbo | 1679 | 712 | -0.2% | -0.12 | -0.05 |
| walnutz | 642 | 331 | -1.8% | -0.44 | -0.19 |
| TAIWANNUMBERONE | 1517 | 811 | -3.7% | -1.42 | -0.38 |
| ZEST011 | 723 | 538 | +2.2% | 0.9 | +0.22 |
| 0ooo0o0o0oo0o0 | 1379 | 754 | -2.5% | -0.94 | -0.25 |
| 0x567212c82AAa6fe589bE5A2f4C | 649 | 335 | +4.5% | 1.12 | +0.62 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 1142 | 505 | +2.4% | 0.48 | +0.23 |
| torta.tech | 1870 | 1121 | -0.4% | -0.16 | -0.04 |
| GamblingOdyssey | 437 | 221 | +6.1% | 1.27 | +0.71 |
| UNEB3154s4f251 | 2021 | 1273 | +2.5% | 1.44 | +0.26 |
| 0xffAaEFb5f6762Cc70cb575Da87 | 685 | 323 | +2.1% | 0.34 | +0.20 |
| MIracle33 | 909 | 455 | +4.7% | 1.23 | +0.46 |
| jiafan | 1061 | 633 | +0.8% | 0.21 | +0.07 |
| cm2897 | 1061 | 515 | +1.3% | 0.12 | +0.06 |
| 0010001000001100 | 127 | 60 | +1.0% | -0.26 | -0.35 |
| Jsram | 95 | 56 | +0.0% | 0.21 | +0.19 |
| Petal | 927 | 437 | -6.7% | -1.7 | -0.67 |

## Esports specialists (copies on esports markets only)

2832 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 167 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | tag | 76 | 43 | +48.6% | 2.16 | +31.5% (11) | +51.5% (65) | no |
| pltrkr111 | tag | 271 | 160 | +35.4% | 3.48 | +55.1% (167) | +3.9% (104) | yes |
| juice-fruit | current | 25 | 19 | +28.5% | 1.64 | +0.0% (0) | +28.5% (25) | no |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 324 | 194 | +20.0% | 2.3 | +18.8% (230) | +22.9% (94) | no |
| am100 | tag | 1016 | 607 | +11.1% | 3.12 | +8.7% (916) | +31.6% (100) | yes |
| MIracle33 | tag | 440 | 226 | +10.4% | 1.8 | +11.4% (314) | +7.8% (126) | yes |
| yakz | leaderboard | 162 | 79 | +19.4% | 1.34 | +31.0% (76) | +9.0% (86) | yes |
| SimpleTony | tag | 1222 | 391 | +9.0% | 1.77 | +6.7% (862) | +14.4% (360) | yes |
| -5rud | tag | 563 | 388 | +7.3% | 1.87 | +7.2% (405) | +7.6% (158) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1516 | 801 | +5.5% | 1.88 | +6.5% (1230) | +1.5% (286) | yes |
| BunCaCham | tag | 20 | 19 | +7.6% | 1.29 | +4.9% (14) | +13.9% (6) | yes |
| 0x6918EA182D963b1Fb7888860b8 | tag | 804 | 471 | +6.4% | 1.43 | +2.1% (638) | +23.2% (166) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 649 | 335 | +4.5% | 1.12 | +7.8% (431) | -1.8% (218) | yes |
| AmericaFirst1 | current | 256 | 165 | +5.1% | 1.03 | +8.4% (175) | -1.9% (81) | yes |
| ZEST011 | tag | 723 | 538 | +2.2% | 0.9 | +2.2% (620) | +2.3% (103) | yes |
| Saber-greed | leaderboard | 431 | 221 | +8.0% | 0.91 | +5.3% (392) | +34.3% (39) | yes |
| shaw | tag | 315 | 179 | +4.8% | 0.8 | +6.7% (245) | -2.0% (70) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 153 | 103 | +4.6% | 0.77 | +4.2% (87) | +5.1% (66) | yes |
| GC-C | tag | 727 | 507 | +0.9% | 0.37 | +1.7% (220) | +0.5% (507) | yes |
| berlinskies | tag | 1032 | 604 | +1.3% | 0.42 | +5.1% (745) | -8.3% (287) | yes |
| Nooserac | tag | 200 | 106 | +6.1% | 0.74 | -1.4% (152) | +30.3% (48) | yes |
| 0xcf279d52 | tag | 490 | 293 | +2.5% | 0.52 | +6.6% (333) | -6.4% (157) | yes |
| 0x09dAc7226f8df37eBFAF277252 | tag | 531 | 314 | +1.3% | 0.41 | +4.8% (458) | -20.7% (73) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -9.6% (94) | +10.9% (124) | yes |
| moreplatesmoredates | tag | 956 | 481 | +0.3% | 0.27 | -4.7% (565) | +7.6% (391) | yes |
| dddd123s | tag | 545 | 329 | +0.4% | 0.1 | +6.8% (284) | -6.4% (261) | yes |
| Diabolical-Prize | tag | 224 | 118 | +2.1% | 0.47 | +15.0% (145) | -21.2% (79) | no |
| Future-Tarot-Trader | tag | 2178 | 1107 | -0.2% | -0.17 | -1.7% (1884) | +8.7% (294) | yes |
| 0xffAaEFb5f6762Cc70cb575Da87 | tag | 685 | 323 | +2.1% | 0.34 | +3.3% (509) | -1.2% (176) | yes |
| vardaman-bundren | tag | 406 | 186 | +2.8% | 0.38 | +0.4% (294) | +9.1% (112) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 318 | 136 | -5.3% | -0.82 | no |
| Kch-Temp | 119 | 57 | -6.7% | -0.63 | no |
| EdZachary | 85 | 38 | -8.4% | -0.81 | no |
| KaneAnalytics | 110 | 66 | +17.2% | 1.32 | yes |
| Jsram | 95 | 56 | +0.0% | 0.21 | yes |
| Kkunn | 686 | 287 | +2.1% | 0.59 | no |
| Sisyphus- | 121 | 72 | +0.8% | 0.1 | yes |
| PEYZ-BIGGEST-FAN | 377 | 189 | +3.8% | 0.57 | no |
| theowalcott | 92 | 51 | +4.3% | 0.58 | yes |
| HVAB | 317 | 196 | +0.1% | 0.01 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 293 | 153 | +6.9% | 1.26 | no |
| Talvez10 | 576 | 319 | +5.9% | 1.12 | no |
| BunCaCham | 48 | 44 | +28.8% | 3.4 | yes |
| 0010001000001100 | 127 | 60 | +1.0% | -0.26 | yes |
| totoro3miyazaki | 48 | 30 | +7.0% | 0.55 | no |
| 1l2ihj34li12u34 | 57 | 35 | +25.0% | 2.01 | yes |
| yabanci | 38 | 26 | +23.5% | 1.89 | yes |
| 0x20D6436849F930584892730C7F | 151 | 85 | +26.1% | 1.91 | yes |
| juice-fruit | 35 | 25 | +15.2% | 1.1 | yes |
| 0x16bb9951a36fce71e2ef57890b | 834 | 454 | +6.5% | 1.94 | yes |
| GamblingOdyssey | 437 | 221 | +6.1% | 1.27 | yes |
| plonker2026 | 114 | 75 | +28.8% | 3.32 | yes |
| xxyx0xx | 260 | 131 | +6.8% | 0.63 | yes |
| monkeymashingkeyboard | 1957 | 1097 | +6.4% | 2.78 | yes |
| Tiger105 | 44 | 29 | +23.0% | 1.61 | yes |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 509 | 317 | +5.7% | 1.4 | yes |
| UNEB3154s4f251 | 2021 | 1273 | +2.5% | 1.44 | yes |
