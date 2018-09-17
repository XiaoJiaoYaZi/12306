import requests
import random
import json
import os

ran = random.random()
session = requests.session()


class Func12306():
    def __init__(self):
        self.uamtk =''
        self.header = ''
        self.cookies = ''
        session.tk = ''

f12306 = Func12306()

header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }

def get_img():
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}".format(ran)
    response = session.get(url=url,headers=header)
    with open("./img.png", 'wb') as f:
        f.write(response.content)

def verify(clickList):
    url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'

    code = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']
    verifyList = ''
    for a in clickList:
       verifyList+=code[int(a)]
       verifyList+=','
    verifyList = verifyList[:-1]
    data = {
       'answer': verifyList,
       'login_site': 'E',
       'rand': 'sjrand',
       '_json_att':"",
    }

    response = session.post(url=url, data=data, headers=header)
    try:
        dic = json.loads(response.text)
    except:
        return "NetWorkError"
    resultCode = dic['result_code']
    resultMsg = dic['result_message']
    verifyInfo = resultMsg
    if str(resultCode) == "4":
        return True,"verifySuccessful"
    else:
       return False,'verifyFail'

def check_usr():
    url = 'https://kyfw.12306.cn/passport/web/login'
    data = {
        'username': 'lqd5906313',
        'password': 'Lqd5906313',
        'appid': 'otn',
        '_json_att': "",
    }

    response = session.post(url=url,data=data)
    info = None
    try:
        info = json.loads(response.text)
    except:
        return 'NetWorkError'

    resultCode = info['result_code']
    resultMsg = info['result_message']

    if int(resultCode)==0:
        print(resultMsg)
    else:
        print(resultMsg)
        return False

    if 'uamtk' in info.keys():
        f12306.uamtk = info['uamtk']

    url2 = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
    data2 = {
            "appid": "otn",
            '_json_att':""
        }
    response2 = session.post(url=url2,data=data2)
    info2 = None
    try:
        info2 = json.loads(response2.text)
    except:
        return 'url2 error'
    resultCode = info2['result_code']
    resultMsg = info2['result_message']
    if int(resultCode)==0:
        print(resultMsg)
    else:
        print(resultMsg)
        return False

    if 'newapptk' in info2.keys():
        f12306.tk = info2["newapptk"]
        # Func12306.cookies.pop('uamtk')
        # Func12306.cookies['tk'] = Func12306.tk

    url3 = 'https://kyfw.12306.cn/otn/uamauthclient'
    data3 = {"tk": f12306.tk,
             '_json_att': "",
             }

    response3 = session.post(url=url3,data=data3)
    info3 = None
    try:
        info3 = json.loads(response3.text)
    except:
        print('url3 error')
        return False

    resultCode = info3['result_code']
    resultMsg = info3['result_message']
    if int(resultCode)==0:
        print(resultMsg)
    else:
        print(resultMsg)
        return False
    return True

def login():
    get_img()
    num = input('请输入验证码\n')
    clickList = num.split(',')
    verify(clickList)
    check_usr()

def get_passenger_info():
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'

    response = session.post(url=url)
    info = None
    try:
        info = json.loads(response.text)
    except:
        print('get_passenger_info error')
        return False

    if info['message'] !=[]:
        if info['message'][0] == '系统忙，请稍后重试':
            return False

        #passenger_info =

def serch_tickets():
    pass

def get_stations():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    response = session.get(url=url)
    if response.status_code == 200:




login()
get_stations()
get_passenger_info()



































