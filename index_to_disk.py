import json

def get_json(indexFile):
    with open(indexFile) as handle:
        return json.load(handle)

def index_to_database():
    index_file = "C:/Users/nicho/Desktop/index_with_body/Index_file.json"
    # index_file = "C:/Users/nicho/Desktop/test.json"
    index = get_json(index_file)
    count = 0
    # index = {'0': {'0/11': {'tf':1, 'tf-idf': 0.1}}, '1': {'0/12': {'tf':1, 'tf-idf': 0.1}}}

    for item in index:
        # count += 1
        # if not item[0].isdigit():
        try:
            with open('/Users/nicho/Desktop/result/' + item[0] + '.json', 'w') as outfile:
                mydict = dict([item])
                outfile.write(json.dumps(mydict))
        except:
            print "error: ", item[0]


index_to_database()

