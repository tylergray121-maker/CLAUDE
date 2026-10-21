"""Polymarket US bot.

    python -m pmbot scan  --minutes 60     # measure: is there an edge? (no orders)
    python -m pmbot paper --minutes 600    # simulated trading on live quotes
    python -m pmbot live                   # real orders (needs keys + confirmation)

Live trading reads PMUS_KEY_ID and PMUS_SECRET_KEY from the environment
(create them at polymarket.us > Settings > API keys) and needs
``pip install polymarket-us``. Create a file named STOP to halt the bot;
it cancels all its orders on exit.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

from .engine import Engine, EngineConfig
from .risk import RiskConfig, RiskManager
from .strategy import StrategyConfig

CONFIRM = "I accept the risk of losing this money"


def parse_args(argv=None):
    p = argparse.ArgumentParser(prog="pmbot", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=("scan", "paper", "live"))
    e, s, r = EngineConfig(), StrategyConfig(), RiskConfig()
    g = p.add_argument_group("run")
    g.add_argument("--minutes", type=float, default=e.minutes, help="0 = until stopped")
    g.add_argument("--cycle-seconds", type=float, default=e.cycle_seconds)
    g.add_argument("--max-markets", type=int, default=e.max_markets)
    g.add_argument("--pairs-file", default="", help="reviewed pairs.json to trade")
    g.add_argument("--out-dir", default=e.out_dir)
    g.add_argument("--max-rps", type=float, default=e.max_rps)
    g.add_argument("--resume", action="store_true",
                   help="paper: continue the account saved in OUT_DIR/state.json")
    g.add_argument("--snapshot-seconds", type=float, default=e.snapshot_seconds)
    g.add_argument("--equity-seconds", type=float, default=e.equity_seconds)
    g = p.add_argument_group("strategy")
    g.add_argument("--strategies", default="sportsgameday,fairvalue",
                   help="comma list, in priority order: sportsgameday, fairvalue")
    g.add_argument("--maker-edge", type=float, default=s.maker_edge)
    g.add_argument("--taker-edge", type=float, default=s.taker_edge)
    g.add_argument("--order-usd", type=float, default=s.order_usd)
    g.add_argument("--max-fair-spread", type=float, default=s.max_fair_spread)
    g.add_argument("--no-taker", action="store_true")
    g.add_argument("--no-maker", action="store_true")
    g = p.add_argument_group("risk")
    g.add_argument("--bankroll", type=float, default=r.bankroll)
    g.add_argument("--max-market-usd", type=float, default=r.max_market_usd)
    g.add_argument("--max-total-usd", type=float, default=r.max_total_usd)
    g.add_argument("--daily-loss-limit", type=float, default=r.daily_loss_limit)
    g.add_argument("--kill-file", default=r.kill_file)
    p.add_argument("--yes", action="store_true",
                   help=f"live only: skip typing the confirmation ({CONFIRM!r})")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv=None) -> int:
    a = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    ecfg = EngineConfig(mode=a.mode, out_dir=a.out_dir, minutes=a.minutes,
                        cycle_seconds=a.cycle_seconds, max_markets=a.max_markets,
                        pairs_file=a.pairs_file, max_rps=a.max_rps, resume=a.resume,
                        snapshot_seconds=a.snapshot_seconds,
                        equity_seconds=a.equity_seconds)
    scfg = StrategyConfig(maker_edge=a.maker_edge, taker_edge=a.taker_edge,
                          order_usd=a.order_usd, max_fair_spread=a.max_fair_spread,
                          taker_enabled=not a.no_taker, maker_enabled=not a.no_maker)
    rcfg = RiskConfig(bankroll=a.bankroll, max_market_usd=a.max_market_usd,
                      max_total_usd=a.max_total_usd,
                      daily_loss_limit=a.daily_loss_limit, kill_file=a.kill_file)
    broker = None
    if a.mode == "live":
        key, secret = os.environ.get("PMUS_KEY_ID"), os.environ.get("PMUS_SECRET_KEY")
        if not key or not secret:
            print("Set PMUS_KEY_ID and PMUS_SECRET_KEY first.", file=sys.stderr)
            return 2
        print(f"LIVE trading on Polymarket US with real money. Limits: ${rcfg.max_total_usd:.0f} "
              f"total, ${rcfg.max_market_usd:.0f} per market, stop after "
              f"${rcfg.daily_loss_limit:.0f} daily loss.")
        if not a.yes and input(f"Type '{CONFIRM}' to continue: ").strip() != CONFIRM:
            print("Not confirmed; exiting.")
            return 1
        from .broker import LiveBroker
        broker = LiveBroker(key, secret, os.path.join(ecfg.out_dir, "live_orders.json"))
        os.makedirs(ecfg.out_dir, exist_ok=True)
        broker.sync()
        broker.cancel_all()  # start clean: drop this bot's own leftovers
    from .strategies import build
    Engine(ecfg, scfg, RiskManager(rcfg), broker, build(a.strategies, scfg)).run()
    print(open(os.path.join(ecfg.out_dir, "report.md")).read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
