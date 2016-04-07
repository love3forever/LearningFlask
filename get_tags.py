#-*- coding: UTF-8 -*- 
# 通过传入的类别，获取不同类型的标签

import re

def get_tags(category):
	filename = ''

	if category == "movie":
		filename = './tag/movies.html'
	elif category == "book":
		filename = './tag/books.html'
	elif category == "music":
		filename = './tag/music.html'
	else:
		print "Haven't added this tag yet"

	return match_tag(filename)


# 通过文件名 获取标签项
def match_tag(filename):
	filetags=[]
	file = open(filename)
	for line in file.xreadlines():
		# 匹配对应文件的标签
	    book_tag = re.findall(r'class="tag">(.*?)</a>',line,re.S)
	    if book_tag:
	    	for item in book_tag:
	    		filetags.append(item)
	return filetags	  




	  