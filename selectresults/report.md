# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-17 09:00 UTC: 5590 candidates, 3662 with trades copytop could copy, 239 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 1380 | 656 | $13,782 | -1,010.58 | -7.3% | -1.97 |
| every wallet that qualified on the first part (test window) | 3800 | 1955 | $38,097 | -1,892.66 | -5.0% | -2.52 |
| currently copied (test window) | 3761 | 1898 | $36,702 | -1,897.99 | -5.2% | -2.58 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 1380 | 656 | $13,782 | -1,010.58 | -7.3% | -1.97 | 2795 | 1445 | $27,701 | +1,649.68 | +6.0% | 2.81 |
| copy their sells too | 1380 | 649 | $13,782 | -1,217.80 | -8.8% | -2.53 | 2795 | 1414 | $27,701 | +1,158.85 | +4.2% | 2.17 |
| size by conviction (x0.5 / x1 / x1.5) | 1362 | 641 | $17,043 | -1,136.14 | -6.7% | -2.19 | 2734 | 1394 | $34,285 | +1,836.18 | +5.4% | 2.27 |
| skip bets under 0.5x their usual | 1265 | 621 | $12,627 | -689.59 | -5.5% | -1.42 | 2615 | 1381 | $25,958 | +1,698.34 | +6.5% | 3.05 |
| pre-game only | 739 | 351 | $7,344 | -658.08 | -9.0% | -2.22 | 1759 | 963 | $17,247 | +1,639.63 | +9.5% | 4.13 |
| skip prices under 30c | 1116 | 608 | $11,052 | -637.46 | -5.8% | -1.83 | 2262 | 1332 | $22,211 | +1,603.43 | +7.2% | 4.03 |
| favorites only (50c+) | 622 | 421 | $6,101 | +58.22 | +0.9% | 0.48 | 1186 | 819 | $11,535 | +633.96 | +5.5% | 2.8 |
| 15s delay | 1461 | 698 | $14,603 | -1,209.14 | -8.3% | -2.34 | 2917 | 1506 | $28,920 | +1,500.91 | +5.2% | 2.61 |
| 60s delay | 1380 | 656 | $13,782 | -1,010.58 | -7.3% | -1.97 | 2795 | 1445 | $27,701 | +1,649.68 | +6.0% | 2.81 |
| allow 2c over their price | 1455 | 685 | $14,535 | -1,152.45 | -7.9% | -2.17 | 2915 | 1495 | $28,880 | +1,504.92 | +5.2% | 2.58 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 118 | +27.9% | 2.55 | 131 | -8.3% | -0.77 |
| conviction:1-2x | 132 | +19.1% | 1.95 | 142 | -8.4% | -0.75 |
| conviction:2x+ | 975 | +17.8% | 4.22 | 901 | -4.7% | -1.14 |
| conviction:under 0.5x | 190 | +21.0% | 2.02 | 206 | -17.6% | -1.35 |
| delay_move:flat | 890 | +25.0% | 6.66 | 697 | -4.5% | -0.82 |
| delay_move:price fell | 525 | +9.5% | 1.35 | 683 | -10.2% | -1.91 |
| exit:settle | 1415 | +19.1% | 5.55 | 1380 | -7.3% | -1.97 |
| kind:moneyline | 1027 | +17.9% | 4.01 | 750 | -5.1% | -0.93 |
| kind:result | 209 | +31.7% | 4.86 | 269 | -23.4% | -3.58 |
| kind:totals | 179 | +11.9% | 2.04 | 361 | -0.0% | -0.04 |
| league:acle | 1 | +73.1% | — | 20 | -70.9% | -3.88 |
| league:atp | 292 | +3.1% | 0.58 | 203 | -38.3% | -5.01 |
| league:bel1 | 2 | +18.2% | 0.17 | 14 | +28.4% | 1.03 |
| league:bra | 7 | +106.0% | 31.89 | 15 | +0.3% | 0.04 |
| league:cfb | 102 | +33.7% | 1.3 | 26 | +0.7% | 0.06 |
| league:cs2 | 193 | +13.4% | 2.0 | 75 | +1.7% | 0.05 |
| league:dota2 | 45 | -7.1% | -0.48 | 35 | -4.0% | -0.19 |
| league:epl | 84 | +17.8% | 1.96 | 54 | +10.2% | 0.45 |
| league:lal | 13 | -4.9% | -0.17 | 32 | -2.7% | -0.16 |
| league:mls | 57 | -0.0% | 0.21 | 39 | -33.9% | -2.46 |
| league:nba | 1 | -100.0% | — | 295 | -1.3% | -0.11 |
| league:nfl | 75 | +37.7% | 2.15 | 26 | +41.9% | 0.71 |
| league:nhl | 89 | +30.9% | 3.69 | 62 | +13.3% | 1.44 |
| league:sea | 41 | +36.1% | 2.49 | 51 | +26.0% | 0.94 |
| league:spl | 8 | +61.6% | 1.96 | 33 | -76.2% | -6.45 |
| league:ucl | 67 | +26.7% | 3.14 | 68 | -36.1% | -3.11 |
| league:uel | 7 | +85.8% | 38.67 | 25 | +31.9% | 1.88 |
| league:unl | 29 | +69.4% | 2.83 | 45 | -26.7% | -1.66 |
| league:wta | 294 | +19.4% | 2.38 | 255 | +9.4% | 1.49 |
| price:30-70c | 1040 | +20.7% | 6.85 | 902 | -7.6% | -2.04 |
| price:over 70c | 98 | +9.1% | 2.35 | 210 | +4.4% | 1.61 |
| price:under 30c | 277 | +16.7% | 1.29 | 268 | -15.0% | -1.12 |
| timing:in-play | 395 | +9.0% | 0.98 | 641 | -5.5% | -0.81 |
| timing:pre-game | 1020 | +23.2% | 6.85 | 739 | -9.0% | -2.22 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 131602 | 69232 | $1,306,011 | -56,466.16 | -4.3% | -13.38 |
| consistency (winning weeks), top 16 | 8073 | 3947 | $80,521 | -5,223.08 | -6.5% | -4.83 |
| consistency (winning weeks), top 40 | 19364 | 10342 | $191,828 | -10,156.14 | -5.3% | -6.44 |
| copy return, average, top 16 | 4286 | 2157 | $41,997 | -2,323.51 | -5.5% | -2.93 |
| copy return, average, top 40 | 15220 | 7765 | $150,745 | -7,715.62 | -5.1% | -5.22 |
| copy return, lower bound, top 16 | 5609 | 2895 | $54,901 | -2,777.23 | -5.1% | -3.27 |
| copy return, lower bound, top 40 | 21909 | 12314 | $216,512 | -7,505.09 | -3.5% | -4.62 |
| copy return, shrunk, top 16 | 5294 | 2644 | $51,822 | -3,170.38 | -6.1% | -3.72 |
| copy return, shrunk, top 40 | 15380 | 7837 | $152,395 | -7,163.96 | -4.7% | -4.77 |
| markout 2h, average, top 16 | 5202 | 2780 | $52,042 | -2,833.11 | -5.4% | -3.30 |
| markout 2h, average, top 40 | 16312 | 8716 | $162,765 | -6,960.31 | -4.3% | -4.56 |
| markout 2h, lower bound, top 16 | 7473 | 4235 | $74,249 | -2,384.50 | -3.2% | -2.33 |
| markout 2h, lower bound, top 40 | 20584 | 11360 | $204,861 | -8,635.02 | -4.2% | -5.30 |
| markout 30m, average, top 16 | 6701 | 3561 | $67,191 | -1,815.90 | -2.7% | -1.70 |
| markout 30m, average, top 40 | 20526 | 11573 | $204,768 | -6,138.94 | -3.0% | -3.75 |
| most active, top 16 | 26403 | 14239 | $260,860 | -11,982.82 | -4.6% | -6.64 |
| most active, top 40 | 47321 | 25123 | $468,014 | -22,234.39 | -4.8% | -9.00 |
| win rate vs the odds, top 16 | 3207 | 1736 | $31,335 | -809.60 | -2.6% | -1.14 |
| win rate vs the odds, top 40 | 15730 | 8065 | $156,035 | -6,785.91 | -4.3% | -4.38 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 37 | 32 | +53.7% | 3.82 | +5.28 |
| Kch-Temp | 185 | 107 | +14.4% | 1.9 | +1.57 |
| l..messi | 426 | 203 | +12.8% | 1.39 | +1.25 |
| Wiretransferxyz | 547 | 322 | -1.4% | -0.2 | -0.08 |
| arahbo | 794 | 322 | +9.7% | 1.47 | +0.95 |
| yabanci | 110 | 63 | +10.9% | 0.91 | +1.21 |
| forsenxd | 356 | 199 | +5.3% | 0.88 | +0.52 |
| SimpleTony | 532 | 191 | +7.9% | 1.13 | +0.80 |
| NS13 | 1175 | 462 | -1.2% | -0.3 | -0.15 |
| Car-c | 1478 | 779 | +4.3% | 1.1 | +0.42 |
| nibbio3 | 361 | 154 | +8.9% | 0.88 | +0.86 |
| nightcity2077 | 534 | 253 | -2.8% | -0.4 | -0.26 |
| hydra1248 | 619 | 456 | +5.9% | 2.26 | +0.65 |
| Kuntro2 | 472 | 164 | -5.3% | -0.71 | -0.54 |
| juice-fruit | 70 | 46 | +4.8% | 0.57 | +0.59 |
| Lisanal-Gaib | 485 | 277 | -0.7% | -0.19 | -0.09 |
| carelia | 1209 | 569 | -2.6% | -0.76 | -0.27 |
| pltrkr111 | 999 | 559 | +4.7% | 1.35 | +0.47 |
| cosmicsteaks | 590 | 280 | +4.5% | 0.7 | +0.44 |
| yoooogo | 613 | 340 | -3.1% | -0.67 | -0.27 |
| anontrader11 | 489 | 275 | +5.0% | 0.96 | +0.50 |
| TearsInTheRain | 571 | 382 | +1.2% | 0.34 | +0.12 |
| timurdrevoz | 484 | 239 | +3.8% | 0.56 | +0.35 |
| Kkunn | 920 | 386 | +1.4% | 0.5 | +0.24 |
| seeyouanymore | 510 | 260 | -5.9% | -0.83 | -0.57 |
| 0xE16D3F2A5807999b358aFfD944 | 614 | 338 | -3.8% | -1.13 | -0.44 |
| szy10010 | 417 | 237 | -0.3% | -0.07 | -0.03 |
| over96 | 637 | 571 | +2.2% | 1.22 | +0.21 |
| growzizi | 512 | 295 | +2.4% | 0.39 | +0.23 |
| monkeymashingkeyboard | 1086 | 564 | +1.1% | 0.38 | +0.12 |
| Manchester4ever | 1081 | 612 | +2.2% | 0.73 | +0.22 |
| User7429 | 915 | 481 | -2.2% | -0.58 | -0.23 |
| shiifoo | 430 | 169 | -5.5% | -0.83 | -0.57 |
| 0x567212c82AAa6fe589bE5A2f4C | 405 | 212 | -0.3% | 0.37 | +0.26 |
| KaneAnalytics | 181 | 98 | +5.7% | 0.53 | +0.56 |
| TRCM | 2208 | 1124 | -6.3% | -2.31 | -0.62 |
| jiafan | 788 | 464 | +1.1% | 0.23 | +0.09 |
| 0x5fD2D9C60781D711721145Ff2b | 673 | 369 | -1.2% | -0.25 | -0.13 |
| LonnieHawkinss | 213 | 133 | +1.5% | 0.15 | +0.13 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 844 | 369 | +3.9% | 0.61 | +0.35 |

## Esports specialists (copies on esports markets only)

2963 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 163 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| 0xBc43c8bfBC4d77c2FC9011adaD | leaderboard | 19 | 12 | +55.9% | 2.02 | +37.0% (8) | +71.1% (11) | yes |
| Tomahawkmaster | leaderboard | 12 | 5 | +86.1% | 1.23 | +0.0% (0) | +86.1% (12) | yes |
| manvsrice42 | tag | 66 | 39 | +24.1% | 1.67 | +32.3% (45) | +6.4% (21) | yes |
| anontrader11 | tag | 164 | 96 | +18.5% | 2.03 | +66.8% (17) | +12.7% (147) | yes |
| Manchester4ever | tag | 164 | 105 | +14.1% | 1.99 | +15.7% (120) | +9.6% (44) | yes |
| Diabolical-Prize | current | 183 | 104 | +12.9% | 1.88 | +12.9% (183) | +0.0% (0) | no |
| growzizi | tag | 110 | 73 | +17.8% | 1.66 | +1.7% (38) | +26.2% (72) | yes |
| GoingStraightAhead | tag | 81 | 50 | +24.7% | 1.39 | +46.8% (20) | +17.5% (61) | yes |
| Deliles | tag | 31 | 16 | +51.3% | 1.16 | +96.2% (17) | -4.0% (14) | yes |
| over96 | tag | 119 | 114 | +8.4% | 3.73 | +7.7% (90) | +10.7% (29) | yes |
| 0x765e6a480ae3f05c3f2e6c50f4 | tag | 46 | 26 | +31.0% | 1.22 | +0.0% (0) | +31.0% (46) | yes |
| CUTJALENHURTS | tag | 60 | 35 | +17.6% | 1.19 | +19.2% (47) | +12.1% (13) | yes |
| juice-fruit | current | 29 | 20 | +19.4% | 1.16 | +28.5% (25) | -34.5% (4) | no |
| igot50k | tag | 279 | 150 | +11.0% | 1.14 | +12.2% (249) | +1.8% (30) | no |
| carelia | tag | 123 | 76 | +9.8% | 1.08 | +8.3% (78) | +12.4% (45) | yes |
| SimpleTony | tag | 517 | 183 | +6.7% | 0.96 | -0.7% (324) | +19.1% (193) | yes |
| nightcity2077 | tag | 79 | 42 | +20.8% | 0.98 | +25.7% (75) | -72.5% (4) | no |
| returdmaxxer | tag | 288 | 265 | +1.2% | 0.69 | +3.4% (218) | -5.4% (70) | yes |
| forsenxd | tag | 356 | 199 | +5.3% | 0.88 | -0.2% (317) | +50.1% (39) | yes |
| foxy4 | tag | 87 | 56 | +12.7% | 0.94 | -2.8% (2) | +13.1% (85) | yes |
| sara341 | tag | 100 | 47 | +15.6% | 0.94 | +16.2% (17) | +15.4% (83) | yes |
| arahbo | tag | 216 | 113 | +8.0% | 0.86 | -0.8% (142) | +24.8% (74) | yes |
| 0x6bfC64cb52307DeE90011412C6 | tag | 72 | 49 | +8.3% | 0.84 | +0.0% (0) | +8.3% (72) | yes |
| superlxj | tag | 144 | 98 | +4.7% | 0.74 | +4.9% (140) | -1.4% (4) | no |
| swaz13131313 | tag | 65 | 56 | +3.1% | 0.6 | +0.0% (0) | +3.1% (65) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 12 | 7 | +39.8% | 0.94 | +39.8% (12) | +0.0% (0) | no |
| dfdeath | tag | 1069 | 558 | +1.5% | 0.37 | +2.5% (504) | +0.7% (565) | yes |
| 0xf9B5e9803Ea977b7111c9B7728 | tag | 250 | 126 | +4.1% | 0.65 | +15.7% (75) | -0.9% (175) | yes |
| chux.cc | tag | 164 | 120 | +3.1% | 0.5 | +4.1% (135) | -1.7% (29) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 246 | 129 | +3.0% | 0.54 | +8.9% (205) | -25.9% (41) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 525 | 229 | -8.6% | -1.66 | no |
| Kch-Temp | 185 | 107 | +14.4% | 1.9 | yes |
| EdZachary | 155 | 56 | -16.5% | -1.67 | no |
| KaneAnalytics | 181 | 98 | +5.7% | 0.53 | yes |
| Jsram | 105 | 68 | +11.6% | 1.48 | no |
| Kkunn | 920 | 386 | +1.4% | 0.5 | yes |
| Sisyphus- | 137 | 75 | -2.8% | -0.31 | no |
| PEYZ-BIGGEST-FAN | 288 | 143 | -8.8% | -1.28 | no |
| theowalcott | 75 | 44 | +9.8% | 1.05 | no |
| HVAB | 387 | 234 | -5.2% | -1.13 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 242 | 133 | +14.8% | 2.3 | no |
| Talvez10 | 111 | 90 | +45.2% | 6.28 | no |
| BunCaCham | 37 | 32 | +53.7% | 3.82 | yes |
| 0010001000001100 | 341 | 164 | -2.9% | -0.56 | no |
| totoro3miyazaki | 55 | 31 | -3.3% | -0.23 | no |
| 1l2ihj34li12u34 | 173 | 88 | +0.2% | 0.34 | no |
| yabanci | 110 | 63 | +10.9% | 0.91 | yes |
| 0x20D6436849F930584892730C7F | 124 | 70 | +30.4% | 1.84 | no |
| juice-fruit | 70 | 46 | +4.8% | 0.57 | yes |
| 0x16bb9951a36fce71e2ef57890b | 69 | 24 | -16.0% | -1.14 | no |
| GamblingOdyssey | 330 | 185 | +4.5% | 0.93 | no |
| plonker2026 | 134 | 71 | +2.9% | 0.58 | no |
| xxyx0xx | 277 | 129 | +4.0% | 0.27 | no |
| monkeymashingkeyboard | 1086 | 564 | +1.1% | 0.38 | yes |
| Tiger105 | 43 | 29 | +23.5% | 1.68 | no |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 465 | 261 | +0.0% | 0.01 | no |
| UNEB3154s4f251 | 2247 | 1417 | +2.2% | 1.35 | no |
