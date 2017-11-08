YahooFetcher
===============

A Python class to extract stock data from famous Yahoo Finance API.
Last update fixes the new Yahoo Finance API workaround that had to be implemented after 17th May when Yahoo decided to change the whole structure.

Features:
  * eod quotes, dividends and splits information
  * Index components (up to 30 underlying instruments)
  * NASDAQ and NYSE exchange components


Disclaimer:
this module provides access to a non-official Yahoo API. In fact they do not provide any type of support/documentation
of it and all existent information has been obtained through reverse engineering. <br>
Use at your own risk and do not abuse Yahoo resources.

Example
=======
Run sampleMSFT.py to fetch IBM quote price for last year:
```python
import YahooFetcher

y = YahooFetcher.YahooFetcher()
print (y.getHistAsJson ('IBM','20160101','20161231'))
```
The output will look like
```javascript
[{'c': 175.800003, 'v': 4094800, 'ticker': 'IBM', 'h': 177.070007, 'adjc': 175.800003, 'l': 174.580002, 'date': '2017-01-30', 'o': 176.979996},
...]
```

Quotes, Dividends

It also provides a method to extract the underlying components of an index (up to 30):
```python
print YahooQuery().getComponents("DJI")

['JNJ', 'CAT', 'MCD', 'V', 'MSFT', 'PG', 'PFE', 'UTX', 'MMM', 'AXP', 'JPM', 'VZ', 'INTC', 'BA', 'GE', 'HD', 'GS', 'DIS', 'IBM', 'AAPL', 'UNH', 'XOM', 'WMT', 'KO', 'TRV', 'DD', 'NKE', 'MRK', 'CSCO', 'CVX']
```
