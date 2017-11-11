from setuptools import setup
setup(
  name = 'yfm',
  packages = ['yfm'],
  version = '1.2.0',
  description = 'A command line tool to store and manage Yahoo Finance stock data in a MongoDb database',
  author = 'Ruben Afonso',
  author_email = 'rbfrancos@gmail.com',
  url = 'https://github.com/rubenafo/yfMongo', 
  download_url = 'https://github.com/rubenafo/yfMongo/archive/1.2.zip',
  keywords = ['yahoo-finance', 'mongodb', 'finance','stock'],
  classifiers = [],
  install_requires=['pymongo']
)

