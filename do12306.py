from train.login.Login import Login
from train.submit.Submit import Submit
from train.query.query import Query
from configparser import ConfigParser
from train.Content import *


config = ConfigParser()
config.read('config.ini','utf-8')

login = Login()
login.Login(config['config']['usr'], config['config']['pwd'])


while True:
    try:
        print('*'*40)
        ticket = Query.loopQuery(config['config']['startStation'], config['config']['endStattion'], config['config']['time'],
                                 config['config']['seatType'].split(','), config['config']['train'].split(','), 5)
        print('已查询到余票：%s'%ticket)

        submit = Submit(ticket, config['config']['passenger'].split(','))
        if submit.submit():
            submit.showSubmitInfoPretty()
            break

    except Exception as e:
        print(e)