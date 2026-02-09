import pandas as pd
import yfinance as yf

def get_data(ticker="RELIANCE.NS"):
    df = yf.download(ticker, period="6mo", interval="1d")
    return df

def add_indicators(df):
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    return df

def check_signal(df):
    if df["MA20"].iloc[-1] > df["MA50"].iloc[-1]:
        return "BUY SIGNAL 📈"
    else:
        return "NO BUY ❌"

df = get_data()
df = add_indicators(df)
print(df.tail())
print("Signal:", check_signal(df))
