#
# Copyright 2017, Ruben Afonso - http://www.github.com/rubenafo
# Licensed under the Apache License (see the LICENSE file)
#

#
# This class builds the URL using Yahoo conventions.
#

class Query:

  HIST_BASE_URL = "http://ichart.finance.yahoo.com/table.csv?s=_SYMBOL_&a=_M1_&b=_D1_&c=_Y1_&d=_M2_&e=_D2_&f=_Y2_&g=_TYPE_&ignore=.csv"
  BASE_URL="http://finance.yahoo.com/d/quotes.csv?s="

  def __init__(self):
    None

  # Returns the url string given the attributes (as defined in yfinanceoptions.txt),
  # and the stock symbols to fetch (e.g. GOOG for google).
  def queryStock (self, symbols, attr):
    baseUrl = self.BASE_URL
    baseUrl += symbols
    options = self.__parseAttr(attr);
    return baseUrl + options

  def __parseAttr (self, attr):
    tokens = attr.split(",")
    elems = "&f="
    for str in tokens:
      elems += str
    return elems

  #
  # Historical data methods
  #

  # Date params are in format dd/mm/yyyy
  def getHist (self, symbol, startDate, endDate, type):   # type = d daily, w weekly, m monthly, v dividend
      return self.__buildHistURL (symbol, startDate, endDate, type)

  def __buildHistURL (self, symbol, startDate, endDate, type):
    symbol_url = self.HIST_BASE_URL.replace("_SYMBOL_", symbol)
    date1 = startDate.split("/")
    date2 = endDate.split("/")
    symbol_url = symbol_url.replace ("_M1_", str(int(date1[1])-1))   # first, the month -1
    symbol_url = symbol_url.replace ("_D1_", date1[0])     # day
    symbol_url = symbol_url.replace ("_Y1_", date1[2])     # year
    symbol_url = symbol_url.replace ("_M2_", str(int(date2[1])-1))   # idem
    symbol_url = symbol_url.replace ("_D2_", date2[0])
    symbol_url = symbol_url.replace ("_Y2_", date2[2])
    symbol_url = symbol_url.replace ("_TYPE_", type)
    return symbol_url

