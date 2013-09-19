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

import unittest
from pymongo import *
from yfmAdmin import yfmAdmin

class yfmTest (unittest.TestCase):

  admin = None
  db = None

  def __init__(self, testCaseNames):
    unittest.TestCase.__init__(self,testCaseNames)
    client = MongoClient('localhost', 27017)
    self.admin = yfmAdmin(client, "yfmtest", False)
    self.db = client["yfmtest"]

  # Creates some test data in the timeline
  def generateData (self):
    self.db.symbols.insert ({'sym':"a"})
    self.db.symbols.insert ({'sym':"b"})
    self.db.symbols.insert ({'sym':"c"})
    self.db.timeline.insert ({"o":2.3, "c":3.2, "d":0, "v":12000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'a'})
    self.db.timeline.insert ({"o":2.3, "c":3.2, "d":0, "v":12000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'a'})
    self.db.timeline.insert ({"o":3.45, "c":3.0, "d":0, "v":15000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'b'})
    self.db.timeline.insert ({"o":10.3, "c":3.2, "d":0, "v":15000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'b'})
    self.db.timeline.insert ({"o":2.3, "c":3.2, "d":0, "v":1000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'c'})
    self.db.timeline.insert ({"o":2.3, "c":3.2, "d":0, "v":1000, "dv":3.2, "h":4, "ac":0, "l":2.2, "sym":'c'})

  # Creates the empty database, but containing admin documents
  def setUp (self):
    self.admin.clear()
    self.admin.init()

  # Checks the create() generates the correct structure in the db
  def test_init (self):
    self.assertTrue (self.db.admin.find().count() == 2);
    self.assertTrue (self.db.timeline.find().count() == 0);
    self.assertTrue (self.db.symbols.find().count() == 0);

  def test_clear(self):
    self.admin.clear()
    self.assertTrue (self.db.admin.find().count() == 0);
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

  # Test removel of symbol and its related timeline
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
