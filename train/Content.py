
class SeatName(object):
    BUSINESS_SEAT = '商务座'
    SPECIAL_SEAT = '特等座'
    FIRST_CLASS_SEAT = '一等座'
    SECOND_CLASS_SEAT = '二等座'
    ADVANCED_SOFT_SLEEP = '高级软卧'
    SOFT_SLEEP = '软卧'
    HARD_SLEEP = '硬卧'
    SOFT_SEAT = '软座'
    HARD_SEAT = '硬座'
    NO_SEAT = '无座'


# seatType:商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)
SEAT_TYPE = {
    SeatName.BUSINESS_SEAT: '9',
    SeatName.SPECIAL_SEAT: 'P',
    SeatName.FIRST_CLASS_SEAT: 'M',
    SeatName.SECOND_CLASS_SEAT: 'O',
    SeatName.ADVANCED_SOFT_SLEEP: '6',
    SeatName.SOFT_SLEEP: '4',
    SeatName.HARD_SLEEP: '3',
    SeatName.SOFT_SEAT: '2',
    SeatName.HARD_SEAT: '1',
    SeatName.NO_SEAT: '1',
}