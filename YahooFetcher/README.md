YahooFetcher
===============

A Python class to extract stock data from famous Yahoo Finance API.

Features:
  * real-time market data (15 min delayed)
  * historical series
  * Index components

Further information of its usage, in the wiki:
https://github.com/figurebelow/yfinancefetcher/wiki/YFinanceFetcher-how-to

Disclaimer:
this module provides access to a non-official Yahoo API. In fact they do not provide any type of support/documentation
of it and all existent information has been obtained through reverse engineering along the years. <br>
Despite being a well-known API in the finance world, real-time data is not guaranteed to be so real and values may be delayed.<br>
Use at your own risk and do not abuse Yahoo resources.

Example
=======
Run sampleMSFT.py to fetch Microsoft shares for first fourth monts of 2017:
```python
#!/usr/bin/python

import YahooFetcher

y = YahooFetcher.YahooFetcher()
hist = y.getHistAsJson ('MSFT','1/1/2017','15/4/2017','d+v')
for row in hist:
    print row
```
The output will look like this:
```javascript
{'o': '65.290001', 'c': '64.949997', 'd': '13/04/2017', 'v': '17755800', 'dv': 0, 'h': '65.860001', 'ac': '64.949997', 'l': '64.949997', 'sym': 'MSFT'}
...
{'o': '62.790001', 'c': '62.580002', 'd': '03/01/2017', 'v': '20694100', 'dv': 0, 'h': '62.84', 'ac': '62.202897', 'l': '62.130001', 'sym': 'MSFT'}

```

It also provides a method to extract the underlying components of an index (up to 30):
```python
print YahooQuery().getComponents("DJI")

['JNJ', 'CAT', 'MCD', 'V', 'MSFT', 'PG', 'PFE', 'UTX', 'MMM', 'AXP', 'JPM', 'VZ', 'INTC', 'BA', 'GE', 'HD', 'GS', 'DIS', 'IBM', 'AAPL', 'UNH', 'XOM', 'WMT', 'KO', 'TRV', 'DD', 'NKE', 'MRK', 'CSCO', 'CVX']
```
