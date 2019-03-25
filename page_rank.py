import json
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from Tkinter import *
import webbrowser
import time


def callback(url):
    webbrowser.open_new(url)


def get_json(indexFile):
    with open(indexFile) as handle:
        return json.load(handle)


def isstopwords(word):
    sw = set(stopwords.words('english'))
    if word in sw:
        return True
    else:
        return False


def get_query_url(query):

    # index_file = "C:/Users/nicho/Desktop/index_with_body/Index_Copy.json"
    # index = get_json(index_file)
    query_list = query_processing(query)

    # Ranking for single-word query

    if len(query_list) == 1:
        # try:
        query_term = query_list[0]
        index_file = "C:/Users/nicho/Desktop/result/" + query_term + ".json"
        index = get_json(index_file)
        entry = index[query_term]
        documents = entry.keys()

        score = {}
        for d in documents:
            score[d] = entry[d]['tf']
            if len(entry[d]['head']) > 0:
                score[d] = score[d] * 1.5

        ranked_score = sorted(score.items(), key=lambda x:x[1], reverse=True)
        url_list = []
        count = 0
        MapFile = "C:/Users/nicho/PycharmProjects/COMPSCI221/search_engine/WEBPAGES_RAW/bookkeeping.json"
        hash = get_json(MapFile)
        with open('C:/Users/nicho/Desktop/query_toplinks/' + query_term + '.txt', 'w') as f:
            for pair in ranked_score:
                # print pair
                baseUrl = hash[pair[0].decode('utf-8')].encode('utf-8')
                absUrl = 'https://' + baseUrl
                url_list.append(absUrl)
                count += 1
                print>>f, baseUrl, '\n'
            print>>f, "count: ", count

        return url_list

        # except:
        #     print "Sorry, your search did not match any document. "
        #     print "Please check your spell or try different keywords."

    else:
        score = {}
        url_list = []
        for term in query_list:
            try:
                index_file = "C:/Users/nicho/Desktop/result/" + term + ".json"
                index = get_json(index_file)
                entry = index[term]
                documents = entry.keys()
                for d in documents:
                    if d not in score.keys():
                        score[d] = entry[d]['tf-idf']
                    else:
                        score[d] = score[d] + entry[d]['tf-idf']
            except:
                continue

            ranked_score = sorted(score.items(), key=lambda x:x[1], reverse=True)
            count = 0
            MapFile = "C:/Users/nicho/PycharmProjects/COMPSCI221/search_engine/WEBPAGES_RAW/bookkeeping.json"
            hash = get_json(MapFile)
            with open('C:/Users/nicho/Desktop/query_toplinks/' + query_list[0] + '_' + query_list[1] + '.txt', 'w') as f:
                for pair in ranked_score:
                    baseUrl = hash[pair[0].decode('utf-8')].encode('utf-8')
                    absUrl = 'https://' + baseUrl
                    url_list.append(absUrl)
                    count += 1
                    print>> f, baseUrl, '\n'
                print>> f, "count: ", count

        return url_list


def query_processing(raw_query):
    query_list = []

    stemmer = SnowballStemmer('english')
    raw_query_list = raw_query.split(' ')
    raw_query_list = filter(None, raw_query_list)

    for term in raw_query_list:
        # if not isstopwords(term) and not term.isalpha():
        if not term.isdigit():
            stem_term = stemmer.stem(term.lower()).encode('utf-8')
            query_list.append(stem_term)
        else:
            query_list.append(str(term))

    return query_list


def interface():
    root = Tk()
    root.geometry('1000x800')

    root.title("iSearch")

    # logo = Label(root, text = 'iSearch', fg = "blue", font = "Helvetica 64 bold italic")
    logo = Label(root, text='iSearch', fg="cornflower blue", font="Helvetica 64 bold")
    var = StringVar()
    query_ety = Entry(root, textvariable = var, font="Times 15", relief="flat")
    results_output0 = Message(root, text = '', width = 500)
    results_output1 = Label(root, text="", fg='dark green', cursor="hand2" ,font="Times 12")
    results_output2 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")
    results_output3 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")
    results_output4 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")
    results_output5 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")
    results_output6 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")
    results_output7 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")
    results_output8 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")
    results_output9 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")
    results_output10 = Label(root, text="", fg='dark green', cursor="hand2", font="Times 12")

    search_btn = Button(root, text='Search', font="Times 12", relief="raised",
                           command=lambda: print_result(var, results_output0, results_output1, results_output2,
                                                        results_output3, results_output4,
                                                        results_output5, results_output6, results_output7,
                                                        results_output8, results_output9, results_output10))
    root.bind('<Return>',
              lambda event: print_result(var, results_output0, results_output1, results_output2, results_output3,
                                         results_output4, results_output5, results_output6, results_output7,
                                         results_output8, results_output9, results_output10))

    logo.pack(pady=50)
    query_ety.pack(ipadx=200, ipady=8)
    search_btn.pack(ipadx=20, ipady=8)

    results_output0.pack()
    results_output1.pack()
    results_output2.pack()
    results_output3.pack()
    results_output4.pack()
    results_output5.pack()
    results_output6.pack()
    results_output7.pack()
    results_output8.pack()
    results_output9.pack()
    results_output10.pack()

    root.mainloop()


def print_result(var, results_output0, results_output1, results_output2, results_output3, results_output4,
                 results_output5, results_output6, results_output7, results_output8, results_output9, results_output10):
    query = var.get()

    visible_url = []

    try:
        starttime = time.time()
        result_url = get_query_url(query)  # [url]
        # if len(result_url) > 10:
        for url in result_url:
            if len(url) > 50:
                visible_url.append(url[0:50] + '...')
            else:
                visible_url.append(url)
        # else:
        if len(result_url) < 10:
            diff = 10 - len(result_url)
            for i in range(diff):
                visible_url.append(' ')

        runtime = time.time() - starttime
        results0 = "Search time is " + str(runtime) + "s."

    except:
        results0 = 'No search results for ' + query + '!'
        for i in range(10):
            visible_url.append(' ')

    results_output0.config(text=results0, font="Times 10")
    results_output1.config(text=visible_url[0])
    results_output2.config(text=visible_url[1])
    results_output3.config(text=visible_url[2])
    results_output4.config(text=visible_url[3])
    results_output5.config(text=visible_url[4])
    results_output6.config(text=visible_url[5])
    results_output7.config(text=visible_url[6])
    results_output8.config(text=visible_url[7])
    results_output9.config(text=visible_url[8])
    results_output10.config(text=visible_url[9])

    results_output1.bind("<Button-1>", lambda event: callback(result_url[0]))
    results_output2.bind("<Button-1>", lambda event: callback(result_url[1]))
    results_output3.bind("<Button-1>", lambda event: callback(result_url[2]))
    results_output4.bind("<Button-1>", lambda event: callback(result_url[3]))
    results_output5.bind("<Button-1>", lambda event: callback(result_url[4]))
    results_output6.bind("<Button-1>", lambda event: callback(result_url[5]))
    results_output7.bind("<Button-1>", lambda event: callback(result_url[6]))
    results_output8.bind("<Button-1>", lambda event: callback(result_url[7]))
    results_output9.bind("<Button-1>", lambda event: callback(result_url[8]))
    results_output10.bind("<Button-1>", lambda event: callback(result_url[9]))

    # results_output13.bind("<Button-1>", lambda event: callback(result_url[4]))


interface()
# query = raw_input("What would you like to search?")
# get_query_url(query)
