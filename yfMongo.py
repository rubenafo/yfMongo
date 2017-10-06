# 
# Copyright 2017 Ruben Afonso, <http://rubenaf.com>
# Licensed under the Apache License (see LICENSE)
#

import sys
import re
import csv
import json
from datetime import datetime, date, time
sys.path.append("YahooFetcher")
from YahooFetcher import *
import ast
from pymongo import *

class yfMongo:

  mongoClient = None
  yfdb = None;
  verbose = False

  #
  # Used to print messages only if the verbose flag was enabled
  #
  def sprint (self, msg):
    if self.verbose:
      print (msg)

  #
  # Generic function to check all user input dates
  # The format must be dd/mm/yyyy and cannot be a date in the future.
  # In case of error the execution of the application is stopped.
  #
  def __checkDate (self, date):
    try:
      inputDate = datetime.strptime(date, "%Y/%m/%d")
      currentTime = datetime.now()
      if (inputDate > currentTime):
        self.sprint ("Error: provided date (" + date + ") is in the future")
        exit()
    except ValueError:
      self.sprint ("Error: invalid provided date format (expected yyyy/mm/dd)")
      exit()

  #
  # Given a symbol document in the mongodb this returns the date it contains.
  #
  def __getFormattedDate (self, symbol):
      try:
        return datetime.strptime(symbol['date'], "%Y-%m-%d")
      except ValueError:
        self.sprint ("Error: invalid provided date format (expected yyyy/mm/dd)")

  #
  # Initialises the ddbb
  #
  def __init__(self, user="admin", password="", hostname="localhost", port=27017, database="yfmongo", verbose=True):
    userAndPass = ""
    if user and password:
      userAndPass = user + ":" + str(password) + "@"
    url = "mongodb://" + userAndPass + hostname + ":" + str(port)
    self.mongoClient = MongoClient(url)
    self.yfdb = self.mongoClient[database];
    self.verbose = verbose

  #
  # Removes all content in the database (Caution!)
  #
  def clear (self, keepSymbols=False):
      if keepSymbols:
        self.sprint ("Removing data ... done")
        self.yfdb.timeline.delete_many({});
      else:
        self.sprint ("Removing all collections [symbols and timeline] ... done")
        self.yfdb.timeline.delete_many({});
        self.yfdb.symbols.delete_many({});

  def add (self, symbol, startDate = None, endDate = None):
    exists = self.yfdb.symbols.find ({'sym':symbol}).count()
    if not exists:
      self.yfdb.symbols.insert_one ({'sym':symbol});
      self.sprint ("'" + symbol + "'" + " added to the database")
    if startDate != None:
      if endDate != None:
        self.fetchInterval (startDate, endDate, symbol)
      else:
        self.fetch (startDate, symbol)

  #
  # Removes a symbol from the ddbb, including all timeline entries
  #
  def remove (self, value):
      exists = self.yfdb.symbols.find({'sym': value}).count();
      if not exists:
        self.sprint ("Error: symbol'" + value + "' not in the database")
      else:
        self.yfdb.symbols.delete_many ({'sym':value});
        self.yfdb.timeline.delete_many ({'sym':value});
        self.sprint ("'" + value + "'" + " removed from the database")

  #
  # Prints information regarding the admin info (start and end dates)
  # and the symbols contained in the database
  #
  def info (self):
    symbols = self.yfdb.symbols.find();
    for symb in symbols:   
      print (symb['sym'])
    print ("Timeline size: " + str(self.yfdb.timeline.find().count()))
    print ("Symbols: " + str(symbols.count()))
    dates = []
    symbols = self.yfdb.timeline.find()
    for symb in symbols:
       date = self.__getFormattedDate (symb)
       dates.append(date)
    if dates:
      print ("Oldest record: " + min(dates).strftime("%Y/%m/%d"))
      print ("Most recent record: " + max(dates).strftime("%Y/%m/%d"))

  #
  # Updates the database fetching data for all symbols since last 
  # date in the data until today
  #
  def update (self):
    tickers = self.yfdb.symbols.find()
    for ticker in tickers:
      tickerTimeline = list(self.yfdb.timeline.find({'ticker':ticker["sym"]}))
      if len(tickerTimeline) > 0:
        oldestDate = max(map (lambda s: self.__getFormattedDate(s), tickerTimeline))
        if oldestDate is not None:
          self.fetchInterval (oldestDate.strftime("%Y/%m/%d"), 
                              date.today().strftime("%Y/%m/%d"),
                              symbol=ticker["sym"])
      else:
          self.fetchInterval("2000/01/01",
                             date.today().strftime("%Y/%m/%d"),
                             symbol=ticker["sym"]) 

  #
  # Fetches symbol data for the interval between startDate and endDate
  # If the symbol is not None, all symbols found in the database are
  # updated.
  #
  def fetchInterval (self, startDate, endDate, symbol=None):
    date = None
    try:
      sdate = datetime.strptime(startDate, "%Y/%m/%d")
      edate = datetime.strptime(endDate, "%Y/%m/%d")
    except ValueError:
      print ("Error: invalid provided date format (expected yyyy/mm/dd)")
      return
    yfetcher = YahooFetcher.YahooFetcher()
    if symbol == None:
      symbols = self.yfdb.symbols.find()
    else:
      symbols = self.yfdb.symbols.find ({'sym':symbol})
    for symbol in symbols:
      data = yfetcher.getHistAsJson(symbol['sym'], startDate.replace("/",""), endDate.replace("/",""))
      self.sprint ("Adding '[" + startDate +", " + endDate  + "]' data for symbol '" 
        + symbol['sym'] + "' (" + str(len(data)) + " entries)")
      if len(data) > 0:
        self.yfdb.timeline.insert(data)

  #
  # Loads symbols from a file, separated by spaces or commas
  #
  def loadSymbols (self, sfile):
    symbols = [];
    lines = (line.rstrip('\n') for line in open(sfile))
    for line in lines:
      values = re.split(" |,", line)
      values = [x.strip(' ') for x in values]
      values = filter (None, values)
      for value in values:
        self.add (value)

  #
  # Exports the timeline content to the given filename in JSON format
  #
  def exportJSON (self, filename):
    exportFile = open (filename, "w")
    symbols = self.yfdb.timeline.find({}, { '_id': 0})
    output = [];
    for symb in symbols:
        output.append(symb)
    exportFile.write (json.dumps(output))
    exportFile.close()

  #
  # Exports the timeline content to the given filename in CSV format
  #
  def exportCSV (self, filename):
    exportFile = open (filename, "w")
    # exclude the _id
    symbols = self.yfdb.timeline.find({}, { '_id': 0})
    first = symbols[0]
    if first:
      w = csv.DictWriter(exportFile, first.keys())
      w.writeheader()
      for symb in symbols:
        w.writerow(symb)
      exportFile.close()

  def addIndex (self, indexName):
    yfetcher = YahooFetcher.YahooFetcher()
    components = yfetcher.getComponents(indexName)
    for component in components:
      self.add(component)

  def getTicker (self, symbol):
    symbols = self.yfdb.timeline.find({'ticker': symbol})
    cleanSymbols = []
    for s in symbols:
      s["date"] = datetime.strptime(s["date"], "%Y-%m-%d")
      del s["_id"]
      cleanSymbols.append(s)
    return cleanSymbols
