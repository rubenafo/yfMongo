YfinanceMongo
==============

This module provides a database admin command line interface to store the stock content fetched using 
__[yfinancefetcher](http://www.github.com/figurebelow/yfinancefetcher)__ module into a MongoDb.

The main idea is to provide a wrap application to handle the database content in order to keep some consistency between the 
stock information, the symbols in the database and their time window.

### Requirements
* Python v2.6 at least
* Pymongo python module
* a running MongoDb 

### Usage
The command line help shows the available functionality:
```
Usage :
 yfm-cli clear                      -- clear all content from the db
 yfm-cli add <symbol>               -- add a symbol to the db
         add <symbol> <date>        -- add a symbol, then fetch the date
         add <symbol> <start> <end> -- add a symbol and fetch the period
 yfm-cli load-symbols <file>        -- load the symbols from a file
 yfm-cli remove <symbol>            -- remove a symbol from the db
 yfm-cli fetch <date>               -- fetch the given date for all symbols in the db
         fetch <start> <end>        -- fetch data between both dates for all symbols 
 yfm-cli info                       -- print out database info
 yfm-cli info symbols               -- print symbols

```
