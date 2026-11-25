# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-25 09:00 UTC: 5785 candidates, 3850 with trades copytop could copy, 236 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 307 | 164 | $3,056 | +33.59 | +1.1% | +0.27 |
| every wallet that qualified on the first part (test window) | 2407 | 1189 | $24,041 | -397.25 | -1.7% | -0.63 |
| currently copied (test window) | 3124 | 1568 | $30,428 | -423.93 | -1.4% | -0.45 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 307 | 164 | $3,056 | +33.59 | +1.1% | 0.27 | 1140 | 704 | $11,067 | +1,956.30 | +17.7% | 5.6 |
| copy their sells too | 307 | 158 | $3,056 | -26.04 | -0.9% | -0.02 | 1140 | 689 | $11,067 | +1,823.32 | +16.5% | 5.3 |
| size by conviction (x0.5 / x1 / x1.5) | 300 | 157 | $3,838 | +13.24 | +0.4% | -0.05 | 1090 | 659 | $13,465 | +2,096.14 | +15.6% | 4.77 |
| skip bets under 0.5x their usual | 295 | 158 | $2,934 | +43.07 | +1.5% | 0.31 | 1103 | 683 | $10,750 | +1,922.94 | +17.9% | 5.5 |
| pre-game only | 246 | 131 | $2,442 | -6.54 | -0.3% | 0.09 | 936 | 585 | $9,015 | +1,529.78 | +17.0% | 5.73 |
| skip prices under 30c | 293 | 160 | $2,910 | -53.03 | -1.8% | -0.18 | 1052 | 683 | $10,166 | +1,734.15 | +17.1% | 6.47 |
| favorites only (50c+) | 163 | 109 | $1,606 | +146.32 | +9.1% | 1.46 | 601 | 447 | $5,772 | +1,115.09 | +19.3% | 6.63 |
| 15s delay | 314 | 168 | $3,127 | -26.61 | -0.9% | -0.03 | 1148 | 710 | $11,148 | +1,920.34 | +17.2% | 5.65 |
| 60s delay | 307 | 164 | $3,056 | +33.59 | +1.1% | 0.27 | 1140 | 704 | $11,067 | +1,956.30 | +17.7% | 5.6 |
| allow 2c over their price | 319 | 172 | $3,176 | +51.52 | +1.6% | 0.36 | 1168 | 720 | $11,346 | +1,942.02 | +17.1% | 5.53 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 87 | +21.4% | 2.65 | 20 | -5.3% | -0.27 |
| conviction:1-2x | 74 | +57.9% | 3.82 | 25 | +22.8% | 1.02 |
| conviction:2x+ | 557 | +20.3% | 4.33 | 215 | +2.1% | 0.34 |
| conviction:under 0.5x | 115 | +21.3% | 2.42 | 47 | -12.8% | -0.75 |
| delay_move:flat | 656 | +28.4% | 6.61 | 236 | +3.0% | 0.56 |
| delay_move:price fell | 177 | +8.2% | 1.2 | 71 | -5.2% | -0.23 |
| exit:settle | 833 | +24.0% | 6.43 | 307 | +1.1% | 0.27 |
| kind:moneyline | 487 | +27.8% | 4.97 | 91 | -19.5% | -1.27 |
| kind:result | 203 | +25.4% | 4.52 | 149 | +3.4% | 0.64 |
| kind:totals | 143 | +9.1% | 1.41 | 67 | +23.7% | 1.99 |
| league:acle | 1 | +73.1% | — | 17 | -100.0% | — |
| league:atp | 10 | +1.3% | 0.12 | 10 | -15.1% | -0.44 |
| league:bel1 | 4 | +41.0% | 0.84 | 15 | -4.2% | -0.16 |
| league:bra | 7 | +106.5% | 37.76 | 7 | +23.5% | 0.7 |
| league:cfb | 92 | +8.7% | 0.76 | 3 | +15.9% | 0.12 |
| league:cs2 | 193 | +15.2% | 2.32 | 16 | -29.0% | -1.29 |
| league:dota2 | 37 | +7.0% | 0.46 | 4 | +13.5% | 0.36 |
| league:epl | 108 | +17.9% | 2.05 | 40 | +26.9% | 1.68 |
| league:ere | 6 | -73.1% | -2.64 | 19 | +26.8% | 1.38 |
| league:lal | 8 | -76.6% | -3.22 | 20 | +36.6% | 1.72 |
| league:mls | 47 | +11.2% | 1.05 | 8 | -53.2% | -1.72 |
| league:nba | 40 | +25.1% | 2.11 | 45 | -8.8% | -0.6 |
| league:nfl | 80 | +57.1% | 2.39 | 8 | -0.9% | -0.03 |
| league:nhl | 93 | +47.5% | 6.21 | 34 | -24.9% | -0.74 |
| league:sea | 14 | +83.1% | 5.88 | 20 | +13.6% | 0.89 |
| league:ucl | 74 | +12.0% | 1.52 | 22 | +26.4% | 1.25 |
| league:uel | 8 | +88.7% | 25.12 | 9 | +74.9% | 3.21 |
| price:30-70c | 684 | +25.1% | 7.34 | 264 | -3.7% | -0.45 |
| price:over 70c | 71 | +17.1% | 5.51 | 29 | +15.4% | 2.47 |
| price:under 30c | 78 | +20.9% | 0.79 | 14 | +59.2% | 0.67 |
| timing:in-play | 143 | +26.9% | 1.91 | 61 | +6.5% | 0.31 |
| timing:pre-game | 690 | +23.4% | 6.67 | 246 | -0.3% | 0.09 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 131531 | 68959 | $1,306,577 | -53,453.02 | -4.1% | -12.59 |
| consistency (winning weeks), top 16 | 7341 | 3813 | $73,102 | -3,237.75 | -4.4% | -3.30 |
| consistency (winning weeks), top 40 | 18719 | 10045 | $186,553 | -8,732.63 | -4.7% | -5.75 |
| copy return, average, top 16 | 3982 | 1931 | $39,783 | -1,014.65 | -2.5% | -1.16 |
| copy return, average, top 40 | 17466 | 9133 | $173,930 | -6,113.05 | -3.5% | -3.98 |
| copy return, lower bound, top 16 | 5960 | 3239 | $59,073 | -2,096.07 | -3.5% | -2.61 |
| copy return, lower bound, top 40 | 23199 | 12890 | $229,902 | -9,127.00 | -4.0% | -5.53 |
| copy return, shrunk, top 16 | 5155 | 2563 | $51,517 | -2,209.31 | -4.3% | -2.50 |
| copy return, shrunk, top 40 | 18727 | 9766 | $186,653 | -5,996.81 | -3.2% | -3.77 |
| markout 2h, average, top 16 | 5626 | 3136 | $56,277 | -1,629.53 | -2.9% | -1.91 |
| markout 2h, average, top 40 | 14905 | 7899 | $147,903 | -5,197.17 | -3.5% | -3.77 |
| markout 2h, lower bound, top 16 | 6426 | 3798 | $63,945 | -2,027.52 | -3.2% | -2.43 |
| markout 2h, lower bound, top 40 | 22795 | 12134 | $226,425 | -10,567.93 | -4.7% | -6.30 |
| markout 30m, average, top 16 | 5530 | 3070 | $55,379 | -382.83 | -0.7% | -0.50 |
| markout 30m, average, top 40 | 16414 | 8953 | $164,430 | -4,808.03 | -2.9% | -3.13 |
| most active, top 16 | 24883 | 13177 | $246,186 | -13,744.86 | -5.6% | -7.56 |
| most active, top 40 | 47635 | 24646 | $472,556 | -23,519.24 | -5.0% | -9.14 |
| win rate vs the odds, top 16 | 4189 | 2322 | $41,448 | -176.89 | -0.4% | -0.24 |
| win rate vs the odds, top 40 | 16102 | 8504 | $160,337 | -5,457.38 | -3.4% | -3.64 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 27 | 21 | +33.3% | 1.78 | +3.24 |
| Kch-Temp | 186 | 111 | +15.2% | 1.98 | +1.60 |
| THEHIGHLIFE | 149 | 68 | +0.6% | 0.03 | +0.03 |
| strawberrycreek | 1147 | 702 | +13.9% | 4.59 | +1.33 |
| l..messi | 421 | 193 | +5.0% | 0.61 | +0.49 |
| 1l2ihj34li12u34 | 195 | 114 | +13.1% | 2.2 | +1.57 |
| Maizuqiu | 852 | 406 | +9.3% | 1.51 | +0.90 |
| pltrkr111 | 918 | 520 | +3.4% | 1.08 | +0.37 |
| 0xE16D3F2A5807999b358aFfD944 | 652 | 363 | -1.0% | -0.48 | -0.18 |
| whosay | 604 | 326 | -2.9% | -0.67 | -0.31 |
| Lisanal-Gaib | 506 | 299 | +2.5% | 0.48 | +0.22 |
| arahbo | 858 | 343 | +8.5% | 1.38 | +0.85 |
| yabanci | 145 | 82 | +5.8% | 0.64 | +0.68 |
| Car-c | 1418 | 727 | +2.4% | 0.53 | +0.21 |
| KaneAnalytics | 185 | 101 | +6.9% | 0.63 | +0.67 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 644 | 274 | +2.6% | 0.3 | +0.21 |
| TearsInTheRain | 581 | 389 | +1.5% | 0.44 | +0.16 |
| latvian.demon | 557 | 322 | +3.0% | 0.69 | +0.28 |
| User7429 | 904 | 477 | -0.8% | -0.22 | -0.09 |
| monkeymashingkeyboard | 1184 | 626 | +3.6% | 1.23 | +0.38 |
| JAMJAMJAM4 | 1248 | 654 | -1.7% | -0.6 | -0.17 |
| juice-fruit | 77 | 50 | +5.1% | 0.61 | +0.61 |
| timurdrevoz | 511 | 251 | +1.8% | 0.26 | +0.16 |
| redvinny | 543 | 423 | +2.9% | 1.09 | +0.29 |
| astapzippo | 1048 | 482 | -1.8% | -0.77 | -0.30 |
| anontrader11 | 603 | 336 | +2.9% | 0.64 | +0.30 |
| WagerWizard | 435 | 277 | +5.2% | 0.99 | +0.52 |
| skywalkerxx | 853 | 314 | -11.2% | -2.24 | -1.12 |
| carelia | 1150 | 541 | -3.3% | -0.96 | -0.34 |
| TRCM | 1838 | 945 | -5.6% | -1.86 | -0.55 |
| 0x58e8375623D848b1C154A073d0 | 588 | 302 | +1.0% | 0.19 | +0.10 |
| 0x724924919B3d684cE0400BC307 | 1183 | 724 | -8.0% | -3.21 | -0.77 |
| 0x567212c82AAa6fe589bE5A2f4C | 439 | 227 | -3.5% | -0.13 | -0.08 |
| dfdeath | 2249 | 1141 | -0.8% | -0.34 | -0.09 |
| growzizi | 524 | 298 | +0.2% | 0.03 | +0.02 |
| cosmicsteaks | 622 | 286 | +3.8% | 0.6 | +0.38 |
| 13034431 | 404 | 190 | +0.3% | 0.06 | +0.04 |
| SHLDota | 537 | 339 | -7.6% | -2.19 | -0.73 |
| tensec | 1211 | 678 | -0.5% | 0.03 | +0.01 |
| pauleta231 | 561 | 254 | -0.1% | -0.0 | -0.00 |

## Esports specialists (copies on esports markets only)

3166 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 162 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| hedgevaultmainnet1 | leaderboard | 10 | 10 | +66.3% | 3.7 | +0.0% (0) | +66.3% (10) | yes |
| Tomahawkmaster | leaderboard | 23 | 12 | +52.8% | 1.37 | +0.0% (0) | +52.8% (23) | yes |
| fg383dgjdflk2 | tag | 97 | 50 | +24.3% | 1.69 | +0.0% (0) | +24.3% (97) | yes |
| CUTJALENHURTS | tag | 45 | 27 | +28.9% | 1.53 | +36.4% (34) | +7.4% (11) | yes |
| Diabolical-Prize | current | 183 | 104 | +12.9% | 1.88 | +12.9% (183) | +0.0% (0) | no |
| Manchester4ever | tag | 159 | 102 | +12.9% | 1.85 | +19.3% (107) | -0.2% (52) | yes |
| username122 | leaderboard | 99 | 58 | +20.0% | 1.43 | +46.9% (1) | +19.7% (98) | yes |
| THEHIGHLIFE | tag | 119 | 63 | +15.9% | 1.48 | +12.9% (103) | +36.5% (16) | yes |
| growzizi | tag | 124 | 81 | +15.2% | 1.53 | +25.7% (70) | +1.5% (54) | yes |
| DrShredz | tag | 10 | 9 | +20.6% | 1.29 | +25.4% (6) | +13.3% (4) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 123 | 87 | +9.9% | 1.47 | +6.7% (112) | +42.5% (11) | yes |
| Zzzz87 | tag | 108 | 75 | +11.8% | 1.29 | -1.5% (67) | +33.2% (41) | yes |
| anontrader11 | tag | 260 | 145 | +9.0% | 1.33 | +34.0% (84) | -3.0% (176) | yes |
| sara341 | tag | 113 | 53 | +17.4% | 1.13 | +37.6% (50) | +1.5% (63) | yes |
| juice-fruit | current | 31 | 21 | +17.4% | 1.08 | +28.8% (27) | -56.0% (4) | yes |
| redvinny | tag | 61 | 53 | +7.2% | 1.19 | +3.2% (34) | +12.3% (27) | yes |
| returdmaxxer | tag | 291 | 268 | +1.9% | 1.01 | +3.2% (205) | -1.2% (86) | yes |
| asdfasdf333 | tag | 343 | 219 | +4.2% | 0.95 | +4.2% (343) | +0.0% (0) | no |
| swaz13131313 | tag | 75 | 65 | +3.7% | 0.79 | +0.0% (0) | +3.7% (75) | yes |
| igot50k | tag | 232 | 124 | +9.8% | 0.87 | +11.9% (222) | -38.7% (10) | no |
| chux.cc | leaderboard | 157 | 118 | +4.5% | 0.75 | +1.9% (130) | +17.4% (27) | yes |
| ckryptoworker | tag | 86 | 46 | +12.2% | 0.89 | +8.4% (43) | +16.0% (43) | yes |
| superlxj | tag | 144 | 98 | +4.7% | 0.74 | +4.7% (144) | +0.0% (0) | no |
| latvian.demon | tag | 114 | 69 | +7.1% | 0.79 | +11.5% (67) | +0.8% (47) | yes |
| Lisanal-Gaib | tag | 506 | 299 | +2.5% | 0.48 | -0.9% (356) | +10.3% (150) | yes |
| 0x6daae04265d65cb2aae7fe6db4 | tag | 88 | 56 | +7.6% | 0.76 | +9.7% (71) | -1.2% (17) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 12 | 7 | +39.8% | 0.94 | +39.8% (12) | +0.0% (0) | no |
| 0x45EEcadDA7Cfa2a2891aC6344D | tag | 163 | 71 | +8.1% | 0.75 | +10.4% (116) | +2.2% (47) | yes |
| dfdeath | tag | 1191 | 612 | +1.4% | 0.31 | +2.3% (621) | +0.4% (570) | yes |
| asdfasdfasdf34 | tag | 479 | 296 | +0.4% | 0.14 | +0.4% (479) | +0.0% (0) | no |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 640 | 277 | -5.2% | -0.89 | no |
| Kch-Temp | 186 | 111 | +15.2% | 1.98 | yes |
| EdZachary | 188 | 75 | -3.6% | -0.5 | no |
| KaneAnalytics | 185 | 101 | +6.9% | 0.63 | yes |
| Jsram | 147 | 96 | +10.8% | 1.57 | no |
| Kkunn | 920 | 386 | +1.4% | 0.5 | no |
| Sisyphus- | 151 | 81 | -6.0% | -0.73 | no |
| PEYZ-BIGGEST-FAN | 300 | 147 | -10.1% | -1.51 | no |
| theowalcott | 73 | 48 | +19.7% | 2.09 | no |
| HVAB | 393 | 240 | -2.8% | -0.57 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 242 | 133 | +14.8% | 2.3 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 27 | 21 | +33.3% | 1.78 | yes |
| 0010001000001100 | 487 | 233 | -5.6% | -0.96 | no |
| totoro3miyazaki | 62 | 39 | +12.6% | 1.0 | no |
| 1l2ihj34li12u34 | 195 | 114 | +13.1% | 2.2 | yes |
| yabanci | 145 | 82 | +5.8% | 0.64 | yes |
| 0x20D6436849F930584892730C7F | 123 | 70 | +31.4% | 1.89 | no |
| juice-fruit | 77 | 50 | +5.1% | 0.61 | yes |
| 0x16bb9951a36fce71e2ef57890b | 74 | 25 | -18.6% | -1.37 | no |
| GamblingOdyssey | 320 | 177 | +1.4% | 0.44 | no |
| plonker2026 | 281 | 131 | -7.1% | -0.78 | no |
| xxyx0xx | 277 | 131 | -11.6% | -1.41 | no |
| monkeymashingkeyboard | 1184 | 626 | +3.6% | 1.23 | yes |
| Tiger105 | 41 | 28 | +27.0% | 1.84 | no |
| THEHIGHLIFE | 149 | 68 | +0.6% | 0.03 | yes |
| AmericaFirst1 | 498 | 258 | +1.2% | 0.21 | no |
| UNEB3154s4f251 | 2117 | 1326 | +2.2% | 1.29 | no |
