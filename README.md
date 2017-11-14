[![PyPI version](https://badge.fury.io/py/yfm.svg)](https://badge.fury.io/py/yfm)   
yfMongo
==============

yfMongo is a simple command line app to store and manage Yahoo Finance stock data in a MongoDb database.   
It allows you to build a local corpus of stock data that can be reused and updated easily wihout having to be constantly online.     
The API access is handled using __[YahooFetcher](http://www.github.com/rubenafo/YahooFetcher)__ .

### Install ###
```
pip install yfm
```

### Features
* Retrieve stock data from Yahoo Finance using Yahoo tickers
* Store tickers locally in MongoDb
* Retrieve some indexes constituent data
* Update tickers data daily
* Fetch by date range
* Export the data to JSON and CSV

### Requirements
* Python v2.6 at least
* Pymongo python module
* a running MongoDb instance

#### Database structure

By default yfMongo creates a database called _yfmongo_ in your local MongoDb setup.
Inside this database, two collections contain all the data:
* _symbols_ : tickers list
* _timeline_ : tickers data (opening price, closing, max, min, volumen and date)

### Usage

_yfm_ can be used as a command line tool to load symbols into the mongodb database or directly as a python module:

```
yfm add goog                        # add the 'goog' ticker to the database
yfm add mse  06/05/2013 12/05/2013  # add mse and fetch the data between 6th May 2013 and 12th May 2013.
yfm add index ftse                  # add the tickers for the index FTSE
yfm remove goog                     # removes GOOG from the db, ticker and timeline info
yfm update                          # for each ticker retrieve data since last day until today
yfm show mse                        # displays mse content
```
Directly from within python, tipycally to read from the database
```
import yfm
fetcher = yfm.fetcher()
fetcher.getTicker("goog")  # read from the db
fetcher.update() # same as 'yfm update'
```

### Openshift integration

In order to use _yfm_ in OpenShift, edit _yfm_ file and override the following parameters:
  hostname = os.environ.get("OPENSHIFT_MONGODB_DB_HOST")
  port = os.environ.get("OPENSHIFT_MONGODB_DB_PORT")
  user = os.environ.get("OPENSHIFT_MONGODB_DB_USERNAME")
  password = os.environ.get("OPENSHIFT_MONGODB_DB_PASSWORD")
