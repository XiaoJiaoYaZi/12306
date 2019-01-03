
import random

USER_AGENT = [
    #  Opera
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60 Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    #  Firefox
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    #  Safari
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    #  chrome
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    #  360
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #  淘宝浏览器
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    #  猎豹浏览器
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)" ',
    #  QQ浏览器
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ',
    #  sogou浏览器
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
    #  maxthon浏览器
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    #  UC浏览器
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
]


header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': random.choice(USER_AGENT),
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
        'url':'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT',
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