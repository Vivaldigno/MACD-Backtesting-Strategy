import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path
import matplotlib.pyplot as plt

filepath = Path('C:\Program Files (x86)\MACD Trading Model - Backtest/out.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)

# Create a dataframe filled with info about the companies of th S&P 500
companies_data = pd.read_csv("C:\\Users\\35988\\Downloads\\constituents-financials_csv.csv")
# Create list that holds the cumulative returns over a 10-year period
cumulative_strategy_returns_list = []
cumulative_daily_returns_list = []

for x in companies_data["Symbol"]:
    # Import the stock data
    data = yf.download(x, '2012-01-01')

    # Calculating the Exponential Moving Averages - ЕMA
    data["12d_EMA"] = data["Close"].ewm(span=12, adjust=False).mean()
    data["26d_EMA"] = data["Close"].ewm(span=26, adjust=False).mean()

    # Calculate MACD line
    data["MACD"] = data["12d_EMA"] - data["26d_EMA"]

    # Calculate MACD Signal line
    data["MACD_signal"] = data["MACD"].ewm(span=9, adjust=False).mean()

    # Trade signals: 1 --> buy signal, -1 --> sell signal
    data["Trade_Signal"] = np.nan

    # Buy signals
    data.loc[data["MACD"] > data["MACD_signal"], "Trade_Signal"] = 1

    # Sell signals
    data.loc[data["MACD"] < data["MACD_signal"], "Trade_Signal"] = -1

    # Fill the null values with the last recorded non-null value, until another is recorded
    data = data.fillna(method="ffill")

    # The stock's daily percentage change
    data["Daily%_change"] = data["Close"].pct_change()

    # The daily percentage change of the strategy
    data["Strategy%_change"] = data["Daily%_change"] * data["Trade_Signal"].shift(1)

    # Calculate cumulative strategy returns
    cumulative_strategy_returns = (data["Strategy%_change"] + 1).cumprod()
    cumulative_daily_returns = (data["Daily%_change"] + 1).cumprod()
    if cumulative_strategy_returns.shape == (0,):
        cumulative_strategy_returns_list.append(0)
    else:
        cumulative_strategy_returns_list.append(cumulative_strategy_returns[-1])

    if cumulative_daily_returns.shape == (0,):
        cumulative_daily_returns_list.append(0)
    else:
        cumulative_daily_returns_list.append(cumulative_daily_returns[-1])

companies_data["cumstrat_returns_10y"] = cumulative_strategy_returns_list
companies_data["cum_returns_10y"] = cumulative_daily_returns_list

companies_data = companies_data.loc[companies_data["cumstrat_returns_10y"] != 0]

companies_data.to_csv(filepath)
