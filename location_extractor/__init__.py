from os.path import dirname, realpath
from os import listdir
from re import findall, finditer, IGNORECASE, MULTILINE, search, sub, UNICODE
flags = MULTILINE|UNICODE

try:
    from language_detector import detect_language
except ImportError:
    detect_language = None

try:
    from date_extractor import extract_date
except ImportError:
    extract_date = None

try:
    from bscrp import isJavaScript
except ImportError:
    isJavaScript = None
try:
    from PyPDF2 import PdfFileReader
except ImportError:
    PdfFileReader = None


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
            for e in element.split(","):
                e = e.strip()
                if e:
                    result.append(e)
    return result

def load_language_into_dictionary_of_keywords(language):
    dictionary_of_keywords[language] = {}
    directory_of_language_files = directory_of_keywords + "/" + language
    language_files = listdir(directory_of_language_files)
    #print "language_files are", language_files
    for filename in language_files:

        # ignore hidden and temporary files like .listed.swp
        if not filename.startswith("."):
            name = filename.split(".")[0]
            #print "filename is", filename
            if filename == "demonyms.txt":
                #print "d emmeomnymys"
                pass
            else:
                with open(directory_of_language_files + "/" + filename) as f:
                    keywords = [keyword for keyword in f.read().decode("utf-8").strip().split("\n") if keyword]
                    keywords += [keyword.title() for keyword in keywords]
                    dictionary_of_keywords[language][name] = keywords

def extract_locations_from_text(text):
    print "starting extract_locations_from_text"
    if isinstance(text, str):
        text = text.decode("utf-8")

    # see if we can figure out what language the text is
    # if we can't figure it out, just try to extract locations using all the languages we got
    languages = []

    # language_detector isn't reliable enough yet
    #if detect_language:
    #    detected_language = detect_language(text)
    #    if detected_language:
    #        languages = [detected_language]

    if not languages: 
        languages = listdir(directory_of_keywords)

    #print "languages = ", languages

    locations = set()

    for language in languages:

        if language not in dictionary_of_keywords:
            load_language_into_dictionary_of_keywords(language)

        #print "language =", language
        if language == "English":

            d = dictionary_of_keywords[language]

            location_pattern = "((?:(?:[A-Z][a-z]+) )?[A-Z][a-z]+|[A-Z]{2,})"

            #keyword comes before location
            locations.update(flatten(findall(ur"(?:(?:[^A-Za-z]|^)(?:"+ "|".join(d['before']) + ") )" + location_pattern, text, flags)))
            #print "\nbefore locations are", locations

            #keywords comes after location
            locations.update(flatten(findall(location_pattern + ur" (?:" + "|".join(d['after']) + ")", text, flags)))

            #keyword is something that a country can possess, like a president (e.g., "America's President")
            locations.update(flatten(findall(location_pattern + ur"'s (?:" + "|".join(d['possessed']) + ")", text, flags)))

            #keyword is something can be listed, like the islands of Santo Domingo and Cuba
            locations_pattern = location_pattern + "((?:, " + location_pattern + ")*),? and " + location_pattern
            pattern = ur"(?:" + "|".join(d['listed']) + ")" + ur"(?: | of |, |, [a-z]* )" + locations_pattern
            #print "text is", text
            #print "pattern is", pattern
            locations.update(flatten(findall(pattern, text, flags)))
            #print "locations are", locations

            #ignore demonyms for now, because accuracy is not that high
            #Eritreans, Syrian
            for m in finditer(ur"([A-Z][a-z]{3,}ans?)", text, MULTILINE):
                demonym = m.group(0)
                if "demonyms" in d:
                    if demonym in d['demonyms']:
                        country = d['demonyms'][demonym]
                        locations.add(country)

        elif language == "Arabic":

            d = dictionary_of_keywords[language]
            arabic_letter = u"[\u0600-\u061E\u0620-\u06EF\u06FA-\u06FF]"
            location_pattern = u"(" + arabic_letter + "{3,}(?: \u0627\u0644" + arabic_letter + "{3,})*)"
            locations.update(flatten(findall(ur"(?:"+ "|".join(d['before']) + ") " + location_pattern, text, flags)))


    # filter out things we often capture that aren't locations
    # and that are actually names of random places
    nonlocations = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    locations = [location for location in locations if location not in nonlocations]


    #convert locations to a list
    locations = list(locations)
    return locations

def extract_location(inpt):
    # returns a random location ... in the future make this so return the first location matched.. but implement as separate method entirely
    return extract_locations(inpt)[0]


def extract_locations_with_context_from_text(text):
    print "starting extract_locations_with_context_from_text with", type(text)

    if not extract_date:
        raise Exception("You must have date-extractor installed to use this method.  To fix the problem, run: pip install date-extractor")

    # this is the list of locations that we will return
    locations = []

    # got locations as list of words
    names = extract_locations(text)

    # find locations and surrounding information including date and paragraph
    pattern = "(" + "|".join(names) + ")"
    for matchgroup in finditer(pattern, text, flags):
        name = matchgroup.group(0)
        #print "name is", name
        text = matchgroup.string
        #print "text is", len(text), text[:100]
        start = matchgroup.start()
        #print "start is", start
        end = matchgroup.end()
        #print "end is", end
        middle = float(end + start) / 2
        #print "middle is", middle
        sentence = [m.group(0) for m in list(finditer("[^\.\n]+",text)) if m.start() < middle < m.end()][0].strip()
        paragraph = [m.group(0) for m in list(finditer("[^\n]+",text)) if m.start() < middle < m.end()][0].strip()
        #print "\nparagraph is", paragraph

        dictionary_of_location = {}

        dictionary_of_location['name'] = name

        dictionary_of_location['date'] = date = extract_date(sentence) or extract_date(paragraph)

        if not isJavaScript or not isJavaScript(paragraph):
            dictionary_of_location['context'] = paragraph

        dictionary_of_location['hash'] = str(date) + "-" + name

        locations.append(dictionary_of_location)

    # get locations by looking for columns with location keywords in them
    lists = findall("((?:\n^[^\n]{4,20}$){5,})", text, MULTILINE)
    for text_of_list in lists:
        count = 0
        keywords = []
        for language in dictionary_of_keywords:
            keywords += dictionary_of_keywords[language]["general"]
           
        for keyword in keywords: 
            count += text_of_list.count(keyword)

        if count > 5:
            lines = text_of_list.split("\n")
            names = [line for line in lines if line and len(line) > 4 and line not in keywords]

            for name in names:
                date = extract_date(text_of_list)
                locations.append({"name": name, "date": date, "hash": str(date) + "-" + name, "context": name})

    names = [location['name'] for location in locations]

    #see: http://stackoverflow.com/questions/21720199/python-remove-any-element-from-a-list-of-strings-that-is-a-substring-of-anothe
    names_verbose = filter(lambda x: [x for i in names if x in i and x != i] == [], names)
    for location in locations:
        name = location['name']
        for name_verbose in names_verbose:
            if not name == name_verbose and name in name_verbose:
                location['name'] = name_verbose

    grouped_by_hash = {}
    for location in locations:
        h = location['hash']
        if h in grouped_by_hash:
            #if have same hash, then have same exact location and date, so just need to update context
            if "context" in location and location['context']:
                grouped_by_hash[h]['context'] += "\n ... \n" + location['context']
        else:
            d = {'date': location['date'], 'name': location['name']}
            if "context" in location and location['context']:
                d['context'] = location['context']
            grouped_by_hash[h] = d
 
    locations = grouped_by_hash.values()

    return locations
       
def extract_locations_from_path_to_pdf(path_to_pdf):
    with open(path_to_pdf) as f:
        return extract_locations_from_pdf(pdf)

# takes in a pdf file and returns the text
def get_text_from_pdf_file(pdf_file):
    pdfFileReader = PdfFileReader(pdf_file)
    number_of_pages = pdfFileReader.getNumPages()
    text = ""
    for i in range(number_of_pages):
        text += pdfFileReader.getPage(i).extractText()
    text = sub(" *\n[\n ]*", "\n", text)
    lines = text.split("\n")
    lines = [line for line in lines if len(line) > 4]
    text = "\n".join(lines)
    return text
 
def extract_locations_from_pdf(pdf_file):
    print "starting extract_locations_from_pdf"
    return extract_locations_from_text(get_text_from_pdf_file(pdf_file))

def extract_locations_with_context_from_pdf(pdf_file):
    print "starting extract_locations_with_context_from_pdf"
    return extract_locations_with_context_from_text(get_text_from_pdf_file(pdf_file))

def extract_location_with_context(inpt):
    return extract_locations_with_context(inpt)[0]

def extract_locations(inpt):
    if isinstance(inpt, str) or isinstance(inpt, unicode):
        if inpt.endswith(".pdf"):
            return extract_locations_from_path_to_pdf(inpt)
        else:
            return extract_locations_from_text(inpt)
    elif isinstance(inpt, file):
        if f.name.endswith(".pdf"):
            return extract_locations_from_pdf(inpt)

def extract_locations_with_context(inpt):
    print "starting extract_locations_with_context with", type(inpt)
    if isinstance(inpt, str) or isinstance(inpt, unicode):
        if inpt.endswith(".pdf"):
            return extract_locations_with_context_from_pdf(inpt)
        else:
            return extract_locations_with_context_from_text(inpt)
    elif "InMemoryUploadedFile" in str(inpt) or isinstance(inpt, file):
        print "isinstance file"
        if inpt.name.endswith(".pdf"):
            return extract_locations_with_context_from_pdf(inpt)

el = extract_locations
elc = extract_locations_with_context
