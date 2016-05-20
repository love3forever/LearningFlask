from pymongo import MongoClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt

keys = ['school', 'location', 'major', 'position', 'employment']


def get_userData():
    client = MongoClient()
    db = client['Zhihu']
    col = db['UserInfo']

    return col.find()


def get_word(userdata, keyword='school'):
    useful = {}
    print keyword
    if keyword in keys:
        for user in userdata:
            if user[keyword]:
                if user[keyword] in useful.keys():
                    useful[user[keyword]] += 1
                else:
                    useful[user[keyword]] = 1
    frequency = []
    for k in useful.keys():
        frequency.append((unicode(k), useful[k]))
    return frequency


def show_pic(frequency):
    if frequency:
    	print "pic making"
        wordcloud = WordCloud(font_path='./msyh.ttf').fit_words(frequency)
        plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()


data = get_userData()
freq = get_word(data, 'school')
show_pic(freq)
