#!/usr/bin/python3.6

#
# Copyright 2017, Ruben Afonso - http://www.github.com/rubenafo
# Licensed under the Apache License (see the LICENSE file)
#

import YahooFetcher

y = YahooFetcher.YahooFetcher()
print (y.getHistAsJson ('IBM','20160101','20161231'))

