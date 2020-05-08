[![Build Status](https://travis-ci.org/DanielJDufour/location-extractor.svg?branch=master)](https://travis-ci.org/DanielJDufour/location-extractor)

[![Requirements Status](https://requires.io/github/DanielJDufour/location-extractor/requirements.svg?branch=master)](https://requires.io/github/DanielJDufour/location-extractor/requirements/?branch=master)

# location-extractor
location-extractor helps you extract locations from text

# Installation
`pipenv install location-extractor` or `pip3 install location-extractor`

# Use
```
from location_extractor import extract_locations
text = "I arrived in New York on January 4, 1937"
locations = extract_locations(text)
```

# Output
Each location is represented by a Python with the following keys
| Name | Description | Required | Example |
| ---- | ---- | ---- | ---- |
| start | Index of the input text where the location starts| Yes | 42 |
| end | Index of the input text where the location ends | Yes | 54 |
| location | Full location text captured | Required | New York City |
| admin1code | Administrative Level 1 Code (i.e. State or Province Abbreviation) | No | NY |
| abbreviation | abbreviation of the place name | No | NYC |
| country | Name of the Country for the extracted place | No | United States |
| country_code | Country code of the extracted place | No | US |
| demonym | if location was actually a demonym | No | Spanish |

# Features
| Languages Supported |
| ------------------- |
| Arabic |
| Chinese |
| English |

# Testing
To test the package run
```
python3 -m unittest location_extractor.tests
```
