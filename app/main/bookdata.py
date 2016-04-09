#-*- coding: UTF-8 -*-
from db import client
import json
db = client['DouBanBook']


def get_bookinfo(tag, num=0):
    col = db[tag]
    num = num*15
    cursor = col.find({}, {"_id": 0, "title": 1, "alt": 1, "author": 1, "image": 1, "rating": 1, "pubdate": 1, "publisher": 1,
                           "price": 1}, skip=int(num)).limit(15)
    return cursor
