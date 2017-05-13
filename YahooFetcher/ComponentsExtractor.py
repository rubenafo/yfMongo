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

  # and the stock symbols to fetch (e.g. GOOG for google).
  def getComponents (self, index):
    queryURL = self.BASE_URL.replace ("_INDEX_", index)
    instrumentPage = urllib3.PoolManager().request ("GET", queryURL)
    soup = BeautifulSoup(instrumentPage.data, "html.parser")
    try:
      divMain = soup.find ("div", id="Main").findAll("a")
      return [n.text.encode("ascii") for n in divMain]
    except AttributeError:
      return []
