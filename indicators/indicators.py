import pandas_ta as ta

def add_indicators(df):
    df["EMA50"] = ta.ema(df["Close"], length=50)
    df["EMA200"] = ta.ema(df["Close"], length=200)
    df["RSI"] = ta.rsi(df["Close"], length=14)
    return df
