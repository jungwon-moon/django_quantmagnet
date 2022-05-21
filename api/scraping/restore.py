import json
import requests
from pathlib import Path
from datetime import datetime
from qm.db.connect import postgres_connect
from qm import scraping, utils


### slack webhook connect
headers = {
    "Content-type": "application/json"
}

### postgresql connect
SECRET_PATH = Path(__file__).resolve().parent.parent.parent
SECRET_FILE = SECRET_PATH / 'config/.config_secret/db.json'
secrets = json.loads(open(SECRET_FILE).read())

for key, value in secrets.items():
    if key == 'gcp':
        pgdb_properties = value
    if key == 'slack_scraping':
        slack_url = value

date = utils.dt2str(datetime.today())


def replace_zero(text):
    text = text.replace(',', '')
    if text == '-':
        return None
    return text


def stock_price_restore(date=date):
    adj_date = utils.check_trading_day(date)
    # print('date:', date)
    # print('adj_date:', adj_date)
    if adj_date == date:
        data = scraping.get_all_stock_price(adj_date)
        db = postgres_connect(pgdb_properties)
        values = []
        for stock in data:
            if stock['MKT_NM'] != 'KONEX':
                value = (
                    adj_date, stock['ISU_SRT_CD'], stock['MKT_NM'],
                    replace_zero(stock['FLUC_RT']), # 등락률
                    replace_zero(stock['CMPPREVDD_PRC']), # 대비
                    replace_zero(stock['TDD_OPNPRC']),
                    replace_zero(stock['TDD_HGPRC']), 
                    replace_zero(stock['TDD_LWPRC']),
                    replace_zero(stock['TDD_CLSPRC']), 
                    replace_zero(stock['ACC_TRDVOL']),
                    replace_zero(stock['ACC_TRDVAL']), 
                    replace_zero(stock['MKTCAP'])
                    )
                values.append(value)
        db.multiInsertDB('stock_price', values)


def calc_roe(eps, bps):
    eps = replace_zero(eps)
    bps = replace_zero(bps)
    if eps == None or bps == None:
        return None
    return str(round(float(eps) / float(bps) * 100, 2))


def valuation_restore(date=date):
    # 실행일과 거래일이 일치하는지 확인
    adj_date = utils.check_trading_day(date)
    # print('date:', date)
    # print('adj_date:', adj_date)
    if adj_date == date:
        data = scraping.get_fundamentalv1(adj_date)
        db = postgres_connect(pgdb_properties)
        values = []
        for stock in data:
            value = (
                adj_date, stock['ISU_SRT_CD'], 
                stock['ISU_ABBRV'],
                replace_zero(stock['EPS']), 
                replace_zero(stock['PER']),
                replace_zero(stock['BPS']), 
                replace_zero(stock['PBR']),
                replace_zero(stock['DPS']), 
                replace_zero(stock['DVD_YLD']),
                calc_roe(stock['EPS'], stock['BPS'])   # ROE
                )
            values.append(value)
        db.multiInsertDB('valuation', values)


def holiday_restore():
    data = scraping.get_holiday(yy)
    db = postgres_connect(pgdb_properties)
    values = []
    for row in data:
        date = ''.join(row['calnd_dd'].split('-'))
        value = date, row['dy_tp_cd'], row['kr_dy_tp'], row['holdy_nm']
        values.append(value)
    db.multiInsertDB('holiday', values)


date = '20220331'
yy = '2021'

st = datetime.today()

stock_price_restore('20220520')
# valuation_restore('20220520')

# for yy in range(2000, 2021):
# print(yy)
# holiday_restore()


ed = datetime.today()
print(ed-st)
