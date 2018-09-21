from adress.Urls import Urls
from adress.CityCode import *
from net.MyNet import MyNets
from train.ticketDetails import TicketDetails
from train.TrainFuncs import *
import time

#  车次：3
INDEX_TRAIN_NO = 3
#  start_station_code:起始站：4
INDEX_TRAIN_START_STATION_CODE = 4
#  end_station_code终点站：5
INDEX_TRAIN_END_STATION_CODE = 5
#  from_station_code:出发站：6
INDEX_TRAIN_FROM_STATION_CODE = 6
#  to_station_code:到达站：7
INDEX_TRAIN_TO_STATION_CODE = 7
#  start_time:出发时间：8
INDEX_TRAIN_LEAVE_TIME = 8
#  arrive_time:达到时间：9
INDEX_TRAIN_ARRIVE_TIME = 9
#  历时：10
INDEX_TRAIN_TOTAL_CONSUME = 10
#  商务特等座：32
INDEX_TRAIN_BUSINESS_SEAT = 32
#  一等座：31
INDEX_TRAIN_FIRST_CLASS_SEAT = 31
#  二等座：30
INDEX_TRAIN_SECOND_CLASS_SEAT = 30
#  高级软卧：21
INDEX_TRAIN_ADVANCED_SOFT_SLEEP = 21
#  软卧：23
INDEX_TRAIN_SOFT_SLEEP = 23
#  动卧：33
INDEX_TRAIN_MOVE_SLEEP = 33
#  硬卧：28
INDEX_TRAIN_HARD_SLEEP = 28
#  软座：24
INDEX_TRAIN_SOFT_SEAT = 24
#  硬座：29
INDEX_TRAIN_HARD_SEAT = 29
#  无座：26
INDEX_TRAIN_NO_SEAT = 28
#  其他：22
INDEX_TRAIN_OTHER = 22
#  备注：1
INDEX_TRAIN_MARK = 1

INDEX_SECRET_STR = 0

INDEX_START_DATE = 13  # 车票出发日期

class Query(object):

    @staticmethod
    def search_tickets(startStation,endStation,startDate):
        urlInfo = Urls['search-tickets']
        urlInfo['url'] = urlInfo['url'].format(startDate,city2code(startStation),city2code(endStation))

        f_station = startStation.encode('unicode_escape').title().replace(b'\\', b'%u').decode('latin-1') + '%2C' + \
                    city2code(startStation)
        t_station = endStation.encode('unicode_escape').title().replace(b'\\', b'%u').decode('latin-1') + '%2C' + \
                    city2code(endStation)

        cookies = {
            '_jc_save_fromDate': startDate,
            '_jc_save_fromStation': f_station,
            '_jc_save_toDate': startDate,
            '_jc_save_toStation': t_station,
            '_jc_save_wfdc_flag': 'dc'
        }
        MyNets.setCookies(**cookies)
        response = MyNets.send(urlInfo=urlInfo)
        try:
            if response:
                return Query.__decode(response['data']['result'])
        except Exception as e:
            print(e)
        return []


    @staticmethod
    def __decode(trainInfos):
        for train in trainInfos:
            info = train.split('|')
            ticket = TicketDetails()
            ticket.trainNo = info[INDEX_TRAIN_NO]
            ticket.startStationCode = info[INDEX_TRAIN_START_STATION_CODE]
            ticket.endStationCode = info[INDEX_TRAIN_END_STATION_CODE]
            ticket.fromStationCode = info[INDEX_TRAIN_FROM_STATION_CODE]
            ticket.toStationCode = info[INDEX_TRAIN_TO_STATION_CODE]
            ticket.leaveTime = info[INDEX_TRAIN_LEAVE_TIME]
            ticket.arriveTime = info[INDEX_TRAIN_ARRIVE_TIME]
            ticket.totalConsume = info[INDEX_TRAIN_TOTAL_CONSUME]
            ticket.businessSeat = info[INDEX_TRAIN_BUSINESS_SEAT]
            ticket.firstClassSeat = info[INDEX_TRAIN_FIRST_CLASS_SEAT]
            ticket.secondClassSeat = info[INDEX_TRAIN_SECOND_CLASS_SEAT]
            ticket.advancedSoftSleep = info[INDEX_TRAIN_ADVANCED_SOFT_SLEEP]
            ticket.softSleep = info[INDEX_TRAIN_SOFT_SLEEP]
            ticket.moveSleep = info[INDEX_TRAIN_MOVE_SLEEP]
            ticket.hardSleep = info[INDEX_TRAIN_HARD_SLEEP]
            ticket.softSeat = info[INDEX_TRAIN_SOFT_SEAT]
            ticket.hardSeat = info[INDEX_TRAIN_HARD_SEAT]
            ticket.noSeat = info[INDEX_TRAIN_NO_SEAT]
            ticket.other = info[INDEX_TRAIN_OTHER]
            ticket.mark = info[INDEX_TRAIN_MARK]
            ticket.startStation = code2city(ticket.startStationCode)
            ticket.endStation = code2city(ticket.endStationCode)
            ticket.fromStation = code2city(ticket.fromStationCode)
            ticket.toStation = code2city(ticket.toStationCode)
            ticket.secretStr = info[INDEX_SECRET_STR]
            ticket.startDate = info[INDEX_START_DATE]
            yield ticket


    @staticmethod
    def check_tickets(startStation,endStation,startDate,seatType,trainName):
        for ticket in Query.search_tickets(startStation,endStation,startDate):
            if not filterTrain(ticket,trainName):
                continue
            for seat , retain in filterTickets(ticket,seatType):
                if retain and retain !='无':
                    print(seat,retain)
                    ticket.queryseat = seat
                    yield ticket
        return None

    @staticmethod
    def loopQuery(startStation,endStation,startDate,seatType,trainName,timeInterval):
        n = 0
        while True:
            n+=1
            print('正在进行第%d次查票'% n)
            for ticket in Query.check_tickets(startStation,endStation,startDate,seatType,trainName):
                if ticket:
                    return ticket
            time.sleep(timeInterval)

if __name__ == "__main__":
    from train.login.Login import Login
    #login = Login()
    #login.Login('lqd5906313','Lqd5906313')
    print(Query.loopQuery('北京','上海','2018-09-26',['M','O'],['G101'],1))


