#-*- coding: utf-8 -*-
import unittest
from location_extractor import extract_location, extract_locations

class TestStringMethods(unittest.TestCase):

    def test_english(self):
        text = "I arrived in New York on January 4, 2007"
        location = extract_location(text)['location']
        self.assertEqual(location, "New York")

        text = "Blablabla County is a very nice plase"
        location = extract_location(text)['location']
        self.assertEqual(location, "Blablabla")

        text = "New Jersey's governor said something last week."
        location = extract_location(text)['location']
        self.assertEqual(location, "New Jersey")

        text = "Cities of San Antonio, Dallas and Austin make up the...."
        print "text is", text
        locations = [element['location'] for element in extract_locations(text)]
        self.assertEqual(set(locations), set(["San Antonio","Dallas","Austin"]))

        text = """
        President Obama has used Oval Office speeches sparingly, compared with previous presidents. His previous two addresses, both in 2010, covered the Deepwater Horizon oil spill and the end of combat operations in Iraq.
        """
        location = extract_location(text)['location']
        self.assertEqual(location, "Iraq")

if __name__ == '__main__':
    unittest.main()
