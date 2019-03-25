from __future__ import division
from bs4 import BeautifulSoup, Comment
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import numpy as np
import json
import time
import re
global DocumentNum


# credit: github.com/GJzh/SearchEngine


def get_json(indexFile):
    with open(indexFile) as handle:
        return json.load(handle)


def indexer():
    global DocumentNum
    global running_time

    DocumentNum = 0
    print("Indexing!")
    filePathBase = "C:/Users/nicho/PycharmProjects/COMPSCI221/search_engine/WEBPAGES_RAW/"
    Index = {}
    global res
    res = []
    MapFile = "C:/Users/nicho/PycharmProjects/COMPSCI221/search_engine/WEBPAGES_RAW/bookkeeping.json"
    hash = get_json(MapFile)
    for i in range(75):
    # for i in range(1):
        fileFolder = '%d' % i
        if i<=73:
            N=500
        else:
            N=497
        # N = 20
        for j in range(N):
            fileName = '%d' % j
            document = fileFolder + '/' + fileName
            filePath = filePathBase + fileFolder + '/' + fileName
            print(filePath)
            res.append(filePath)
            # process web page content
            with open(filePath) as f:
                DocumentNum += 1
                soup = BeautifulSoup(f.read(), "lxml")
                if soup.head is not None:
                    text = soup.head.findAll(text=True)
                    visible_text = filter(visible, text)
                    visible_text = [term.string.encode('utf-8') for term in visible_text]
                    head_terms = termProcessing(visible_text)
                    res.append(head_terms)
                    for k in range(len(head_terms)):
                        term = head_terms[k]
                        if term not in Index:
                            # a new term
                            Index[term] = {}
                            Index[term][document] = {'tf': 0, 'tf-idf': 0, 'head': [], 'body':[]}
                        elif document not in Index[term]:
                            # an existing term but not the first occurance in the current document
                            Index[term][document] = {'tf': 0, 'tf-idf': 0, 'head': [], 'body':[]}
                        Index[term][document]['tf'] += 1
                        Index[term][document]['head'].append(k)
                # if soup.body is not None and not duplication:
                if soup.body is not None:
                    text = soup.body.findAll(text=True)
                    visible_text = filter(visible, text)
                    visible_text = [term.string.encode('utf-8') for term in visible_text]
                    body_terms = termProcessing(visible_text)
                    res.append(body_terms)
                    for k in range(len(body_terms)):
                        term = body_terms[k]
                    # for term in body_terms:
                        if term not in Index:
                            # a new term
                            Index[term] = {}
                            Index[term][document] = {'tf': 0, 'tf-idf': 0, 'head': [], 'body': []}
                        elif document not in Index[term]:
                            # an existing term but not the first occurance in the current document
                            Index[term][document] = {'tf': 0, 'tf-idf': 0, 'head': [], 'body':[]}
                        Index[term][document]['tf'] += 1
                        Index[term][document]['body'].append(k)
                # process the urls
                # if not duplication:
                #     baseUrl = hash[document.decode('utf-8')].encode('utf-8')
                #     urls = []
                #     urls.append(baseUrl)
                #     for link in soup.find_all('a'):
                #         if 'href' in link.attrs:
                #             newurl = link.attrs['href']
                #             # relative url changes to absolution url
                #             if newurl.startswith('/'):
                #                 newurl = urljoin(baseUrl, newurl)
                #             urls.append(newurl.encode('utf-8'))
                #     url_terms = termProcessing(urls)
                #     res.append(url_terms)

    for term in Index:
        df = len(Index[term])
        for document in Index[term]:
            tf = Index[term][document]['tf']
            Index[term][document]['tf-idf'] = calculate_Tfidf(tf, df)
    with open('Index', 'w') as f:
        f.write(json.dumps(Index))
    Index = sorted(Index.iteritems(), key=lambda d: d[0])
    return Index


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'meta']:
        return False
    elif isinstance(element, Comment):
        return False
    return True


def get_stem(content):
    stemmer = SnowballStemmer('english')
    for k in range(len(content)):
        content[k] = stemmer.stem(content[k]).encode('utf-8')
    return [stemmer.stem(term).encode('utf-8') for term in content]


def isstopwords(word):
    sw = set(stopwords.words('english'))
    if word in sw:
        return True
    else:
        return False


def termProcessing(content):
    terms = []

    tokenizer = RegexpTokenizer(r'\w+')
    for line in content:
        line = line.lower()
        line = re.sub(r'[^\x00-\x7F]+', ' ', line)   # Replace non-ASCII character with white space
        tokens = tokenizer.tokenize(line)
        for t in tokens:
            if t is not None and len(t) >=3 and len(t) <= 15 and not isstopwords(t)\
                    and re.match(r'[a-zA-Z0-9]', t):
                terms.append(t)
    get_stem(terms)
    return terms


def calculate_Tfidf(tf, df):
    # N=500*75-3
    N = DocumentNum
    if tf == 0 or df == 0:
        return 0
    else:
        return (1 + np.log10(tf)) * (np.log10(N / df))


def save_data(indexdict):
    global DocumentNum
    global running_time

    with open('Index_file', 'w') as f:
        f.write(json.dumps(indexdict))

    # for term in indexdict:
    #     with open('C:/Users/nicho/Desktop/result/' + term[0] + '.json', 'w') as outfile:
    #         outfile.write(json.dumps([term]))

    with open('StatisticData', 'w') as test:
        print>> test, "DocumentNum:", DocumentNum, "\n"
        print>> test, "running time:", running_time, "\n"
        print>> test, "The number of unique words (after tokenizing) is %d" % (len(Index))


global res
global running_time
start_time = time.time()
Index = indexer()
# print(Index[0])
# print(Index[0][1])
# print(Index[0][1].keys())

end_time = time.time()
running_time = end_time - start_time
print "Indexing ended after %.2f seconds." % (running_time)
print "Number of documents: ", DocumentNum
print("The number of unique words (after tokenizing) is %d" % (len(Index)))
print("Saving results...")
save_data(Index)
with open('filetext','w') as test:
    for i in range(len(res)):
        print>>test, res[i]

# MapFile = "C:/Users/nicho/PycharmProjects/COMPSCI221/search_engine/WEBPAGES_RAW/bookkeeping.json"
# hash = get_json(MapFile)
# for k in Index[0][1].keys():
#     baseUrl = hash[k.decode('utf-8')].encode('utf-8')
#     print baseUrl
