#
# Copyright 2017, Ruben Afonso - http://www.github.com/rubenafo
# Licensed under the Apache License (see the LICENSE file)
#

#
# This class extracts a list of components given a Yahoo index name
#

from bs4 import BeautifulSoup
import urllib3

class ComponentsExtractor:

  BASE_URL="https://finance.yahoo.com/quote/^_INDEX_/components?p=^_INDEX_"

  def __init__(self):
    None

  # Extracts the index constituent data (limited to 30 underlying secs)
  # Check the list in globalIndexes file
  def getComponents (self, index):
    queryURL = self.BASE_URL.replace ("_INDEX_", index)
    instrumentPage = urllib3.PoolManager().request ("GET", queryURL)
    soup = BeautifulSoup(instrumentPage.data, "html.parser")
    try:
      divMain = soup.find ("div", id="Main").findAll("a")
      return [n.text.encode("ascii").decode("UTF-8") for n in divMain]
    except AttributeError:
      return []

  # Extracts the stocks listed in a stock from eoddata.com
  # Check the list in the exchanges file
  # 
  def getExchange (self, exch):
    BASE_URL = "http://www.eoddata.com/stocklist/_EXCHANGE_ID_/_L_.htm"
    exchangeUrl = BASE_URL.replace("_EXCHANGE_ID_", exch);
    exchangeStocks = []
    for one in range(97,123): # a .. z 123
      url = exchangeUrl.replace("_L_", chr(one))
      quotesPage = urllib3.PoolManager().request("GET", url)
      soup = BeautifulSoup(quotesPage.data, "html.parser")
      try:
        divMain = soup.find ("table", class_="quotes").findAll("a")
        exchangeStocks += [n.text.encode("ascii") for n in divMain if n.text != '']
      except AttributeError:
        print ("Error retrieving data: " + url)
    return exchangeStocks
  
