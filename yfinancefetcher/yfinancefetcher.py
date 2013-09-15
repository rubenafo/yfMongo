# Copyright 2012 Ruben Afonso, http://www.figurebelow.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv;
import urllib2;
import yfinancequery;

#
# This class invokes a query builder, fetches the content from the received URL
# and returns the result
#

class YFinanceFetcher:

  def __init__(self):
    None

  def __appendSymbol (self, table, symbol, append):
    if (append == True):
      table[0].insert(0,"Symbol")
      for row in table[1:]:
        row.insert(0, symbol)

  def __appendHeader (self, table, keepHeader):
      if (keepHeader == False):
        table.pop(0)

  # Gets historical data in _table_ format.
  # - symbol: an list of stock symbols, e.g. 'GOOG,MICRO'
  # - starDate: starting date, e.g 12/5/2012 for 12th of May of 2012
  # - endDate: end date
  # - info: interval time. Accepted values:
  #   d daily, w weekly, m monthly, v dividends, and d+v for daily data and dividends
  # - appendSymbol: whether each row must contain the symbol at the begining
  # - keepHeader: whether the first row is the description header
  #
  # Returned values:
  #  a list of lists where each one has the following elements:
  #  Symbol (optional), Date, Open, High, Low, Close, Volume, Adj Close, Dividends(optional)
  #
  def getHist (self, symbol, startDate, endDate, info, appendSymbol, appendHeader):
    query = yfinancequery.YFinanceQuery ()
    if (info == "d+v"):
      url_daily = urllib2.urlopen (query.getHist(symbol, startDate, endDate, "d"))
      table_daily = csv.reader (url_daily.read().splitlines())
      url_div = urllib2.urlopen (query.getHist(symbol, startDate, endDate, "v"))
      table_div = csv.reader (url_div.read().splitlines())
      table_daily = list(table_daily)
      table_div = list(table_div)
      if (len(table_div) > 0):
        for rowdaily in table_daily:
          hasdiv = False
          for rowdiv in table_div:
            # matching dates? This also matches the headers, adding
            # automagically the 'Dividends' column ...
            if (rowdaily[0] == rowdiv[0]):
              rowdaily.append(rowdiv[1])
              hasdiv = True
              break
          if (hasdiv == False):
            rowdaily.append (0)
      self.__appendSymbol (table_daily, symbol, appendSymbol)
      self.__appendHeader (table_daily, appendHeader)
      return table_daily
    else:
      if (info in ['w','m','d']):
        url = urllib2.urlopen (query.getHist(symbol, startDate, endDate, info));
        table = csv.reader (url.read().splitlines())
        table = list(table)
        self.__appendSymbol(table, symbol, appendSymbol)
        self.__appendHeader(table, appendHeader)
        return table
      else:
        print "Error: invalid time option in getHist(): " + info
        return []

  # Gets historical data as CSV
  # - symbol: an list of stock symbols, e.g. 'GOOG,MICRO'
  # - starDate: starting date, e.g 12/5/2012 for 12th of May of 2012
  # - endDate: end date
  # - info: interval time. Accepted values:
  #      d daily, w weekly, m monthly, v dividends, and d+v for daily data and dividends
  #
  # Returned values:
  #  a list of JSON elements where each one has the following fields:
  #     * 'sym': symbol,
  #     * 'd': date,
  #     * 'o': open,
  #     * 'h': high,
  #     * 'l': low,
  #     * 'c': close,
  #     * 'v': volume,
  #     * 'ac': adjusted close,
  #     * 'dv': dividends (optional)
  #
  def getHistAsJson (self, symbol, startDate, endDate, info):
    data = self.getHist (symbol, startDate, endDate, info, True, False)
    jsonList = [];
    for elem in data:
      json = {'sym': elem[0], 'd': elem[1], 'o': elem[2], 'h': elem[3], \
          'l': elem[4], 'c': elem[5], 'v': elem[6], 'ac':elem[7]};
      if (len(elem) == 9): # contains dividens
        json['dv'] = elem[8]
      jsonList.append(json)
    return jsonList


  # Gets current stock data.
  # - symbol: list of stock symbols e.g. 'GOOG,MICRO'
  # - attr: a list of attributes to get as described in the file 'yfinanceoptions.txt'
  def getStock (self, symbols, attr):
    query = yfinancequery.YFinanceQuery ()
    url = query.queryStock (attr, symbols)
    urldata = urllib2.urlopen (url)
    return list(csv.reader (urldata.read().splitlines()))

