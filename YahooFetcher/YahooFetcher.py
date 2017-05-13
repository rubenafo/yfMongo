#
# Copyright 2017, Ruben Afonso - http://www.github.com/rubenafo
# Licensed under the Apache License (see the LICENSE file)
#

import csv
import urllib2
import QueryBuilder
from ComponentsExtractor import ComponentsExtractor
from urllib2 import *

#
# This class invokes a query builder, fetches the content from the received URL
# and returns the result
#

class YahooFetcher:

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

  #
  # Converts default Yahoo Finance date format (yyyy-mm-dd)
  # to dd/mm/yyyy
  #
  def __convertDates (self, table, hasHeader, initBySymbol):
    firstRow = 0
    firstCol = 0
    if hasHeader:
      firstRow = 1
    if initBySymbol:
      firstCol = 1
    for row in table[firstRow:]:
      dateSplit = row[firstCol].split("-")
      newDate = dateSplit[2] + "/" + dateSplit[1] + "/" + dateSplit[0]
      row[firstCol] = newDate


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
    query = QueryBuilder.Query ()
    if (info == "d+v"):
      try:
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
        self.__convertDates (table_daily, appendHeader, appendSymbol)
        return table_daily
      except HTTPError: # yahoo returns a 404, sometimes it happens
        return []
      except URLError: # if for example there is no internet access
        return []
    else:
      if (info in ['w','m','d']):
        try:
          url = urllib2.urlopen (query.getHist(symbol, startDate, endDate, info));
          table = csv.reader (url.read().splitlines())
          table = list(table)
          self.__appendSymbol(table, symbol, appendSymbol)
          self.__appendHeader(table, appendHeader)
          self.__convertDates(table, appendHeader, appendSymbol)
          return table
        except HTTPError: # yahoo returns a 404, sometimes it happens
          return []
        except URLError: # if for example there is no internet access
          return []
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
      if (len(elem) == 9): # contains dividends
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

  def getComponents(self, index):
    return ComponentsExtractor().getComponents(index);
