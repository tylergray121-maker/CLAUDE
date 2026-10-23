# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-23 04:00 UTC: 5486 candidates, 3841 with trades copytop could copy, 228 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 2084 | 1014 | $20,353 | +248.66 | +1.2% | +0.67 |
| every wallet that qualified on the first part (test window) | 2166 | 1051 | $21,191 | +342.36 | +1.6% | +0.80 |
| currently copied (test window) | 4060 | 2156 | $39,888 | +1,618.36 | +4.1% | +2.48 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 2084 | 1014 | $20,353 | +248.66 | +1.2% | 0.67 | 5099 | 2664 | $49,092 | +4,443.46 | +9.0% | 5.14 |
| copy their sells too | 2084 | 985 | $20,353 | -244.28 | -1.2% | -0.21 | 5099 | 2618 | $49,092 | +3,648.66 | +7.4% | 4.38 |
| size by conviction (x0.5 / x1 / x1.5) | 1994 | 960 | $24,554 | +339.98 | +1.4% | 0.42 | 4753 | 2460 | $57,904 | +4,536.05 | +7.8% | 4.78 |
| skip bets under 0.5x their usual | 1966 | 969 | $19,273 | +393.58 | +2.0% | 1.01 | 4867 | 2565 | $46,940 | +4,352.01 | +9.3% | 5.21 |
| pre-game only | 1524 | 786 | $14,681 | +357.11 | +2.4% | 1.07 | 4078 | 2216 | $38,733 | +3,782.00 | +9.8% | 5.21 |
| skip prices under 30c | 1696 | 931 | $16,399 | +588.49 | +3.6% | 1.67 | 4442 | 2470 | $42,428 | +1,947.01 | +4.6% | 3.23 |
| favorites only (50c+) | 855 | 567 | $8,172 | +546.43 | +6.7% | 2.61 | 2372 | 1532 | $22,457 | +1,061.64 | +4.7% | 3.05 |
| 15s delay | 2145 | 1039 | $20,960 | +84.42 | +0.4% | 0.43 | 5246 | 2746 | $50,558 | +4,737.19 | +9.4% | 5.42 |
| 60s delay | 2084 | 1014 | $20,353 | +248.66 | +1.2% | 0.67 | 5099 | 2664 | $49,092 | +4,443.46 | +9.0% | 5.14 |
| allow 2c over their price | 2176 | 1048 | $21,230 | +82.19 | +0.4% | 0.41 | 5317 | 2764 | $51,222 | +4,683.94 | +9.1% | 5.25 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 364 | +22.3% | 3.29 | 219 | +13.6% | 1.57 |
| conviction:1-2x | 487 | +12.1% | 1.64 | 221 | -18.8% | -2.3 |
| conviction:2x+ | 1895 | +11.2% | 3.99 | 1354 | +3.2% | 0.9 |
| conviction:under 0.5x | 269 | +32.9% | 3.12 | 290 | -2.5% | 0.06 |
| delay_move:flat | 2306 | +15.7% | 5.74 | 1427 | +3.4% | 1.32 |
| delay_move:price fell | 709 | +11.2% | 2.13 | 657 | -3.3% | -0.6 |
| exit:settle | 3015 | +14.6% | 6.03 | 2084 | +1.2% | 0.67 |
| kind:moneyline | 2447 | +13.8% | 5.0 | 1779 | +2.7% | 1.1 |
| kind:result | 179 | +39.9% | 4.77 | 143 | -0.1% | 0.18 |
| kind:totals | 389 | +7.7% | 1.25 | 162 | -14.1% | -1.87 |
| league:atp | 377 | +12.6% | 1.62 | 482 | -14.6% | -2.51 |
| league:bra | 8 | +102.8% | 3.0 | 2 | -24.5% | -0.31 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 2 | -100.0% | — | 115 | -5.0% | -0.29 |
| league:cs2 | 125 | +24.0% | 2.57 | 101 | +8.5% | 1.02 |
| league:dota2 | 64 | +38.9% | 2.08 | 93 | -10.2% | -0.83 |
| league:epl | 52 | +34.2% | 3.05 | 39 | -24.6% | -1.88 |
| league:ere | 8 | +106.7% | 28.83 | 12 | +166.2% | 6.87 |
| league:lal | 29 | +5.9% | 0.5 | 8 | +152.3% | 1.06 |
| league:lol | 218 | +60.7% | 3.7 | 120 | -18.0% | -1.89 |
| league:mlb | 1515 | +2.1% | 0.63 | 268 | +14.5% | 2.68 |
| league:mls | 43 | +28.4% | 2.05 | 37 | -23.4% | -1.33 |
| league:nba | 0 | +0.0% | — | 87 | -6.2% | -0.5 |
| league:nfl | 126 | +26.0% | 1.78 | 92 | +47.4% | 2.34 |
| league:nhl | 0 | +0.0% | — | 28 | -11.6% | -1.06 |
| league:sea | 45 | +57.3% | 3.21 | 31 | -45.4% | -2.77 |
| league:wnba | 119 | +23.0% | 2.74 | 32 | -42.4% | -2.95 |
| league:wta | 275 | +10.5% | 1.42 | 531 | +13.6% | 2.41 |
| price:30-70c | 2570 | +4.5% | 2.27 | 1560 | +3.6% | 1.61 |
| price:over 70c | 172 | +14.5% | 5.67 | 128 | +4.7% | 0.96 |
| price:under 30c | 273 | +104.2% | 6.18 | 396 | -8.8% | -0.85 |
| timing:in-play | 461 | +16.4% | 2.33 | 560 | -1.9% | -0.22 |
| timing:pre-game | 2554 | +14.2% | 5.59 | 1524 | +2.4% | 1.07 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 139607 | 72819 | $1,387,064 | -53,437.09 | -3.9% | -12.56 |
| consistency (winning weeks), top 16 | 7861 | 4037 | $77,616 | -1,767.72 | -2.3% | -1.61 |
| consistency (winning weeks), top 40 | 20484 | 10646 | $203,177 | -5,739.87 | -2.8% | -3.28 |
| copy return, average, top 16 | 4604 | 2158 | $45,668 | +268.44 | +0.6% | +0.29 |
| copy return, average, top 40 | 21404 | 10891 | $212,132 | -2,757.20 | -1.3% | -1.55 |
| copy return, lower bound, top 16 | 5502 | 2715 | $54,151 | -392.57 | -0.7% | -0.30 |
| copy return, lower bound, top 40 | 23213 | 12451 | $229,612 | -4,303.86 | -1.9% | -2.39 |
| copy return, shrunk, top 16 | 5166 | 2349 | $51,368 | -971.49 | -1.9% | -1.02 |
| copy return, shrunk, top 40 | 21020 | 10647 | $208,660 | -2,961.27 | -1.4% | -1.60 |
| markout 2h, average, top 16 | 5878 | 2956 | $58,937 | -67.96 | -0.1% | -0.05 |
| markout 2h, average, top 40 | 16759 | 9028 | $167,231 | -1,330.83 | -0.8% | -0.78 |
| markout 2h, lower bound, top 16 | 5580 | 2721 | $55,777 | -519.91 | -0.9% | -0.47 |
| markout 2h, lower bound, top 40 | 22881 | 11721 | $228,004 | -2,258.08 | -1.0% | -1.25 |
| markout 30m, average, top 16 | 7733 | 4114 | $77,010 | -1,816.48 | -2.4% | -1.68 |
| markout 30m, average, top 40 | 21110 | 11260 | $210,493 | -7,116.63 | -3.4% | -4.08 |
| most active, top 16 | 24688 | 12438 | $245,067 | -14,818.25 | -6.0% | -8.56 |
| most active, top 40 | 48797 | 25173 | $484,206 | -23,529.82 | -4.9% | -9.50 |
| win rate vs the odds, top 16 | 3617 | 1796 | $35,672 | +452.62 | +1.3% | +0.58 |
| win rate vs the odds, top 40 | 18691 | 9549 | $185,444 | -1,418.57 | -0.8% | -0.83 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| 0010001000001100 | 35 | 21 | +61.6% | 1.49 | +5.95 |
| BunCaCham | 31 | 28 | +33.7% | 2.94 | +3.30 |
| plonker2026 | 82 | 57 | +39.6% | 3.69 | +4.49 |
| yabanci | 27 | 19 | +28.0% | 1.94 | +3.35 |
| 0x20D6436849F930584892730C7F | 151 | 87 | +28.7% | 2.1 | +2.91 |
| 1l2ihj34li12u34 | 30 | 22 | +47.7% | 2.81 | +4.95 |
| tiger105 | 42 | 28 | +27.2% | 1.84 | +2.71 |
| juice-fruit | 30 | 22 | +22.7% | 1.46 | +2.34 |
| theowalcott | 57 | 36 | +24.8% | 1.96 | +2.64 |
| 0x16bb9951a36fce71e2ef57890b | 858 | 466 | +6.3% | 1.87 | +0.64 |
| KaneAnalytics | 93 | 55 | +15.7% | 1.08 | +1.53 |
| smithagent | 656 | 349 | +6.5% | 0.89 | +0.63 |
| monkeymashingkeyboard | 1938 | 1098 | +7.7% | 3.35 | +0.76 |
| GamblingOdyssey | 417 | 211 | +6.7% | 1.34 | +0.78 |
| arahbo | 1047 | 443 | +4.6% | 0.77 | +0.43 |
| eskk | 895 | 215 | -0.1% | 0.03 | +0.02 |
| AmericaFirst1 | 440 | 278 | +7.7% | 1.74 | +0.78 |
| nightcity2077 | 837 | 402 | +2.0% | 0.35 | +0.20 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 952 | 419 | +2.4% | 0.46 | +0.23 |
| polkals | 560 | 253 | +7.1% | 1.04 | +0.68 |
| cosmicsteaks | 752 | 334 | -1.9% | -0.36 | -0.20 |
| NeedForDead | 376 | 158 | +10.4% | 1.34 | +1.04 |
| RensPeters | 572 | 284 | +1.1% | 0.23 | +0.11 |
| 0x567212c82AAa6fe589bE5A2f4C | 517 | 261 | +4.1% | 0.99 | +0.62 |
| Petal | 855 | 405 | -5.8% | -1.41 | -0.58 |
| jiafan | 842 | 510 | +5.4% | 1.31 | +0.50 |
| walnutz | 620 | 322 | -1.8% | -0.42 | -0.18 |
| Wiretransferxyz | 690 | 364 | -10.3% | -2.98 | -1.04 |
| Kkunn | 649 | 278 | +4.4% | 1.0 | +0.55 |
| UNEB3154s4f251 | 1847 | 1160 | +3.6% | 1.96 | +0.37 |
| oookkjjdd | 830 | 424 | -0.3% | -0.03 | -0.01 |
| TheRomanProcurator | 3438 | 1715 | +3.1% | 1.34 | +0.31 |
| SimpleTony | 1054 | 332 | +5.1% | 1.01 | +0.56 |
| n1ck10s | 961 | 513 | +2.4% | 0.65 | +0.24 |
| 0x7a3FB8C5aD2aF4C621B2138D95 | 463 | 190 | -9.0% | -1.25 | -0.89 |
| littlebay | 701 | 461 | +2.2% | 0.55 | +0.21 |
| sinhtuycanh | 615 | 433 | +1.8% | 0.69 | +0.19 |
| SharkVision | 751 | 350 | -3.2% | -0.56 | -0.30 |
| torta.tech | 1754 | 1041 | -1.9% | -0.78 | -0.18 |
| sbsport | 882 | 476 | +1.6% | 0.44 | +0.14 |

## Esports specialists (copies on esports markets only)

2796 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 170 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| pltrkr111 | tag | 180 | 99 | +40.9% | 2.83 | +69.8% (112) | -7.2% (68) | no |
| THEHIGHLIFE | tag | 248 | 127 | +32.5% | 2.64 | +52.1% (147) | +3.6% (101) | no |
| juice-fruit | current | 25 | 19 | +28.5% | 1.64 | +0.0% (0) | +28.5% (25) | yes |
| NeedForDead | tag | 40 | 22 | +31.0% | 1.54 | +44.1% (25) | +9.2% (15) | no |
| PT-S3 | leaderboard | 11 | 10 | +18.3% | 1.41 | +18.3% (11) | +0.0% (0) | no |
| yakz | leaderboard | 122 | 61 | +21.8% | 1.36 | +19.1% (73) | +25.8% (49) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 223 | 114 | +16.3% | 1.24 | +21.0% (156) | +5.1% (67) | no |
| AmericaFirst1 | current | 193 | 130 | +8.1% | 1.44 | +2.2% (129) | +19.5% (64) | yes |
| ehl-rungs | tag | 197 | 149 | +6.4% | 1.38 | +6.4% (197) | +0.0% (0) | no |
| RensPeters | tag | 77 | 46 | +13.4% | 1.13 | +7.2% (44) | +21.6% (33) | no |
| newUser2025 | tag | 125 | 87 | +7.9% | 1.18 | +9.3% (81) | +5.3% (44) | yes |
| dddd123s | tag | 439 | 279 | +5.3% | 1.27 | +6.6% (186) | +4.3% (253) | yes |
| sinhtuycanh | tag | 152 | 112 | +6.1% | 1.11 | -0.1% (72) | +11.6% (80) | yes |
| mpoly | tag | 230 | 167 | +5.5% | 1.11 | +9.3% (148) | -1.2% (82) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 517 | 261 | +4.1% | 0.99 | +9.8% (320) | -5.3% (197) | yes |
| SimpleTony | tag | 1045 | 328 | +5.0% | 0.98 | +6.8% (705) | +1.3% (340) | yes |
| littlebay | tag | 88 | 66 | +6.7% | 0.94 | +36.4% (12) | +1.9% (76) | no |
| smartcombo | tag | 186 | 107 | +8.4% | 0.94 | +13.6% (158) | -20.0% (28) | yes |
| returdmaxxer | tag | 277 | 253 | +0.8% | 0.41 | +1.5% (169) | -0.3% (108) | no |
| MIracle33 | tag | 303 | 153 | +5.1% | 0.81 | +16.5% (196) | -15.7% (107) | yes |
| superlxj | tag | 195 | 135 | +3.5% | 0.71 | -8.0% (91) | +14.1% (104) | yes |
| 0xcf279d52 | tag | 312 | 193 | +3.2% | 0.67 | +2.3% (155) | +4.2% (157) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 138 | 94 | +4.0% | 0.66 | +2.4% (65) | +5.5% (73) | yes |
| jiafan | tag | 413 | 247 | +2.8% | 0.55 | +4.7% (355) | -9.0% (58) | yes |
| nightcity2077 | tag | 297 | 151 | +7.2% | 0.75 | +7.7% (280) | -0.7% (17) | no |
| lll981kd | tag | 643 | 415 | +0.4% | 0.16 | -3.5% (180) | +1.9% (463) | yes |
| 8dddj | tag | 696 | 451 | -0.2% | 0.01 | -3.9% (196) | +1.2% (500) | yes |
| darkumbreon88 | tag | 273 | 194 | +1.2% | 0.28 | +5.8% (115) | -2.0% (158) | yes |
| igot50k | tag | 678 | 350 | +2.6% | 0.43 | -0.7% (518) | +13.5% (160) | yes |
| 0x09dAc7226f8df37eBFAF277252 | tag | 534 | 312 | +0.1% | 0.12 | +3.6% (454) | -19.4% (80) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 302 | 130 | -5.0% | -0.77 | no |
| Kch-Temp | 114 | 52 | -9.6% | -0.9 | no |
| EdZachary | 82 | 36 | -10.2% | -0.94 | no |
| KaneAnalytics | 93 | 55 | +15.7% | 1.08 | yes |
| Jsram | 57 | 28 | -16.0% | -1.31 | no |
| Kkunn | 649 | 278 | +4.4% | 1.0 | yes |
| Sisyphus- | 115 | 68 | -1.8% | -0.21 | no |
| PEYZ-BIGGEST-FAN | 212 | 109 | +0.1% | 0.1 | no |
| theowalcott | 57 | 36 | +24.8% | 1.96 | yes |
| HVAB | 316 | 198 | +1.0% | 0.18 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 277 | 142 | +6.5% | 1.16 | no |
| Talvez10 | 593 | 321 | +3.6% | 0.61 | no |
| BunCaCham | 31 | 28 | +33.7% | 2.94 | yes |
| 0010001000001100 | 35 | 21 | +61.6% | 1.49 | yes |
| totoro3miyazaki | 39 | 29 | +28.0% | 1.96 | no |
| 1l2ihj34li12u34 | 30 | 22 | +47.7% | 2.81 | yes |
| yabanci | 27 | 19 | +28.0% | 1.94 | yes |
| 0x20D6436849F930584892730C7F | 151 | 87 | +28.7% | 2.1 | yes |
| juice-fruit | 30 | 22 | +22.7% | 1.46 | yes |
| 0x16bb9951a36fce71e2ef57890b | 858 | 466 | +6.3% | 1.87 | yes |
| GamblingOdyssey | 417 | 211 | +6.7% | 1.34 | yes |
| plonker2026 | 82 | 57 | +39.6% | 3.69 | yes |
| xxyx0xx | 173 | 86 | +1.8% | 0.1 | no |
| monkeymashingkeyboard | 1938 | 1098 | +7.7% | 3.35 | yes |
| Tiger105 | 42 | 28 | +27.2% | 1.84 | yes |
| THEHIGHLIFE | 278 | 133 | +24.2% | 2.13 | no |
| AmericaFirst1 | 440 | 278 | +7.7% | 1.74 | yes |
| UNEB3154s4f251 | 1847 | 1160 | +3.6% | 1.96 | yes |
