import pandas as pd

def add_indicators(df):
    # EMA
    df["EMA200"] = df["Close"].ewm(span=200, adjust=False).mean()

    # RSI Calculation
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

def generate_signal(row):
    if row["Close"] > row["EMA200"] and row["RSI"] < 40:
        return "BUY"
    elif row["RSI"] > 70:
        return "SELL"
    else:
        return "HOLD"
