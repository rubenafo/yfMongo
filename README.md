Yfinance-mongo
==============

This module provides a database admin command line interface to store the stock content fetched using 
__[yfinancefetcher](http://www.github.com/figurebelow/yfinancefetcher)__ module into a MongoDb.

The main idea is to provide a wrap application to handle the database content in order to keep some consistency between the 
stock information, the symbols in the database and their time window.

### Requirements
* Python v2.7 at least
* a MongoDb running on standard port

### Usage
The command line help shows the available functionality:
```
Usage : yfm-cli clear                -- clears the DB
        yfm-cli init                 -- clears AND creates the base structure
        yfm-cli add <stock>          -- adds a stock to the db
        yfm-cli load-symbols <file>  -- loads symbols from a file
        yfm-cli remove <stock>       -- removes a stock from the db
        yfm-cli fetch <date>         -- fetches all symbols for given date
        yfm-cli fetch <start> <end>  -- fetches data between both dates
        yfm-cli info                 -- prints out admin info and symbols
        yfm-cli info symbols         -- prints symbols
```
