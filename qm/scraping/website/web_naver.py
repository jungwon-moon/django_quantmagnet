import requests
from qm import utils


today = utils._today


def get_adjusted_stock_price(stcd):
    url = f"https://api.finance.naver.com/siseJson.naver?symbol={stcd}&requestType=1&startTime=20150101&endTime={today}&timeframe=day"
    r = requests.get(url)
    return r
