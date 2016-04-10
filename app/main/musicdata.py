#-*- coding: UTF-8 -*-
from db import client
import json
db = client['music']


def get_musicinfo(tag, num=0):
    col = db[tag]
    num = num*15
    cursor = col.find({}, {"_id": 0, "attrs": 1, "alt": 1, "alt_title": 1, "title": 1,
                           "author": 1, "image": 1, "rating": 1}, skip=int(num)).limit(15)
    realdata = []
    for movie in cursor:
	    if movie['image']:
	        movie['image'] = movie['image'].replace('spic','mpic')
		realdata.append(movie)
    return realdata