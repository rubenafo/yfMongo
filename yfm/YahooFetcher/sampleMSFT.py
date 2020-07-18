#!/usr/bin/python3

#
# Copyright 2020, Ruben Afonso - http://www.github.com/rubenafo
# Licensed under the Apache License (see the LICENSE file)
#

import YahooFetcher

y = YahooFetcher.YahooFetcher()
print (y.getHistAsJson ('HO.PA','20180101','20180220'))

