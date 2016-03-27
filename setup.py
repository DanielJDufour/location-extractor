from distutils.core import setup

setup(
  name = 'location-extractor',
  packages = ['location_extractor'],
  package_dir = {'location_extractor': 'location_extractor'},
  package_data = {'location_extractor': ['prep/char_language.txt','tests/__init__.py','tests/test.py']},
  version = '2.7',
  description = 'Extract locations from text',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/location-extractor',
  download_url = 'https://github.com/DanielJDufour/location-extractor/tarball/download',
  keywords = ['location','geo','python','tagging'],
  classifiers = [],
)
