#
# Copyright 2017, Ruben Afonso - http://www.github.com/rubenafo
# Licensed under the Apache License (see the LICENSE file)
#

import csv
from QueryBuilder import QueryBuilder
from ComponentsExtractor import ComponentsExtractor
from urllib3 import *
import urllib

#
# This class invokes a query builder, fetches the content from the received URL
# and returns the result
#

class YahooFetcher:

  def __init__(self):
    self.query = QueryBuilder ()

  #
  # Gets historical data in json format.
  #
  # Output: ticker, date, open, high, low, close, volume, adjusted close
  #
  def getHistAsJson (self, symbol, startDate, endDate, event="quote"):
    rows = self.query.getHistURL(symbol, startDate, endDate, event)
    fullData = [data.split(",") for data in rows[1:]]
    jsonList = [];
    if event == "quote":
      for elem in fullData[1:]:
        if len([n for n in elem if n == 'null']) > 0:
          continue
        json = {'date': elem[0], 'o': float(elem[1]), 'h': float(elem[2]), 'l': float(elem[3]), \
            'c': float(elem[4]), 'adjc': float(elem[5]), 'v': int(elem[6]), "ticker":symbol};
        jsonList.append(json)
      return jsonList
    elif event == "div" or event == "split":
      for elem in fullData[1:]:
        json = {"date":elem[0], event:float(elem[1])}
        jsonList.append(json)
      return jsonList

  def getComponents(self, index):
    return ComponentsExtractor().getComponents(index);

    
