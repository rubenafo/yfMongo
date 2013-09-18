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
from pymongo import *
from yfmAdmin import yfmAdmin

##
## yFinance-mongo command line interface
##

#
# Help message when no valid options are provided
#
def showHelp ():
    print "Usage : yfm-cli clear                -- clears the DB"
    print "        yfm-cli init                 -- clears AND creates the base structure"
    print "        yfm-cli add <stock>          -- adds a stock to the db"
    print "        yfm-cli load-symbols <file>  -- loads symbols from file"
    print "        yfm-cli remove <stock>       -- removes a stock from the db"
    print "        yfm-cli fetch <date>         -- fetches all symbols for given date"
    print "        yfm-cli fetch <start> <end>  -- fetches data between both dates"
    print "        yfm-cli info                 -- prints out admin info"
    print "        yfm-cli info symbols         -- prints symbols"

# end showHelp

client = MongoClient('localhost', 27017)
moAdmin = yfmAdmin(client, "yf-mongo")

numParams = len(sys.argv)
if numParams == 1: # no args
    showHelp()
    exit()

firstParam = sys.argv[1]
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
    secondParam = sys.argv[2]
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
    showHelp()

if numParams == 4:
    if firstParam == "fetch":
      startDate = sys.argv[2]
      endDate = sys.argv[3]
      moAdmin.fetchInterval (startDate, endDate)
      exit()

showHelp()

# end main
