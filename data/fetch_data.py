import yfinance as yf

def get_data(ticker="RELIANCE.NS"):
    df = yf.download(ticker, period="6mo", interval="1d")
    return df


if __name__ == "__main__":
    df = get_data("RELIANCE.NS")
    print(df.tail())
