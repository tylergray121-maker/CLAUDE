# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-10-26 09:00 UTC: 5572 candidates, 3885 with trades copytop could copy, 218 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 1946 | 883 | $19,260 | -32.27 | -0.2% | +0.21 |
| every wallet that qualified on the first part (test window) | 2334 | 1073 | $23,177 | +164.42 | +0.7% | +0.46 |
| currently copied (test window) | 4381 | 2328 | $42,995 | +1,035.25 | +2.4% | +1.60 |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 1946 | 883 | $19,260 | -32.27 | -0.2% | 0.21 | 5702 | 2791 | $55,869 | +3,970.83 | +7.1% | 4.18 |
| copy their sells too | 1946 | 862 | $19,260 | -355.05 | -1.8% | -0.37 | 5702 | 2761 | $55,869 | +3,574.81 | +6.4% | 3.81 |
| size by conviction (x0.5 / x1 / x1.5) | 1896 | 858 | $23,979 | +129.22 | +0.5% | -0.11 | 5493 | 2686 | $68,536 | +4,673.49 | +6.8% | 3.92 |
| skip bets under 0.5x their usual | 1825 | 828 | $18,160 | +174.88 | +1.0% | 0.61 | 5270 | 2564 | $52,029 | +3,807.84 | +7.3% | 4.05 |
| pre-game only | 1563 | 755 | $15,377 | +294.43 | +1.9% | 0.86 | 4968 | 2528 | $48,447 | +4,478.32 | +9.2% | 5.18 |
| skip prices under 30c | 1473 | 775 | $14,500 | +7.76 | +0.1% | 0.16 | 4458 | 2459 | $43,493 | +1,377.66 | +3.2% | 2.34 |
| favorites only (50c+) | 682 | 459 | $6,632 | +368.76 | +5.6% | 2.07 | 2216 | 1490 | $21,338 | +907.72 | +4.2% | 2.87 |
| 15s delay | 2001 | 911 | $19,813 | +32.34 | +0.2% | 0.36 | 5810 | 2843 | $56,973 | +4,209.84 | +7.4% | 4.4 |
| 60s delay | 1946 | 883 | $19,260 | -32.27 | -0.2% | 0.21 | 5702 | 2791 | $55,869 | +3,970.83 | +7.1% | 4.18 |
| allow 2c over their price | 2049 | 931 | $20,225 | +26.74 | +0.1% | 0.34 | 5988 | 2926 | $58,628 | +4,145.32 | +7.1% | 4.23 |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|
| conviction:0.5-1x | 365 | +7.7% | 1.2 | 170 | +9.4% | 0.94 |
| conviction:1-2x | 452 | +14.6% | 1.84 | 181 | -12.9% | -1.3 |
| conviction:2x+ | 2444 | +9.6% | 3.4 | 1343 | +2.2% | 0.74 |
| conviction:under 0.5x | 495 | +17.3% | 3.32 | 252 | -10.4% | -1.08 |
| delay_move:flat | 2301 | +11.8% | 4.0 | 1341 | +0.4% | 0.36 |
| delay_move:price fell | 1455 | +9.6% | 2.89 | 603 | -2.6% | -0.33 |
| exit:settle | 3756 | +10.9% | 4.94 | 1946 | -0.2% | 0.21 |
| kind:moneyline | 2468 | +9.9% | 3.37 | 1508 | +0.8% | 0.46 |
| kind:result | 798 | +20.6% | 4.49 | 285 | +7.8% | 1.34 |
| kind:totals | 490 | +0.6% | 0.22 | 153 | -24.3% | -3.25 |
| league:atp | 309 | +19.5% | 2.41 | 408 | -11.5% | -1.63 |
| league:bun | 8 | +50.3% | 14.89 | 4 | -100.0% | — |
| league:cfb | 16 | -79.3% | -5.41 | 34 | +44.8% | 1.8 |
| league:cs2 | 315 | +4.9% | 0.64 | 207 | -12.0% | -0.93 |
| league:dota2 | 80 | -11.3% | -0.83 | 109 | +24.5% | 1.52 |
| league:epl | 52 | +34.2% | 3.05 | 50 | -13.4% | -1.19 |
| league:lal | 20 | +17.4% | 1.12 | 3 | -34.5% | -0.55 |
| league:lol | 1736 | +15.5% | 4.02 | 345 | +9.4% | 1.19 |
| league:mlb | 869 | +1.3% | 0.39 | 145 | -19.5% | -2.45 |
| league:mls | 41 | +14.7% | 1.07 | 47 | -7.1% | -0.37 |
| league:nfl | 36 | +26.0% | 1.08 | 32 | +19.1% | 1.01 |
| league:sea | 33 | +59.4% | 3.41 | 33 | -52.1% | -3.39 |
| league:ucl | 40 | -8.0% | -0.57 | 61 | +15.9% | 1.3 |
| league:wnba | 0 | +0.0% | — | 11 | -63.8% | -3.0 |
| league:wta | 192 | +7.4% | 1.02 | 452 | +11.2% | 1.83 |
| price:30-70c | 2600 | +4.9% | 2.54 | 1321 | -0.2% | 0.08 |
| price:over 70c | 381 | +3.6% | 1.67 | 140 | +2.2% | 0.49 |
| price:under 30c | 775 | +34.4% | 4.15 | 485 | -0.8% | 0.14 |
| timing:in-play | 351 | -5.1% | -0.68 | 383 | -8.4% | -0.97 |
| timing:pre-game | 3405 | +12.7% | 5.57 | 1563 | +1.9% | 0.86 |

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 149200 | 76905 | $1,482,863 | -62,998.96 | -4.2% | -14.11 |
| consistency (winning weeks), top 16 | 10441 | 5419 | $103,227 | -3,726.98 | -3.6% | -3.12 |
| consistency (winning weeks), top 40 | 26748 | 13874 | $263,549 | -10,211.65 | -3.9% | -5.57 |
| copy return, average, top 16 | 6610 | 3167 | $65,430 | -1,032.00 | -1.6% | -0.94 |
| copy return, average, top 40 | 23064 | 11938 | $228,757 | -3,620.78 | -1.6% | -2.02 |
| copy return, lower bound, top 16 | 7733 | 3942 | $76,738 | -1,403.80 | -1.8% | -1.24 |
| copy return, lower bound, top 40 | 27845 | 14953 | $275,280 | -6,668.77 | -2.4% | -3.65 |
| copy return, shrunk, top 16 | 8008 | 3910 | $79,289 | -2,436.29 | -3.1% | -2.09 |
| copy return, shrunk, top 40 | 23064 | 11938 | $228,757 | -3,620.78 | -1.6% | -2.02 |
| markout 2h, average, top 16 | 5909 | 2870 | $59,302 | -401.91 | -0.7% | -0.34 |
| markout 2h, average, top 40 | 19879 | 10180 | $199,174 | -4,248.07 | -2.1% | -2.26 |
| markout 2h, lower bound, top 16 | 9939 | 5237 | $98,927 | -1,752.34 | -1.8% | -1.40 |
| markout 2h, lower bound, top 40 | 25927 | 13593 | $256,506 | -7,057.95 | -2.8% | -3.86 |
| markout 30m, average, top 16 | 7380 | 3788 | $74,085 | -3,116.47 | -4.2% | -3.03 |
| markout 30m, average, top 40 | 20712 | 10960 | $207,220 | -7,170.06 | -3.5% | -3.92 |
| most active, top 16 | 29158 | 14880 | $289,524 | -14,762.62 | -5.1% | -7.69 |
| most active, top 40 | 51780 | 26411 | $514,382 | -24,829.92 | -4.8% | -9.58 |
| win rate vs the odds, top 16 | 5832 | 3050 | $57,150 | -1,448.50 | -2.5% | -1.72 |
| win rate vs the odds, top 40 | 22468 | 11618 | $222,459 | -5,062.98 | -2.3% | -2.93 |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (40 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|
| BunCaCham | 49 | 45 | +29.7% | 3.56 | +2.90 |
| 0x20D6436849F930584892730C7F | 150 | 86 | +28.2% | 2.05 | +2.87 |
| yabanci | 44 | 32 | +23.3% | 2.13 | +2.68 |
| tiger105 | 40 | 26 | +21.8% | 1.45 | +2.17 |
| theowalcott | 62 | 38 | +15.7% | 1.44 | +1.75 |
| xxyx0xx | 259 | 129 | +6.3% | 0.57 | +0.58 |
| platarb | 884 | 354 | +3.0% | 0.64 | +0.29 |
| 0x16bb9951a36fce71e2ef57890b | 822 | 448 | +6.6% | 1.95 | +0.68 |
| 0x6918EA182D963b1Fb7888860b8 | 794 | 468 | +7.1% | 1.63 | +0.60 |
| juice-fruit | 40 | 28 | +12.1% | 0.96 | +1.30 |
| 1l2ihj34li12u34 | 58 | 36 | +25.3% | 2.09 | +2.87 |
| am100 | 1010 | 604 | +11.3% | 3.16 | +1.13 |
| monkeymashingkeyboard | 1967 | 1105 | +6.4% | 2.78 | +0.62 |
| KaneAnalytics | 124 | 71 | +9.7% | 0.82 | +0.95 |
| AmericaFirst1 | 505 | 313 | +5.7% | 1.39 | +0.58 |
| smithagent | 823 | 437 | +5.8% | 0.87 | +0.55 |
| 0x8Cb25E16F2F0893C1bd4d70773 | 1053 | 462 | +2.6% | 0.5 | +0.25 |
| moreplatesmoredates | 964 | 484 | -0.2% | 0.16 | +0.07 |
| Sisyphus- | 123 | 73 | +0.3% | 0.05 | +0.04 |
| 0xffAaEFb5f6762Cc70cb575Da87 | 685 | 323 | +2.1% | 0.34 | +0.20 |
| arahbo | 1658 | 708 | +0.5% | 0.08 | +0.03 |
| cosmicsteaks | 1325 | 570 | -2.6% | -0.65 | -0.28 |
| TAIWANNUMBERONE | 1515 | 814 | -3.5% | -1.3 | -0.35 |
| ZEST011 | 723 | 539 | +2.7% | 1.06 | +0.26 |
| SimpleTony | 1245 | 400 | +9.1% | 1.78 | +0.92 |
| GamblingOdyssey | 435 | 219 | +6.4% | 1.3 | +0.74 |
| 0x567212c82AAa6fe589bE5A2f4C | 649 | 334 | +4.1% | 1.04 | +0.58 |
| 0ooo0o0o0oo0o0 | 1356 | 740 | -2.5% | -0.95 | -0.26 |
| walnutz | 648 | 335 | -1.7% | -0.41 | -0.18 |
| UNEB3154s4f251 | 2035 | 1294 | +3.7% | 2.09 | +0.37 |
| jiafan | 1091 | 657 | +1.2% | 0.38 | +0.12 |
| eskk | 1071 | 269 | -0.1% | 0.02 | +0.02 |
| Talvez10 | 571 | 313 | +4.4% | 0.8 | +0.32 |
| torta.tech | 1864 | 1119 | -0.4% | -0.15 | -0.03 |
| iseedota | 1156 | 500 | -2.3% | -0.56 | -0.23 |
| Jsram | 95 | 56 | +0.0% | 0.21 | +0.19 |
| littlebay | 742 | 490 | +1.5% | 0.41 | +0.15 |
| MIracle33 | 899 | 448 | +4.3% | 1.11 | +0.42 |
| igot50k | 1825 | 1057 | -2.7% | -1.02 | -0.27 |
| TheRomanProcurator | 4059 | 2004 | +1.2% | 0.57 | +0.12 |

## Esports specialists (copies on esports markets only)

2894 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 165 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|
| xxyx0xx | tag | 76 | 43 | +48.6% | 2.16 | +8.8% (17) | +60.1% (59) | no |
| pltrkr111 | tag | 271 | 160 | +35.4% | 3.48 | +51.7% (177) | +4.7% (94) | yes |
| 0x0x23kjookhaiuohduoayh8c9 | tag | 323 | 193 | +19.9% | 2.27 | +16.4% (235) | +29.0% (88) | no |
| am100 | tag | 1010 | 604 | +11.3% | 3.16 | +9.6% (916) | +27.2% (94) | yes |
| juice-fruit | current | 26 | 19 | +23.3% | 1.36 | +0.0% (0) | +23.3% (26) | yes |
| yakz | leaderboard | 167 | 82 | +19.5% | 1.38 | +35.6% (80) | +4.3% (87) | yes |
| MIracle33 | tag | 440 | 226 | +10.4% | 1.8 | +11.3% (326) | +7.6% (114) | yes |
| SimpleTony | tag | 1231 | 392 | +8.5% | 1.66 | +8.8% (869) | +7.8% (362) | yes |
| -5rud | tag | 565 | 387 | +6.8% | 1.74 | +7.1% (424) | +6.0% (141) | yes |
| 0xa3B5dA76FfBBE3325BB1b40A30 | tag | 1499 | 790 | +5.6% | 1.85 | +6.9% (1234) | -0.5% (265) | yes |
| 0x6918EA182D963b1Fb7888860b8 | tag | 794 | 468 | +7.1% | 1.63 | +5.9% (640) | +12.4% (154) | yes |
| BunCaCham | tag | 20 | 19 | +7.6% | 1.29 | +4.9% (14) | +13.9% (6) | yes |
| littlebay | tag | 90 | 68 | +7.3% | 1.05 | +18.7% (28) | +2.2% (62) | yes |
| 0x567212c82AAa6fe589bE5A2f4C | tag | 649 | 334 | +4.1% | 1.04 | +6.9% (439) | -1.7% (210) | yes |
| AmericaFirst1 | current | 256 | 165 | +5.1% | 1.03 | +8.3% (182) | -2.7% (74) | yes |
| ZEST011 | tag | 723 | 539 | +2.7% | 1.06 | +1.8% (617) | +7.7% (106) | yes |
| Saber-greed | leaderboard | 431 | 221 | +8.0% | 0.91 | +5.1% (397) | +41.0% (34) | yes |
| 0x5974813b27CdE970e736AE3b55 | tag | 154 | 104 | +4.7% | 0.8 | +4.9% (92) | +4.5% (62) | yes |
| Nooserac | tag | 202 | 108 | +6.9% | 0.84 | -1.4% (152) | +32.4% (50) | yes |
| GC-C | tag | 727 | 507 | +0.9% | 0.37 | -0.3% (249) | +1.5% (478) | yes |
| shaw | tag | 315 | 177 | +4.3% | 0.72 | +6.4% (241) | -2.5% (74) | yes |
| berlinskies | tag | 1027 | 598 | +1.2% | 0.38 | +4.8% (755) | -8.8% (272) | yes |
| 0xcf279d52 | tag | 497 | 296 | +2.1% | 0.45 | +6.9% (337) | -7.9% (160) | yes |
| superlxj | tag | 218 | 152 | +1.8% | 0.42 | -9.6% (94) | +10.9% (124) | yes |
| 0x09dAc7226f8df37eBFAF277252 | tag | 527 | 310 | +0.9% | 0.3 | +4.7% (455) | -22.3% (72) | yes |
| dddd123s | tag | 552 | 332 | +0.5% | 0.12 | +7.2% (300) | -7.4% (252) | yes |
| moreplatesmoredates | tag | 964 | 484 | -0.2% | 0.16 | -3.1% (616) | +5.0% (348) | yes |
| Diabolical-Prize | tag | 224 | 118 | +2.1% | 0.47 | +13.4% (148) | -19.6% (76) | no |
| 0xffAaEFb5f6762Cc70cb575Da87 | tag | 685 | 323 | +2.1% | 0.34 | +4.9% (523) | -6.8% (162) | yes |
| Future-Tarot-Trader | tag | 2163 | 1099 | -0.6% | -0.27 | -1.8% (1879) | +7.3% (284) | yes |

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | 324 | 137 | -6.6% | -1.01 | no |
| Kch-Temp | 120 | 57 | -7.0% | -0.67 | no |
| EdZachary | 104 | 45 | +2.4% | 0.07 | no |
| KaneAnalytics | 124 | 71 | +9.7% | 0.82 | yes |
| Jsram | 95 | 56 | +0.0% | 0.21 | yes |
| Kkunn | 702 | 292 | +1.1% | 0.41 | no |
| Sisyphus- | 123 | 73 | +0.3% | 0.05 | yes |
| PEYZ-BIGGEST-FAN | 391 | 191 | +1.3% | 0.2 | no |
| theowalcott | 62 | 38 | +15.7% | 1.44 | yes |
| HVAB | 317 | 197 | +0.5% | 0.08 | no |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | 293 | 153 | +6.9% | 1.26 | no |
| Talvez10 | 571 | 313 | +4.4% | 0.8 | yes |
| BunCaCham | 49 | 45 | +29.7% | 3.56 | yes |
| 0010001000001100 | 141 | 63 | -6.8% | -0.81 | no |
| totoro3miyazaki | 48 | 30 | +7.0% | 0.55 | no |
| 1l2ihj34li12u34 | 58 | 36 | +25.3% | 2.09 | yes |
| yabanci | 44 | 32 | +23.3% | 2.13 | yes |
| 0x20D6436849F930584892730C7F | 150 | 86 | +28.2% | 2.05 | yes |
| juice-fruit | 40 | 28 | +12.1% | 0.96 | yes |
| 0x16bb9951a36fce71e2ef57890b | 822 | 448 | +6.6% | 1.95 | yes |
| GamblingOdyssey | 435 | 219 | +6.4% | 1.3 | yes |
| plonker2026 | 94 | 55 | +5.8% | 1.01 | no |
| xxyx0xx | 259 | 129 | +6.3% | 0.57 | yes |
| monkeymashingkeyboard | 1967 | 1105 | +6.4% | 2.78 | yes |
| Tiger105 | 40 | 26 | +21.8% | 1.45 | yes |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | 505 | 313 | +5.7% | 1.39 | yes |
| UNEB3154s4f251 | 2035 | 1294 | +3.7% | 2.09 | yes |
