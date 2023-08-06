from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'urlcounter',
  packages = ['urlcounter'],
  version = '0.0.3',
  description = 'A set of functions that tally URLs within an event-based corpus. It assumes that you have data divided into a range of event-based periods with community-detected modules/hubs. It also assumes that you have unspooled and cleaned your URL data. See Deen Freelon\'s unspooler module for help: https://github.com/dfreelon/unspooler.',
  author = 'Chris A. Lindgren',
  author_email = 'chris.a.lindgren@gmail.com',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url = 'https://github.com/lingeringcode/urlcounter/',
  download_url = 'https://github.com/lingeringcode/urlcounter/',
  install_requires = ['pandas'],
  keywords = ['data processing', 'summary analysis', 'URL', 'circulation studies'],
  classifiers = [],
  include_package_data=True
)
