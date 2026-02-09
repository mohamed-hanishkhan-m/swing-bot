import json
import csv
import os
from datetime import datetime
from telegram_bot import send_message


PORTFOLIO_FILE = "paper_trading/portfolio.json"
TRADES_FILE = "paper_trading/trades.csv"

RISK_PERCENT = 0.01      # 1%
STOP_LOSS_PCT = 0.02     # 2%
TARGET_PCT = 0.04        # 4%
START_CAPITAL = 10000
MAX_DRAWDOWN_PCT = 0.05  # 5%
STATE_FILE = "paper_trading/state.json"


def load_portfolio():
    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)

def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_trade(row):
    with open(TRADES_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def try_buy(stock, price):
    portfolio = load_portfolio()
    state = load_state()

    # Kill switch active → no new trades
    if state["paused"]:
        return

    # Duplicate-signal blocker (once per stock per day)
    today = datetime.now().strftime("%Y-%m-%d")
    if state["last_signal_date"].get(stock) == today:
        return

    # Only one open trade at a time
    if portfolio["open_trade"] is not None:
        return

    capital = portfolio["capital"]
    risk_amount = capital * RISK_PERCENT
    position_size = risk_amount / STOP_LOSS_PCT
    qty = int(position_size / price)

    if qty <= 0:
        return

    trade = {
        "stock": stock,
        "buy_price": price,
        "qty": qty,
        "stop_loss": price * (1 - STOP_LOSS_PCT),
        "target": price * (1 + TARGET_PCT)
    }

    portfolio["open_trade"] = trade
    save_portfolio(portfolio)

    state["last_signal_date"][stock] = today
    save_state(state)

    log_trade([
        datetime.now(), stock, "BUY", price, qty, 0, capital
    ])


def try_sell(price):
    portfolio = load_portfolio()
    state = load_state()
    trade = portfolio["open_trade"]

    if trade is None:
        return

    if price <= trade["stop_loss"] or price >= trade["target"]:
        buy_price = trade["buy_price"]
        qty = trade["qty"]
        pnl = (price - buy_price) * qty

        portfolio["capital"] += pnl
        portfolio["open_trade"] = None
        save_portfolio(portfolio)

        log_trade([
            datetime.now(), trade["stock"], "SELL", price, qty, pnl, portfolio["capital"]
        ])

        # 🔴 Drawdown kill-switch check
        max_allowed_loss = START_CAPITAL * MAX_DRAWDOWN_PCT
        if (START_CAPITAL - portfolio["capital"]) >= max_allowed_loss:
            if not state["kill_switch_triggered"]:
                state["paused"] = True
                state["kill_switch_triggered"] = True
                save_state(state)

                send_message(
                    "🚨 DRAW DOWN KILL-SWITCH ACTIVATED 🚨\n\n"
                    f"Capital dropped to ₹{portfolio['capital']:.2f}\n"
                    "Bot has PAUSED new trades.\n"
                    "Manual review required."
                )

def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "paused": False,
            "kill_switch_triggered": False,
            "last_signal_date": {}
        }
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
