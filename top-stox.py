import pandas as pd
from scipy.stats import gmean
import os
from config import *

# Load all symbols from the combined file
all_symbols = pd.read_csv(ALL_SYMBOLS_FILE)

# length of the sliding window
change_weeks = 52 # 1 year of weekly data

# overall period to analyze
history_weeks = 5 * 52 # 5 years of weekly data

rows = []
for _, row in all_symbols.iterrows():
  symbol = row['symbol']
  name = row['name']
  symbol_type = row['type']
  filename = f'{symbol}.csv'
  filepath = os.path.join(STOCK_HISTORY_DIR, filename)
  if not os.path.exists(filepath):
    continue
  history = pd.read_csv(filepath)
  if len(history) < history_weeks:
    continue
  history = history.tail(history_weeks)
  change = history.Close.iloc[-1] / history.Close.iloc[0] - 1
  sma = history.Close.rolling(window=13).mean().dropna() # 13 weeks = 3 months smoothing
  cagr = (sma.iloc[-1] / sma.iloc[0]) ** (52 / len(sma)) - 1 # annualized change
  changes = history.Close.pct_change(periods=change_weeks).dropna()
  gmean_change = gmean(1 + changes) - 1 # geometric mean of changes
  std = changes.std()
  if std == 0:
    continue
  rows.append({
    'symbol': symbol,
    'name': name,
    'type': symbol_type,
    '5y change': change,
    'gmean change': gmean_change,
    'volatility': std,
    'ratio': gmean_change / std,
  })

if not rows:
  print("No valid symbols found. Run fetch-history.py first to fetch historical data.")
  exit(1)

df = pd.DataFrame(rows).sort_values(by='ratio', ascending=False)
df.to_csv(RESULT_FILE, index=False)
print(f"Results: {len(rows)}/{len(all_symbols)} saved to {RESULT_FILE}")