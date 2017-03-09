from distutils.core import setup

setup(
  name = 'location-extractor',
  packages = ['location_extractor'],
  package_dir = {'location_extractor': 'location_extractor'},
  package_data = {'location_extractor': ['__init__.py','keywords/Arabic/before.txt','keywords/Arabic/general.txt','keywords/Arabic/after.txt','keywords/Arabic/demonyms.txt','keywords/English/abbreviations.txt','keywords/English/after.txt','keywords/English/before.txt','keywords/English/demonyms.txt','keywords/English/general.txt','keywords/English/listed.txt','keywords/English/possessed.txt','keywords/Spanish/after.txt','keywords/Spanish/before.txt','keywords/Spanish/demonyms.txt','keywords/Spanish/listed.txt','tests/__init__.py','tests/test.py','nonlocations.txt','letters/Arabic.txt']},
  version = '7.0',
  description = 'Extract locations from text',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/location-extractor',
  download_url = 'https://github.com/DanielJDufour/location-extractor/tarball/download',
  keywords = ['location','geo','python','tagging'],
  classifiers = [],
)
