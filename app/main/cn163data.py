#-*- coding: UTF-8 -*-
import urllib,urllib2,cookielib


def get_cn163data(tag):
	if tag:
		requesturl="http://www.dygod.net"
		print "获取"+tag+"数据"
		requesturl+=tag+"&x=0&y=0"
		user_agent = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
		request = urllib2.Request(requesturl)
		request.add_header("User-Agent", user_agent)
		resp=urllib2.urlopen(request)
		data=resp.read()
		print data
	else:
		print "未能正确获取数据"

#get_cn163data('纸牌屋')


def get_dygodRecentdata():
	recent_url="http://www.dygod.net/html/gndy/dyzz/index.html"
	print "获取最新电影数据"
	headers={
		'Referer':"http://www.dygod.net/",
		'User-Agent':"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
	}
	try:
		request = urllib2.Request(url=recent_url,headers=headers)
		resp=urllib2.urlopen(request)
		data = resp.read()
		print data
	except Exception, e:
		raise e


def cookieTest():
	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	response = opener.open("http://www.dygod.net/")
	for item in cookie:
		print item.value

cookieTest()
#get_dygodRecentdata()