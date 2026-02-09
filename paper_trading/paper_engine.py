import json
import csv
from datetime import datetime

PORTFOLIO_FILE = "paper_trading/portfolio.json"
TRADES_FILE = "paper_trading/trades.csv"

RISK_PERCENT = 0.01      # 1%
STOP_LOSS_PCT = 0.02     # 2%
TARGET_PCT = 0.04        # 4%

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

    log_trade([
        datetime.now(), stock, "BUY", price, qty, 0, capital
    ])

def try_sell(price):
    portfolio = load_portfolio()
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
