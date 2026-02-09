import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
from datetime import datetime
import matplotlib.pyplot as plt
from telegram_bot import send_photo



TRADES_FILE = "paper_trading/trades.csv"
OUTPUT_FILE = "paper_trading/equity_curve.png"


def generate_equity_curve(send_to_telegram=False):
    dates = []
    capital_values = []

    with open(TRADES_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["action"] == "SELL":
                dates.append(datetime.fromisoformat(row["date"]))
                capital_values.append(float(row["capital"]))

    if not dates:
        print("No completed trades yet. Equity curve not generated.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(dates, capital_values, marker="o")
    # Drawdown kill-switch line (-5%)
    START_CAPITAL = 10000
    MAX_DRAWDOWN_PCT = 0.05
    drawdown_level = START_CAPITAL * (1 - MAX_DRAWDOWN_PCT)

    plt.axhline(
        y=drawdown_level,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Max Drawdown (-5%)"
    )

    plt.title("Paper Trading – Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Capital (₹)")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.savefig(OUTPUT_FILE)
    plt.close()

    print(f"Equity curve saved to {OUTPUT_FILE}")

    if send_to_telegram:
        caption = (
            "📈 Paper Trading – Equity Curve\n\n"
            f"Capital: ₹{capital_values[-1]:,.2f}\n"
            f"Completed Trades: {len(capital_values)}"
        )
    send_photo(OUTPUT_FILE, caption)


if __name__ == "__main__":
    # Change to True when you want to send image
    generate_equity_curve(send_to_telegram=True)
