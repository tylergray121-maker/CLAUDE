# copybt — Polymarket copy-trade backtester

Gravia (gravia.trade) is an analytics front-end over Polymarket's public
on-chain data. This tool goes to the same source directly: it pulls leaderboard
wallets, replays each wallet's trades against a small bankroll ($200 by
default) with realistic copy constraints, and ranks who would actually have
been worth copying.

Python 3.10+, standard library only.

```bash
python -m copybt                        # top ~1500 leaderboard wallets, last 90 days
python -m copybt --wallets-file picks.txt --no-leaderboard   # your own list (e.g. from Gravia)
python -m copybt --categories OVERALL,POLITICS,SPORTS,CRYPTO --days 180
python -m copybt --slippage 0.02 --delay-seconds 30          # harsher execution
python -m unittest discover -s tests    # tests (offline)
```

Outputs land in `results/`: `report.md` (recommendation and top 15),
`ranking.csv` (every wallet, every metric) and `top_equity_curves.csv`.
API responses are cached in `.cache/`, so re-runs with different copy rules are fast.

Needs network access to `data-api.polymarket.com`, `gamma-api.polymarket.com`
and `clob.polymarket.com`.

## How a wallet is simulated

- **Buys:** each leader buy is copied with 5% of your current equity, scaled by
  the leader's conviction (their trade size compared with the median of their
  *earlier* buys, clipped to 0.25–3x). Each trade is capped at 20% of equity,
  each market at 35%, and orders under $1 (Polymarket's minimum) are skipped.
- **Sells:** when the leader sells X% of a position, you sell X% of yours.
- **Fills:** the leader's price plus 1¢ of slippage, or with `--delay-seconds`
  the worse of the leader's price and the market price after the delay.
  Buys above 99¢ are skipped.
- **Settlement:** positions pay out at market resolution; positions still open
  at the end are marked at the current market price.
- **No lookahead:** sizing uses only past trades; the window is split into a
  qualifying period (first 67%) and an out-of-sample test period.

## Ranking

A wallet is eligible when it made money in the qualifying period, gave at
least 15 copyable buys, and isn't flagged as impractical to copy:

| flag | meaning |
|---|---|
| `high_frequency` | > 100 trades/day — you can't keep up |
| `short_duration_markets` | mostly 5/15-minute "Up or Down" markets |
| `bonder` | mostly buys at ≥ 95¢ — slippage eats the edge |
| `too_many_trades` | > 20k trades in the window (bots / market makers) |

Eligible wallets are ranked by **out-of-sample return − 0.5 × max drawdown**,
and the top 25 are re-run at double slippage to check the edge survives.
`--include-flagged` ranks everything.

Past performance doesn't predict future returns; treat the output as research,
not a guarantee.
