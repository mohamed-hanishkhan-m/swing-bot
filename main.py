from data.fetch_data import get_data
from strategies.swing_strategy import add_indicators, generate_signal

df = get_data("RELIANCE.NS")

# FIX MultiIndex issue
if isinstance(df.columns, type(df.columns)):
    df.columns = df.columns.get_level_values(0)

df = add_indicators(df)
df["Signal"] = df.apply(generate_signal, axis=1)

print(df.tail())
