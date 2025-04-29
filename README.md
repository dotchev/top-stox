# top-stox

Here we derive some stats on top US stocks & ETFs.

Our stock universe:
- [S&P 500 stocks](data/sp500_stocks.csv) (source [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies))
- [Top 1000 ETFs](data/top-etfs.csv) by assets (Source [etfdb.com](https://etfdb.com/screener/#sort_by=assets&sort_direction=desc&page=1))

## Prerequisites

:information_source: You need this only if you want to play with the Python code.
Can also jump straight to the results at the bottom.

Python 3.12 or later

Install required libraries
```sh
pip install -r requirements.txt
```

## Fetching stock data
Scrape S&P 500 stocks from Wikipedia
```sh
python scrape_sp500_stox.py
```

Fetch historical price data for all stocks and ETFs in our universe<br/>
:warning: this takes about 30m.
```sh
python fetch-stocks-history.py
```
All the data is already present in [data/stock_history](data/stock_history).

## Number crunching

Here for each stock/ETF we load the historical price data and calculate:
- Compound Annual Growth Rate (CAGR) or annualized growth rate
- Average change over a sliding window of 1 year
- Standard deviation (std) of the above 1 year change
- Return / risk ratio (the ratio of the two values above)

```sh
python top-stox.py 
```

[The result](data/top-stox.csv) is sorted by return / risk ratio so you can see the top stocks/ETFs at the top.
