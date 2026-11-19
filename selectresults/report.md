# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-19 09:00 UTC: 5609 candidates, 3667 with trades copytop could copy, 236 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2962 | 1445 | $29,129 | -1,693.84 | -5.8% | -2.59 |
| every wallet that qualified on the first part (test window) | 3745 | 1820 | $37,049 | -2,722.31 | -7.3% | -3.65 |
| currently copied (test window) | 3551 | 1785 | $34,658 | -1,867.40 | -5.4% | -2.69 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2962 | 1445 | $29,129 | -1,693.84 | -5.8% | -2.59 | 6230 | 3144 | $61,552 | +2,046.75 | +3.3% | 2.46 |
| copy their sells too | 2962 | 1289 | $29,129 | -1,829.54 | -6.3% | -3.07 | 6230 | 2820 | $61,552 | +854.30 | +1.4% | 1.31 |
| size by conviction (x0.5 / x1 / x1.5) | 2837 | 1376 | $35,844 | -1,915.43 | -5.3% | -2.75 | 6022 | 3021 | $76,029 | +2,236.39 | +2.9% | 2.18 |
| skip bets under 0.5x their usual | 2904 | 1421 | $28,584 | -1,583.42 | -5.5% | -2.43 | 6066 | 3076 | $60,022 | +1,980.21 | +3.3% | 2.39 |
| pre-game only | 2576 | 1275 | $25,235 | -1,311.96 | -5.2% | -2.24 | 5224 | 2654 | $51,407 | +1,723.70 | +3.4% | 2.37 |
| skip prices under 30c | 2562 | 1385 | $25,033 | -399.55 | -1.6% | -0.63 | 5266 | 2930 | $51,688 | +2,087.06 | +4.0% | 3.19 |
| favorites only (50c+) | 1444 | 903 | $13,926 | -242.99 | -1.7% | -0.72 | 2646 | 1718 | $25,582 | +316.50 | +1.2% | 0.93 |
| 15s delay | 2988 | 1459 | $29,389 | -1,671.14 | -5.7% | -2.52 | 6278 | 3171 | $62,023 | +1,981.21 | +3.2% | 2.41 |
| 60s delay | 2962 | 1445 | $29,129 | -1,693.84 | -5.8% | -2.59 | 6230 | 3144 | $61,552 | +2,046.75 | +3.3% | 2.46 |
| allow 2c over their price | 3281 | 1613 | $32,351 | -1,493.01 | -4.6% | -2.13 | 6880 | 3466 | $68,091 | +2,319.20 | +3.4% | 2.63 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 417 | +17.2% | 2.53 | 415 | -13.2% | -2.6 |
| conviction:1-2x | 585 | +13.7% | 2.5 | 531 | -9.3% | -1.56 |
| conviction:2x+ | 2012 | +9.0% | 3.31 | 1842 | -2.9% | -1.04 |
| conviction:under 0.5x | 254 | +17.0% | 2.18 | 174 | -8.3% | -0.68 |
| delay_move:flat | 2247 | +14.6% | 5.46 | 2191 | -5.0% | -1.92 |
| delay_move:price fell | 1021 | +4.9% | 1.28 | 770 | -7.9% | -1.78 |
| exit:settle | 3268 | +11.5% | 5.27 | 2962 | -5.8% | -2.59 |
| kind:moneyline | 2225 | +12.1% | 4.33 | 1499 | -4.9% | -1.41 |
| kind:result | 722 | +7.7% | 2.06 | 556 | -1.5% | -0.16 |
| kind:totals | 321 | +16.4% | 2.36 | 907 | -10.0% | -2.82 |
| league:acle | 1 | +73.1% | — | 15 | -100.0% | — |
| league:atp | 866 | +5.2% | 1.21 | 525 | -16.8% | -3.13 |
| league:bel1 | 2 | +18.2% | 0.17 | 13 | +20.9% | 0.73 |
| league:bra | 12 | +51.1% | 2.16 | 21 | -22.4% | -1.11 |
| league:bun | 20 | +51.5% | 2.62 | 9 | -38.4% | -1.54 |
| league:cfb | 114 | -4.2% | -0.22 | 15 | +7.8% | 0.03 |
| league:cs2 | 193 | +13.4% | 2.0 | 24 | +8.1% | 0.23 |
| league:dota2 | 45 | -7.1% | -0.48 | 1 | +13.9% | — |
| league:epl | 65 | +43.9% | 1.89 | 62 | +2.6% | 0.04 |
| league:ere | 21 | +92.1% | 3.7 | 33 | +8.5% | 0.32 |
| league:lal | 94 | -11.1% | -1.06 | 97 | -12.3% | -1.07 |
| league:mls | 344 | +6.5% | 1.08 | 205 | -11.0% | -1.65 |
| league:nba | 23 | +12.9% | 0.54 | 971 | -7.1% | -2.12 |
| league:nfl | 201 | +37.4% | 2.95 | 62 | +10.5% | 0.87 |
| league:nhl | 122 | +21.8% | 2.69 | 50 | +24.4% | 2.57 |
| league:sea | 210 | +2.1% | 0.55 | 198 | +10.3% | 0.96 |
| league:spl | 7 | +85.8% | 3.44 | 3 | -63.2% | -1.69 |
| league:ucl | 166 | +13.1% | 1.35 | 206 | -7.2% | -0.8 |
| league:uel | 20 | +6.3% | 0.33 | 61 | +8.2% | 0.88 |
| league:wta | 737 | +13.5% | 2.68 | 388 | +2.1% | 0.55 |
| price:30-70c | 2399 | +9.4% | 4.51 | 2230 | -2.8% | -1.08 |
| price:over 70c | 294 | +8.2% | 3.37 | 325 | +3.5% | 1.39 |
| price:under 30c | 575 | +21.7% | 2.56 | 407 | -28.6% | -3.26 |
| timing:in-play | 620 | +11.3% | 1.9 | 386 | -9.8% | -1.32 |
| timing:pre-game | 2648 | +11.6% | 4.98 | 2576 | -5.2% | -2.24 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 130459 | 68448 | $1,295,422 | -53,134.05 | -4.1% | -12.71 |
| consistency (winning weeks), top 16 | 5434 | 2659 | $54,369 | -2,582.53 | -4.8% | -2.47 |
| consistency (winning weeks), top 40 | 17143 | 8795 | $170,679 | -6,207.92 | -3.6% | -3.84 |
| copy return, average, top 16 | 4588 | 2493 | $45,003 | -1,884.84 | -4.2% | -2.21 |
| copy return, average, top 40 | 17519 | 8887 | $173,937 | -7,957.67 | -4.6% | -4.93 |
| copy return, lower bound, top 16 | 6348 | 3409 | $61,826 | -2,547.54 | -4.1% | -2.90 |
| copy return, lower bound, top 40 | 21301 | 11629 | $211,192 | -8,826.65 | -4.2% | -5.35 |
| copy return, shrunk, top 16 | 4978 | 2576 | $49,078 | -2,461.33 | -5.0% | -2.58 |
| copy return, shrunk, top 40 | 17896 | 9053 | $177,744 | -8,244.51 | -4.6% | -5.02 |
| markout 2h, average, top 16 | 5131 | 2821 | $51,077 | -2,172.28 | -4.2% | -2.36 |
| markout 2h, average, top 40 | 15767 | 8292 | $157,692 | -4,591.28 | -2.9% | -2.73 |
| markout 2h, lower bound, top 16 | 7437 | 4048 | $73,979 | -2,935.75 | -4.0% | -2.88 |
| markout 2h, lower bound, top 40 | 20553 | 11075 | $204,779 | -8,634.71 | -4.2% | -5.21 |
| markout 30m, average, top 16 | 7039 | 3977 | $70,028 | -2,232.08 | -3.2% | -2.27 |
| markout 30m, average, top 40 | 20282 | 11263 | $202,602 | -3,745.16 | -1.8% | -2.24 |
| most active, top 16 | 26471 | 14262 | $261,852 | -13,084.75 | -5.0% | -7.30 |
| most active, top 40 | 46525 | 24593 | $460,043 | -21,711.96 | -4.7% | -8.90 |
| win rate vs the odds, top 16 | 3475 | 1912 | $33,992 | -706.39 | -2.1% | -1.05 |
| win rate vs the odds, top 40 | 16560 | 8655 | $164,608 | -6,790.61 | -4.1% | -4.20 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 36 | 31 | +54.9% | 3.82 | +5.41 |
| Kch-Temp | 185 | 107 | +14.4% | 1.9 | +1.57 |
| l..messi | 426 | 202 | +13.0% | 1.4 | +1.26 |
| yabanci | 121 | 72 | +13.9% | 1.21 | +1.49 |
| arahbo | 785 | 319 | +10.3% | 1.56 | +1.02 |
| NS13 | 1164 | 457 | -1.1% | -0.28 | -0.14 |
| strawberrycreek | 911 | 536 | +9.2% | 2.64 | +0.86 |
| Car-c | 1324 | 693 | +3.5% | 0.81 | +0.34 |
| KaneAnalytics | 181 | 98 | +5.7% | 0.53 | +0.56 |
| 0xE16D3F2A5807999b358aFfD944 | 598 | 338 | -1.2% | -0.49 | -0.19 |
| carelia | 1201 | 572 | -2.9% | -0.85 | -0.29 |
| yoooogo | 593 | 330 | -1.9% | -0.35 | -0.15 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 899 | 399 | +4.6% | 0.76 | +0.42 |
| cosmicsteaks | 576 | 272 | +5.4% | 0.81 | +0.53 |
| anontrader11 | 503 | 284 | +5.1% | 1.0 | +0.52 |
| whosay | 589 | 314 | -3.8% | -0.88 | -0.40 |
| timurdrevoz | 493 | 241 | +2.7% | 0.39 | +0.24 |
| skywalkerxx | 897 | 331 | -10.8% | -2.22 | -1.08 |
| 0x16bb9951a36fce71e2ef57890b | 69 | 24 | -16.0% | -1.14 | -1.66 |
| pltrkr111 | 1001 | 564 | +5.4% | 1.56 | +0.54 |
| rossoftw | 618 | 317 | +2.9% | 0.54 | +0.27 |
| seeyouanymore | 499 | 252 | -5.4% | -0.73 | -0.52 |
| 0x567212c82AAa6fe589bE5A2f4C | 409 | 214 | +0.1% | 0.41 | +0.28 |
| juice-fruit | 70 | 46 | +4.8% | 0.57 | +0.59 |
| OVER955 | 646 | 578 | +1.9% | 1.09 | +0.19 |
| TearsInTheRain | 582 | 391 | +1.7% | 0.48 | +0.17 |
| User7429 | 942 | 503 | -1.1% | -0.3 | -0.11 |
| Lisanal-Gaib | 479 | 275 | -0.4% | -0.14 | -0.07 |
| TRCM | 2172 | 1108 | -5.7% | -2.04 | -0.56 |
| 0x5fD2D9C60781D711721145Ff2b | 690 | 379 | -4.5% | -0.97 | -0.44 |
| 0xf9B5e9803Ea977b7111c9B7728 | 523 | 215 | +3.1% | 0.5 | +0.35 |
| LonnieHawkinss | 236 | 152 | +8.3% | 0.95 | +0.78 |
| Kkunn | 920 | 386 | +1.4% | 0.5 | +0.24 |
| nibbio3 | 373 | 159 | +3.2% | 0.38 | +0.32 |
| vardaman-bundren | 414 | 199 | +1.3% | 0.2 | +0.12 |
| dfdeath | 2020 | 1032 | -1.1% | -0.41 | -0.12 |
| F-812 | 828 | 454 | +0.1% | 0.01 | +0.00 |
| WagerWizard | 573 | 329 | -1.1% | -0.2 | -0.10 |
| ludo-money | 821 | 470 | -1.4% | -0.33 | -0.12 |
| Manchester4ever | 1108 | 621 | +1.2% | 0.41 | +0.12 |

## Esports specialists (copies on esports markets only)

2988 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 158 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| oxbus | leaderboard | 42 | 24 | +96.3% | 2.8 | +18.1% (16) | +143.7% (26) | yes |
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 19 | 12 | +55.9% | 2.02 | +37.0% (8) | +71.1% (11) | yes |
| Tomahawkmaster | leaderboard | 12 | 5 | +86.1% | 1.23 | +0.0% (0) | +86.1% (12) | yes |
| CUTJALENHURTS | tag | 53 | 33 | +25.2% | 1.57 | +31.4% (42) | +3.6% (11) | yes |
| anontrader11 | tag | 174 | 101 | +17.2% | 1.96 | +54.1% (26) | +10.8% (148) | yes |
| Manchester4ever | tag | 152 | 99 | +15.7% | 2.16 | +18.6% (109) | +8.3% (43) | yes |
| growzizi | tag | 113 | 75 | +17.9% | 1.7 | -1.7% (45) | +30.8% (68) | yes |
| Diabolical-Prize | current | 183 | 104 | +12.9% | 1.88 | +12.9% (183) | +0.0% (0) | no |
| Deliles | tag | 31 | 16 | +51.3% | 1.16 | +96.2% (17) | -4.0% (14) | yes |
| OVER955 | tag | 119 | 114 | +8.4% | 3.73 | +7.9% (94) | +10.3% (25) | yes |
| GoingStraightAhead | tag | 82 | 50 | +23.2% | 1.32 | +31.5% (32) | +17.8% (50) | yes |
| nightcity2077 | tag | 68 | 38 | +28.6% | 1.19 | +34.9% (64) | -72.5% (4) | no |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +28.5% (25) | -34.5% (4) | no |
| igot50k | tag | 247 | 132 | +11.0% | 1.02 | +11.7% (218) | +5.1% (29) | no |
| 0x5974813b27CdE970e736AE3b55 | tag | 117 | 81 | +7.1% | 1.01 | +4.2% (90) | +16.9% (27) | yes |
| returdmaxxer | tag | 298 | 275 | +1.6% | 0.92 | +3.4% (218) | -3.1% (80) | yes |
| sara341 | tag | 102 | 48 | +16.2% | 0.99 | +32.5% (24) | +11.1% (78) | yes |
| 0xf9B5e9803Ea977b7111c9B7728 | tag | 273 | 142 | +5.5% | 0.88 | +16.2% (84) | +0.7% (189) | yes |
| vardaman-bundren | tag | 205 | 102 | +7.9% | 0.88 | +7.3% (145) | +9.4% (60) | yes |
| arahbo | tag | 215 | 112 | +7.9% | 0.85 | -1.7% (146) | +28.1% (69) | yes |
| nibbio3 | tag | 73 | 36 | +17.1% | 0.92 | +13.2% (40) | +21.8% (33) | yes |
| dfdeath | tag | 1103 | 575 | +2.6% | 0.62 | +2.9% (532) | +2.3% (571) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 74 | 50 | +8.3% | 0.84 | +0.0% (0) | +8.3% (74) | yes |
| superlxj | tag | 144 | 98 | +4.7% | 0.74 | +4.7% (144) | +0.0% (0) | no |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 243 | 129 | +4.3% | 0.71 | +10.3% (204) | -26.2% (39) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 12 | 7 | +39.8% | 0.94 | +39.8% (12) | +0.0% (0) | no |
| swaz13131313 | tag | 69 | 59 | +2.6% | 0.5 | +0.0% (0) | +2.6% (69) | yes |
| carelia | tag | 127 | 76 | +6.4% | 0.72 | +8.3% (78) | +3.2% (49) | yes |
| chux.cc | tag | 164 | 120 | +3.1% | 0.5 | +4.1% (135) | -1.7% (29) | no |
| .d-.-b. | tag | 40 | 21 | +19.3% | 0.86 | -28.0% (9) | +32.8% (31) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 534 | 232 | -8.7% | -1.7 | no |
| Kch-Temp | 185 | 107 | +14.4% | 1.9 | yes |
| EdZachary | 155 | 56 | -16.5% | -1.67 | no |
| KaneAnalytics | 181 | 98 | +5.7% | 0.53 | yes |
| Jsram | 96 | 61 | +9.7% | 1.21 | no |
| Kkunn | 920 | 386 | +1.4% | 0.5 | yes |
| Sisyphus- | 134 | 74 | -2.7% | -0.29 | no |
| PEYZ-BIGGEST-FAN | 290 | 143 | -9.5% | -1.39 | no |
| theowalcott | 97 | 53 | +3.7% | 0.53 | no |
| HVAB | 409 | 252 | -1.5% | -0.32 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 241 | 133 | +15.3% | 2.36 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 36 | 31 | +54.9% | 3.82 | yes |
| 0010001000001100 | 245 | 119 | -1.0% | -0.31 | no |
| totoro3miyazaki | 50 | 31 | +6.5% | 0.52 | no |
| 1l2ihj34li12u34 | 151 | 83 | +8.5% | 1.33 | no |
| yabanci | 121 | 72 | +13.9% | 1.21 | yes |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | no |
| juice-fruit | 70 | 46 | +4.8% | 0.57 | yes |
| 0x16bb9951a36fce71e2ef57890b | 69 | 24 | -16.0% | -1.14 | yes |
| GamblingOdyssey | 313 | 177 | +4.4% | 0.95 | no |
| plonker2026 | 166 | 90 | +8.4% | 1.36 | no |
| xxyx0xx | 248 | 120 | -5.3% | -0.61 | no |
| monkeymashingkeyboard | 1112 | 577 | +1.2% | 0.39 | no |
| Tiger105 | 42 | 27 | +17.9% | 1.23 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 451 | 248 | -0.1% | -0.02 | no |
| UNEB3154s4f251 | 2244 | 1404 | +2.0% | 1.23 | no |
