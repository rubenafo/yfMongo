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
    print "Usage : yfm-cli clear            -- clears the DB"
    print "        yfm-cli create           -- clears AND creates the base structure"
    print "        yfm-cli add <stock>      -- adds a stock to the db"
    print "        yfm-cli remove <stock>   -- removes a stock from the db"
    print "        yfm-cli sync             -- fetches symbol data according to the defined"
    print "                                    start date and end date"
    print "        yfm-cli info             -- prints out admin info and symbols"
    print "        yfm-cli set-start <date> -- set the start date"
    print "        yfm-cli set-end <date>   -- set the end date"

# end showHelp

client = MongoClient('localhost', 27017)
moAdmin = yfmAdmin(client)

numParams = len(sys.argv)
if numParams == 1: # no args
    showHelp()
    exit()

firstParam = sys.argv[1]
if numParams == 2:
    if firstParam == "sync":
      moAdmin.sync ()
      exit()

    if firstParam == "clear":
      moAdmin.clear()
      exit()

    if firstParam == "info":
      moAdmin.info()
      exit()

    if firstParam == "create":
      moAdmin.clear()
      moAdmin.create()
      exit()
    else:
      showHelp()
      exit()

if numParams == 3:
    secondParam = sys.argv[2]
    if firstParam == "add":
      moAdmin.add(secondParam)
      exit()
    if firstParam == "remove":
      moAdmin.remove (secondParam)
      exit()
    if firstParam == "set-start":
      moAdmin.setStart (secondParam);
      exit()
    if firstParam == "set-end":
      moAdmin.setEnd (secondParam);
      exit()
    showHelp()

showHelp()

# end main
