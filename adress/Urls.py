
import random

header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }

Urls = {
    'init': {
        'url': r'https://kyfw.12306.cn/otn/login/init',
        'method': 'GET',
        'headers': {
            'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
        },
        'response': 'html',
    },
    #获取验证码
    'capture':{
        'url' :"https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}",
        'method':'GET',
        'response':'img'
    },
    #检验验证码
    'capture-check':{
        'url':'https://kyfw.12306.cn/passport/captcha/captcha-check',
        'method':'POST',
        'response':'json',
    },
    #登录
    'login':{
        'url': 'https://kyfw.12306.cn/passport/web/login',
        'method':'POST',
        'response':'json'
    },
    #uamtk 校验
    'uamtk':{
        'url':'https://kyfw.12306.cn/passport/web/auth/uamtk',
        'method':'POST',
        'response':'json'
    },
    #newapptk 校验
    'newapptk':{
        'url':'https://kyfw.12306.cn/otn/uamauthclient',
        'method':'post',
        'response':'json'
    },
    'uamauthclient': {
        'url': 'https://kyfw.12306.cn/otn/uamauthclient',
        'method': 'POST',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
        },
        'response':'json'
    },
    #PassengerDTOs获取联系人
    'PassengerDTOs':{
        'url':'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
        'method':'POST',
        'response':'json'
    },
    #查票
    'search-tickets':{
        'url':'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT',
        'method':'GET',
        'response':'json'
    },
    #获取车站信息
    'station_name':{
        'url':'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js',
        'method':'GET',
        'resopnse':'json'
    },
    #checkUser验证用户在线
    'checkUser':{
        'url':'https://kyfw.12306.cn/otn/login/checkUser',
        'method':'POST',
        'response':'json'
    },
    #退出
    'loginOut': {
        'url': 'https://kyfw.12306.cn/otn/login/loginOut',
        'method': 'GET',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/index/initMy12306',
        },
        'response': 'html',
    },
    # submitOrderRequest提交信息
    'submitOrderRequest':{
        'url':'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
        'method':'POST',
        'response':'json',
    },
    #initDc
    'initDc':{
        'url':'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        'method':'POST',
        'response':'html'
    },
    #checkOrderInfo
    'checkOrderInfo':{
        'url':'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
        'method':'POST',
        'response':'json'
    },
    #购票时的验证码
    'CaptureNew':{
        'url':'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&{}',
        'method':'GET',
        'response':'img',
    },
    #getQueueCount 购票队列
    'getQueueCount':{
        'url':'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
        'method':'POST',
        'response':'json',
    },
    #confirmSingleForQueue 单人队列
    'confirmSingleForQueue':{
        'url':'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue',
        'method':'POST',
        'response':'json',
    },
    #wait_time #等待订单生成
    'wait-time':{
        'url':'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}',
        'method':'GET',
        'response':'json',
    },
    #
    'resultOrderForQueue': {
        'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue',
        'method': 'POST',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        },
        'response':'json'
    },
    #
    'queryMyOrderNoComplete': {
        'url': r'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
        'method': 'POST',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/queryOrder/initNoComplete',
        },
        'response':'json'
    }
}