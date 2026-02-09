import matplotlib.pyplot as plt
from data.fetch_data import get_data
from strategies.swing_strategy import add_indicators

# Get data
df = get_data("RELIANCE.NS")
df.columns = df.columns.get_level_values(0)
df = add_indicators(df)

# Plot
plt.figure(figsize=(12,6))
plt.plot(df["Close"], label="Close Price")
plt.plot(df["EMA200"], label="EMA200", color="orange")

# Mark Buy Signals
buy = df[(df["Close"] > df["EMA200"]) & (df["RSI"] < 40)]
plt.scatter(buy.index, buy["Close"], marker="^", color="green", label="BUY")

# Mark Sell Signals
sell = df[df["RSI"] > 70]
plt.scatter(sell.index, sell["Close"], marker="v", color="red", label="SELL")

plt.title("RELIANCE Swing Trading Bot")
plt.legend()
plt.show()
