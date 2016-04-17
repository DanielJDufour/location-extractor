from distutils.core import setup

setup(
  name = 'location-extractor',
  packages = ['location_extractor'],
  package_dir = {'location_extractor': 'location_extractor'},
  package_data = {'location_extractor': ['*']},
  version = '3.4',
  description = 'Extract locations from text',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/location-extractor',
  download_url = 'https://github.com/DanielJDufour/location-extractor/tarball/download',
  keywords = ['location','geo','python','tagging'],
  classifiers = [],
)
