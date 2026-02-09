# backtest/pro_backtester.py
from data.fetch_data import get_data
from strategies.swing_strategy import add_indicators

capital = 100000
balance = capital
position = 0
trades = []

df = get_data("RELIANCE.NS")
df.columns = df.columns.get_level_values(0)
df = add_indicators(df)

for i in range(len(df)):
    row = df.iloc[i]

    # BUY
    if row["Close"] > row["EMA200"] and row["RSI"] < 40 and position == 0:
        position = balance / row["Close"]
        buy_price = row["Close"]
        balance = 0
        trades.append(("BUY", row.name, buy_price))

    # SELL
    elif row["RSI"] > 70 and position > 0:
        sell_price = row["Close"]
        balance = position * sell_price
        profit = balance - capital
        trades.append(("SELL", row.name, sell_price, profit))
        position = 0

final_value = balance if position == 0 else position * df.iloc[-1]["Close"]
profit = final_value - capital

print("Initial Capital:", capital)
print("Final Value:", final_value)
print("Total Profit:", profit)
print("Total Trades:", len(trades))

for t in trades:
    print(t)
