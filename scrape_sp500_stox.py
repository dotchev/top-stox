import pandas as pd
import os
from config import *

os.makedirs("data", exist_ok=True)
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)
sp500_df = tables[0]
sp500_df = sp500_df.sort_values(by="Symbol")
sp500_df.to_csv(SP500_STOCKS_FILE, index=False)
print(f"S&P 500 stocks data saved to {SP500_STOCKS_FILE}")