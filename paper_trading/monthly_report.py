import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
from datetime import datetime
from telegram_bot import send_message

TRADES_FILE = "paper_trading/trades.csv"
START_CAPITAL = 10000


def generate_monthly_report():
    now = datetime.now()
    month = now.strftime("%B %Y")

    trades = []
    with open(TRADES_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trades.append(row)

    sell_trades = [t for t in trades if t["action"] == "SELL"]

    if not sell_trades:
        message = f"📊 Paper Trading – {month}\n\nNo trades executed this month."
        send_message(message)
        return

    final_capital = float(sell_trades[-1]["capital"])
    profit = final_capital - START_CAPITAL
    profit_pct = (profit / START_CAPITAL) * 100

    wins = [t for t in sell_trades if float(t["pnl"]) > 0]
    losses = [t for t in sell_trades if float(t["pnl"]) <= 0]

    message = f"""
📊 Paper Trading – Monthly Report ({month})

Starting Capital: ₹{START_CAPITAL:,.0f}
Ending Capital:   ₹{final_capital:,.0f}

Net P&L: ₹{profit:,.0f} ({profit_pct:.2f}%)

Trades Taken: {len(sell_trades)}
Winning Trades: {len(wins)}
Losing Trades: {len(losses)}
Win Rate: {(len(wins)/len(sell_trades))*100:.1f}%
"""

    send_message(message.strip())


if __name__ == "__main__":
    generate_monthly_report()
