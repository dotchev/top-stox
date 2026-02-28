# This script fetches historical data for stocks, ETFs, UCITS, and other symbols from Yahoo Finance
# and saves it to CSV files.

import os
import pandas as pd
import yfinance as yf
import time
from config import *

def build_all_symbols():
    """Load all symbol files and build a combined dataframe with columns: symbol, type, name"""
    
    # Load S&P 500 stocks
    sp500_data = pd.read_csv(SP500_STOCKS_FILE)
    sp500_df = pd.DataFrame({
        'symbol': sp500_data['Symbol'].str.replace('.', '-', regex=False),  # for Yahoo Finance compatibility
        'type': 'stock',
        'name': sp500_data['Security']
    })
    print(f'Loaded {len(sp500_df)} S&P 500 stocks')
    
    # Load ETFs
    etf_data = pd.read_csv('data/etfs-by-assets.csv')[:1500]  # limit to top 1500 ETFs by assets
    etf_df = pd.DataFrame({
        'symbol': etf_data['symbol'].str.replace('.', '-', regex=False),  # for Yahoo Finance compatibility
        'type': 'ETF',
        'name': etf_data['name']
    })
    print(f'Loaded {len(etf_df)} ETFs')
    
    # Load UCITS
    ucits_data = pd.read_csv(TOP_UCITS_FILE)
    ucits_df = pd.DataFrame({
        'symbol': ucits_data['symbol'],
        'type': 'UCITS',
        'name': ucits_data['name']
    })
    print(f'Loaded {len(ucits_df)} UCITS')
    
    # Load extra symbols (already has symbol, type, name columns)
    extra_data = pd.read_csv(EXTRA_SYMBOLS_FILE)
    print(f'Loaded {len(extra_data)} extra symbols')
    
    # Combine all dataframes
    all_symbols = pd.concat([sp500_df, etf_df, ucits_df, extra_data], ignore_index=True)
    
    # Save to CSV
    all_symbols.to_csv(ALL_SYMBOLS_FILE, index=False)
    print(f'Saved {len(all_symbols)} symbols to {ALL_SYMBOLS_FILE}')
    
    return all_symbols

os.makedirs(STOCK_HISTORY_DIR, exist_ok=True)

# Build combined symbols file and load it
all_symbols = build_all_symbols()
print(f'Loaded {len(all_symbols)} symbols')

for i, row in all_symbols.iterrows():
    symbol = row['symbol']
    name = row['name']
    symbol_type = row['type']

    f = os.path.join(STOCK_HISTORY_DIR, symbol + '.csv')
    if os.path.exists(f):
        continue
    
    print(f'[{i+1}/{len(all_symbols)}] fetching {symbol} ({symbol_type}: {name})')
    try:
        td = yf.Ticker(symbol)
        history = td.history(interval='1wk', period='5y')  # 5 years of weekly data
    except Exception as e:
        print(f"Failed to fetch history for {symbol}: {e}")
        continue

    print(f'Fetched {len(history)} weeks of history')
    history.to_csv(f)

    time.sleep(1)  # avoid rate limiting and getting blocked by Yahoo Finance