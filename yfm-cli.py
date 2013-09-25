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

#
# Helper class providing options configuration to invoke the yfinanceMongo
# command line utility class.
#

import sys
import os
from yfinanceCli import *

# Default connection values, customized as needed
# These are classical default values
hostname = "localhost"
port = 27017
user = "admin"
password = ""
database = "yfmongo"

cli = yfinanceCli (sys.argv, hostname, port, database, user, password, verbose=True)
