#!/usr/bin/python
# 
# Copyright 2017 Ruben Afonso, <http://rubenaf.com>
# Licensed under the Apache License (see LICENSE)
#


import unittest
from pymongo import *
from yfMongo import *

class yfmTest (unittest.TestCase):

  admin = None
  db = None
  client = None

  def __init__(self, testCaseNames):
    unittest.TestCase.__init__(self,testCaseNames)
    # our yfinanceMongo client
    self.admin = yfMongo(hostname="localhost", port=27017, database="yfmtest", verbose=False)
    # setup a client to access the mongodb and check its content directly
    self.client = MongoClient ("localhost", 27017);
    self.db = self.client["yfmtest"]

  #
  # Class destructor cleans the database removing the test db
  #
  def __del__(self):
    self.client.drop_database('yfmtest')

  # Creates some test data in the timeline
  def generateData (self):
    self.db.symbols.insert_one ({'sym':"a"})
    self.db.symbols.insert_one ({'sym':"b"})
    self.db.symbols.insert_one ({'sym':"c"})
    self.db.timeline.insert_one ({"o":2.3, "c":3.2, "d":0, "v":12000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'a'})
    self.db.timeline.insert_one ({"o":2.3, "c":3.2, "d":0, "v":12000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'a'})
    self.db.timeline.insert_one ({"o":3.45, "c":3.0, "d":0, "v":15000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'b'})
    self.db.timeline.insert_one ({"o":10.3, "c":3.2, "d":0, "v":15000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'b'})
    self.db.timeline.insert_one ({"o":2.3, "c":3.2, "d":0, "v":1000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'c'})
    self.db.timeline.insert_one ({"o":2.3, "c":3.2, "d":0, "v":1000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'c'})

  # Creates the empty database, but containing admin documents
  def setUp (self):
    self.admin.clear()

  # Checks the create() generates the correct structure in the db
  def test_init (self):
    self.assertTrue (self.db.timeline.find().count() == 0);
    self.assertTrue (self.db.symbols.find().count() == 0);

  def test_clear(self):
    self.admin.clear()
    self.assertTrue (self.db.timeline.find().count() == 0);
    self.assertEqual (self.db.symbols.find().count(), 0);

  # Stocks are added correctly
  def test_add_stock (self):
    self.admin.add("a")
    self.admin.add("b")
    self.admin.add("c")
    self.assertTrue (self.db.symbols.count() == 3);

  # Repeated stocks arent added
  def test_add_repeat_stocks (self):
    self.admin.add ("a")
    self.admin.add ("b")
    self.admin.add ("a")
    self.assertTrue (self.db.symbols.count() == 2);

  # Test the symbol loading from file
  def test_load_symbols_file (self):
    self.admin.loadSymbols ("dowjones")
    self.assertEqual (self.db.symbols.count(), 30)

  # Test the removal of a symbol
  def test_removal (self):
    self.admin.loadSymbols ("dowjones")
    self.admin.remove ("ibm")
    self.assertEqual (self.db.symbols.count(), 29)
    self.assertEqual (self.db.symbols.find({'sym':"ibm"}).count(), 0)

  # Test removal of symbol and its related timeline
  def test_full_removal (self):
    self.generateData()
    self.assertEqual(self.db.timeline.count(), 6)
    self.admin.remove("a")
    self.assertEqual (self.db.symbols.count(), 2)
    self.assertEqual (self.db.timeline.count(), 4)
    self.admin.remove("b")
    self.assertEqual (self.db.symbols.count(), 1)
    self.assertEqual (self.db.timeline.count(), 2)
    self.admin.remove("c")
    self.assertEqual (self.db.symbols.count(), 0)
    self.assertEqual (self.db.timeline.count(), 0)

if __name__ == '__main__':
      unittest.main()
