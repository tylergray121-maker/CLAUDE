# Which wallets to copy on Polymarket US

Backtest of copytop's own rules over 90 days to 2026-11-03 09:00 UTC: 5501 candidates, 0 with trades copytop could copy, 0 re-priced at a 60s copy delay. Choosing window: first 67%; test window: the rest (30 days).

## Does choosing this way hold up?

Wallets ranked on the choosing window only (lower bound of per-copy return, 15+ closed copies), then scored on the test window they never saw:

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| chosen on the first part (test window) | 0 | 0 | $0 | +0.00 | — | — |
| every wallet that qualified on the first part (test window) | 0 | 0 | $0 | +0.00 | — | — |
| currently copied (test window) | 0 | 0 | $0 | +0.00 | — | — |

## Copy rules, on the chosen wallets

| | test window | | | | | | whole window | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base: 60s delay, 1c limit, hold to settlement | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| copy their sells too | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| size by conviction (x0.5 / x1 / x1.5) | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| skip bets under 0.5x their usual | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| pre-game only | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| skip prices under 30c | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| favorites only (50c+) | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| 15s delay | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| 60s delay | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |
| allow 2c over their price | 0 | 0 | $0 | +0.00 | +0.0% | — | 0 | 0 | $0 | +0.00 | +0.0% | — |

## Patterns, on the chosen wallets (choosing window → test window)

| pattern | copies | return | t | → copies | return | t |
|---|---|---|---|---|---|---|

## Ranking methods, walk-forward

Choose on 45 days, score the next 15 days, 3 folds pooled. 'Every qualified wallet' is the no-ranking baseline.

| | copies | won | staked | P&L | return | t |
|---|---|---|---|---|---|---|
| every qualified wallet | 0 | 0 | $0 | +0.00 | — | — |
| consistency (winning weeks), top 16 | 0 | 0 | $0 | +0.00 | — | — |
| consistency (winning weeks), top 40 | 0 | 0 | $0 | +0.00 | — | — |
| copy return, average, top 16 | 0 | 0 | $0 | +0.00 | — | — |
| copy return, average, top 40 | 0 | 0 | $0 | +0.00 | — | — |
| copy return, lower bound, top 16 | 0 | 0 | $0 | +0.00 | — | — |
| copy return, lower bound, top 40 | 0 | 0 | $0 | +0.00 | — | — |
| copy return, shrunk, top 16 | 0 | 0 | $0 | +0.00 | — | — |
| copy return, shrunk, top 40 | 0 | 0 | $0 | +0.00 | — | — |
| markout 2h, average, top 16 | 0 | 0 | $0 | +0.00 | — | — |
| markout 2h, average, top 40 | 0 | 0 | $0 | +0.00 | — | — |
| markout 2h, lower bound, top 16 | 0 | 0 | $0 | +0.00 | — | — |
| markout 2h, lower bound, top 40 | 0 | 0 | $0 | +0.00 | — | — |
| markout 30m, average, top 16 | 0 | 0 | $0 | +0.00 | — | — |
| markout 30m, average, top 40 | 0 | 0 | $0 | +0.00 | — | — |
| most active, top 16 | 0 | 0 | $0 | +0.00 | — | — |
| most active, top 40 | 0 | 0 | $0 | +0.00 | — | — |
| win rate vs the odds, top 16 | 0 | 0 | $0 | +0.00 | — | — |
| win rate vs the odds, top 40 | 0 | 0 | $0 | +0.00 | — | — |

Used for the final list: **every qualified wallet (no ranking method beat it out of sample)** (0 wallets, copied in the last week).

## Final picks (copied in the last week)

| wallet | copies | won | return | t | per $10 copy |
|---|---|---|---|---|---|

## Esports specialists (copies on esports markets only)

2919 wallets found by tag (esports, counter-strike-2, league-of-legends, dota-2, valorant); 0 with 10+ closed esports copies.

| wallet | source | copies | won | return | t | first part | test part | active last week |
|---|---|---|---|---|---|---|---|---|

## Currently copied wallets

| wallet | copies | won | return | t | in final picks |
|---|---|---|---|---|---|
| 0x006cc834Cc092684F1B56626E2 | — | — | — | — | no copyable trades |
| primm | — | — | — | — | no copyable trades |
| Kch-Temp | — | — | — | — | no copyable trades |
| EdZachary | — | — | — | — | no copyable trades |
| KaneAnalytics | — | — | — | — | no copyable trades |
| Jsram | — | — | — | — | no copyable trades |
| Kkunn | — | — | — | — | no copyable trades |
| Sisyphus- | — | — | — | — | no copyable trades |
| PEYZ-BIGGEST-FAN | — | — | — | — | no copyable trades |
| theowalcott | — | — | — | — | no copyable trades |
| HVAB | — | — | — | — | no copyable trades |
| BreakTheBank | — | — | — | — | no copyable trades |
| Diabolical-Prize | — | — | — | — | no copyable trades |
| Talvez10 | — | — | — | — | no copyable trades |
| BunCaCham | — | — | — | — | no copyable trades |
| 0010001000001100 | — | — | — | — | no copyable trades |
| totoro3miyazaki | — | — | — | — | no copyable trades |
| 1l2ihj34li12u34 | — | — | — | — | no copyable trades |
| yabanci | — | — | — | — | no copyable trades |
| 0x20D6436849F930584892730C7F | — | — | — | — | no copyable trades |
| juice-fruit | — | — | — | — | no copyable trades |
| 0x16bb9951a36fce71e2ef57890b | — | — | — | — | no copyable trades |
| GamblingOdyssey | — | — | — | — | no copyable trades |
| plonker2026 | — | — | — | — | no copyable trades |
| xxyx0xx | — | — | — | — | no copyable trades |
| monkeymashingkeyboard | — | — | — | — | no copyable trades |
| Tiger105 | — | — | — | — | no copyable trades |
| THEHIGHLIFE | — | — | — | — | no copyable trades |
| AmericaFirst1 | — | — | — | — | no copyable trades |
| UNEB3154s4f251 | — | — | — | — | no copyable trades |
