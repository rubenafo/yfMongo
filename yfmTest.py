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
    self.admin = yfmAdmin(client, "yfmtest")
    self.db = client["yfmtest"]

  # Creates the empty database, but containing admin documents
  def setUp (self):
    self.admin.clear()
    self.admin.create()

  # Checks the create() generates the correct structure in the db
  def test_init (self):
    self.assertTrue (self.db.admin.find().count() == 2);
    self.assertTrue (self.db.timeline.find().count() == 0);
    self.assertTrue (self.db.symbols.find().count() == 0);

if __name__ == '__main__':
      unittest.main()
