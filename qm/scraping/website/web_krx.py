import requests
from qm import utils
from datetime import datetime


now = datetime.now()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def get_holiday(yy=None):
    if yy == None:
        yy = utils.dt2str(now)[:4]

    req_url = 'https://open.krx.co.kr/contents/OPN/99/OPN99000001.jspx'
    params = {
        'search_bas_yy': yy,
        'gridTp': 'KRX',
        'pagePath': '/contents/MKD/01/0110/01100305/MKD01100305.jsp',
        'code': 'JwqlNosVVtCXa7sc5spaVOEA1htzXlH2x9wOa34CWCMdk0SsTxu0w811j9T6paVtRuwRBShCPN9M9smK1s2Tx2DmoC2+E9KJ7ThLD+Z1eepP07eP9j9j8AojpkvULQ07jLt02MKabSy7E7lEbxmTiNaUlYtYKrL1K0TbXUyQoiNSxQv0LKol5HBRIxz26/hr'
    }
    r = requests.get(req_url, params=params, headers=headers)

    return r
