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

class yfmAdmin:

  DATABASE_NAME = "yf-mongo";
  yfdb = None;

  def __init__(self, dbClient, databaseName):
    self.yfdb = dbClient[databaseName];

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
      print "Removing all collections [admin, data, symbols] ... done";
      self.yfdb.admin.remove();
      self.yfdb.timeline.remove();
      self.yfdb.symbols.remove();

  def init (self):
      print "Initializing base structure for admin ... done";
      self.yfdb.admin.insert ({'type':'user', 'user':'admin', 'password':'', 'lastLogin':''});
      self.yfdb.admin.insert ({'type':'content', 'startDate':'', 'endDate':'', 'lastUpdate':'', 'consistent':1});

  def add (self, value):
      exists = self.yfdb.symbols.find ({'sym':value}).count()
      if exists:
        print "Error: symbol'" + value + "' already in the database"
      else:
        self.yfdb.symbols.insert ({'sym':value});
        print "'" + value + "'" + " added to the database"

  def remove (self, value):
      exists = self.yfdb.symbols.find({'sym': value}).count();
      if not exists:
        print "Error: symbol'" + value + "' not in the database"
      else:
        self.yfdb.symbols.remove ({'sym':value});
        self.yfdb.timeline.remove ({'sym':value});
        print "'" + value + "'" + " removed from the database"

  #
  # Syncs the database. Basically it reads the defined start and end
  # dates and, if they are valid, retrieves the time window between both
  # for each one of the symbols in the database.
  #
  def sync (self):
    adminReg = self._getAdminDocument()
    if adminReg == None:
      print "Error: admin info (startDate, endDate) couldn't be found. Run 'create' option"
    else:
      startDateStr = adminReg['startDate']
      endDateStr = adminReg['endDate']
      if not startDateStr:
        print "Error: start date not set. Sync stopped"
        return
      if not endDateStr:
        print "Error: end date not set. Sync stopped"
        return
      startDate = datetime.strptime(startDateStr, "%d/%m/%Y")
      endDate = datetime.strptime(endDateStr, "%d/%m/%Y")
      if (startDate > endDate):
        print "Error: start date more recent than end date. Sync stopped"
      symbols = []
      for symb in self.yfdb.symbols.find():
        symbols.append(symb['sym']);
      days = (endDate-startDate).days
      symbs = len(symbols)
      print "Total: " + str(days * symbs) + " rows (" + str(days) + " days for " + str(symbs) + " symbols) " \
          + "between " + startDateStr + " and " + endDateStr + " ..."
      yfetcher = YFinanceFetcher()
      for symbol in symbols:
        self.yfdb.timeline.remove ({'sym':symbol});
        data = yfetcher.getHistAsJson(symbol, startDateStr, endDateStr, 'd+v')
        for entry in data:
          self.yfdb.timeline.insert(entry)
        print "Fetched '" + symbol + "' values "

  #
  # Prints information regarding the admin info (start and end dates)
  # and the symbols contained in the database
  #
  def info (self):
    adminReg = self._getAdminDocument()
    if adminReg == None:
      print "Error: admin info (startDate, endDate) couldn't be found. Run 'create' option"
    else:
      startDateStr = adminReg['startDate']
      endDateStr = adminReg['endDate']
      print "Start date: " + startDateStr
      print "End date: " + endDateStr
      symbols = self.yfdb.symbols.find();
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
      print "Error: admin info couldn't be found. Run 'create' option"
    else:
      date = None
      try:
        date = datetime.strptime(targetDate, "%d/%m/%Y")
        startDateStr = adminReg['startDate']
        endDateStr = adminReg['endDate']
        if not startDateStr:
          print "Error: start date not set. Sync stopped"
          return
        if not endDateStr:
          print "Error: end date not set. Sync stopped"
          return
        startDate = datetime.strptime(startDateStr, "%d/%m/%Y")
        endDate = datetime.strptime(endDateStr, "%d/%m/%Y")
        if (date < startDate):
          self.yfdb.admin.update (adminReg, { "$set":{ "startDate": targetDate} });
        if (date > endDate):
          self.yfdb.admin.update (adminReg, { "$set":{ "endDate": targetDate} });
        yfetcher = YFinanceFetcher()
        symbols = self.yfdb.symbols.find()
        for symbol in symbols:
          data = yfetcher.getHistAsJson(symbol['sym'], targetDate, targetDate, 'd+v')
          print "Adding '" + targetDate + "' data for symbol '" + symbol['sym'] + "'"
          for entry in data:
            self.yfdb.timeline.insert(entry)
      except ValueError:
        print "Error: invalid provided date format (expected dd/mm/yyyy)"

  def fetchInterval (self, startDate, endDate):
    adminReg = self._getAdminDocument()
    if adminReg == None:
      print "Error: admin info couldn't be found. Run 'create' option"
    else:
      date = None
      try:
        sdate = datetime.strptime(startDate, "%d/%m/%Y")
        edate = datetime.strptime(endDate, "%d/%m/%Y")
        startDateStr = adminReg['startDate']
        endDateStr = adminReg['endDate']
        if (len(startDateStr)):
          storedStartDate = datetime.strptime(startDateStr, "%d/%m/%Y")
        if (len(endDateStr)):
          storedEndDate = datetime.strptime(endDateStr, "%d/%m/%Y")
        if (len(startDateStr) > 0 & sdate < storedStartDate):
          self.yfdb.admin.update (adminReg, { "$set":{ "startDate": startDate} });
        if (len(endDateStr) > 0 & edate > storedEndDate):
          self.yfdb.admin.update (adminReg, { "$set":{ "endDate": endDate} });
        yfetcher = YFinanceFetcher()
        symbols = self.yfdb.symbols.find()
        for symbol in symbols:
          data = yfetcher.getHistAsJson(symbol['sym'], startDate, endDate, 'd+v')
          print "Adding '[" + startDate +", " + endDate  + "]' data for symbol '" + symbol['sym'] + "'"
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

