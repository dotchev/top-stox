import pandas as pd
import os
from config import *

os.makedirs("data", exist_ok=True)
url = "https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"
sp500_df = pd.read_csv(url)
sp500_df = sp500_df.sort_values(by="Symbol")
sp500_df.to_csv(SP500_STOCKS_FILE, index=False)
print(f"S&P 500 stocks data saved to {SP500_STOCKS_FILE}")