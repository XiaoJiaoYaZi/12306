import requests
import time
import random
import re
from adress import Urls

url = 'http://www.xicidaili.com/nn/'
html = requests.get(url=url, headers=Urls.header).text
regip = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s*?<td>(\d*)</td>'
matcher = re.compile(regip)
ipstr = re.findall(matcher, html)
ip_list = {}
for ipport in ipstr:
    ip_list[ipport[0]] = ipport[1]
# 随机获取列表中一个ip
ip = random.choice(list(ip_list.keys()))
ip = {ip:ip_list[ip]}


def sendLogic(func):
    def wrapper(*args,**kwargs):
        for i in range(5):
            response = func(*args,**kwargs)
            if response:
                return response
            time.sleep(1)
        return None
    return wrapper

class MyNets(object):
    __session =requests.session()
    @staticmethod
    def updateHeaders(headers):
        MyNets.__session.headers.update(headers)

    @staticmethod
    def resetHeaders():
        MyNets.__session.headers.clear()
        MyNets.__session.headers.update(Urls.header)

    @staticmethod
    def setCookies(**kwargs):
        for k, v in kwargs.items():
            MyNets.__session.cookies.set(k, v)

    @staticmethod
    def removeCookies(key=None):
        MyNets.__session.cookies.set(key, None) if key else MyNets.__session.cookies.clear()

    @staticmethod
    @sendLogic
    def send(urlInfo, params=None, data=None, **kwargs):
        MyNets.resetHeaders()
        if 'headers' in urlInfo and urlInfo['headers']:
            MyNets.updateHeaders(urlInfo['headers'])
        try:
            response = MyNets.__session.request(method=urlInfo['method'],
                                                url=urlInfo['url'],
                                                params=params,
                                                data=data,
                                                timeout=10,
                                                allow_redirects=False,
                                                proxies = ip,
                                                **kwargs)
            if response.status_code == requests.codes.ok:
                try:
                    if 'response' in urlInfo:
                        if urlInfo['response'] == 'img':
                            return response.content
                        if urlInfo['response'] == 'html':
                            response.encoding = response.apparent_encoding
                            return response.text
                        if urlInfo['response'] == 'json':
                            return response.json()
                except Exception as e:
                    print(e)
                return None
        except Exception as e:
            return None
            pass
        return None

if __name__ == '__main__':
    MyNets.send('hell')
