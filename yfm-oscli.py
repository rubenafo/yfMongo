#!/usr/bin/env python
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

##
## yFinanceMongo command line interface for OpenShift
##

import sys
import os
from yfinanceCli import *

# This lines set the host, port, user and password to connect to a MongoDB in
# an Openshift account.
hostname = os.environ.get("OPENSHIFT_MONGODB_DB_HOST")
port = os.environ.get("OPENSHIFT_MONGODB_DB_PORT")
user = os.environ.get("OPENSHIFT_MONGODB_DB_USERNAME")
password = os.environ.get("OPENSHIFT_MONGODB_DB_PASSWORD")

# The database name, anything goes well
database = "yfmongo"


cli = yfinanceCli (sys.argv, hostname=hostname, port=port, user=user, password=password, database=database, verbose=True)
