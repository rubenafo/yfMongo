#!/usr/bin/python
## Copyright 2013 Ruben Afonso, http://www.figurebelow.com
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
from yfinanceMongo import *

##
## yFinanceMongo command line interface
##

class yfinanceCli:

  #
  # Help message when no valid options are provided
  #
  def showHelp (self):
    print "Usage : yfm-cli clear                -- clears the DB"
    print "        yfm-cli init                 -- clears AND creates the base structure"
    print "        yfm-cli add <stock>          -- adds a stock to the db"
    print "        yfm-cli load-symbols <file>  -- loads symbols from file"
    print "        yfm-cli remove <stock>       -- removes a stock from the db"
    print "        yfm-cli fetch <date>         -- fetches all symbols for given date"
    print "        yfm-cli fetch <start> <end>  -- fetches data between both dates"
    print "        yfm-cli info                 -- prints out admin info"
    print "        yfm-cli info symbols         -- prints symbols"

  def __init__(self, cliParams, hostname, port, database, user, password, verbose):
    moAdmin = yfinanceMongo(hostname=hostname, port=port, database=database, user=user, password=password, verbose=verbose)

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

      if firstParam == "init":
        moAdmin.clear()
        moAdmin.init()
        exit()
      else:
        showHelp()
        exit()

    if numParams == 3:
      secondParam = cliParams[2]
      if firstParam == "fetch":
        moAdmin.fetch(secondParam)
        exit()
      if firstParam == "add":
        moAdmin.add(secondParam)
        exit()
      if firstParam == "remove":
        moAdmin.remove (secondParam)
        exit()
      if firstParam == "info":
        if secondParam == "symbols":
          moAdmin.infoSymbols ()
          exit()
      if firstParam == "load-symbols":
        moAdmin.loadSymbols (secondParam);
        exit();
      self.showHelp()

    if numParams == 4:
      if firstParam == "fetch":
        startDate = cliParams[2]
        endDate = cliParams[3]
        moAdmin.fetchInterval (startDate, endDate)
        exit()
    # defaul help output when no option matched
    self.showHelp()

