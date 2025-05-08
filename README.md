# top-stox

Here we list the top US stocks & ETFs by return / risk ratio.

Our stock universe:
- [S&P 500 stocks](data/sp500_stocks.csv) (source [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies))
- [Top 1000 ETFs](data/top-etfs.csv) by assets (Source [etfdb.com](https://etfdb.com/screener/#sort_by=assets&sort_direction=desc&page=1))

If you are in a hurry, you can jump straight to [the results](#the-results) at the bottom.

Read on to find out how we got to these results.

## Prerequisites

Python 3.12 or later

Install required libraries
```sh
pip install -r requirements.txt
```

## Getting stock tickers
Scrape S&P 500 stocks from Wikipedia
```sh
python scrape_sp500_stox.py
```
The result will is stored in [data/sp500_stocks.csv](data/sp500_stocks.csv).

A list of top 1000 ETFs by assets is already prepared in [data/top-etfs.csv](data/top-etfs.csv).

## Fetching price data
Fetch historical price data for all stocks and ETFs in our universe (~1500 symbols).<br/>
:warning: This takes about 30m.
```sh
python fetch-stocks-history.py
```
This script fetches from Yahoo Finance weekly price data for the past 5 years for each symbol.
It creates a csv file for each symbol in [data/stock_history](data/stock_history).
The script skips any symbols for which the corresponding csv file already exists.
This allows it to resume operation from the point it left.

All the data is already present in [data/stock_history](data/stock_history).
So, the script will do nothing.

## Number crunching

Here for each stock/ETF we load the historical price data and calculate:
- Annualized growth rate (annual change) of 3 month moving average
- Standard deviation of changes over a sliding window of 1 year (volatility)
- Return / risk ratio (the ratio of the two values above)

```sh
python top-stox.py 
```
This will produce [data/top-stox.csv](data/top-stox.csv).
Notice that the result is smaller (~1274 rows) than our stock universe.
This is because some symbols have history shorter than 5 years.

## The results
Data as of 2024-04-29

The results are already provided in [data/top-stox.csv](data/top-stox.csv).
It lists the stocks and ETFs in [our universe](#top-stox) sorted by return / risk ratio so you can see the best stocks/ETFs at the top.
The previous section describes the table columns.

You can open the table in an easier to view format in [Google Sheets](https://docs.google.com/spreadsheets/d/1FcSCCSSMf4GDMnWiIf6uvauVM-bnhS9nifoqAC2VCtM).
From the menu select _Data > Create filter view_ and you will get filter buttons on each column.
You can use them to slice and dice the data.