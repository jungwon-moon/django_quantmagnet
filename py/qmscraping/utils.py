from pymongo import MongoClient

import datetime


##################################################
# 데이터 베이스 연결
client = MongoClient('localhost', 27017)
db = client.django_test
##################################################


def check_trading_day(cd):
    '''
    ==========input==========
    dd
    ==========Return==========
    False: non trading day
    cd: trading day
    '''
    
    cd = ''.join(str(cd).split('-'))
    # 과거 확인

    # 주말 확인
    if datetime.date(int(cd[:4]), int(cd[4:6]), int(cd[6:])).weekday() > 4:
        return False
    # 공휴일 확인(db)
    if db.non_traing_days.count_documents({'calnd_dd': cd}) > 0:
        return False
    return cd
