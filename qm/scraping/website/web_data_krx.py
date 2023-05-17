import requests
from qm import utils


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def get_valuation(dt=None):

    if dt == None:
        dt = utils._today

    headers['Referer'] = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'
    req_url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    params = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT03501',
        'searchType': '1',
        'mktId': 'ALL',
        'trdDd': str(dt),
    }
    r = requests.get(req_url, params=params, headers=headers)

    return r


def get_stock_price(dt=None):
    if dt == None:
        dt = utils._today

    headers['Origin'] = 'http://data.krx.co.kr'
    headers['Referer'] = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'
    req_url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    params = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'trdDd': dt,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }
    r = requests.get(req_url, params=params, headers=headers)
    return r


def get_stock_index(indIdx="1", dt=None):
    '''
    지수-주가지수-개별지수 시세추이
    indIdx : 1=kospi, 2=kosdaq
    strtDd : 특정일
    endDd : 특정일
    '''
    if dt == None:
        dt = utils._today

    headers['Referer'] = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'
    headers['Origin'] = 'http://data.krx.co.kr'
    req_url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    params = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00301',
        'locale': 'ko_KR',
        'indIdx': indIdx,
        'indIdx2': '001',
        'strtDd': dt,
        'endDd': dt,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }
    r = requests.get(req_url, params=params, headers=headers)
    return r
