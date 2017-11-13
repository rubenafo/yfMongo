from setuptools import setup, find_packages

setup(
  name = 'yfm',
  packages = find_packages(),
  version = '1.3.5',
  description = 'A command line tool to store and manage Yahoo Finance stock data in a MongoDb database',
  author = 'Ruben Afonso',
  author_email = 'rbfrancos@gmail.com',
  url = 'https://github.com/rubenafo/yfMongo', 
  download_url = 'https://github.com/rubenafo/yfMongo/archive/1.3.5.zip',
  keywords = ['yahoo-finance', 'mongodb', 'finance','stock'],
  classifiers = [],
  install_requires=['pymongo'],
  entry_points={'console_scripts':['yfm = yfm.yfmcli:main']}
)

