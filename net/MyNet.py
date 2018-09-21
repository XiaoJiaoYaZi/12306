import requests
import time



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
        MyNets.__session.headers.update({
            'Host': r'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        })

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
        except:
            pass
        return None

if __name__ == '__main__':
    MyNets.send('hell')
