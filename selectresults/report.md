# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-24 09:00 UTC: 5788 candidates, 3846 with trades copytop could copy, 236 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 369 | 192 | $3,654 | +24.15 | +0.7% | +0.19 |
| every wallet that qualified on the first part (test window) | 647 | 328 | $6,463 | -282.11 | -4.4% | -0.78 |
| currently copied (test window) | 3064 | 1527 | $29,928 | -604.60 | -2.0% | -0.73 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 369 | 192 | $3,654 | +24.15 | +0.7% | 0.19 | 1237 | 743 | $12,053 | +1,870.33 | +15.5% | 4.89 |
| copy their sells too | 369 | 144 | $3,654 | -64.40 | -1.8% | -0.2 | 1237 | 600 | $12,053 | +1,373.90 | +11.4% | 4.14 |
| size by conviction (x0.5 / x1 / x1.5) | 361 | 185 | $4,727 | +33.97 | +0.7% | -0.11 | 1192 | 703 | $15,195 | +2,022.90 | +13.3% | 4.06 |
| skip bets under 0.5x their usual | 354 | 183 | $3,509 | +11.72 | +0.3% | 0.11 | 1194 | 721 | $11,640 | +1,828.75 | +15.7% | 4.84 |
| pre-game only | 230 | 118 | $2,262 | +43.33 | +1.9% | 0.43 | 810 | 483 | $7,786 | +1,334.69 | +17.1% | 5.14 |
| skip prices under 30c | 343 | 185 | $3,381 | -128.52 | -3.8% | -0.57 | 1113 | 708 | $10,785 | +1,379.26 | +12.8% | 5.01 |
| favorites only (50c+) | 188 | 118 | $1,840 | -57.29 | -3.1% | -0.52 | 629 | 454 | $6,041 | +594.43 | +9.8% | 3.52 |
| 15s delay | 372 | 195 | $3,682 | -18.50 | -0.5% | 0.02 | 1237 | 748 | $12,049 | +1,806.60 | +15.0% | 4.93 |
| 60s delay | 369 | 192 | $3,654 | +24.15 | +0.7% | 0.19 | 1237 | 743 | $12,053 | +1,870.33 | +15.5% | 4.89 |
| allow 2c over their price | 387 | 204 | $3,834 | +52.27 | +1.4% | 0.31 | 1284 | 771 | $12,520 | +1,841.55 | +14.7% | 4.79 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 72 | +30.4% | 2.85 | 25 | -10.9% | -0.69 |
| conviction:1-2x | 59 | +74.5% | 3.64 | 28 | -12.0% | -0.61 |
| conviction:2x+ | 627 | +17.3% | 3.9 | 272 | +5.0% | 0.73 |
| conviction:under 0.5x | 110 | +14.4% | 1.8 | 44 | -11.1% | -0.58 |
| delay_move:flat | 582 | +28.1% | 5.89 | 236 | +3.4% | 0.62 |
| delay_move:price fell | 286 | +10.0% | 1.59 | 133 | -4.1% | -0.31 |
| exit:settle | 868 | +22.0% | 5.79 | 369 | +0.7% | 0.19 |
| kind:moneyline | 448 | +28.9% | 4.86 | 67 | -15.0% | -0.79 |
| kind:result | 257 | +12.5% | 2.36 | 173 | +11.0% | 1.41 |
| kind:totals | 163 | +18.0% | 2.15 | 129 | -4.9% | -0.66 |
| league:acle | 1 | +73.1% | — | 15 | -100.0% | — |
| league:bel1 | 4 | +41.0% | 0.84 | 15 | -4.2% | -0.16 |
| league:bra | 6 | -8.1% | -0.29 | 15 | -16.5% | -0.46 |
| league:bun | 6 | +47.1% | 112.33 | 6 | +87.9% | 48.16 |
| league:cfb | 90 | +7.5% | 0.66 | 3 | +15.9% | 0.12 |
| league:cs2 | 166 | +12.8% | 1.88 | 11 | -6.4% | -0.22 |
| league:dota2 | 37 | +7.0% | 0.46 | 1 | +13.9% | — |
| league:epl | 39 | +39.2% | 2.11 | 39 | +7.9% | 0.29 |
| league:ere | 34 | +21.5% | 0.94 | 29 | +47.8% | 2.72 |
| league:lal | 31 | -31.5% | -2.28 | 40 | +13.7% | 1.0 |
| league:mls | 89 | +20.3% | 1.57 | 21 | -11.9% | -0.67 |
| league:nba | 32 | +17.0% | 1.3 | 50 | +3.9% | 0.37 |
| league:nfl | 74 | +63.8% | 2.49 | 3 | +30.2% | 0.21 |
| league:nhl | 94 | +50.2% | 6.65 | 35 | -27.0% | -0.82 |
| league:sea | 58 | +22.6% | 2.15 | 39 | -6.8% | -0.27 |
| league:ucl | 73 | +0.6% | 0.35 | 34 | +4.2% | 0.02 |
| league:uel | 18 | +43.5% | 2.12 | 11 | +31.4% | 1.35 |
| price:30-70c | 636 | +23.0% | 6.28 | 286 | -3.6% | -0.42 |
| price:over 70c | 130 | +5.7% | 1.69 | 57 | -4.7% | -0.73 |
| price:under 30c | 102 | +35.7% | 1.61 | 26 | +55.9% | 0.94 |
| timing:in-play | 288 | +19.3% | 2.28 | 139 | -1.4% | -0.13 |
| timing:pre-game | 580 | +23.4% | 5.81 | 230 | +1.9% | 0.43 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 131651 | 68986 | $1,308,058 | -50,098.07 | -3.8% | -11.82 |
| consistency (winning weeks), top 16 | 6182 | 3103 | $61,776 | -3,696.49 | -6.0% | -4.08 |
| consistency (winning weeks), top 40 | 17764 | 9576 | $177,183 | -6,803.87 | -3.8% | -4.44 |
| copy return, average, top 16 | 3154 | 1604 | $31,524 | -1,157.15 | -3.7% | -1.47 |
| copy return, average, top 40 | 17135 | 8670 | $170,578 | -7,741.00 | -4.5% | -5.01 |
| copy return, lower bound, top 16 | 4798 | 2565 | $47,650 | -1,802.02 | -3.8% | -2.29 |
| copy return, lower bound, top 40 | 21145 | 11846 | $210,192 | -9,211.39 | -4.4% | -5.96 |
| copy return, shrunk, top 16 | 3705 | 1830 | $36,881 | -1,653.98 | -4.5% | -2.14 |
| copy return, shrunk, top 40 | 17667 | 8915 | $175,856 | -8,497.14 | -4.8% | -5.42 |
| markout 2h, average, top 16 | 4164 | 2245 | $41,744 | -914.54 | -2.2% | -1.13 |
| markout 2h, average, top 40 | 16038 | 8593 | $159,252 | -5,126.61 | -3.2% | -3.48 |
| markout 2h, lower bound, top 16 | 6550 | 3777 | $65,244 | -2,627.50 | -4.0% | -2.91 |
| markout 2h, lower bound, top 40 | 19279 | 10361 | $192,731 | -8,363.09 | -4.3% | -5.33 |
| markout 30m, average, top 16 | 5308 | 2890 | $53,247 | -254.22 | -0.5% | -0.37 |
| markout 30m, average, top 40 | 18737 | 10305 | $187,619 | -3,293.39 | -1.8% | -1.96 |
| most active, top 16 | 25082 | 13214 | $248,239 | -14,412.86 | -5.8% | -7.98 |
| most active, top 40 | 45196 | 23462 | $449,234 | -22,435.07 | -5.0% | -8.94 |
| win rate vs the odds, top 16 | 3320 | 1783 | $32,806 | -786.19 | -2.4% | -1.18 |
| win rate vs the odds, top 40 | 15329 | 7917 | $152,558 | -6,040.84 | -4.0% | -4.10 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 36 | 30 | +51.5% | 3.44 | +5.07 |
| Kch-Temp | 186 | 107 | +13.8% | 1.83 | +1.51 |
| THEHIGHLIFE | 147 | 67 | +0.7% | 0.03 | +0.03 |
| l..messi | 397 | 187 | +8.7% | 1.0 | +0.86 |
| Car-c | 1176 | 612 | +6.6% | 1.32 | +0.63 |
| strawberrycreek | 1110 | 669 | +12.2% | 3.94 | +1.17 |
| Maizuqiu | 809 | 392 | +12.5% | 1.95 | +1.21 |
| KaneAnalytics | 185 | 101 | +6.9% | 0.63 | +0.67 |
| pltrkr111 | 931 | 513 | +0.3% | 0.13 | +0.04 |
| 0xE16D3F2A5807999b358aFfD944 | 636 | 357 | -0.6% | -0.35 | -0.13 |
| whosay | 604 | 326 | -2.9% | -0.67 | -0.31 |
| 1l2ihj34li12u34 | 178 | 101 | +10.5% | 1.72 | +1.31 |
| arahbo | 863 | 348 | +8.8% | 1.43 | +0.87 |
| yabanci | 138 | 77 | +5.6% | 0.6 | +0.67 |
| Lisanal-Gaib | 499 | 292 | +1.7% | 0.32 | +0.15 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 742 | 327 | +3.4% | 0.47 | +0.29 |
| TearsInTheRain | 573 | 384 | +1.6% | 0.44 | +0.16 |
| User7429 | 936 | 501 | +0.2% | 0.03 | +0.01 |
| 0x567212c82AAa6fe589bE5A2f4C | 425 | 223 | -1.5% | 0.18 | +0.12 |
| latvian.demon | 529 | 304 | +2.4% | 0.51 | +0.21 |
| carelia | 1180 | 563 | -2.6% | -0.78 | -0.27 |
| redvinny | 541 | 421 | +2.9% | 1.08 | +0.29 |
| nibbio3 | 378 | 156 | +4.1% | 0.45 | +0.39 |
| Petal | 664 | 339 | +1.9% | 0.37 | +0.18 |
| monkeymashingkeyboard | 1169 | 612 | +2.6% | 0.86 | +0.27 |
| juice-fruit | 75 | 49 | +4.3% | 0.54 | +0.54 |
| skywalkerxx | 859 | 319 | -10.3% | -2.07 | -1.03 |
| timurdrevoz | 508 | 248 | +1.2% | 0.17 | +0.10 |
| 0010001000001100 | 250 | 121 | +6.0% | 0.27 | +0.33 |
| JAMJAMJAM4 | 1284 | 667 | -2.5% | -0.84 | -0.24 |
| 0xB8B95F31906f509d2a73eFF3d0 | 366 | 189 | -0.4% | -0.06 | -0.03 |
| AmericaFirst1 | 491 | 256 | +1.7% | 0.31 | +0.16 |
| anontrader11 | 573 | 322 | +3.2% | 0.7 | +0.33 |
| 0x58e8375623D848b1C154A073d0 | 560 | 287 | +1.6% | 0.28 | +0.15 |
| 13034431 | 372 | 175 | +1.4% | 0.18 | +0.14 |
| primm | 633 | 277 | -4.1% | -0.68 | -0.37 |
| dfdeath | 2185 | 1115 | -0.7% | -0.29 | -0.08 |
| astapzippo | 1040 | 478 | -1.8% | -0.77 | -0.30 |
| TRCM | 1891 | 975 | -5.7% | -1.92 | -0.56 |
| vardaman-bundren | 441 | 211 | +1.5% | 0.25 | +0.14 |

## Esports specialists (copies on esports markets only)

3169 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 161 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| CUTJALENHURTS | tag | 45 | 28 | +33.8% | 1.8 | +38.7% (35) | +17.9% (10) | yes |
| Diabolical-Prize | current | 183 | 104 | +12.9% | 1.88 | +12.9% (183) | +0.0% (0) | no |
| sara341 | tag | 109 | 53 | +21.8% | 1.38 | +29.9% (45) | +16.1% (64) | yes |
| Manchester4ever | tag | 157 | 100 | +12.4% | 1.76 | +19.4% (107) | -2.3% (50) | yes |
| Tomahawkmaster | leaderboard | 21 | 10 | +48.1% | 1.13 | +0.0% (0) | +48.1% (21) | yes |
| growzizi | tag | 123 | 80 | +15.0% | 1.5 | +22.9% (66) | +5.9% (57) | yes |
| DrShredz | tag | 10 | 9 | +20.6% | 1.29 | +25.4% (6) | +13.3% (4) | yes |
| THEHIGHLIFE | tag | 118 | 62 | +15.3% | 1.41 | +12.9% (101) | +30.2% (17) | yes |
| username122 | leaderboard | 85 | 49 | +20.0% | 1.25 | +0.0% (0) | +20.0% (85) | yes |
| anontrader11 | tag | 232 | 132 | +10.2% | 1.44 | +45.0% (65) | -3.3% (167) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 121 | 85 | +9.2% | 1.34 | +7.3% (110) | +27.4% (11) | yes |
| juice-fruit | current | 31 | 21 | +17.4% | 1.08 | +28.5% (25) | -26.7% (6) | yes |
| redvinny | tag | 60 | 52 | +7.2% | 1.16 | +1.9% (32) | +13.2% (28) | yes |
| Zzzz87 | tag | 110 | 75 | +9.7% | 1.08 | -10.0% (68) | +40.9% (42) | yes |
| asdfasdf333 | tag | 349 | 224 | +4.6% | 1.05 | +4.6% (349) | +0.0% (0) | no |
| ckryptoworker | tag | 83 | 45 | +14.1% | 1.0 | +15.0% (37) | +13.3% (46) | yes |
| returdmaxxer | tag | 298 | 274 | +1.7% | 0.89 | +3.8% (208) | -3.1% (90) | yes |
| igot50k | tag | 232 | 124 | +9.8% | 0.87 | +11.9% (218) | -24.1% (14) | no |
| swaz13131313 | tag | 72 | 62 | +3.4% | 0.68 | +0.0% (0) | +3.4% (72) | yes |
| superlxj | tag | 144 | 98 | +4.7% | 0.74 | +4.7% (144) | +0.0% (0) | no |
| chux.cc | leaderboard | 162 | 120 | +4.0% | 0.63 | +1.3% (135) | +17.4% (27) | yes |
| vardaman-bundren | tag | 207 | 102 | +6.7% | 0.75 | +5.5% (155) | +10.3% (52) | yes |
| 0x6daae04265d65cb2aae7fe6db4 | tag | 88 | 56 | +7.6% | 0.76 | +11.3% (70) | -6.7% (18) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 12 | 7 | +39.8% | 0.94 | +39.8% (12) | +0.0% (0) | no |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 241 | 127 | +4.0% | 0.66 | +7.9% (208) | -20.0% (33) | no |
| dfdeath | tag | 1167 | 601 | +1.6% | 0.36 | +3.0% (612) | -0.1% (555) | yes |
| 0x45EEcadDA7Cfa2a2891aC6344D | tag | 163 | 71 | +8.1% | 0.75 | +8.0% (114) | +8.2% (49) | yes |
| arahbo | tag | 206 | 109 | +6.3% | 0.69 | +0.9% (142) | +18.3% (64) | yes |
| asdfasdfasdf34 | tag | 479 | 296 | +0.4% | 0.14 | +0.4% (479) | +0.0% (0) | no |
| Lisanal-Gaib | tag | 499 | 292 | +1.7% | 0.32 | -0.9% (350) | +7.9% (149) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 633 | 277 | -4.1% | -0.68 | yes |
| Kch-Temp | 186 | 107 | +13.8% | 1.83 | yes |
| EdZachary | 181 | 68 | -11.2% | -1.35 | no |
| KaneAnalytics | 185 | 101 | +6.9% | 0.63 | yes |
| Jsram | 96 | 61 | +9.7% | 1.21 | no |
| Kkunn | 920 | 386 | +1.4% | 0.5 | no |
| Sisyphus- | 145 | 79 | -3.9% | -0.45 | no |
| PEYZ-BIGGEST-FAN | 300 | 147 | -10.1% | -1.51 | no |
| theowalcott | 95 | 51 | -0.3% | 0.16 | no |
| HVAB | 402 | 246 | -2.1% | -0.43 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 241 | 133 | +15.3% | 2.36 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 36 | 30 | +51.5% | 3.44 | yes |
| 0010001000001100 | 250 | 121 | +6.0% | 0.27 | yes |
| totoro3miyazaki | 50 | 31 | +6.5% | 0.52 | no |
| 1l2ihj34li12u34 | 178 | 101 | +10.5% | 1.72 | yes |
| yabanci | 138 | 77 | +5.6% | 0.6 | yes |
| 0x20D6436849F930584892730C7F | 123 | 70 | +31.4% | 1.89 | no |
| juice-fruit | 75 | 49 | +4.3% | 0.54 | yes |
| 0x16bb9951a36fce71e2ef57890b | 74 | 25 | -18.6% | -1.37 | no |
| GamblingOdyssey | 323 | 180 | +2.4% | 0.61 | no |
| plonker2026 | 158 | 82 | +5.3% | 0.94 | no |
| xxyx0xx | 233 | 111 | -6.3% | -0.69 | no |
| monkeymashingkeyboard | 1169 | 612 | +2.6% | 0.86 | yes |
| Tiger105 | 41 | 27 | +20.8% | 1.42 | no |
| THEHIGHLIFE | 147 | 67 | +0.7% | 0.03 | yes |
| AmericaFirst1 | 491 | 256 | +1.7% | 0.31 | yes |
| UNEB3154s4f251 | 2130 | 1324 | +2.1% | 1.21 | no |
