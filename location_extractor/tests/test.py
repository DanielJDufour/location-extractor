#-*- coding: utf-8 -*-
import unittest
from datetime import datetime
from location_extractor import *

class TestStringMethods(unittest.TestCase):

    def test_counting(self):
        text = "I was in Germany and then I was in Spain.  Before I was in Germany, I was in Romania."
        locations = extract_locations_with_context(text)
        location = [location for location in locations if location['name'] == "Germany"][0]
        self.assertEqual(location['count'], 2)

    def test_arabic(self):
        text = """
        يقول منظمو محادثات التغير المناخي في باريس إنهم اتفقوا على نص مسودة نهائية بعد قرابة أسبوعين من المفاوضات المكثفة.
        """.decode("utf-8")
        location = extract_location(text)
        self.assertEqual(location, "باريس".decode("utf-8"))

    def test_english(self):

        text = "Hospital attack sparks new security concerns in Rio de Janeiro"
        location = extract_location(text)
        self.assertEqual(location, "Rio de Janeiro")

        text = "I arrived in New York on January 4, 2007"
        location = extract_location(text)
        self.assertEqual(location, "New York")

        text = "Blablabla County is a very nice plase"
        location = extract_location(text)
        self.assertEqual(location, "Blablabla")

        text = "New Jersey's governor said something last week."
        location = extract_location(text)
        self.assertEqual(location, "New Jersey")

        text = "Cities of San Antonio, Dallas and Austin make up the...."
        print "text is", text
        locations = extract_locations(text)
        print "location sare", locations
        self.assertTrue("Austin" in locations)
        self.assertTrue("Dallas" in locations)
        self.assertTrue("San Antonio" in locations)

        text = """
        President Obama has used Oval Office speeches sparingly, compared with previous presidents. His previous two addresses, both in 2010, covered the Deepwater Horizon oil spill and the end of combat operations in Iraq.
        """
        location = extract_location(text)
        self.assertEqual(location, "Iraq")

        text = "The supposed events occurred in Lothlorien, Manchuria, Hong Kong, London, New York, Trenton, Chicago and Atlantic City from January to March 1920."
        locations = extract_locations(text)
        self.assertTrue("Lothlorien" in locations)
        self.assertTrue("Manchuria" in locations)
        self.assertTrue("Hong Kong" in locations)
        self.assertTrue("London" in locations)
        self.assertTrue("New York" in locations)
        self.assertTrue("Trenton" in locations)
        self.assertTrue("Chicago" in locations)
        self.assertTrue("Atlantic City" in locations)

    def test_english_with_context(self):
        text = """
        President Obama has used Oval Office speeches sparingly, compared with previous presidents. His previous two addresses, both in 2010, covered the Deepwater Horizon oil spill and the end of combat operations in Iraq.
        """
        location = extract_location_with_context(text)
        self.assertEqual(location['name'], "Iraq")
        self.assertEqual(str(location['date']), "2010-01-01 00:00:00+00:00")

    def test_demonym(self):
        print "starting test_demonym"
        text = "That guy is English."
        location = extract_location(text)
        self.assertEqual(location, "England") 

    def test_demonym2(self):
        print "starting test_demonym"
        text = "That guy is Albertan."
        location = extract_location(text)
        self.assertEqual(location, "Alberta") 

    def test_spanish(self):
        text = "Soy es una abanquina"
        location = extract_location(text)
        self.assertEqual(location, "Abancay")

    def test_english_after(self):
        text = "This is Costa Brava County."
        location = extract_location(text)
        self.assertEqual(location, "Costa Brava")

if __name__ == '__main__':
    unittest.main()
