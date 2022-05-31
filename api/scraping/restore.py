import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
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
    if key == 'lightsail_db':
        pgdb_properties = value
    if key == 'slack_scraping':
        slack_url = value

date = utils.dt2str(datetime.today())


### Utils function
def replace_zero(text):
    text = text.replace(',', '')
    if text == '-':
        return None
    return text

def calc_roe(eps, bps):
    eps = replace_zero(eps)
    bps = replace_zero(bps)
    if eps == None or bps == None:
        return None
    return str(round(float(eps) / float(bps) * 100, 2))

def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]
    return dates


### Main function
def stock_price_restore(*dates):
    try:
        for date in dates[0]:
            # 실행일과 거래일이 일치하는지 확인
            if utils.check_trading_day(date):
                data = scraping.get_all_stock_price(date)
                db = postgres_connect(pgdb_properties)
                values = []
                for stock in data:
                    if stock['MKT_NM'] != 'KONEX':
                        value = (
                            date, stock['ISU_SRT_CD'], stock['MKT_NM'],
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

        txt = f'Restore | Stock_price | Success'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Restore | Stock_price | {date} * Failed * : {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def valuation_restore(*dates):
    try:
        for date in dates[0]:
        # 실행일과 거래일이 일치하는지 확인
            if utils.check_trading_day(date):
                data = scraping.get_valuation(date)
                db = postgres_connect(pgdb_properties)
                values = []
                for stock in data:
                    value = (
                        date, stock['ISU_SRT_CD'], 
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

        txt = f'Restore | Valiation | Success '
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Restore | Valiation | {date} * Failed * : {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def holiday_restore(yy=None):
    try:
        data = scraping.get_holiday(yy)
        db = postgres_connect(pgdb_properties)
        values = []
        for row in data:
            date = ''.join(row['calnd_dd'].split('-'))
            value = date, row['dy_tp_cd'], row['kr_dy_tp'], row['holdy_nm']
            values.append(value)
        db.multiInsertDB('holiday', values)
        
        txt = f'Restore | Holiday | Success: {yy}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Restore | Holiday | * Failed * : {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)



### Run
# holiday_restore('2022')
dates = date_range('20220101', '20220530')
# stock_price_restore(dates)
# valuation_restore(dates)
