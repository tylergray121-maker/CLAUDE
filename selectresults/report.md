# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-23 09:00 UTC: 5777 candidates, 3828 with trades copytop could copy, 239 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 3278 | 1627 | $32,021 | -1,803.40 | -5.6% | -2.67 |
| every wallet that qualified on the first part (test window) | 3580 | 1774 | $35,075 | -2,058.60 | -5.9% | -2.85 |
| currently copied (test window) | 3218 | 1627 | $31,474 | -401.26 | -1.3% | -0.39 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 3278 | 1627 | $32,021 | -1,803.40 | -5.6% | -2.67 | 4332 | 2287 | $42,349 | +665.61 | +1.6% | 0.74 |
| copy their sells too | 3278 | 1576 | $32,021 | -1,890.23 | -5.9% | -2.82 | 4332 | 2149 | $42,349 | +223.15 | +0.5% | 0.24 |
| size by conviction (x0.5 / x1 / x1.5) | 3203 | 1586 | $35,668 | -1,946.84 | -5.5% | -2.55 | 4234 | 2223 | $48,815 | +829.23 | +1.7% | 0.61 |
| skip bets under 0.5x their usual | 2995 | 1542 | $29,273 | -2,103.28 | -7.2% | -3.56 | 4020 | 2187 | $39,351 | +355.37 | +0.9% | 0.4 |
| pre-game only | 400 | 207 | $3,988 | -179.26 | -4.5% | -0.77 | 1060 | 634 | $10,366 | +1,352.80 | +13.1% | 4.72 |
| skip prices under 30c | 2591 | 1535 | $25,264 | -812.43 | -3.2% | -1.87 | 3516 | 2162 | $34,262 | +985.24 | +2.9% | 2.1 |
| favorites only (50c+) | 1731 | 1206 | $16,781 | -270.73 | -1.6% | -0.93 | 2247 | 1592 | $21,769 | +344.89 | +1.6% | 1.14 |
| 15s delay | 3456 | 1733 | $33,481 | -2,015.65 | -6.0% | -2.99 | 4518 | 2400 | $43,869 | +450.71 | +1.0% | 0.53 |
| 60s delay | 3278 | 1627 | $32,021 | -1,803.40 | -5.6% | -2.67 | 4332 | 2287 | $42,349 | +665.61 | +1.6% | 0.74 |
| allow 2c over their price | 3504 | 1760 | $34,069 | -1,582.09 | -4.6% | -2.37 | 4594 | 2441 | $44,755 | +935.27 | +2.1% | 0.93 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 85 | +58.1% | 2.1 | 520 | -12.1% | -1.78 |
| conviction:1-2x | 90 | +51.7% | 2.97 | 739 | -8.5% | -2.37 |
| conviction:2x+ | 765 | +17.2% | 4.33 | 1511 | -4.3% | -1.55 |
| conviction:under 0.5x | 114 | +21.8% | 2.02 | 508 | +1.3% | -0.07 |
| delay_move:flat | 649 | +27.8% | 6.16 | 1230 | -4.6% | -1.41 |
| delay_move:price fell | 405 | +17.9% | 2.26 | 2048 | -6.3% | -2.26 |
| exit:settle | 1054 | +23.9% | 5.85 | 3278 | -5.6% | -2.67 |
| kind:moneyline | 652 | +28.6% | 4.81 | 2807 | -5.8% | -2.56 |
| kind:result | 228 | +11.8% | 2.12 | 207 | -1.0% | -0.01 |
| kind:totals | 174 | +22.2% | 2.81 | 264 | -7.1% | -1.05 |
| league:acle | 1 | +73.1% | — | 15 | -100.0% | — |
| league:atp | 96 | +14.1% | 1.46 | 976 | -0.4% | -0.31 |
| league:bel1 | 2 | +18.2% | 0.17 | 18 | -2.1% | -0.09 |
| league:bra | 12 | +51.3% | 2.17 | 26 | -21.4% | -1.12 |
| league:cfb | 91 | +8.1% | 0.71 | 747 | +1.1% | 0.12 |
| league:cs2 | 184 | +15.4% | 2.28 | 20 | -7.0% | -0.26 |
| league:dota2 | 37 | +7.0% | 0.46 | 3 | -2.6% | -0.02 |
| league:epl | 26 | +87.1% | 4.5 | 19 | +36.7% | 1.54 |
| league:lal | 22 | -14.2% | -0.83 | 49 | -4.9% | -0.36 |
| league:mls | 148 | +12.5% | 1.46 | 62 | -27.2% | -2.5 |
| league:nba | 36 | -7.0% | -0.28 | 242 | -7.3% | -0.97 |
| league:nfl | 74 | +63.8% | 2.49 | 253 | -14.8% | -2.37 |
| league:nhl | 129 | +33.9% | 5.18 | 457 | -15.1% | -2.98 |
| league:sea | 36 | +33.1% | 2.76 | 48 | +5.3% | 0.63 |
| league:ucl | 54 | -4.0% | -0.12 | 32 | +36.5% | 1.12 |
| league:uel | 8 | +88.7% | 25.12 | 10 | +55.9% | 2.13 |
| league:wta | 91 | +44.1% | 1.44 | 292 | -18.3% | -2.85 |
| price:30-70c | 746 | +23.6% | 6.96 | 1802 | -4.8% | -1.92 |
| price:over 70c | 175 | +3.1% | 0.97 | 748 | +0.8% | 0.16 |
| price:under 30c | 133 | +51.2% | 1.94 | 728 | -13.9% | -1.98 |
| timing:in-play | 394 | +23.7% | 2.5 | 2878 | -5.8% | -2.55 |
| timing:pre-game | 660 | +24.0% | 6.54 | 400 | -4.5% | -0.77 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 131594 | 69010 | $1,306,270 | -50,902.54 | -3.9% | -12.05 |
| consistency (winning weeks), top 16 | 7232 | 3808 | $72,224 | -3,034.50 | -4.2% | -2.88 |
| consistency (winning weeks), top 40 | 19222 | 10149 | $192,199 | -6,834.97 | -3.6% | -4.09 |
| copy return, average, top 16 | 5394 | 2687 | $52,916 | -3,130.35 | -5.9% | -3.46 |
| copy return, average, top 40 | 18386 | 9289 | $182,423 | -9,104.90 | -5.0% | -5.78 |
| copy return, lower bound, top 16 | 7206 | 3712 | $70,905 | -4,378.18 | -6.2% | -4.60 |
| copy return, lower bound, top 40 | 22965 | 12400 | $227,670 | -10,876.65 | -4.8% | -6.46 |
| copy return, shrunk, top 16 | 6144 | 3062 | $60,394 | -3,747.62 | -6.2% | -3.96 |
| copy return, shrunk, top 40 | 19003 | 9581 | $188,415 | -9,271.09 | -4.9% | -5.76 |
| markout 2h, average, top 16 | 4767 | 2756 | $47,560 | -1,768.60 | -3.7% | -2.09 |
| markout 2h, average, top 40 | 13599 | 7225 | $136,433 | -4,247.37 | -3.1% | -2.83 |
| markout 2h, lower bound, top 16 | 6405 | 3587 | $63,984 | -2,288.11 | -3.6% | -2.41 |
| markout 2h, lower bound, top 40 | 19871 | 10808 | $198,479 | -8,115.34 | -4.1% | -4.90 |
| markout 30m, average, top 16 | 5540 | 3152 | $55,440 | -226.79 | -0.4% | -0.33 |
| markout 30m, average, top 40 | 17926 | 10077 | $179,249 | -4,416.67 | -2.5% | -2.86 |
| most active, top 16 | 24205 | 12790 | $239,436 | -13,901.62 | -5.8% | -7.87 |
| most active, top 40 | 43756 | 22747 | $433,839 | -22,176.11 | -5.1% | -9.20 |
| win rate vs the odds, top 16 | 3764 | 2020 | $36,970 | -1,446.00 | -3.9% | -2.15 |
| win rate vs the odds, top 40 | 14922 | 7791 | $148,264 | -6,002.45 | -4.0% | -4.09 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 36 | 30 | +51.5% | 3.44 | +5.07 |
| Kch-Temp | 186 | 107 | +13.8% | 1.83 | +1.51 |
| l..messi | 394 | 184 | +9.3% | 1.04 | +0.91 |
| strawberrycreek | 1074 | 655 | +13.1% | 4.22 | +1.25 |
| NS13 | 1148 | 449 | -1.3% | -0.31 | -0.16 |
| Maizuqiu | 649 | 306 | +11.7% | 1.59 | +1.12 |
| Car-c | 1121 | 585 | +5.2% | 1.08 | +0.50 |
| pltrkr111 | 958 | 535 | +2.6% | 0.82 | +0.28 |
| KaneAnalytics | 185 | 101 | +6.9% | 0.63 | +0.67 |
| 1l2ihj34li12u34 | 152 | 87 | +12.5% | 1.83 | +1.51 |
| yabanci | 136 | 76 | +6.2% | 0.65 | +0.73 |
| whosay | 604 | 326 | -2.9% | -0.67 | -0.31 |
| arahbo | 865 | 349 | +9.2% | 1.5 | +0.92 |
| 0xE16D3F2A5807999b358aFfD944 | 624 | 346 | -2.2% | -0.76 | -0.29 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 760 | 337 | +4.1% | 0.59 | +0.36 |
| User7429 | 933 | 500 | +0.6% | 0.11 | +0.04 |
| TearsInTheRain | 571 | 382 | +1.5% | 0.43 | +0.16 |
| 0xf9B5e9803Ea977b7111c9B7728 | 552 | 227 | +1.5% | 0.28 | +0.19 |
| timurdrevoz | 508 | 248 | +1.3% | 0.19 | +0.11 |
| juice-fruit | 75 | 49 | +4.3% | 0.54 | +0.54 |
| latvian.demon | 514 | 295 | +2.0% | 0.42 | +0.18 |
| AmericaFirst1 | 491 | 256 | +1.7% | 0.31 | +0.16 |
| redvinny | 539 | 421 | +3.3% | 1.22 | +0.33 |
| 0010001000001100 | 248 | 121 | +6.9% | 0.33 | +0.42 |
| 0x567212c82AAa6fe589bE5A2f4C | 420 | 220 | -1.1% | 0.24 | +0.16 |
| Lisanal-Gaib | 488 | 285 | +1.5% | 0.27 | +0.13 |
| carelia | 1172 | 558 | -2.8% | -0.84 | -0.29 |
| Petal | 746 | 374 | -2.0% | -0.48 | -0.21 |
| 13034431 | 334 | 157 | +3.1% | 0.37 | +0.29 |
| monkeymashingkeyboard | 1147 | 602 | +2.7% | 0.92 | +0.29 |
| primm | 633 | 277 | -4.1% | -0.68 | -0.37 |
| anontrader11 | 546 | 308 | +3.5% | 0.75 | +0.36 |
| dfdeath | 2147 | 1098 | -0.9% | -0.32 | -0.09 |
| 0xB8B95F31906f509d2a73eFF3d0 | 366 | 189 | -0.4% | -0.06 | -0.03 |
| skywalkerxx | 860 | 319 | -10.1% | -2.03 | -1.02 |
| Hugin-og-Munin | 462 | 262 | +2.2% | 0.41 | +0.21 |
| cosmicsteaks | 591 | 279 | +4.3% | 0.67 | +0.43 |
| vardaman-bundren | 434 | 209 | +1.4% | 0.24 | +0.14 |
| Bimboslaff | 618 | 292 | -2.5% | -0.47 | -0.23 |
| rossoftw | 712 | 360 | +1.8% | 0.35 | +0.16 |

## Esports specialists (copies on esports markets only)

3153 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 161 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| Tomahawkmaster | leaderboard | 12 | 5 | +86.1% | 1.23 | +0.0% (0) | +86.1% (12) | yes |
| CUTJALENHURTS | tag | 43 | 26 | +27.7% | 1.45 | +36.0% (33) | +2.1% (10) | no |
| Diabolical-Prize | current | 183 | 104 | +12.9% | 1.88 | +12.9% (183) | +0.0% (0) | no |
| Manchester4ever | tag | 154 | 99 | +13.9% | 1.93 | +19.4% (107) | +1.5% (47) | yes |
| sara341 | tag | 109 | 53 | +21.8% | 1.38 | +36.1% (41) | +13.2% (68) | yes |
| GoingStraightAhead | tag | 82 | 50 | +23.2% | 1.32 | +25.9% (53) | +18.1% (29) | yes |
| DrShredz | tag | 10 | 9 | +20.6% | 1.29 | +25.4% (6) | +13.3% (4) | yes |
| anontrader11 | tag | 205 | 118 | +12.0% | 1.57 | +51.0% (57) | -2.8% (148) | yes |
| growzizi | tag | 121 | 78 | +14.1% | 1.39 | +19.2% (62) | +8.8% (59) | yes |
| THEHIGHLIFE | tag | 117 | 61 | +14.2% | 1.31 | +15.2% (99) | +8.6% (18) | no |
| redvinny | tag | 59 | 52 | +8.9% | 1.49 | +1.9% (32) | +17.2% (27) | yes |
| juice-fruit | current | 31 | 21 | +17.4% | 1.08 | +28.5% (25) | -26.7% (6) | yes |
| .d-.-b. | tag | 42 | 23 | +21.9% | 1.03 | -30.0% (11) | +40.0% (31) | yes |
| asdfasdf333 | tag | 361 | 233 | +4.9% | 1.16 | +4.9% (361) | +0.0% (0) | no |
| 0x5974813b27CdE970e736AE3b55 | tag | 118 | 82 | +7.4% | 1.06 | +7.2% (109) | +10.1% (9) | yes |
| returdmaxxer | tag | 302 | 278 | +1.7% | 0.94 | +3.8% (213) | -3.3% (89) | yes |
| igot50k | tag | 232 | 124 | +9.8% | 0.87 | +12.0% (216) | -20.8% (16) | no |
| swaz13131313 | tag | 72 | 62 | +3.4% | 0.68 | +0.0% (0) | +3.4% (72) | yes |
| arahbo | tag | 206 | 109 | +7.6% | 0.83 | +2.4% (143) | +19.4% (63) | yes |
| vardaman-bundren | tag | 206 | 102 | +7.2% | 0.81 | +6.1% (154) | +10.3% (52) | yes |
| superlxj | tag | 144 | 98 | +4.7% | 0.74 | +4.7% (144) | +0.0% (0) | no |
| dfdeath | tag | 1148 | 595 | +2.2% | 0.53 | +2.8% (602) | +1.6% (546) | yes |
| Zzzz87 | tag | 107 | 72 | +6.5% | 0.74 | -8.6% (67) | +31.4% (40) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 242 | 128 | +4.0% | 0.67 | +8.5% (208) | -22.3% (34) | no |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 12 | 7 | +39.8% | 0.94 | +39.8% (12) | +0.0% (0) | no |
| 0xf9B5e9803Ea977b7111c9B7728 | tag | 293 | 151 | +3.4% | 0.61 | +16.9% (97) | -3.5% (196) | yes |
| chux.cc | leaderboard | 164 | 120 | +3.1% | 0.5 | +2.0% (139) | +8.8% (25) | no |
| asdfasdfasdf34 | tag | 482 | 299 | +0.7% | 0.23 | +0.7% (482) | +0.0% (0) | no |
| 0x6daae04265d65cb2aae7fe6db4 | tag | 87 | 55 | +7.0% | 0.69 | +4.6% (67) | +14.9% (20) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 80 | 53 | +6.2% | 0.65 | +3.6% (15) | +6.8% (65) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 633 | 277 | -4.1% | -0.68 | yes |
| Kch-Temp | 186 | 107 | +13.8% | 1.83 | yes |
| EdZachary | 175 | 68 | -8.3% | -1.01 | no |
| KaneAnalytics | 185 | 101 | +6.9% | 0.63 | yes |
| Jsram | 96 | 61 | +9.7% | 1.21 | no |
| Kkunn | 920 | 386 | +1.4% | 0.5 | no |
| Sisyphus- | 140 | 77 | -3.5% | -0.39 | no |
| PEYZ-BIGGEST-FAN | 299 | 147 | -9.7% | -1.46 | no |
| theowalcott | 95 | 51 | -0.3% | 0.16 | no |
| HVAB | 401 | 247 | -1.0% | -0.21 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 241 | 133 | +15.3% | 2.36 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 36 | 30 | +51.5% | 3.44 | yes |
| 0010001000001100 | 248 | 121 | +6.9% | 0.33 | yes |
| totoro3miyazaki | 50 | 31 | +6.5% | 0.52 | no |
| 1l2ihj34li12u34 | 152 | 87 | +12.5% | 1.83 | yes |
| yabanci | 136 | 76 | +6.2% | 0.65 | yes |
| 0x20D6436849F930584892730C7F | 123 | 70 | +31.4% | 1.89 | no |
| juice-fruit | 75 | 49 | +4.3% | 0.54 | yes |
| 0x16bb9951a36fce71e2ef57890b | 74 | 25 | -18.6% | -1.37 | no |
| GamblingOdyssey | 320 | 179 | +2.8% | 0.69 | no |
| plonker2026 | 120 | 58 | -9.9% | -0.72 | no |
| xxyx0xx | 231 | 109 | -6.6% | -0.72 | no |
| monkeymashingkeyboard | 1147 | 602 | +2.7% | 0.92 | yes |
| Tiger105 | 41 | 27 | +20.8% | 1.42 | no |
| THEHIGHLIFE | 146 | 66 | -0.2% | -0.06 | no |
| AmericaFirst1 | 491 | 256 | +1.7% | 0.31 | yes |
| UNEB3154s4f251 | 2121 | 1321 | +2.3% | 1.35 | no |
