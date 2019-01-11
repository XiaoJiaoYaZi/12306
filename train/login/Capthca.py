from adress.Urls import Urls
from io import BytesIO
from PIL import Image
from net.MyNet import MyNets
import time
import random
import base64

SHOW_MODEL = '''
            -----------------
            | 0 | 1 | 2 | 3 |
            -----------------
            | 4 | 5 | 6 | 7 |
            -----------------
'''

CAPTURE_CODE = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']




class Capture(object):
    __CapTureName = './capture.png'


    def getCapture(self):
        urlInfo = Urls['capture']
        urlInfo['url'] = urlInfo['url'].format(random.random())
        response =  MyNets.send(urlInfo=urlInfo)
        if response is None:
            urlInfo = Urls['capture2']
            now = int(time.time()*1000)
            urlInfo['url'] = urlInfo['url'].format(now)
            response = MyNets.send(urlInfo=urlInfo)
            return base64.b64decode(response['image'])
        else:
            return response

    def QueryManual(self):
        def capTure():
            while True:
                try:
                    img = Image.open(BytesIO(self.getCapture()))
                    img.show()
                    break
                except:
                    continue
            print(SHOW_MODEL)
            text = input("请输入验证码,按上图所示,多个用’,'分割")
            return self._makeCode(text.split(','))
        verifylist = capTure()
        result = self._verify(verifylist)
        if result[0] == False:
            print(result[1])
            return self.QueryManual()
        print(result)
        return True

    @staticmethod
    def _makeCode(text):
        verifyList = ''
        for a in text:
            verifyList+=CAPTURE_CODE[int(a)]
            verifyList+=','
        return verifyList[:-1]

    def _verify(self,answer):
        urlInfo = Urls['capture-check']
        data = {
            'answer': answer,
            'login_site': 'E',
            'rand': 'sjrand',
            '_json_att': "",
        }
        response = MyNets.send(urlInfo=urlInfo, data=data)
        if response['result_code'] =='4':
            return True,response['result_message']
        return False,response['result_message']



































































