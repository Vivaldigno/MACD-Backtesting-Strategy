import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path
import matplotlib.pyplot as plt


companies_data = pd.read_csv("C:\\Program Files (x86)\\MACD Trading Model - Backtest\\out.csv")
sectors = companies_data.groupby('Sector', as_index=False)["cumstrat_returns_10y"].mean()
sector = companies_data.groupby('Sector', as_index=False)['cum_returns_10y'].mean()
x_axis = np.arange(len(sectors["Sector"]))
plt.bar(sectors["Sector"],sectors["cumstrat_returns_10y"], 0.4,label='cum_strat_returns_10y')
plt.bar(sectors["Sector"],sector["cum_returns_10y"], 0.4, alpha = 0.4, label='cum_returns_10y')
plt.title('Cumulative Return of Strategy by Industry')
plt.xlabel('Industries')
plt.xticks(rotation=30)
plt.ylabel('Cumulative Return of Strategy')
plt.legend()
plt.show()
