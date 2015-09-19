import http.cookiejar
import urllib.request

def getOpener(head):
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    print('opener created！')
    return opener

import gzip
def getData(op):
    data = op.read()
    if op.info().get('Content-Encoding') == 'gzip':
        data = gzip.decompress(data)
    return data.decode()

def saveData(fileName,data):
    f = open(fileName,'w',encoding = 'utf-8')
    f.write(data)
    f.close()

from bs4 import BeautifulSoup
def login(opener,id,password):
    op = opener.open(urlLogin)
    data = getData(op)
    soup = BeautifulSoup(data,'html.parser')
    postDict = {
        'mobile' : id,
        soup.find('input',{'type':'password'})['name'] : password,
        'vk' : soup.find('input',{'name':'vk'})['value'],
        'remember' : 'on',
        'backURL' : soup.find('input',{'name':'backURL'})['value'],
        'backTitle' : soup.find('input',{'name':'backTitle'})['value'],
        'submit' : soup.find('input',{'name':'submit'})['value'],
        'tryCount' : soup.find('input',{'name':'tryCount'})['value']
    }
    postData = urllib.parse.urlencode(postDict).encode()
    randUrl = soup.find('form',{'action':True})['action']
    op = opener.open(urlLogin+randUrl,postData)
    data = getData(op)
    saveData('login.html',data)
    soup = BeautifulSoup(data,'html.parser')
    if soup.title.get_text() == '我的首页':
        print('login successed！')
        return True
    else:
        print('login failed！')
        return False

header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate',
    'Referer' : 'http://weibo.cn/pub/'
    }

urlLogin = 'http://login.weibo.cn/login/'

id = 'xxxx@sina.cn'
password = 'xxxxx'

opener = getOpener(header)
login(opener,id,password)

#test
urlStart = 'http://weibo.cn/u/2488492271'

op = opener.open(urlStart)
data = getData(op)
saveData('test.html',data)






