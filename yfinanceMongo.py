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

  DATABASE_NAME = "yf-mongo";
  yfdb = None;
  verbose = False

  def sprint (self, msg):
    if self.verbose:
      print msg

  def __init__(self, dbClient, databaseName, verbose):
    self.yfdb = dbClient[databaseName];
    self.verbose = verbose

  #
  # Returns the admin row defining the content, found in the db.admin collection.
  # If it is not found means the environment is not reliable.
  #
  def _getAdminDocument (self):
    row = self.yfdb.admin.find({'type':'content'})
    if row.count() == 0:
      return None
    else:
      return next(row)

  def clear (self):
      self.sprint ("Removing all collections [admin, data, symbols] ... done")
      self.yfdb.admin.remove();
      self.yfdb.timeline.remove();
      self.yfdb.symbols.remove();

  def init (self):
      self.sprint ("Initializing base structure for admin ... done")
      self.yfdb.admin.insert ({'type':'user', 'user':'admin', 'password':'', 'lastLogin':''});
      self.yfdb.admin.insert ({'type':'content', 'lastUpdate':'', 'consistent':1});

  def add (self, value):
      exists = self.yfdb.symbols.find ({'sym':value}).count()
      if exists:
        self.sprint ("Error: symbol'" + value + "' already in the database")
      else:
        self.yfdb.symbols.insert ({'sym':value});
        self.sprint ("'" + value + "'" + " added to the database")

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
    adminReg = self._getAdminDocument()
    if adminReg == None:
      print "Error: admin info couldn't be found. Run 'create' option"
    else:
      symbols = self.yfdb.symbols.find();
      print "Found admin info"
      print "Timeline size: " + str(self.yfdb.timeline.find().count())
      print "Symbols: " + str(symbols.count())

  # Print only symbol ids
  def infoSymbols (self):
      symbols = self.yfdb.symbols.find();
      for symb in symbols:
        print symb['sym']

  #
  # Fetches all symbols for provided date
  #
  def fetch (self, targetDate):
    adminReg = self._getAdminDocument()
    if adminReg == None:
      self.sprint ("Error: admin info couldn't be found. Run 'create' option")
    else:
      date = None
      try:
        date = datetime.strptime(targetDate, "%d/%m/%Y")
        yfetcher = YFinanceFetcher()
        symbols = self.yfdb.symbols.find()
        for symbol in symbols:
          data = yfetcher.getHistAsJson(symbol['sym'], targetDate, targetDate, 'd+v')
          self.sprint ("Adding '" + targetDate + "' data for symbol '" + symbol['sym'] + "'")
          for entry in data:
            self.yfdb.timeline.insert(entry)
      except ValueError:
        print "Error: invalid provided date format (expected dd/mm/yyyy)"

  def fetchInterval (self, startDate, endDate):
    adminReg = self._getAdminDocument()
    if adminReg == None:
      self.sprint ("Error: admin info couldn't be found. Run 'create' option")
    else:
      date = None
      try:
        sdate = datetime.strptime(startDate, "%d/%m/%Y")
        edate = datetime.strptime(endDate, "%d/%m/%Y")
        yfetcher = YFinanceFetcher()
        symbols = self.yfdb.symbols.find()
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

