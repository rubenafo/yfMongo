#!/usr/bin/python

import YahooFetcher

y = YahooFetcher.YahooFetcher()
hist = y.getHistAsJson ('MSFT','1/1/2017','15/4/2017','d+v')
for row in hist:
    print row
