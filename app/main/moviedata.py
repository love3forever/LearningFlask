#-*- coding: UTF-8 -*-
from db import client
import json
db = client['DouBanMovie']


def get_movieinfo(tag, num=0):
    col = db[tag]
    num = num*15
    cursor = col.find({}, {"_id": 0, "title": 1, "alt": 1,
                           "directors": 1, "images": 1, "rating": 1, "year": 1}, skip=int(num)).limit(15)
    return cursor

'''for movie in get_movieinfo("1", num=0):
    if movie['directors']:
        print len(movie['directors'])'''
