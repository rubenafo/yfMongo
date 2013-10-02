# Copyright 2013 Ruben Afonso, http://www.figurebelow.com
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

import sys
import re
from datetime import datetime, date, time
sys.path.append("yfinancefetcher")
from yfinancefetcher import *
from pymongo import *

class yfinanceMongo:

  mongoClient = None
  yfdb = None;
  verbose = False

  def sprint (self, msg):
    if self.verbose:
      print msg

  def __init__(self, user=None, password=None, hostname="localhost", port=27017, database="admin", verbose=True):
    userAndPass = ""
    if user and password:
      userAndPass = user + ":" + str(password) + "@"
    url = "mongodb://" + userAndPass + hostname + ":" + str(port) + "/" + database
    self.mongoClient = MongoClient(url)
    self.yfdb = self.mongoClient[database];
    self.verbose = verbose

  def clear (self):
      self.sprint ("Removing all collections [symbols and timeline] ... done")
      self.yfdb.timeline.remove();
      self.yfdb.symbols.remove();

  def add (self, symbol, startDate = None, endDate = None):
    exists = self.yfdb.symbols.find ({'sym':symbol}).count()
    if not exists:
      self.yfdb.symbols.insert ({'sym':symbol});
      self.sprint ("'" + symbol + "'" + " added to the database")
    if startDate != None:
      if endDate != None:
        self.fetchInterval (startDate, endDate, symbol)
      else:
        self.fetch (startDate, symbol)

  def remove (self, value):
      exists = self.yfdb.symbols.find({'sym': value}).count();
      if not exists:
        self.sprint ("Error: symbol'" + value + "' not in the database")
      else:
        self.yfdb.symbols.remove ({'sym':value});
        self.yfdb.timeline.remove ({'sym':value});
        self.sprint ("'" + value + "'" + " removed from the database")

  #
  # Prints information regarding the admin info (start and end dates)
  # and the symbols contained in the database
  #
  def info (self):
    symbols = self.yfdb.symbols.find();
    print "Timeline size: " + str(self.yfdb.timeline.find().count())
    print "Symbols: " + str(symbols.count())

  # Print only symbol ids
  def infoSymbols (self):
      symbols = self.yfdb.symbols.find();
      for symb in symbols:
        print symb['sym']

  #
  # Fetches symbols for provided date.
  # If provided symbol is not None it fetches only it, otherwise
  # uses as symbols all available symbols in the database.
  #
  def fetch (self, targetDate, symbol=None):
    date = None
    try:
      date = datetime.strptime(targetDate, "%d/%m/%Y")
      yfetcher = YFinanceFetcher()
      if symbol == None:
        symbols = self.yfdb.symbols.find()
      else:
        symbols = self.yfdb.symbols.find({'sym': symbol})
      for symbol in symbols:
        data = yfetcher.getHistAsJson(symbol['sym'], targetDate, targetDate, 'd+v')
        self.sprint ("Adding '" + targetDate + "' data for symbol '" + symbol['sym'] + "'")
        for entry in data:
          self.yfdb.timeline.insert(entry)
    except ValueError:
      print "Error: invalid provided date format (expected dd/mm/yyyy)"

  # Fetches symbol data for the interval between startDate and endDate
  # If the symbol is not None, all symbols found in the database are
  # updated.
  def fetchInterval (self, startDate, endDate, symbol=None):
    date = None
    try:
      sdate = datetime.strptime(startDate, "%d/%m/%Y")
      edate = datetime.strptime(endDate, "%d/%m/%Y")
      yfetcher = YFinanceFetcher()
      if symbol == None:
        symbols = self.yfdb.symbols.find()
      else:
        symbols = self.yfdb.symbols.find ({'sym':symbol})
      for symbol in symbols:
        data = yfetcher.getHistAsJson(symbol['sym'], startDate, endDate, 'd+v')
        self.sprint ("Adding '[" + startDate +", " + endDate  + "]' data for symbol '" + symbol['sym'] + "'")
        for entry in data:
          self.yfdb.timeline.insert(entry)
    except ValueError:
      print "Error: invalid provided date format (expected dd/mm/yyyy)"

  # Loads symbols from a file, separated by spaces or commas
  def loadSymbols (self, sfile):
    symbFile = open (sfile)
    symbols = [];
    lines = (line.rstrip('\n') for line in open(sfile))
    for line in lines:
      values = re.split(" |,", line)
      for value in values:
        self.add (value)
