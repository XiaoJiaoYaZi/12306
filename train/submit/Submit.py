from train.ticketDetails import TicketDetails
from adress.Urls import Urls
from net.MyNet import MyNets
from train.submit.PassengerDetails import PassengerDetails
from train.Content import *
from train.login.Capthca import Capture,SHOW_MODEL
import time
import re
import json
import random
from PIL import Image
from io import BytesIO
import datetime
from urllib.parse import *


def formatDate(date):
    return datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

def undecodeSecretStr(urlDecodedSecretStr):
    return unquote(urlDecodedSecretStr).replace('\n', '')

# 订单信息：票款金额
def submitTicketCostInfo(ticketIndex, jsonTicketInfo, orderDBListIndex=0):
    return '%s%s元' % (
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['ticket_type_name'],
         jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex][
            'str_ticket_price_page'] ,
    )


def submitTrainInfo(ticketIndex, jsonTicketInfo, orderDBListIndex=0):
    return '%s开\n%s %s-%s' % (
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['start_train_date_page'],
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['stationTrainDTO'][
            'station_train_code'],
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['stationTrainDTO']['from_station_name'],
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['stationTrainDTO']['to_station_name'],
    )


# 订单信息：席位信息
def submitCoachInfo(ticketIndex, jsonTicketInfo, orderDBListIndex=0):
    return '%s车厢\n%s%s' % (
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['coach_no'],
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['seat_name'],
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['seat_type_name'],
    )


# 订单信息：旅客信息
def submitPassengerInfo(ticketIndex, jsonTicketInfo, orderDBListIndex=0):
    return '%s\n%s' % (
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['passengerDTO']['passenger_name'],
        jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['passengerDTO'][
            'passenger_id_type_name'],
    )

# 订单信息：车票状态
def submitTicketPayInfo(ticketIndex, jsonTicketInfo, orderDBListIndex=0):
    return jsonTicketInfo['orderDBList'][orderDBListIndex]['tickets'][ticketIndex]['ticket_status_name']


# 订单信息：车票总张数
def submitTicketTotalNum(jsonTicketInfo, orderDBListIndex=0):
    return jsonTicketInfo['orderDBList'][orderDBListIndex]['ticket_totalnum']


# 订单信息：车票总价
def submitTicketTotalCost(jsonTicketInfo, orderDBListIndex=0):
    return jsonTicketInfo['orderDBList'][orderDBListIndex]['ticket_total_price_page']

class Submit(object):
    def __init__(self,ticketDetail:TicketDetails,passengerList):
        self.__ticketDetail = ticketDetail
        self.__passengerList = passengerList

    #验证用户在线
    def _checkusrOnline(self):
        urlInfo = Urls['checkUser']
        data ={
            "_json_att": ""
        }

        response = MyNets.send(urlInfo)
        if response:
            if response['data']['flag']:
                print('用户在线验证成功')
                return True
            else:
                print('检测不到用户在线，请重新登陆')
                return False
        return False

    def _submitOrderRequest(self):
        urlInfo = Urls['submitOrderRequest']
        data = {
            'secretStr': undecodeSecretStr(self.__ticketDetail.secretStr),
            "train_date": formatDate(self.__ticketDetail.startDate),
            "back_train_date": time.strftime("%Y-%m-%d", time.localtime()),
            "tour_flag": "dc",
            "purpose_codes": "ADULT",
            "query_from_station_name": self.__ticketDetail.startStation,
            "query_to_station_name": self.__ticketDetail.endStation,
            "undefined": ""
        }

        response = MyNets.send(urlInfo=urlInfo,data=data)
        if response:
            if response['status']:
                #print('提交订单成功')
                return True,'提交订单成功'
            elif response['messages'] != '[]':
                if response['messages'] == "车票信息已过期，请重新查询最新车票信息":
                    #print('车票信息已过期，请重新查询最新车票信息')
                    return False,'车票信息已过期，请重新查询最新车票信息'
            else:
                #print(response['messages'])
                return False,response['messages']
        return False,''

    def _confirm_passenger(self):
        urlInfo = Urls['initDc']
        data = {
            "_json_att": ''
        }
        html = MyNets.send(urlInfo=urlInfo,data=data)
        if not html:
            return False

        def getreSubmitTk(html):
            return re.findall('globalRepeatSubmitToken = \'(\S+?)\'', html)[0]
        self.__ticketDetail.reSubmitTk = getreSubmitTk(html)

        def getPassengerForm(html):
            return json.loads(re.findall(r'var ticketInfoForPassengerForm=(.*);', html)[0].replace("'", "\""))

        self.__ticketDetail.PassengerForm = getPassengerForm(html)
        return True



    def _getParams(self,html):
        self.reSubmitTk = re.findall('globalRepeatSubmitToken = \'(\S+?)\'', html)[0]
        self.keyIsChange = re.findall('key_check_isChange\':\'(\S+?)\'', html)[0]
        self.leftTicketStr = re.findall('leftTicketStr\':\'(\S+?)\'', html)[0]
        self.train_no = re.findall('train_no\':\'(\S+?)\'', html)[0]
        self.station_train_code = re.findall('station_train_code\':\'(\S+?)\'', html)[0]
        self.train_location = re.findall('train_location\':\'(\S+?)\'', html)[0]
        self.purpose_codes = re.findall('purpose_codes\':\'(\S+?)\'', html)[0]

    #获取联系人信息
    def _getPassengerDTOs(self):

        if not self._confirm_passenger():
            return False

        response = MyNets.send(Urls['PassengerDTOs'])
        if response:
            if response['messages'] =='系统忙，请稍后重试':
                return False
            self.passenger_info = self.__getPassengerInfo(response['data']['normal_passengers'])
            return True
        return False

    def __getPassengerInfo(self, passengersList):
        passengersDetails = {}
        for passengerJson in passengersList:
            passenger = PassengerDetails()
            passenger.passengerName = passengerJson['passenger_name'] or ''
            passenger.code = passengerJson['code'] or ''
            passenger.countryCode = passengerJson['country_code'] or ''
            passenger.passengerIdTypeCode = passengerJson['passenger_id_type_code'] or ''
            passenger.passengerIdTypeName = passengerJson['passenger_id_type_name'] or ''
            passenger.passengerIdNo = passengerJson['passenger_id_no'] or ''
            passenger.passengerType = passengerJson['passenger_type'] or ''
            passenger.passengerFlag = passengerJson['passenger_flag'] or ''
            passenger.passengerTypeName = passengerJson['passenger_type_name'] or ''
            passenger.mobileNo = passengerJson['mobile_no'] or ''
            passenger.phoneNo = passengerJson['phone_no'] or ''
            passenger.postalcode = passengerJson['postalcode'] or ''
            passenger.indexId = passengerJson['index_id'] or ''
            passengersDetails[passenger.passengerName] = passenger
        return passengersDetails

    def _check_order(self):

        passengerTicketStr = ""
        oldPassengerStr = ""
        for a in self.__passengerList:
            #多个联系人用 ’_'链接
            if a not in self.passenger_info.keys():
                print(a+'不在联系人列表，请先添加联系人')
                return False,''
            passengerTicketStr += SEAT_TYPE[self.__ticketDetail.queryseat] + ",0,1,{},1,{},{},N_".format(self.passenger_info[a].passengerName,
                                                                                              self.passenger_info[a].passengerIdNo,
                                                                                              self.passenger_info[a].phoneNo)
            oldPassengerStr += "{},1,{},1_".format(self.passenger_info[a].passengerName, self.passenger_info[a].passengerIdNo)
        #去掉最后的“_”
        #passengerTicketStr = passengerTicketStr[:-1]
        data = {
            "cancel_flag": self.__ticketDetail.PassengerForm['orderRequestDTO']['cancel_flag'] or '2',
            "bed_level_order_num": self.__ticketDetail.PassengerForm['orderRequestDTO'][
                                       'bed_level_order_num'] or '000000000000000000000000000000',
            "passengerTicketStr": passengerTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "tour_flag": "dc",
            "randCode": "",
            "whatsSelect": "1",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.__ticketDetail.reSubmitTk
        }

        response = MyNets.send(urlInfo=Urls['checkOrderInfo'],data=data)

        if response:
            if response['data']['submitStatus']:
                return True,response['data']['ifShowPassCode']
            return False,''
        return False,''

    def _get_buy_image(self):
        urlInfo = Urls['CaptureNew']
        urlInfo['url'] = urlInfo['url'].format(random.random())
        img = Image.open(BytesIO(MyNets.send(urlInfo)))
        return img

    def _getQueueCount(self):
        urlInfo = Urls['getQueueCount']
        data = {
            # Thu+Jan+04+2018+00:00:00+GMT+0800
            # 'train_date': datetime.strptime(
            #     self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_date'], '%Y%m%d').strftime(
            #     '%b+%a+%d+%Y+00:00:00+GMT+0800'),
            # Mon Jan 08 2018 00:00:00 GMT+0800 (中国标准时间)
            'train_date': datetime.datetime.strptime(
                self.__ticketDetail.PassengerForm['queryLeftTicketRequestDTO']['train_date'], '%Y%m%d').strftime(
                '%b %a %d %Y 00:00:00 GMT+0800') + ' (中国标准时间)',
            'train_no': self.__ticketDetail.PassengerForm['queryLeftTicketRequestDTO']['train_no'],
            'stationTrainCode': self.__ticketDetail.trainNo,
            'seatType': SEAT_TYPE[self.__ticketDetail.queryseat],
            'fromStationTelecode': self.__ticketDetail.fromStationCode,
            'toStationTelecode': self.__ticketDetail.toStationCode,
            'leftTicket': self.__ticketDetail.PassengerForm['leftTicketStr'],
            'purpose_codes': self.__ticketDetail.PassengerForm['purpose_codes'],
            'train_location': self.__ticketDetail.PassengerForm['train_location'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticketDetail.reSubmitTk,
        }
        response = MyNets.send(urlInfo=urlInfo,data=data)
        return response['status'], response['messages'], \
               response['data']['ticket'] if 'data' in response and 'ticket' in response['data'] else -1, \
               response['data']['count'] if 'data' in response and 'count' in response['data'] else -1

    def _confirm_single_for_queue(self,clickedList=''):
        urlInfo = Urls['confirmSingleForQueue']
        passengerTicketStr = ""
        oldPassengerStr = ""
        for a in self.__passengerList:
            #多个联系人用 ’_'链接
            passengerTicketStr += SEAT_TYPE[self.__ticketDetail.queryseat] + ",0,1,{},1,{},{},N_".format(self.passenger_info[a].passengerName,
                                                                                              self.passenger_info[a].passengerIdNo,
                                                                                              self.passenger_info[a].phoneNo)
            oldPassengerStr += "{},1,{},1_".format(self.passenger_info[a].passengerName, self.passenger_info[a].passengerIdNo)
        passengerTicketStr = passengerTicketStr[:-1]
        data = {
            "passengerTicketStr": passengerTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "randCode": clickedList,
            "purpose_codes": self.__ticketDetail.PassengerForm['purpose_codes'],
            "key_check_isChange": self.__ticketDetail.PassengerForm['key_check_isChange'],
            "leftTicketStr": self.__ticketDetail.PassengerForm['leftTicketStr'],
            "train_location": self.__ticketDetail.PassengerForm['train_location'],
            "choose_seats": "",
            "seatDetailType": "000",
            "whatsSelect": "1",
            "roomType": "00",
            "dwAll": "N",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.__ticketDetail.reSubmitTk
        }
        response = MyNets.send(urlInfo=urlInfo,data=data)

        if 'data' in response.keys():
            if response['data']['submitStatus'] is True:
                print("提交订单成功")
                return True
            elif response['data']['errMsg'] == "验证码输入错误！":
                return False

        else:
            print("提交订单失败")
            return False


    def _wait_time(self):
        urlInfo = Urls['wait-time']
        urlInfo['url'] = urlInfo['url'].format(round(time.time())*1000,self.__ticketDetail.reSubmitTk)
        response = MyNets.send(Urls['wait-time'])

        return  response['status'], response['messages'], response['data']['waitTime'], response['data']['orderId'], \
                response['data']['msg'] if 'msg' in response['data'] else None

    def __waitForOrderId(self):
        print('正在排队获取订单!')
        count = 0
        while True:
            count += 1
            status, msg, waitTime, orderId, errorMsg = self._wait_time()
            if not status:
                return None
            if waitTime < 0:
                if orderId:
                    print('订单提交成功，订单号: %s' % orderId)
                    return orderId
                elif errorMsg:
                    print(errorMsg)
                    return None
            interval = waitTime // 60
            print('未出票，订单排队中...预估等待时间: %s 分钟' % (interval if interval <= 30 else '超过30'))
            if interval > 30:
                time.sleep(60)
            elif interval > 20:
                time.sleep(30)
            elif interval > 10:
                time.sleep(10)
            else:
                time.sleep(3)

    def _resultOrderForDcOrWcQueue(self, orderSequenceNo):
        formData = {
            'orderSequence_no': orderSequenceNo,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticketDetail.reSubmitTk,
        }
        jsonRet = MyNets.send(Urls['resultOrderForQueue'], data=formData)
        print('resultOrderForDcOrWcQueue', jsonRet)
        return jsonRet['status'], jsonRet['messages'], jsonRet['data']['submitStatus']

    def submit(self):
        result,msg = self._submitOrderRequest()
        print(msg)
        if not result:
            return False

        if not self._getPassengerDTOs():
            return False

        result ,msg = self._check_order()
        img = self._get_buy_image()
        verify = ''
        if msg =='Y':
            img.show()
            print(SHOW_MODEL)
            text = input("请输入验证码,按上图所示,多个用’,'分割")
            verify = Capture._makeCode(text.split(','))

        status, msg, leftTickets, personsCount = self._getQueueCount()
        if not status:
            return False
        print('%s 剩余车票:%s ,目前排队人数: %s' % (self.__ticketDetail.trainNo, leftTickets, personsCount))

        if not self._confirm_single_for_queue(verify):
            return False

        orderId = self.__waitForOrderId()

        status, msg, submitStatus = self._resultOrderForDcOrWcQueue(orderId)
        print(msg)
        if not status:
            return False
        if not submitStatus:
            print(msg)
        print('您已成功订购火车票！请在30分钟内前往12306官方网站进行支付！')
        return True

    def _queryMyOrderNoComplete(self):
        formData = {
            '_json_att': '',
        }
        jsonRet = MyNets.send(Urls['queryMyOrderNoComplete'], data=formData)
        return jsonRet['status'], jsonRet['messages'], jsonRet['data']


    def showSubmitInfoPretty(self):
        status, msg, jsonTicketInfo = self._queryMyOrderNoComplete()
        if not status:
            return False
        from prettytable import PrettyTable
        table = PrettyTable()
        table.field_names = '序号 车次信息 席位信息 旅客信息 票款金额 车票状态'.split(sep=' ')
        totalTicketNum = submitTicketTotalNum(jsonTicketInfo)
        for i in range(totalTicketNum):
            table.add_row([i + 1,
                           submitTrainInfo(i, jsonTicketInfo),
                           submitCoachInfo(i, jsonTicketInfo),
                           submitPassengerInfo(i, jsonTicketInfo),
                           submitTicketCostInfo(i, jsonTicketInfo),
                           submitTicketPayInfo(i, jsonTicketInfo),
                           ])
            if not i == totalTicketNum - 1:
                table.add_row([2 * '-', 2 * '-', 2 * '-', 2 * '-', 2 * '-', 2 * '-'])

        print(table)
        print('总张数:%d\t待支付金额:%s' % (
            totalTicketNum, '{}元'.format(submitTicketTotalCost(jsonTicketInfo))))
        return True

if __name__ == '__main__':
    pass



















