from net.MyNet import MyNets
from adress.Urls import Urls
from train.login.Capthca import Capture



RESULT_OK = 0

def LoginLogic(func):
    def wrapper(*args,**kwargs):
        response = func(*args,**kwargs)
        print(response)
        if response['result_code'] == RESULT_OK:
            return True
        else:
            return False
    return wrapper



class Login(object):
    def _checkusr(self):
        pass

    @LoginLogic
    def __login(self, usrname, password):
        urlInfo = Urls['login']
        data = {
            'username': usrname,
            'password': password,
            'appid': 'otn',
            '_json_att': "",
        }
        response = MyNets.send(urlInfo=urlInfo, data=data)
        if 'uamtk' in response.keys():
            self.uamtk = response['uamtk']
        return response

    @LoginLogic
    def __uamtk(self):
        urlInfo = Urls['uamtk']
        data = {
            "appid": "otn",
            '_json_att': ""
        }
        response = MyNets.send(urlInfo=urlInfo, data=data)
        if 'newapptk' in response.keys():
            self.tk = response["newapptk"]
        return response

    @LoginLogic
    def __uamauthclient(self):
        urlInfo =Urls['uamauthclient']
        data = {
            "tk": self.tk,
            '_json_att': "",
        }
        return MyNets.send(urlInfo=urlInfo, data=data)

    def Login(self,usrname,password):
        print('正在登陆...')
        if not Capture().QueryManual():
            return False
        if not self.__login(usrname,password) or\
            not self.__uamtk() or \
            not self.__uamauthclient():
            return False
        print('登陆成功')
        return True
    def _init(self):
        MyNets.send(Urls['init'])
    def LogOut(self):
        #urlInfo = Urls['loginOut']
        MyNets.send(Urls['loginOut'])
        self._init()
        return self.__uamtk()



if __name__ == '__main__':
    login = Login()
    login.Login('lqd5906313','Lqd5906313')
    a = login.LogOut()
    print(a)