from os.path import dirname, realpath
from os import listdir


from re import findall, finditer, IGNORECASE, MULTILINE, search, sub, UNICODE
flags = MULTILINE|UNICODE

try:
    from date_extractor import extract_date, extract_dates
except ImportError:
    date_extractor = None

try:
    from language_detector import detect_language
except ImportError:
    detect_language = None

directory_of_this_file = dirname(realpath(__file__))
directory_of_keywords = directory_of_this_file + "/keywords"
languages = listdir(directory_of_keywords)

dictionary_of_keywords = {}

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

def get_info_from_match_group(m):
    print "m.groups() = ", m.groups()
    results = []
    for group in m.groups():
        location = group.title()
        print "location is", location
        text = m.string
        start = m.start()
        end = m.end()
        middle = float(end - start) / 2
        sentence = [m.group(0) for m in list(finditer("[^\.\n]+",text)) if m.start() < middle < m.end()][0].strip()
        paragraph = [m.group(0) for m in list(finditer("[^\n]+",text)) if m.start() < middle < m.end()][0].strip()
        date = extract_date(sentence) or extract_date(paragraph) if extract_date else None
        # need to filter out javascript paragraph
        result = {'date': date, 'hash': str(date) + "-" + str(location), 'location': location, 'context': paragraph}
        print "result is", result
        results.append(result)
    return results


def extract_locations(text):
    if isinstance(text, str):
        text = text.decode("utf-8")

    # see if we can figure out what language the text is
    # if we can't figure it out, just try to extract locations using all the languages we got
    if detect_language:
        languages = [detect_language(text)]
    else:
        languages = listdir(directory_of_keywords)

    print "languages = ", languages

    results = []

    for language in languages:

        if language not in dictionary_of_keywords:
            load_language_into_dictionary_of_keywords(language)

        print "language =", language
        if language == "English":

            d = dictionary_of_keywords[language]

            location_pattern = "((?:(?:[A-Z][a-z]+) )?[A-Z][a-z]+|[A-Z]{2,})"

            #keyword comes before location
            for m in finditer(ur"(?:(?:[^A-Za-z]|^)(?:"+ "|".join(d['before']) + ") )" + location_pattern, text, flags):
                results += get_info_from_match_group(m)

            #keywords comes after location
            for m in finditer(location_pattern + ur" (?:" + "|".join(d['after']) + ")", text, flags):
                results += get_info_from_match_group(m)

            #keyword is something that a country can possess, like a president (e.g., "America's President")
            for m in finditer(location_pattern + ur"'s (?:" + "|".join(d['possessed']) + ")", text, flags):
                results += get_info_from_match_group(m)

            #keyword is something can be listed, like the islands of Santo Domingo and Cuba
            locations_pattern = location_pattern + "(?:, " + location_pattern + ")*,? and " + location_pattern
            pattern = ur"(?:" + "|".join(d['listed']) + ")" + ur"(?: of |, |, [a-z]* )" + locations_pattern
            for m in finditer(pattern, text, flags):
                print "for m is", m
                results += get_info_from_match_group(m)

            #ignore demonyms for now, because accuracy is not that high
            #Eritreans, Syrian
            for m in finditer(ur"([A-Z][a-z]{3,}ans?)", text, MULTILINE):
                demonym = m.group(0)
                if demonym in dictionary:
                    country = dictionary[demonym]
                    result = get_info_from_match_group(m)
                    result['location'] = country
                    results.append(result)

        elif language == "Arabic":
            pass

    print "results are", results
    locations = [result['location'] for result in results]

    #see: http://stackoverflow.com/questions/21720199/python-remove-any-element-from-a-list-of-strings-that-is-a-substring-of-anothe
    locations_verbose = filter(lambda x: [x for i in locations if x in i and x != i] == [], locations)
    for result in results:
        location = result['location']
        for location_verbose in locations_verbose:
            if not location == location_verbose and location in location_verbose:
                result['location'] = location_verbose

    grouped_by_hash = {}
    for result in results:
        h = result['hash']
        if h in grouped_by_hash:
            #if have same hash, then have same exact location and date, so just need to update context
            grouped_by_hash[h]['context'] += "\n ... \n" + result['context']
        else:
            grouped_by_hash[h] = {'context': result['context'], 'date': result['date'], 'location': result['location']}

    results = grouped_by_hash.values()
    print "results are", results

    return results

def extract_location(text):
    return extract_locations(text)[0]

x = extract_locations
