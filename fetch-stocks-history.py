# This script fetches historical data for S&P 500 stocks and top ETFs from Yahoo Finance
# and saves it to CSV files.

import os
import pandas as pd
import yfinance as yf
import time
from config import *

os.makedirs(STOCK_HISTORY_DIR, exist_ok=True)

sp500_data = pd.read_csv(SP500_STOCKS_FILE)
etf_data = pd.read_csv(TOP_ETFS_FILE)

sp500_symbols = [(row['Symbol'], row['Security']) for _, row in sp500_data.iterrows()]
etf_symbols = [(row['Symbol'], row['ETF Name']) for _, row in etf_data.iterrows()]

symbols = sp500_symbols + etf_symbols
print(f'Loaded {len(symbols)} symbols')

for i, (symbol, description) in enumerate(symbols):
  symbol = symbol.replace('.', '-')  # for yahoo finance compatibility

  f = os.path.join(STOCK_HISTORY_DIR, symbol + '.csv')
  if os.path.exists(f):
      continue
  
  print(f'Processing {i+1}/{len(symbols)} - {symbol} ({description})')
  try:
      td = yf.Ticker(symbol)
      history = td.history(interval='1wk', period='5y') # 5 years of weekly data
  except Exception as e:
      print(f"Failed to fetch history for {symbol}: {e}")
      continue

  print(f'Fetched {len(history)} weeks of history')
  history.to_csv(f)

  time.sleep(1)  # avoid rate limiting and getting blocked by Yahoo Finance