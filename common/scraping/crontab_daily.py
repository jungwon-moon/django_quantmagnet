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

today = utils.dt2str(datetime.today())


def rep_0(text):
    text = text.replace(',', '')
    if text == '-':
        return None
    return text


### functions
def holiday():

    # 실행일과 거래일이 일치하는지 확인
    global today
    adj_date = utils.check_trading_day(today)
    if adj_date == today:
        try:
            data = scraping.get_holiday()
            db = postgres_connect(pgdb_properties)

            for row in data:
                date = ''.join(row['calnd_dd'].split('-'))
                value = date, row['dy_tp_cd'], row['kr_dy_tp'], row['holdy_nm']
                db.upsertDB('holiday', value, 'calnd_dd')

            txt = f'| holiday | Run'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'| holiday | * Error * : {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)


def fundamental_v1():
    # 실행일과 거래일이 일치하는지 확인
    global today
    adj_date = utils.check_trading_day(today)
    if adj_date == today:
        try:
            data = scraping.get_fundamentalv1()
            db = postgres_connect(pgdb_properties)
            values = []
            for stock in data:
                value = (
                    adj_date, stock['ISU_SRT_CD'], stock['ISU_ABBRV'],
                    rep_0(stock['EPS']), rep_0(stock['PER']),
                    rep_0(stock['BPS']), rep_0(stock['PBR']),
                    rep_0(stock['DPS']), rep_0(stock['DVD_YLD']),
                    rep_0(round((stock['EPS']/stock['BPS'])*100))   # ROE 계산
                    )
                values.append(value)
            db.multiInsertDB('fundamental_v1', values)
            txt = f'| fundamental_v1 | Run'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'| fundamental_v1 | * Error * : {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)


def stock_price():
    # 실행일과 거래일이 일치하는지 확인
    global today
    adj_date = utils.check_trading_day(today)
    if adj_date == today:
        try:
            data = scraping.get_all_stock_price()
            db = postgres_connect(pgdb_properties)

            values = []
            for stock in data:
                if stock['MKT_NM'] != 'KONEX':
                    value = (adj_date, stock['ISU_SRT_CD'], stock['MKT_NM'],
                        rep_0(stock['FLUC_RT']), rep_0(stock['TDD_OPNPRC']),
                        rep_0(stock['TDD_HGPRC']), rep_0(stock['TDD_LWPRC']),
                        rep_0(stock['TDD_CLSPRC']), rep_0(stock['ACC_TRDVOL']),
                        rep_0(stock['ACC_TRDVAL']), rep_0(stock['MKTCAP']))
                    values.append(value)
            db.multiInsertDB('stock_price', values)

            txt = f'| stock_price | Run'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'| stock_price | * Error * : {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
