print('starting update_data.py')

from os.path import isfile, join
from wake import get_wikidata_entities

from enums import keywords_dir

code_to_lang = {
    'ar': 'Arabic',
    'en': 'English',
    'zh': 'Chinese',
    'zh-hans': 'Chinese',
    'zh-hant': 'Chinese',
    'zh-tw': 'Chinese'
}

# should probably be saving state and country if available
def save_city_name(name, language):
    print("starting save_city_name with", name, language)
    dirpath = join(keywords_dir, language)
    filepath = join(dirpath, 'cities.txt')

    if isfile(filepath):
        with open(filepath, 'r') as f:
            cities = set(f.read().strip().split("\n"))
    else:
        cities = set()

    cities.add(name)

    with open(filepath, 'w') as f:
        sorted_cities = sorted(list(cities))
        f.write('\n'.join(sorted_cities) + '\n')

for city in get_wikidata_entities(instance_of="Q515", sleep_time=0):
    labels = city.get('labels', [])
    for code, lang in code_to_lang.items():
        label = labels.get(code, None)
        if isinstance(label, list):
            for spelling in label:
                save_city_name(spelling['value'], lang)
        elif isinstance(label, dict):
            save_city_name(label['value'], lang)

    if 'claims' in city:
        # pull out country
        # pull out demonyms
        # pull out coordinates
        pass
        
print('finishing update_data.py')
