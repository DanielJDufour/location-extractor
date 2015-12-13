from os.path import dirname, realpath
from os import listdir
from re import findall, finditer, IGNORECASE, MULTILINE, search, sub, UNICODE
flags = MULTILINE|UNICODE

try:
    from language_detector import detect_language
except ImportError:
    detect_language = None

directory_of_this_file = dirname(realpath(__file__))
directory_of_keywords = directory_of_this_file + "/keywords"
languages = listdir(directory_of_keywords)

dictionary_of_keywords = {}

def flatten(lst):
    result = []
    for element in lst: 
        if hasattr(element, '__iter__'):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result

def load_language_into_dictionary_of_keywords(language):
    dictionary_of_keywords[language] = {}
    directory_of_language_files = directory_of_keywords + "/" + language
    language_files = listdir(directory_of_language_files)
    print "language_files are", language_files
    for filename in language_files:
        name = filename.split(".")[0]
        print "filename is", filename
        if filename == "demonyms.txt":
            print "d emmeomnymys"
        else:
            with open(directory_of_language_files + "/" + filename) as f:
                keywords = f.read().decode("utf-8").strip().split("\n")
                keywords += [keyword.title() for keyword in keywords]
                dictionary_of_keywords[language][name] = keywords

def extract_locations(text):
    if isinstance(text, str):
        text = text.decode("utf-8")

    # see if we can figure out what language the text is
    # if we can't figure it out, just try to extract locations using all the languages we got
    languages = []
    if detect_language:
        detected_language = detect_language(text)
        if detected_language:
            languages = [detected_language]

    if not languages: 
        languages = listdir(directory_of_keywords)

    print "languages = ", languages

    locations = set()

    for language in languages:

        if language not in dictionary_of_keywords:
            load_language_into_dictionary_of_keywords(language)

        print "language =", language
        if language == "English":

            d = dictionary_of_keywords[language]

            location_pattern = "((?:(?:[A-Z][a-z]+) )?[A-Z][a-z]+|[A-Z]{2,})"

            #keyword comes before location
            locations.update(flatten(findall(ur"(?:(?:[^A-Za-z]|^)(?:"+ "|".join(d['before']) + ") )" + location_pattern, text, flags)))
            print "\nbefore locations are", locations

            #keywords comes after location
            locations.update(flatten(findall(location_pattern + ur" (?:" + "|".join(d['after']) + ")", text, flags)))

            #keyword is something that a country can possess, like a president (e.g., "America's President")
            locations.update(flatten(findall(location_pattern + ur"'s (?:" + "|".join(d['possessed']) + ")", text, flags)))

            #keyword is something can be listed, like the islands of Santo Domingo and Cuba
            locations_pattern = location_pattern + "(?:, " + location_pattern + ")*,? and " + location_pattern
            pattern = ur"(?:" + "|".join(d['listed']) + ")" + ur"(?: of |, |, [a-z]* )" + locations_pattern
            locations.update(flatten(findall(pattern, text, flags)))

            #ignore demonyms for now, because accuracy is not that high
            #Eritreans, Syrian
            for m in finditer(ur"([A-Z][a-z]{3,}ans?)", text, MULTILINE):
                demonym = m.group(0)
                if demonym in dictionary:
                    country = dictionary[demonym]
                    locations.add(country)

        elif language == "Arabic":

            d = dictionary_of_keywords[language]
            arabic_letter = u"[\u0600-\u06FF]"
            location_pattern = u"([\u0600-\u06FF]+(?: \u0627\u0644[\u0600-\u06FF]+)*)"
            locations.update(flatten(findall(ur"(?:"+ "|".join(d['before']) + ") " + location_pattern, text, flags)))


    #convert locations to a list
    locations = list(locations)
    return locations

def extract_location(text):
    # returns a random location ... in the future make this so return the first location matched.. but implement as separate method entirely
    return extract_locations(text)[0]

x = extract_locations
