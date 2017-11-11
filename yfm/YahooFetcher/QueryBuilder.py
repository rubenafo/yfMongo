#
# Copyright 2017, Ruben Afonso - http://www.github.com/rubenafo
# Licensed under the Apache License (see the LICENSE file)
#

#
# This class builds the URL using Yahoo conventions.
#

import urllib
from datetime import datetime

class QueryBuilder:

  BASE_URL = "http://finance.yahoo.com/quote/AAPL"
  HIST_URL = "https://query1.finance.yahoo.com/v7/finance/download/{}?{}";

  def refreshCookie (self):
    self.cookie = None
    self.crub = None
    cookier = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(cookier)
    urllib.request.install_opener(opener)
    f = urllib.request.urlopen(self.BASE_URL)
    alines = f.read().decode()
    cs = alines.find('CrumbStore')
    cr = alines.find('crumb', cs + 10)
    cl = alines.find(':', cr + 5)
    q1 = alines.find('"', cl + 1)
    q2 = alines.find('"', q1 + 1)
    crumb = alines[q1 + 1:q2]
    self.crumb = crumb
    for c in cookier.cookiejar:
      if c.domain != '.yahoo.com':
        continue
      if c.name != 'B':
        continue
      self.cookie = c.value

  def __init__(self):
    self.refreshCookie()

  #
  # Historical data methods
  #

  # Date params are in format yyyymmdd
  def getHistURL (self, symbol, begindate, enddate, event):
    tb = datetime(int(begindate[0:4]), int(begindate[4:6]), int(begindate[6:8]), 0, 0)
    te = datetime(int(enddate[0:4]), int(enddate[4:6]), int(enddate[6:8]), 0, 0)
    param = dict()
    param['period1'] = int(tb.timestamp())
    param['period2'] = int(te.timestamp())
    param['interval'] = '1d'
    if event == 'quote':
      param['events'] = 'history'
    elif event == 'div':
      param['events'] = 'div'
    elif event == 'split':
      param['events'] = 'split'
    
    for i in [1,5]:
      try:
        param['crumb'] = self.crumb
        params = urllib.parse.urlencode(param)
        url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?{}'.format(symbol, params)
        f = urllib.request.urlopen(url)
        alines = f.readlines()
        return [a.decode("UTF-8").strip() for a in alines[1:] if len(a) > 0]
      except (urllib.error.HTTPError, urllib.error.URLError):
        # this handles the spurious HTTPError unauthorized, perhaps the yahoo side didn't process the cookie
        # so the crumb gets rejected. 5 times for this should be enough
        self.refreshCookie()
    print ("Warning: unable to retrieve Yahoo data for " + symbol)
    return []
