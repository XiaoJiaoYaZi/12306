import requests
import random
import json
import datetime
import citys
import re
import time
stations = citys.getstations()

ran = random.random()
session = requests.session()

seatCodeList = {
    '商务座特等座':'9',
    '一等座':'M',
    '二等座':'O',
    '高级软卧':'6',
    '软卧':'4',
    '硬卧':'3',
    '软座':'2',
    '硬座':'1',
    '无座':'1'
}

class Func12306():
    def __init__(self):
        self.uamtk =''
        self.header = ''
        self.cookies = {
            "JSESSIONID": "9F1F33A95451ED8AE1BD50EAE23594ED",
            "tk":"Nj8dRP5N3GQgiBE_l3rNUUXSmyxLn43G70boDA09l2l0",
            "route": "9036359bb8a8a461c164a04f8f50b252",
            "BIGipServerpassport":"786956554.50215.0000",
            "BIGipServerotn": "2598633994.24610.0000",
            "RAIL_EXPIRATION":"1537471377553",
            "RAIL_DEVICEID": "o0Wit6ZuEuDBE7L9ETwWApWmSqgA821u8fUX1U0Neb2I0RkSAaFXzSLlaSs0NS2tUySfatfWEVe1LrkceglNIc3S1yASz2ip5SQe69VIZcd_Rx1CKbZUckDPRpJ8T0tuXnMSFKgfdzTlmjzHhaFOOMyyu40p-nsI",
             "BIGipServerpool_passport":"267190794.50215.0000",
            "_jc_save_toStation": "%u4E0A%u6D77%2CSHH",
            "_jc_save_toDate":"2018-09-18",
             "_jc_save_wfdc_flag": "dc",
             "current_captcha_type":"Z",
             "_jc_save_fromDate": "2018-09-19",                                                                                                                                                                                                                                      "_jc_save_fromStation":"%u6210%u90FD%2CCDW"
        }
        self.tk = ''
        self.reSubmitTk = ''
        self.keyIsChange = ''
        self.leftTicketStr =  ''
        self.train_no = ''
        self.station_train_code = ''
        self.train_location = ''

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
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}".format(random.random)
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
        print('NetWorkError')
        return False

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

    f12306.cookies = requests.utils.dict_from_cookiejar(session.cookies)

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
    if not verify(clickList):
        return False
    if not check_usr():
        return False
    return True

class passengerInfo():
    def __init__(self,name,id,mobile):
        self.__name = name
        self.__id = id
        self.__mobile = mobile

My_passengerInfo = {}



def get_passenger_info():
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'

    response = session.post(url=url,headers = header)
    info = None
    try:
        info = json.loads(response.text)
    except:
        print('get_passenger_info error')
        return False
    f12306.cookies = response.cookies
    if int(info['httpstatus']) ==200:
        if info['messages'] == '系统忙，请稍后重试':
            return False

        passenger_info = info['data']['normal_passengers']
        for a in passenger_info:
            My_passengerInfo[a['passenger_name']] = passengerInfo(a['passenger_name'],a['passenger_id_no'],a['mobile_no'])

My_trainInfo = {}

def serch_tickets(date,from_station,to_station):

    #url = "https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date,stations[from_station][1],stations[to_station][1])
    #url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=2018-09-20&leftTicketDTO.from_station=CDW&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'
    url ='https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}'.format(date)+\
          '&leftTicketDTO.from_station={}'.format(stations[from_station][1])+\
          '&leftTicketDTO.to_station={}'.format(stations[to_station][1])+\
          '&purpose_codes=ADULT'
    data = {
        'leftTicketDTO.train_date': date,
        'leftTicketDTO.from_station':from_station,
        'leftTicketDTO.to_station':to_station,
        'purpose_codes':'ADULT'
    }
    f_station = from_station.encode('unicode_escape').title().replace(b'\\',b'%u').decode('latin-1')+'%2C'+stations[from_station][1]
    t_station = to_station.encode('unicode_escape').title().replace(b'\\',b'%u').decode('latin-1')+'%2C'+stations[to_station][1]
    f12306.cookies["_jc_save_fromStation"] =  f_station
    f12306.cookies["_jc_save_toStation"]= t_station
    f12306.cookies["_jc_save_fromDate"]= date
    f12306.cookies["_jc_save_wfdc_flag"]= "dc"
    f12306.cookies["_jc_save_toDate"]= date



    response = session.get(url=url,headers = header,cookies = f12306.cookies,verify = False)
    train_info = None
    try:
        train_info = json.loads(response.text)
    except:
        print('serch_tickets error')
        return False
    for i in train_info['data']['result']:
        info = i.split('|')
        My_trainInfo[info[3]] = trainInfo(*tuple(info))
    return True



    pass

class trainInfo():
    def __init__(self,*args):
        self.__info = {}
        self.__info['SecretStrList'] = args[0]
        self.__info['NoList'] = args[1]
        self.__info['车次']           = args[3]   #车次
        self.__info['发车时间']       = args[8]   #发车时间
        self.__info['到达时间']       = args[9]   #到达时间
        self.__info['耗时']           = args[10]  #耗时
        self.__info['乘车时间']      = args[13]  #乘车时间
        self.__info['locationlist'] = args[15]
        self.__info['软卧']      = args[25]or '--'  # 软卧
        self.__info['无座']         = args[26]or '--'  # 无座
        self.__info['硬卧']  = args[28]or '--'  # 硬卧
        self.__info['硬座']       = args[29]or '--'  # 硬座
        self.__info['二等座']     = args[30]or '--'  # 二等座
        self.__info['一等座']      = args[31]or '--'  # 一等座
        self.__info['商务特等座']       = args[32]or '--'  # 商务特等座
        self.__info['动卧']      = args[33] or '--' # 动卧

    def haseSeat(self,seatType):
        seatInfo = self.__info[seatType]
        if seatInfo !='--' and \
                seatInfo !='无' and \
                seatInfo != '*':
            return seatInfo if seatInfo !='有' else '999'
        else:
            return '0'

    def get_SecretStrList(self):
        return self.__info['SecretStrList']
    def get_locationlist(self):
        return self.__info['locationlist']






def get_stations():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    response = session.get(url=url)
    if response.status_code == 200:
        pass

def check_ticket(startStation,endStation,startDate,seatType,trainName):
    searchResult = serch_tickets(startDate,startStation,endStation)
    if not searchResult:
        return False

    ticketinfo = My_trainInfo
    traininfo = ticketinfo[trainName]
    seatInfo = traininfo.haseSeat(seatType)
    return int(seatInfo)>0


def check_user():
    url = 'https://kyfw.12306.cn/otn/login/checkUser'
    data = {"_json_att": ""}
    # self.headers["Cache-Control"] = "no-cache"
    # self.headers["If-Modified-Since"] = "0"
    response = session.post(url=url, data=data, headers=header)
    try:
        dic = json.loads(response.text)
    except:
        return "NetWorkError"
    if dic['data']['flag']:
        print("用户在线验证成功")
        return True
    else:
        print('检查到用户不在线，请重新登陆')
        return False

def submit_order(startStation, endStation, startDate,trainName):
    url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    data = {"secretStr": My_trainInfo[trainName].get_SecretStrList(),
            "train_date": startDate,
            "back_train_date": '2018-09-18',
            "tour_flag": "dc",
            "purpose_codes": "ADULT",
            "query_from_station_name": startStation,
            "query_to_station_name": endStation,
            "undefined": ""
            }

    response = session.post(url=url, data=data,headers = header,cookies = f12306.cookies,verify = False)
    try:
        dic = json.loads(response.text)
    except:
        print("NetWorkError")
        return False


    if dic['status']:
        print('提交订单成功')
        return True
    elif dic['messages'] != '[]':
        if dic['messages'] == "车票信息已过期，请重新查询最新车票信息":
            print('车票信息已过期，请重新查询最新车票信息')
            return "ticketInfoOutData"
    else:
        print("提交失败")
        return False

def confirm_passenger():
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    data = {"_json_att": ''}
    response = session.post(url=url, data=data)
    try:
        f12306.reSubmitTk = re.findall('globalRepeatSubmitToken = \'(\S+?)\'', response.text)[0]
        f12306.keyIsChange = re.findall('key_check_isChange\':\'(\S+?)\'', response.text)[0]
        f12306.leftTicketStr = re.findall('leftTicketStr\':\'(\S+?)\'', response.text)[0]
        f12306.train_no = re.findall('train_no\':\'(\S+?)\'', response.text)[0]
        f12306.station_train_code = re.findall('station_train_code\':\'(\S+?)\'', response.text)[0]
        f12306.train_location = re.findall('train_location\':\'(\S+?)\'', response.text)[0]
    except:
        print("获取KEY失败")
        return 'NetWorkError'

def check_order( passengersList):
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
    passengerTicketStr = ""
    oldPassengerStr = ""
    for a in passengersList:
        passengerTicketStr += 'O' + ",0,1,{},1,{},{},N_".format(My_passengerInfo[a][0], My_passengerInfo[a][1], My_passengerInfo[a][2])
        oldPassengerStr += "{},1,{},1_".format(My_passengerInfo[a][0], My_passengerInfo[a][1])
    data = {
        "cancel_flag": "2",
        "bed_level_order_num": "000000000000000000000000000000",
        "passengerTicketStr": passengerTicketStr,
        "oldPassengerStr": oldPassengerStr,
        "tour_flag": "dc",
        "randCode": "",
        "whatsSelect": "1",
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": f12306.reSubmitTk
    }
    response = session.post(url=url, data=data)
    try:
        dic = json.loads(response.content)
    except:
        return "NetWorkError"
    if dic['data']['submitStatus'] is True:
        if dic['data']['ifShowPassCode'] == 'N':
            return True
        if dic['data']['ifShowPassCode'] == 'Y':
            return "Need Random Code"
    else:
        print("checkOrderFail")
        return False

def get_buy_image():
    url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&{}'.format(
        random.random())
    response = session.get(url=url, headers=header)
    with open( "./buyimg.jpg", 'wb') as f:
        f.write(response.content)


def get_queue_count( startStation, endStation, startDate, seatType):
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
    thatdaydata = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    train_date = "{} {} {} {} 00:00:00 GMT+0800 (中国标准时间)".format(thatdaydata.strftime('%a'),
                                                                 thatdaydata.strftime('%b'), startDate.split('-')[2],
                                                                 startDate.split('-')[0])
    data = {
        "train_date": train_date,
        "train_no": f12306.train_no,
        "stationTrainCode": f12306.station_train_code,
        "seatType": seatCodeList[seatType],
        "fromStationTelecode": stations[startStation][1],
        "toStationTelecode": stations[endStation][1],
        "leftTicket": f12306.leftTicketStr,
        "purpose_codes": "00",
        "train_location": f12306.train_location,
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": f12306.reSubmitTk
    }
    response = session.post(url=url, data=data, headers=header)
    try:
        dic = json.loads(response.content)
    except:
        return "NetWorkError"
    if dic['status']:
        print("进入队列成功")
        return True
    else:
        print("进入队列失败")
        return False

def confirm_single_for_queue(seatType, passengersList, trainName,clickList = None):
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
    passengerTicketStr = ""
    oldPassengerStr = ""
    for a in passengersList:
        passengerTicketStr += seatCodeList[seatType] + ",0,1,{},1,{},{},N_".format(
            My_passengerInfo[a][0], My_passengerInfo[a][1], My_passengerInfo[a][2])
        oldPassengerStr += "{},1,{},1_".format(My_passengerInfo[a][0], My_passengerInfo[a][1])

    codeList = ''
    if clickList is not None:
        code = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']

        for a in clickList:
            codeList +=code[int(a)]
            codeList+=','
        codeList = codeList[:-1]
        print(codeList)

    data = {
        "passengerTicketStr": passengerTicketStr,
        "oldPassengerStr": oldPassengerStr,
        "randCode": codeList,
        "purpose_codes": "00",
        "key_check_isChange": f12306.keyIsChange,
        "leftTicketStr": f12306.leftTicketStr,
        "train_location": My_trainInfo[trainName].get_locationlist,
        "choose_seats": "",
        "seatDetailType": "000",
        "whatsSelect": "1",
        "roomType": "00",
        "dwAll": "N",
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": f12306.reSubmitTk
    }
    response = session.post(url=url, data=data, headers=header)
    try:
        dic = json.loads(response.content)
    except:
        return "NetWorkError"

    if 'data' in dic.keys():
        if dic['data']['submitStatus'] is True:
            print("提交订单成功")
            return True
        elif dic['data']['errMsg'] == u"验证码输入错误！":
            return "wrongCode"

    else:
        print("提交订单失败")
        return False


def wait_time():
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}'.format(round(time.time()*1000),f12306.reSubmitTk)
    response = session.get(url=url, headers=header)
    try:
        dic = json.loads(response.content)
    except:
        return "NetWorkError"
    if dic['status']:
        if dic['data']['queryOrderWaitTimeStatus']:
            if dic['data']['waitTime'] > 0 :
                return dic['data']['waitTime']
            elif dic['data']['waitTime'] == -1:
                Func12306.orderId = ''
                Func12306.orderId = dic['data']['orderId']
                return dic['data']['waitTime']
            else:
                return False
        else:
            return False
    else:
        return False

while not login():
    continue
#get_passenger_info()
# while not serch_tickets('2018-09-20','北京','上海')[0]:
#     continue
time.sleep(3)
while not check_ticket('北京','上海','2018-09-20','二等座','G101'):
    time.sleep(3)
    continue
check_user()
time.sleep(3)
while not submit_order('北京','上海','2018-09-20','G101'):
    time.sleep(1)
    continue
time.sleep(3)
confirm_passenger()
check_order('李秋东')
get_buy_image()
get_queue_count('北京','上海','2018-09-20','二等座')
confirm_single_for_queue('二等座','李秋东','G101')
wait_time()

#get_passenger_info()



































