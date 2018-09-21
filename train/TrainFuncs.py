
from train.Content import *
from train.ticketDetails import TicketDetails

ADVANCED_SOFT_SLEEP = '高级软卧'
SOFT_SLEEP = '软卧'
HARD_SLEEP = '硬卧'
SOFT_SEAT = '软座'
HARD_SEAT = '硬座'
NO_SEAT = '无座'

def passengerTicketStrs():
    pass

#查找车次
def filterTrain(ticketDetails:TicketDetails, trainsNo:list):
    if not trainsNo:
        return True
    for trainNo in trainsNo:
        if trainNo == ticketDetails.trainNo:
            return True
    return False

#查找余票
def filterTickets(ticketDetail:TicketDetails,seatType:list):
    if not seatType:
        return True
    for seat in seatType:
        if seat == SEAT_TYPE[SeatName.BUSINESS_SEAT]:
            yield SeatName.BUSINESS_SEAT,ticketDetail.businessSeat
            continue
        if seat == SEAT_TYPE[SeatName.SPECIAL_SEAT]:
            yield SeatName.SPECIAL_SEAT,ticketDetail.businessSeat
            continue
        if seat == SEAT_TYPE[SeatName.FIRST_CLASS_SEAT]:
            yield SeatName.FIRST_CLASS_SEAT,ticketDetail.firstClassSeat
            continue
        if seat == SEAT_TYPE[SeatName.SECOND_CLASS_SEAT]:
            yield SeatName.SECOND_CLASS_SEAT,ticketDetail.secondClassSeat
            continue
        if seat == SEAT_TYPE[SeatName.ADVANCED_SOFT_SLEEP]:
            yield SeatName.ADVANCED_SOFT_SLEEP,ticketDetail.advancedSoftSleep
            continue
        if seat == SEAT_TYPE[SeatName.SOFT_SEAT]:
            yield SeatName.SOFT_SEAT,ticketDetail.softSeat
            continue
        if seat == SEAT_TYPE[SeatName.SOFT_SEAT]:
            yield SeatName.SOFT_SEAT,ticketDetail.softSeat
            continue
        if seat == SEAT_TYPE[SeatName.HARD_SLEEP]:
            yield SeatName.HARD_SLEEP, ticketDetail.hardSleep
            continue
        if seat == SEAT_TYPE[SeatName.SOFT_SEAT]:
            yield SeatName.SOFT_SEAT, ticketDetail.softSeat
            continue
        if seat == SEAT_TYPE[SeatName.HARD_SEAT]:
            yield SeatName.HARD_SEAT, ticketDetail.hardSeat
            continue
        if seat == SEAT_TYPE[SeatName.NO_SEAT]:
            yield SeatName.NO_SEAT, ticketDetail.noSeat
