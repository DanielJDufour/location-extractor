# location-extractor
location-extractor helps you extract locations from text

# Installation
```
pip install location-extractor
```

# Use
```
from location_extractor import extract_locations
text = "I arrived in New York on January 4, 1937"
locations = extract_locations(text)
```

# Features
| Languages Supported |
| ------------------- |
| English |

# Testing
To test the package run
```
python -m unittest location_extractor.tests.test
```
