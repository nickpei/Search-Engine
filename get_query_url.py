import json
from nltk.stem.snowball import SnowballStemmer


def get_json(indexFile):
    with open(indexFile) as handle:
        return json.load(handle)


def get_query_url(query):
    index_file = "C:/Users/nicho/Desktop/index_with_body/Index_Copy.json"
    index = get_json(index_file)

    stemmer = SnowballStemmer('english')
    for term in query:
        stem_term = stemmer.stem(term.lower()).encode('utf-8')

        entry = index[stem_term]
        documents = entry.keys()

        MapFile = "C:/Users/nicho/PycharmProjects/COMPSCI221/search_engine/WEBPAGES_RAW/bookkeeping.json"
        hash = get_json(MapFile)
        count = 0
        with open('C:/Users/nicho/Desktop/query_urls/' + term + '.txt', 'w') as f:
            for k in documents:
                baseUrl = hash[k.decode('utf-8')].encode('utf-8')
                count += 1
                print>>f, baseUrl, '\n'
            print>>f, "Number of urls:" , count

query = ['Informatics', 'Mondego', 'Irvine' ]
get_query_url(query)
