from data.fetch_data import get_data
from strategies.swing_strategy import add_indicators
from telegram_bot import send_message
from Paper_Trading.paper_engine import try_buy, try_sell

import time

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

signals = []

for stock in stocks:
    df = get_data(stock)
    df.columns = df.columns.get_level_values(0)
    df = add_indicators(df)

    last = df.iloc[-1]

    # Trading condition
    if last["Close"] > last["EMA200"] and last["RSI"] < 40:
        signals.append(f"BUY: {stock} at {last['Close']} RSI={last['RSI']:.2f}")
    # SELL check (runs every scan)
    try_sell(last["Close"])
    
# # FORCE TEST SIGNAL
# signals.append(f"TEST BUY: {stock} at {last['Close']}")

print("Today's Signals:")
for s in signals:
    print(s)

print("Signals list:", signals)

# Send Telegram
message = "\n".join(signals)
send_message(message)
time.sleep(2)
