import warnings
import requests
from io import BytesIO

import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
}


def fundamental_excel(tdate):
    req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    query_str_parms = {
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
    r = requests.get(req_url, query_str_parms, headers=headers)

    req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
    form_data = {'code': r.content}
    r = requests.get(req_url, form_data, headers=headers)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter('always')
        df = pd.read_excel(BytesIO(r.content), engine='openpyxl')
    
    return df


def fundamental_get_json(tdate):
    req_url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    query_str_parms = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT03501',
        'searchType': '1',
        'mktId': 'ALL',
        'trdDd': str(tdate),
    }
    r = requests.get(req_url, query_str_parms, headers=headers)
    result = r.json()

    return result['output']