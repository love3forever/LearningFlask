# -*- coding: utf-8 -*-


import re
import urllib
import urllib2
import cookielib
import random
import os
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

email = 'xxx@qq.com'
password = 'xxxx'
cookies_file = 'Cookies_saved.txt'


class douban_robot:

    def __init__(self):
        self.email = email
        self.password = password
        self.data = {
            "form_email": email,
            "form_password": password,
            "source": "index_nav",
            "remember": "on"
        }

        self.login_url = 'https://www.douban.com/accounts/login'
        self.load_cookies()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookie))
        self.opener.addheaders = [("User-agent", "Mozilla/5.0 (X11; Linux x86_64)\
          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36")]
        # self.opener.addheaders = [("Origin", "https://www.douban.com")]
        self.get_ck()

    def load_cookies(self):
        try:
            self.cookie = cookielib.MozillaCookieJar()
            self.cookie.load(cookies_file)
            print "loading cookies for file..."
        except Exception, e:

            print "The cookies file is not exist."
            self.login_douban()
            # reload the cookies.
            self.load_cookies()

    def get_ck(self):
        # open a url to get the value of ck.
        self.opener.open('https://www.douban.com')
        # read ck from cookies.
        for c in list(self.cookie):

            if c.name == 'ck':
                self.ck = c.value.strip('"')
                print "ck:%s" % self.ck
                break
        else:
            print 'ck is end of date.'
            self.login_douban()
            # #reload the cookies.
            self.cookie.revert(cookies_file)
            self.get_ck()

    def login_douban(self):
        '''
        login douban and save the cookies into file.

        '''
        cookieJar = cookielib.MozillaCookieJar(cookies_file)
        # will create (and save to) new cookie file

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        #!!! following urllib2 will auto handle cookies
        response = opener.open(self.login_url, urllib.urlencode(self.data))
        html = response.read()
        regex = r'<img id="captcha_image" src="(.+?)" alt="captcha"'
        imgurl = re.compile(regex).findall(html)
        if imgurl:
            # urllib.urlretrieve(imgurl[0], 'captcha.jpg')
            print "The captcha_image url address is %s" % imgurl[0]

            # download the captcha_image file.
            # data = opener.open(imgurl[0]).read()
            # f = file("captcha.jpg","wb")
            # f.write(data)
            # f.close()

            captcha = re.search(
                '<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
            if captcha:
                vcode = raw_input('图片上的验证码是：')
                self.data["captcha-solution"] = vcode
                self.data["captcha-id"] = captcha.group(1)
                self.data["user_login"] = "登录"
                # 验证码验证
                response = opener.open(
                    self.login_url, urllib.urlencode(self.data))
                # fp = open("2.html","wb")
                # fp.write(response.read())
                # fp.close

        # 登录成功
        cookieJar.save()
        if response.geturl() == "http://www.douban.com/":
            print 'login success !'
            # update cookies, save cookies into file
            # cookieJar.save();
        else:
            return False
        return True


    def get_firstpage(self):
        request = urllib2.Request("https://www.douban.com/group/whu/")
        request.add_header('Referer',"https://www.douban.com/") 
        html_data = self.opener.open(request).read()
        #import chardet
        #print chardet.detect(html_data)
        soup = BeautifulSoup(html_data,"html5lib")
        for item in soup.find_all('table'):
            chilesoup = BeautifulSoup(item.encode('utf-8'),"html5lib")
            childtable = chilesoup.table
            if 'class' in childtable.attrs:
                return childtable

####Test Codes#####