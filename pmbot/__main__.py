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
                   help="comma list, in priority order: copytop, evsniper, sportsgameday, fairvalue")
    g.add_argument("--leaders-file", default=os.path.join(os.path.dirname(__file__), "leaders.json"),
                   help="copytop: wallets to copy")
    g.add_argument("--copy-sells", action="store_true",
                   help="copytop: also copy the leaders' sells (default: hold to settlement)")
    g.add_argument("--max-wallet-usd", type=float, default=0.0,
                   help="copytop: most money open copying any one wallet (0 = no cap)")
    g.add_argument("--conviction-sizing", action="store_true",
                   help="copytop: stake x0.5 when a leader bets under half their usual size, "
                   "x1.5 at twice it or more")
    g.add_argument("--ev-min-edge", type=float, default=0.02,
                   help="evsniper: buy when Pinnacle's fair probability beats the ask by this "
                   "much after the taker fee (needs ODDS_API_KEY)")
    g.add_argument("--ev-budget", type=int, default=450,
                   help="evsniper: odds requests per month (free key: 500)")
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
    g.add_argument("--daily-loss-limit", type=float, default=r.daily_loss_limit,
                   help="halt for the day after losing this much (0 = no daily stop)")
    g.add_argument("--kill-file", default=r.kill_file)
    p.add_argument("--no-preview", action="store_true",
                   help="paper: don't check orders with the exchange's order preview "
                   "even when API keys are set")
    p.add_argument("--yes", action="store_true",
                   help=f"live only: skip typing the confirmation ({CONFIRM!r})")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv=None) -> int:
    a = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    logging.getLogger("httpx").setLevel(logging.WARNING)  # one line per API call otherwise
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
        stop = (f"stop after ${rcfg.daily_loss_limit:.0f} daily loss"
                if rcfg.daily_loss_limit > 0 else "no daily stop")
        print(f"LIVE trading on Polymarket US with real money. Limits: ${rcfg.max_total_usd:.0f} "
              f"total, ${rcfg.max_market_usd:.0f} per market, {stop}.")
        if not a.yes and input(f"Type '{CONFIRM}' to continue: ").strip() != CONFIRM:
            print("Not confirmed; exiting.")
            return 1
        from .broker import LiveBroker
        broker = LiveBroker(key, secret, os.path.join(ecfg.out_dir, "live_orders.json"))
        os.makedirs(ecfg.out_dir, exist_ok=True)
        broker.sync()
        broker.cancel_all()  # start clean: drop this bot's own leftovers
    from .strategies import build
    engine = Engine(ecfg, scfg, RiskManager(rcfg), broker,
                    build(a.strategies, scfg, a.leaders_file, copy_sells=a.copy_sells,
                          conviction_sizing=a.conviction_sizing, max_wallet_usd=a.max_wallet_usd,
                          ev_min_edge=a.ev_min_edge, ev_monthly_budget=a.ev_budget))
    if a.mode == "paper" and not a.no_preview and os.environ.get("PMUS_KEY_ID") \
            and os.environ.get("PMUS_SECRET_KEY"):
        from .broker import PreviewChecker
        checker = PreviewChecker(os.environ["PMUS_KEY_ID"], os.environ["PMUS_SECRET_KEY"])
        try:
            checker.verify_keys()
        except Exception as e:
            print(f"Polymarket US API keys didn't authenticate ({type(e).__name__}); "
                  "check PMUS_KEY_ID / PMUS_SECRET_KEY. Not trading.", file=sys.stderr)
            return 2
        engine.broker.checker = checker
        print("Paper orders are checked with Polymarket US order previews (nothing is placed).")
    engine.run()
    print(open(os.path.join(ecfg.out_dir, "report.md")).read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
