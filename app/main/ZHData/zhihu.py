# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- pillow (可选)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.4"
Update
- name   : "wangmengcn"
- email  : "eclipse_sv@163.com"
- date   : "2016.4.21"
'''
import requests
import cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass

from bs4 import BeautifulSoup


# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    index_url = 'http://www.zhihu.com'
    # 获取登录时需要用到的_xsrf
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]


# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, allow_redirects=False).status_code
    if int(x=login_code) == 200:
        return True
    else:
        return False


def login(secret, account):
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
    else:
        print("邮箱登录 \n")
        post_url = 'http://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'email': account,
        }
    try:
        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.text
        print(login_page.status)
        print(login_code)
    except:
        # 需要输入验证码后才能登录成功
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = eval(login_page.text)
        print(login_code['msg'])
    session.cookies.save()

try:
    input = raw_input
except:
    pass


# 获取话题广场的所有主题
def get_topics():
    if isLogin():
        topicurl = "https://www.zhihu.com/topics"
        topics = []
        topicpage = session.get(topicurl).text
        topicsoup = BeautifulSoup(topicpage.encode('utf-8'), 'html5lib')
        #lis = topicsoup.find_all(name='li', attrs={'class':'zm-topic-cat-item'}, recursive=True, text=None, limit=None)
        lis = topicsoup.select(".zm-topic-cat-item", _candidate_generator=None, limit=None)
        if lis:
            for item in lis:
                a = item.a
                topic = topicurl + a['href'].encode('utf-8')
                topics.append(topic)
        return topics
    else:
        account = input('请输入你的用户名\n>  ')
        secret = input("请输入你的密码\n>  ")
        login(secret, account)
        get_topics()

# 获取话题广场的主话题，在每个主题中挑选20个子话题
def get_subtopics():
    topics = get_topics()
    url = "https://www.zhihu.com"
    topanswers=[]
    if len(topics)!=0:
        for topic in topics:
        # 获取子话题页面精华回复链接
            suburl = topic
            subpage = session.get(suburl).text
            subsoup = BeautifulSoup(subpage.encode('utf-8'),'html5lib')
            alis = subsoup.select('a[target="_blank"]', _candidate_generator=None,limit=20)
            if alis:
                #print len(alis)
                for item in alis:
                    #print type(item)
                    answerurl = url +item['href']+"/top-answers"
                    topanswers.append(answerurl)
    return topanswers

# 获取到子话题之后，从每个子话题的精华回答中挑选前20个问题
def get_topanswer():
    answerurl = get_subtopics()
    url = "https://www.zhihu.com"
    questions = []
    if len(answerurl)!=0:
        for item in answerurl:
            question = item
            questionpage = session.get(question).text
            subsoup = BeautifulSoup(questionpage.encode('utf-8'),'html5lib')
            content = subsoup.select(".question_link", _candidate_generator=None, limit=20)
            if content:
                for child in content:
                    questionurl = url+child['href']
                    print questionurl
                    questions.append(questionurl)
            break
        return questions

# 将精华话题中排名前20个回答获取，记录回答人信息、回答内容
def get_individual():
    topanswers = get_topanswer()
    url = "https://www.zhihu.com"
    individual = []
    if len(topanswers)!=0:
        for item in topanswers:
            quryurl = item
            qurydata = session.get(quryurl).text
            soup = BeautifulSoup(qurydata.encode('utf-8'), 'html5lib')
            if soup:
                # 获取问题名称以及对应的知乎链接
                questionurl = quryurl
                question = soup.select('.zm-item-title', _candidate_generator=None, limit=None)[0].next_element.encode('utf-8')
                # 获取回答问题的人和回答内容
                speaker = soup.select('.zm-item-answer', _candidate_generator=None, limit=20)
                if speaker:
                    for s in speaker:
                        authorinfo = s.select('.author-link')[0]
                        authorurl = url + authorinfo['href']
                        authorid = authorinfo.next_element.encode('utf-8')
                        content = s.select('.zm-editable-content')[0].strings
                        contstr =[]
                        print type(content)
                        for st in content:
                            contstr.append(st.encode('utf-8'))
                        bson = {
                        'questionurl':questionurl.encode('utf-8'),
                        'question':question,
                        'authorurl':authorurl.encode('utf-8'),
                        'authorid':authorid,
                        'content':contstr
                        }
                        print bson

if __name__ == '__main__':
    get_individual()
        














