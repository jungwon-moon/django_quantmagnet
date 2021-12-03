import warnings
import requests
from io import BytesIO
from bs4 import BeautifulSoup as bs
import pandas as pd

# 공통 헤더
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}


def fundamental_df(tdate):
    '''
    '''# 펀더멘탈 excel로 스크래핑
    headers['Referer'] = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'
    req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    parms = {
        'searchType': '1',
        'mktId': 'ALL',
        'trdDd': str(tdate),
        'isuCd': 'KR7005930003',
        'isuCd2': 'KR7005930003',
        'param1isuCd_finder_stkisu0_0': 'ALL',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03501',
}
    r = requests.get(req_url, parms, headers=headers)

    req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
    form_data = {'code': r.content}
    r = requests.get(req_url, form_data, headers=headers)
    with warnings.catch_warnings(record=True):
            warnings.simplefilter('always')
            df = pd.read_excel(BytesIO(r.content), engine='openpyxl')

    return df


def fundamental_json(tdate):
    '''

    '''
    headers['Referer'] = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'
    req_url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    parms = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT03501',
        'searchType': '1',
        'mktId': 'ALL',
        'trdDd': str(tdate),
    }
    r = requests.get(req_url, parms, headers=headers)
    result = r.json()

    return result['output']


def non_trading_days_json(yy=2021):
    '''
    휴장일 데이터를 json으로 반환
    ===========================
    yy: 해당연도
    ----------
    Return

    '''
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    req_url = 'https://open.krx.co.kr/contents/OPN/99/OPN99000001.jspx'
    parms= {
        'search_bas_yy': yy,
        'gridTp': 'KRX',
        'pagePath': '/contents/MKD/01/0110/01100305/MKD01100305.jsp',
        'code': 'JwqlNosVVtCXa7sc5spaVOEA1htzXlH2x9wOa34CWCMdk0SsTxu0w811j9T6paVtRuwRBShCPN9M9smK1s2Tx2DmoC2+E9KJ7ThLD+Z1eepP07eP9j9j8AojpkvULQ07jLt02MKabSy7E7lEbxmTiNaUlYtYKrL1K0TbXUyQoiNSxQv0LKol5HBRIxz26/hr'
    }
    r = requests.get(req_url, parms, headers=headers)

    return r.json()['block1']