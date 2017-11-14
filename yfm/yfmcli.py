#!/usr/bin/python
# 
# Copyright 2017 Ruben Afonso, <http://rubenaf.com>
# Licensed under the Apache License (see LICENSE)
#

import sys
from yfm import fetcher

##
## yfMongo command line interface
##

class yfm:

  #
  # Help message when no valid options are provided
  #
  def showHelp (self):
    print ("Usage :")
    print (" yfm clear                      -- clear all content from the db")
    print (" yfm clear data                 -- clear only data, keep symbols")
    print (" yfm add <symbol>               -- add a symbol to the db")
    print ("     add <symbol> <start> <end> -- add a symbol fetch data between dates")
    print ("     add index <index>          -- add underlying index components")
    print (" yfm load-symbols <file>        -- load the symbols from a file")
    print (" yfm remove <symbol>            -- remove a symbol from the db")
    print (" yfm fetch <start> <end>        -- fetch data between both dates")
    print (" yfm update                     -- fetch data since last date until today")
    print (" yfm info                       -- print out admin info")
    print (" yfm show <symbol>              -- shows the data for a symbol")
    print (" yfm export-json filename       -- export the content in JSON format")
    print (" yfm export-csv filename        -- export the content in CSV format")

  def __init__(self, cliParams, hostname, port, database, user, password, verbose):
    moAdmin = fetcher(hostname=hostname, port=port, database=database, user=user, password=password, verbose=verbose)

    numParams = len(cliParams)
    if numParams == 1: # no args
      self.showHelp()
      exit()

    firstParam = cliParams[1]
    if numParams == 2:
      if firstParam == "clear":
        moAdmin.clear()
        exit()
      if firstParam == "info":
        moAdmin.info()
        exit()
      if firstParam == "update":
        moAdmin.update()
        exit()
    if numParams == 3:
      secondParam = cliParams[2]
      if firstParam == "add":
        moAdmin.add(secondParam)
        exit()
      if firstParam == "clear" and secondParam == "data":
        moAdmin.clear(True)
        exit()
      if firstParam == "fetch":
        moAdmin.fetch(secondParam)
        exit()
      if firstParam == "remove":
        moAdmin.remove (secondParam)
        exit()
      if firstParam == "load-symbols":
        moAdmin.loadSymbols (secondParam)
        exit();
      if firstParam == "export-json":
        moAdmin.exportJSON (secondParam)
        exit()
      if firstParam == "export-csv":
        moAdmin.exportCSV (secondParam)
        exit()
      if firstParam == "show":
        entries = moAdmin.getTicker(secondParam)
        print (entries)
        exit()
      self.showHelp()
    if numParams == 4:
      if firstParam == "fetch":
        startDate = cliParams[2]
        endDate = cliParams[3]
        moAdmin.fetchInterval (startDate, endDate)
        exit()
      if firstParam == "add":
        secondParam = cliParams[2]
        if secondParam == "index":
          index = cliParams[3]
          moAdmin.addIndex(index)
          exit()
        else:
          symbol = cliParams[2]
          date = cliParams[3]
          moAdmin.add (symbol, date)
          exit()

    if numParams == 5:
      if firstParam == "add":
        symbol = cliParams[2]
        startDate = cliParams[3]
        endDate = cliParams[4]
        moAdmin.add (symbol, startDate, endDate);
        exit()
    # defaul help output when no option matched
    self.showHelp()

def main():  
  # Default connection values, customized as needed
  hostname = "localhost"
  port = 27017
  user = "admin"
  password = ""
  database = "yfmongo"
  cli = yfm (sys.argv, hostname, port, database, user, password, verbose=True)

if __name__ == "__main__":
  main()
