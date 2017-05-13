yfMongo
==============

yfMongo provides a database admin command line interface to store the stock content fetched using 
__[YahooFetcher](http://www.github.com/rubenafo/YahooFetcher)__ module into a MongoDb.

The main idea is to provide a wrap application to handle the database content in order to keep some consistency between the 
stock information and the symbols in the database so you can relay in your local data whithout query the Yahoo Finance API one time and another.
The queries are run against such API so all stock symbols must be Yahoo-identifiable.

### Requirements
* Python v2.6 at least
* Pymongo python module
* a running MongoDb 

### Openshift integration

In order to use _yfm_ in OpenShift, edit _yfm_ file and override the following parameters:
  hostname = os.environ.get("OPENSHIFT_MONGODB_DB_HOST")
  port = os.environ.get("OPENSHIFT_MONGODB_DB_PORT")
  user = os.environ.get("OPENSHIFT_MONGODB_DB_USERNAME")
  password = os.environ.get("OPENSHIFT_MONGODB_DB_PASSWORD")

#### Database structure

By default yfMongo creates a database called _yfmongo_ in your local MongoDb setup.
Inside this database, two collections are created as well: 
* _symbols_ : contains the defined symbols
* _timeline_ : contains the tickers for the symbols.

### Usage

yfm is a Python script to handle the yfMongo options from the command line.
The command line help shows the available functionality:
```
Usage:
 yfm clear                      -- clear all content from the db
 yfm add <symbol>               -- add a symbol to the db
     add <symbol> <date>        -- add a symbol, then fetch the date
     add <symbol> <start> <end> -- add a symbol and fetch the period
 yfm load-symbols <file>        -- load the symbols from a file
 yfm remove <symbol>            -- remove a symbol from the db
 yfm fetch <date>               -- fetch the given date for all symbols
     fetch <start> <end>        -- fetch data between both dates
 yfm test date                  -- test symbols fetching the given date
 yfm info                       -- print out admin info
 yfm info symbols               -- print symbols

```
#### Clear option

Running

```
yfm clear
```
clears out the db symbols (stored in a Mongo collection called symbols) and 
the fetched data (stored in a Mongo collection called timeline) inside your database.
Use it cautiosly to remove all content.

#### Add option

The add options allows to add symbols to the database. It is possible to just add a symbol, or define also
a date or a time period to fetch the data.

```
yfm goog                  # adds the 'goog' symbol to the database
yfm goog 06/05/2013       # adds the 'goog' symbol to the database and fetch the data for 6th May 2013.
yfm goog 06/05/2013 12/05/2013   # the same but fetch the data between 6th May 2013 and 12th May 2013.
```

#### Load-symbols

This option loads all symbols contained in the specified file as long as they are separated by spaces, commas or tabs.
An example of file is __[dowjones](https://github.com/rubenoaf/yfMongo/blob/master/dowjones)__ containing all Dow Jones
symbols.

```
$ yfm load-symbols ./downjones
'aa' added to the database
'axp' added to the database
...
...
'xom' added to the database
```

#### Remove option

This option removes a symbol from the database, deleting it from 'symbols' collection and all entries in 'timeline' collection.

```
$ yfm remove goog
'goog' removed from the database
```

#### Fetch option

Use 'fetch' to query stock of all defined symbols in the database to the Yahoo Finance API and store them.

```
$ yfm fetch 04/10/2013
Adding '04/10/2013' data for symbol 'aa'
Adding '04/10/2013' data for symbol 'axp'
...
Adding '04/10/2013' data for symbol 'xom'

```

Instead of a date we can provide a time period to fetch all data in the interval 
(keep in mind that bank days/sundays and simila days when market is closed may not have any data):

```
$ yfm fetch 04/10/2013 06/10/2013
Adding '[04/10/2013, 10/10/2013]' data for symbol 'aa'
Adding '[04/10/2013, 10/10/2013]' data for symbol 'axp'
...
Adding '[04/10/2013, 10/10/2013]' data for symbol 'xom'
```

#### Test option

The 'test' option is used to find invalid symbols. 
The provided date should be a valid trading day (working day) so there is data returned. The idea is that all symbols 
that do not have data in such day may be invalid.
It is up to the user to choose a valid test day.<br>
Note that running this option does not add any extra info to the database, it serves only to check the symbols.
```
$ yfm test 04/03/2013
Data found for 'aa', in '04/03/2013'
...
Warning 'foo',  no data found in '04/03/2013'
```

#### Info options
The 'info' options provide information of the content of the database.
Running the 'info' option without parameters returns information of the system:

```
$ yfm info
Timeline size: 13409
Symbols: 30
Oldest record: 06/05/13
Most recent record: 31/05/13
```

The option 'info symbols' returns the symbols in the database:

```
$ yfm info symbols
aa
axp
...
xom
```
