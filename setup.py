from distutils.core import setup
setup(
  name = 'yfm',
  packages = ['yfm'], # this must be the same as the name above
  version = '1.0',
  description = 'A command line tool to store and manage Yahoo Finance stock data in a MongoDb database',
  author = 'Ruben Afonso',
  author_email = 'rbfrancos@gmail.com',
  url = 'https://github.com/rubenafo/yfm', # use the URL to the github repo
  download_url = 'https://github.com/peterldowns/mypackage/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['yahoo-finance', 'mongodb', 'finance','stock'], # arbitrary keywords
  classifiers = [],
)

