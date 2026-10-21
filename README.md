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

## Portfolios and New York

The report's main section builds a portfolio of wallets copied together with
one bankroll, two ways:

- **Plan A:** all Polymarket markets.
- **Plan B:** only markets also listed on Polymarket US, the CFTC-regulated
  exchange New York residents can use. The international exchange the
  wallets trade on is closed to US persons.

Each plan first **validates the picking method**. It ranks wallets on the
qualifying period only, copies the top K together, and scores the result on
the later test period. That is compared with the typical qualified wallet,
i.e. what picking at random would give. If the method doesn't beat that and
make money out of sample, the report says **no edge**. Only then does it
apply the same ranking to the most recent period to give current picks.

Plan B still uses international prices as a stand-in for Polymarket US
prices, which can differ.

## Single-wallet ranking

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

---

# pmbot — Polymarket US trading bot

A small, cautious bot for [Polymarket US](https://polymarket.us), the
CFTC-regulated exchange open to New York residents.

## What it does

- **Fair value** for each US market comes from the same outcome on
  Polymarket's international exchange, which is far deeper. Reading its
  public prices is not trading there.
- **Maker first.** It rests post-only bids at least 2¢ below fair value, and
  post-only asks at least 2¢ above it for contracts it holds. Makers pay no
  taker fee (about 1.7¢ per contract at 50¢) and earn a small rebate.
- **Takes** only when a US price is beyond fair value by more than the taker
  fee plus 3¢, and never for more than the displayed size.
- **Long side only:** buy to open, sell what it holds to close. No shorts.
- **Skips** in-play games, markets closing within an hour, prices outside
  5–95¢, and markets whose reference spread is wider than 4¢. A US/international
  pair is only traded once their live prices agree within 8¢; anything
  further apart is assumed to be a mismatch, not an opportunity.

## Copying the top wallets (`--strategies copytop`)

`pmbot/leaders.json` lists 16 sports wallets from the top-wallet study:
active in the last week, profit that reconciles with their leaderboard
figure, 150+ positions, edge above 4% per dollar. Each cycle the bot polls
their newest public trades. A buy of an outcome that is also on Polymarket
US (through the verified market pairs, live games included) becomes a taker
buy there, at no more than 1¢ above the leader's price and only when the two
prices agree; a leader's sell closes the copy. One order printing as many
fills is copied once, and each leader is copied at most once per market per
10 minutes. Copies pay the Polymarket US taker fee.

## Modes

```bash
python -m pmbot scan  --minutes 60     # read-only: how often is there an edge?
python -m pmbot paper --minutes 1440   # simulated trading on live quotes
python -m pmbot live                   # real money; see below
```

Each run writes `botresults/report.md`, `summary.json`, `events.jsonl`
(every order, fill, cancel and opportunity) and `pairs.json` (the market
mapping, which you can review and pass back with `--pairs-file`).

Paper fills are conservative: a resting order only fills when the market
trades *through* its price, because queue position is unknown.

## Risk limits (defaults for a $200 account)

| setting | default |
|---|---|
| `--order-usd` | $5 per quote or take |
| `--max-market-usd` | $25 committed per market |
| `--max-total-usd` | $150 committed in total |
| `--daily-loss-limit` | halt after losing $30 in a UTC day |
| kill switch | create a file named `STOP`; the bot halts and cancels its orders |

It also caps itself at 30 orders a minute and cancels its orders on exit.

## Going live

Only after a paper run of a few weeks shows a profit after fees.

1. `pip install polymarket-us`
2. Create API keys at polymarket.us (Settings → API keys), then
   `export PMUS_KEY_ID=...` and `export PMUS_SECRET_KEY=...`.
   Never commit them.
3. `python -m pmbot live --minutes 0` and type the confirmation phrase.

The bot only manages and cancels orders it created itself; its order IDs are
kept in `botresults/live_orders.json`. It treats any position in a market it
trades as its own, so don't hold manual positions in those markets. Orders
are flagged as automatic, as the API asks.

Legal status: New York sued Polymarket US in September 2026 to stop it
operating in the state; as of late October 2026 no court had ruled. Check
the current status, and that you meet the age requirement, before trading.
