import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import json
from datetime import datetime
from telegram_bot import send_message

PORTFOLIO_FILE = "paper_trading/portfolio.json"
TRADES_FILE = "paper_trading/trades.csv"


def daily_report():
    today = datetime.now().strftime("%d %b %Y")

    # Load portfolio
    with open(PORTFOLIO_FILE, "r") as f:
        portfolio = json.load(f)

    capital = portfolio["capital"]
    open_trade = portfolio["open_trade"]

    # Load today trades
    trades_today = []
    if os.path.exists(TRADES_FILE):
        with open(TRADES_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["date"].startswith(datetime.now().strftime("%Y-%m-%d")):
                    trades_today.append(row)

    message = f"📅 Daily Paper Trading Report – {today}\n\n"
    message += f"Capital: ₹{capital:,.2f}\n\n"

    if open_trade:
        message += "Open Trade:\n"
        message += f"Stock: {open_trade['stock']}\n"
        message += f"Entry: ₹{open_trade['buy_price']:.2f}\n"
        message += f"SL: ₹{open_trade['stop_loss']:.2f}\n"
        message += f"Target: ₹{open_trade['target']:.2f}\n\n"
    else:
        message += "Open Trade: None\n\n"

    message += f"Trades Today: {len(trades_today)}\n"
    message += "Status: ✅ Bot running normally"

    send_message(message)


if __name__ == "__main__":
    daily_report()
