from data.fetch_data import get_data
from strategies.swing_strategy import add_indicators

capital = 100000
position = 0
buy_price = 0

df = get_data("RELIANCE.NS")
df.columns = df.columns.get_level_values(0)
df = add_indicators(df)

stop_loss_pct = 0.03   # 3%
target_pct = 0.06      # 6%

for i in range(len(df)):
    row = df.iloc[i]

    # BUY
    if row["Close"] > row["EMA200"] and row["RSI"] < 40 and position == 0:
        position = capital / row["Close"]
        buy_price = row["Close"]
        capital = 0
        stop_loss = buy_price * (1 - stop_loss_pct)
        target = buy_price * (1 + target_pct)
        print(f"BUY at {buy_price}")

    # SELL (Target or Stoploss)
    elif position > 0:
        if row["Close"] <= stop_loss or row["Close"] >= target:
            capital = position * row["Close"]
            profit = capital - (position * buy_price)
            print(f"EXIT at {row['Close']} | Profit: {profit:.2f}")
            position = 0


# Final portfolio value
final_value = capital if capital > 0 else position * df.iloc[-1]["Close"]
print("Final Value:", final_value)
print("Total Profit:", final_value - 100000)
