YfinanceMongo
==============

This module provides a database admin command line interface to store the stock content fetched using 
__[yfinancefetcher](http://www.github.com/figurebelow/yfinancefetcher)__ module into a MongoDb.

The main idea is to provide a wrap application to handle the database content in order to keep some consistency between the 
stock information and the symbols in the database so you can relay in your local data whithout query the Yahoo Finance API one time and another.
The queries are run against such API so all stock symbols must be Yahoo-identifiable.

### Requirements
* Python v2.6 at least
* Pymongo python module
* a running MongoDb 

### Openshift integration

The common command-line interface is yfm-cli.py but an aditional client is provided to use yfinanceMongo in  a 
__[Openshift](http://www.openshift.com)__ environment (basically the module is run using Openshift's specific values for
MongoDB connection: user, pass, host and port).<br>
It is called __[yfm-oscli.py](https://github.com/figurebelow/yfinanceMongo/blob/master/yfm-oscli.py)__

#### Database structure

By default yfinanceMongo creates a database called _yfmongo_ in your local MongoDb setup.
Inside this database, two collections are created as well: 
* _symbols_ : contains the defined symbols
* _timeline_ : contains the tickers for the symbols.

### Usage
The command line help shows the available functionality:
```
Usage:
 yfm-cli clear                      -- clear all content from the db
 yfm-cli add <symbol>               -- add a symbol to the db
         add <symbol> <date>        -- add a symbol, then fetch the date
         add <symbol> <start> <end> -- add a symbol and fetch the period
 yfm-cli load-symbols <file>        -- load the symbols from a file
 yfm-cli remove <symbol>            -- remove a symbol from the db
 yfm-cli fetch <date>               -- fetch the given date for all symbols
         fetch <start> <end>        -- fetch data between both dates
 yfm-cli test date                  -- test symbols fetching the given date
 yfm-cli info                       -- print out admin info
 yfm-cli info symbols               -- print symbols

```

yfm-cli is just a command-line interface to handle the main yfinanceMongo functionality easily.

#### Clear option

Running

```
yfm-cli clear
```
clears out the db symbols (stored in a Mongo collection called symbols) and 
the fetched data (stored in a Mongo collection called timeline) inside your database.
Use it cautiosly to remove all content.

#### Add option

The add options allows to add symbols to the database. It is possible to just add a symbol, or define also
a date or a time period to fetch the data.

```
yfm-cli goog                  # adds the 'goog' symbol to the database
yfm-cli goog 06/05/2013       # adds the 'goog' symbol to the database and fetch the data for 6th May 2013.
yfm-cli goog 06/05/2013 12/05/2013   # the same but fetch the data between 6th May 2013 and 12th May 2013.
```

#### Load-symbols

This option loads all symbols contained in the specified file as long as they are separated by spaces, commas or tabs.
An example of file is __[dowjones](https://github.com/figurebelow/yfinanceMongo/blob/master/dowjones)__ containing all Dow Jones
symbols.

```
$ yfm-cli load-symbols ./downjones
'aa' added to the database
'axp' added to the database
...
...
'xom' added to the database
```

#### Remove option

This option removes a symbol from the database, deleting it from 'symbols' collection and all entries in 'timeline' collection.

```
$ yfm-cly remove goog
'goog' removed from the database
```

#### Fetch option

Use 'fetch' to query stock of all defined symbols in the database to the Yahoo Finance API and store them.

```
$ yfm-cli fetch 04/10/2013
Adding '04/10/2013' data for symbol 'aa'
Adding '04/10/2013' data for symbol 'axp'
...
Adding '04/10/2013' data for symbol 'xom'

```

Instead of a date we can provide a time period to fetch all data in the interval 
(keep in mind that bank days/sundays and simila days when market is closed may not have any data):

```
$ yfm-cli fetch 04/10/2013 06/10/2013
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
$ yfm-cli test 04/03/2013
Data found for 'aa', in '04/03/2013'
...
Warning 'foo',  no data found in '04/03/2013'
```

#### Info options
The 'info' options provide information of the content of the database.
Running the 'info' option without parameters returns information of the system:

```
$ yfm-cli info
Timeline size: 13409
Symbols: 30
Oldest record: 06/05/13
Most recent record: 31/05/13
```

The option 'info symbols' returns the symbols in the database:

```
$ yfm-cli info symbols
aa
axp
...
xom
```
