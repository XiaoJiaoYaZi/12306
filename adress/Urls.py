
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
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    #  chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    #  360
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #  淘宝浏览器
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    #  猎豹浏览器
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
    #  QQ浏览器
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    #  sogou浏览器
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
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
            'User-Agent': USER_AGENT[6],
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
        }

Urls = {
    'checkLogin':{
        'url':'https://exservice.12306.cn/excater/login/checkLogin',
        'method':'POST',
        'response':'json',
    },
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
    'capture2':{
        'url' : 'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&{}',
        'method' : 'GET',
        'response' : 'json',
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
        'url': 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue',
        'method': 'POST',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        },
        'response':'json'
    },
    #
    'queryMyOrderNoComplete': {
        'url': 'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
        'method': 'POST',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/view/train_order.html',
        },
        'response':'json'
    }
}

if __name__ == '__main__':
    import base64
    s = '/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a HBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIy MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAC+ASUDASIA AhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA AAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3 ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm p6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA AwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx BhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK U1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3 uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+ivP NS1bUJdPlW2XWIJZ550EExgZ4mwMplZDkA5IIJwGA7Vd8P63d2Wi39zqC3k32C3VmR9gYkKSQPmJ yeMZxQB21FcPqV14igvb/Vfs2qWlklsh8qKS1fGzeWbDk9iOnpU+r6tqVsohtdYij2W48w3GiT3D uxGdweJ0QcEcAcEHnsADsaK4Xwrq2p3un6fBd6zHIk1oqjydGuIpQxQYbzndkyPUrg0zXZdR0fxL pVqmq65c2k9rdTTpbpC8i+W0IDAbMkASNkAEnjAoA72iuH1C6iNlpk1tr11d2lxcPula7WDpE+FL oF24YDIIyCMYzxXKXOoapB4f1W4k1PUY5LfT7qaOctcxqZlVygjJkZWA25ywGRt4OTgA9jorh/Ee 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 FngvGb4A/9kKCg=='
    bs = base64.b64decode(s)
    print(bs)
    from io import BytesIO
    from PIL import Image
    image = Image.open(BytesIO(bs))
    image.show()