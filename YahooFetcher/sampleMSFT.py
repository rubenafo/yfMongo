#!/usr/bin/python

#
# Copyright 2017, Ruben Afonso - http://www.github.com/rubenafo
# Licensed under the Apache License (see the LICENSE file)
#

import YahooFetcher

y = YahooFetcher.YahooFetcher()
hist = y.getHistAsJson ('MSFT','1/1/2017','15/4/2017','d+v')
for row in hist:
    print row

