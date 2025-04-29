import pandas as pd
import os
from config import *

# Load stock and ETF data and create unified symbols list with tuple comprehensions
sp500_stocks = pd.read_csv(SP500_STOCKS_FILE)
top_etfs = pd.read_csv(TOP_ETFS_FILE)

# Create symbols list using list comprehensions for both stocks and ETFs
symbols = (
    [(row['Symbol'], row['Security'], "stock") for _, row in sp500_stocks.iterrows()] +
    [(row['Symbol'], row['ETF Name'], "ETF") for _, row in top_etfs.iterrows()]
)

change_weeks = 52
history_weeks = 262 # 5 years of weekly data

rows = []
for symbol, description, type in symbols:
  symbol = symbol.replace('.', '-')  # for yahoo finance compatibility
  filename = f'{symbol}.csv'
  history = pd.read_csv(os.path.join(STOCK_HISTORY_DIR, filename))
  if len(history) < history_weeks:
    continue
  history = history.tail(history_weeks)
  sma = history.Close.rolling(window=13).mean().dropna() # 13 weeks = 3 months smoothing
  cagr = (sma.iloc[-1] / sma.iloc[0]) ** (52 / len(sma)) - 1
  changes = history.Close.pct_change(periods=change_weeks).dropna()
  mean = changes.mean()
  std = changes.std()
  if std == 0:
    continue
  rows.append({
      'symbol': symbol,
      'description': description,
      'type': type,
      'CAGR': cagr, # Compound Annual Growth Rate
      'avg_change': mean,
      'std': std,
      'R/R': mean / std,
  })

df = pd.DataFrame(rows).sort_values(by='R/R', ascending=False)
df.to_csv(RETURN_RISK_FILE, index=False)
