from qm.scraping.website import web_bigkind, web_data_krx, web_krx, web_bok, web_naver


def holiday(dt=None):
    return web_krx.get_holiday(dt).json()["block1"]


def kr_base_rate():
    return web_bok.get_kr_base_rate()


def valuation(dt=None):
    return web_data_krx.get_valuation(dt).json()['output']


def stock_price(dt=None):
    return web_data_krx.get_stock_price(dt).json()['OutBlock_1']


def kospi(dt=None):
    return web_data_krx.get_stock_index(indIdx="1", dt=dt).json()['output'][0]


def kosdaq(dt=None):
    return web_data_krx.get_stock_index(indIdx="2", dt=dt).json()['output'][0]


def category_keywords():
    return web_bigkind.get_category_keywords().json()['categoryKeyword']


def industry_classification(indIdx, dt=None):
    return web_data_krx.get_industry_classification(indIdx=indIdx, dt=dt).json()['block1']


def adjusted_stock_price(stcd):
    data = web_naver.get_adjusted_stock_price(stcd)
    data = data.text.split(',\n\t\t\n')[1:-1]
    data = list(map(eval, data))
    return data
