# top-stox

Here we compare some assets by return / risk ratio.

Our asset universe:
- [S&P 500 stocks](data/sp500-stocks.csv) (source [datahub.io](https://datahub.io/core/s-and-p-500-companies/r/constituents.csv))
- [Top 1000 ETFs](data/top-etfs.csv) by assets (Source [etfdb.com](https://etfdb.com/screener/#sort_by=assets&sort_direction=desc&page=1))
- [Top 500 UCITS](data/top-ucits.csv) - Euro ETFs with best return/risk (source [justetf.com](https://www.justetf.com/en/search.html?search=ETFS&sortOrder=desc&sortField=fiveYearReturnPerRiskEUR))
- [Additional assets](data/extra-symbols.csv) like Gold and Bitcoin

If you are in a hurry, you can jump straight to [the results](#the-results) at the bottom.

Read on to find out how we got to these results.

## Prerequisites

Python 3.12 or later

Set up a virtual environment and install dependencies:
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Fetching price data
Fetch historical price data for all stocks and ETFs in our universe (~2000 symbols).

:warning: This takes about 42m.
```sh
python fetch-history.py
```
This script fetches from Yahoo Finance weekly price data for the past 5 years for each symbol.
It creates a csv file for each symbol in [data/stock_history](data/stock_history).
The script skips any symbols for which the corresponding csv file already exists.
This allows it to resume operation from the point it left.
To refresh the price data, delete `data/stock_history` before running the script.

All the data is already present in [data/stock_history](data/stock_history).
So, the script will do nothing.

## Number crunching

Here for each symbol we load the historical price data and calculate:
- 5y change
- Geometric mean of 1y changes over a sliding window of 1 year
- Standard deviation of 1y changes over a sliding window of 1 year (volatility)
- Return / risk ratio (the ratio of the two values above)

```sh
python top-stox.py 
```
This will produce [data/top-stox.csv](data/top-stox.csv).
Notice that the result is smaller (~1745 rows) than our stock universe.
This is because some symbols have history shorter than 5 years.

## The results
Data as of 2025-02-14

The results are already provided in [data/top-stox.csv](data/top-stox.csv).
It lists the assets in [our universe](#top-stox) sorted by return / risk ratio so you can see the "best" ones at the top.
The previous section describes the table columns.

You can open the table in an easier to view format in [Google Sheets](https://docs.google.com/spreadsheets/d/1FcSCCSSMf4GDMnWiIf6uvauVM-bnhS9nifoqAC2VCtM).
From the menu select _Data > Create filter view_ and you will get filter buttons on each column.
You can use them to slice and dice the data.