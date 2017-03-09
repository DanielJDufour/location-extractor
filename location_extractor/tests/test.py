#-*- coding: utf-8 -*-
import signal, unittest
from datetime import datetime
from inspect import getargspec
from location_extractor import *
from os.path import abspath, dirname
from requests import get

path_to_directory_of_this_file = dirname(realpath(__file__))

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise OSError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

class TestMethods(unittest.TestCase):


    """
    def test_height(self):
        text = "Bla bla bla       Madison Heights MI      Lorem Ipsum bla bla bla"
        locations = extract_locations_from_text(text, return_abbreviations=True)
        try:
            self.assertEqual(len(locations), 2)
        except Exception as e:
            print "locations:", locations
            print e
            raise e

    def test_performance(self):
        with open(path_to_directory_of_this_file + "/performance.txt") as f:
            text = f.read()
            start = datetime.now()
            with timeout(seconds=3):
                locations = extract_locations_with_context(text, debug=True)
            seconds_took = (datetime.now() - start).total_seconds()
            self.assertEqual(seconds_took < 30)
    """

    def test_max_seconds(self):
        with open(path_to_directory_of_this_file + "/performance.txt") as f:
            text = f.read()
            start = datetime.now()
            with timeout(seconds=10):
                locations = extract_locations_with_context(text, debug=False, max_seconds=5)
            seconds_took = (datetime.now() - start).total_seconds()
            self.assertTrue(seconds_took < 10)
            try:
                self.assertTrue(len(locations) > 10)
            except Exception as e:
                print "len(locations) = ", len(locations)
                raise e



    # like San Cristobal or La Puente
    def test_composite_names(self):
        with open(path_to_directory_of_this_file + "/sample.txt") as f:
            text = f.read()
            locations = extract_locations_with_context(text)
            #for location in locations:
            #    print "\n", location['name'], " : ", (location['context'] if 'context' in location else ''), "\n"

        for name in ["Saudi Arabia", u"\u0053\u00e3\u006f \u0054\u006f\u006d\u00e9", "Santo Domingo", "Cape Town", "New Dehli"]:
            self.assertTrue(extract_location(u"He is from " + name) == name)

    def test_abbreviations(self):
        text = "I was in NJ over the weekend."
        location = extract_location_with_context(text, return_abbreviations=True)
        self.assertEqual(location['name'], "New Jersey")

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

        text= """
‏عاجل‬  كمعلومات أولية صوت انفجار ضخم يهز ارجاء بلدية السواني يرجح علي انه قصف جوي .. من يملك معلومة يفيدنا بها
""".decode("utf-8")
        location = extract_location(text)
        self.assertEqual(location, "السواني".decode("utf-8"))

        text = """
القمة العربية في موريتانيا تدعو لتكريس الجهود لحل القضية الفلسطينية"""
        locations = extract_locations(text)
        self.assertTrue(u'\u0641\u0644\u0633\u0637\u064a\u0646' in locations)
        self.assertTrue(u'\u0645\u0648\u0631\u064a\u062a\u0627\u0646\u064a\u0627' in locations)

        # eastern ghouta
        text = u"\u0023\u0627\u0644\u063a\u0648\u0637\u0629 \u0627\u0644\u0634\u0631\u0642\u064a\u0629"
        location = extract_location(text)
        self.assertEqual(location, u"\u0627\u0644\u063a\u0648\u0637\u0629")


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
        locations = extract_locations(text)
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

        text = "He is a Libyan."
        locations = extract_locations(text)
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], "Libya")

    def test_english_with_context(self):
        text = """
        President Obama has used Oval Office speeches sparingly, compared with previous presidents. His previous two addresses, both in 2010, covered the Deepwater Horizon oil spill and the end of combat operations in Iraq.
        """
        location = extract_location_with_context(text)
        self.assertEqual(location['name'], "Iraq")
        self.assertEqual(str(location['date']), "2010-01-01 00:00:00+00:00")

    def test_demonym(self):
        #print "starting test_demonym"
        text = "That guy is English."
        location = extract_location(text)
        self.assertEqual(location, "England") 

    def test_demonym2(self):
        #print "starting test_demonym"
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

    def test_ignore_these_names(self):
        text = "I went to Brazil and then to the USA."
        locations = extract_locations_with_context(text, ignore_these_names=["USA"])
        self.assertEqual(len(locations), 1)

    def test_state_abbreviations(self):
        text = "I'm from Seattle, WA."
        locations = extract_locations_from_text(text, return_abbreviations=True)
        try:
            self.assertEqual(len(locations), 1)
            seattle = [l for l in locations if l['location'] == "Seattle"][0]
            self.assertEqual(seattle['admin1code'], "WA")
        except Exception as e:
            print e
            print "locations:", locations
            raise e

    def test_state_abbreviations_with_context(self):
        text = "I'm from Seattle, WA."
        try:
            locations = extract_locations_with_context(text, return_abbreviations=True)
            self.assertEqual(len(locations), 1)
            self.assertEqual(locations[0]['name'], "Seattle")
        except Exception as e:
            print "extract_locations_with_context's args:", getargspec(extract_locations_with_context)
            print "locations:", locations
            print e
            raise e

    def test_abbreviations_with_context(self):
        text = "He visited Arlington, TX"
        try:
            names = [u'Arlington']
            locations = extract_locations_with_context(text, names, debug=True, return_abbreviations=True)
            self.assertEqual(len(locations), 1)
            self.assertEqual(locations[0]['name'], "Arlington")
        except Exception as e:
            print e 
            print "locations:", locations
            raise e

    def test_tables(self):
        text = get("http://www.nuforc.org/webreports/ndxlAK.html").text
        locations = extract_locations_with_context_from_html_tables(text, debug=False)
        self.assertTrue(len(locations) > 20)

    def testSaudi(self):
        text = "Saudi foreign minister makes landmark visit to Iraq"
        locations = extract_locations_from_text(text)
        print "sauid locs:", locations
        self.assertEqual(len(locations), 2)
        self.assertTrue("Iraq" in locations)
        self.assertTrue("Saudi Arabia" in locations)

    def testNewDehli(self):
        text = "Fire breaks out at Times of India building in New Delhi"
        locations = extract_locations(text)
        self.assertTrue("New Delhi" in locations)

    """
    def testSharm(self):
        text = "The UK was amongst several European countries to halt flights to Sharm al-Sheikh in November 2015, after a Russian passenger plane crashed in Egyptâs Sinai Peninsula shortly after taking off from the popular Red Sea resort, killing everyone on board."
        locations = extract_locations(text)
        print "sharm locs:", locations
        self.assertTrue("Egypt" in locations)
        self.assertTrue("Europe" in locations)
        self.assertTrue("Red Sea" in locations)
        self.assertTrue("Russia" in locations)
        self.assertTrue("Sharm al-Sheikh" in locations)
        self.assertTrue("Sinai Peninsula" in locations)
        self.assertTrue("United Kingdom" in locations)
    """

    def testWeather(self):
        text = """* Locations impacted includeâ¦ Arlington, Alexandria, Waldorf, Dale City, Clinton, Springfield, Fort Washington, Fort Hunt, Groveton, Forestville, Huntington, Coral Hills, Fort Belvoir, Woodbridge, National Harbor, Quantico, Nationals Park, Reagan National Airport, Crystal City and RFK Stadium."""
        locations = extract_locations(text)

    def testHyphenated(self):
        text = "January 2016 - Live grenade thrown at hostel housing 170 people in the south-western town in Villingen-Schwenningen but fails to detonate"
      
    """  
    def testE(self):
        text = "Where is Sar-e Pul Province?"
        locations = extract_locations(text)
        try:
            self.assertTrue("Sar-e Pul" in locations)
        except Exception as e:
            print "locations:", locations
            raise e
    """

    def testBugFix(self):
        locations = extract_locations_with_context("Alexandria, VA", debug=True, return_abbreviations=True)
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0]['name'], "Alexandria")
        self.assertEqual(locations[0]['admin1code'], "VA")

if __name__ == '__main__':
    unittest.main()
