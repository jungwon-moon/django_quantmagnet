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
                value = (adj_date, stock['ISU_SRT_CD'], stock['ISU_ABBRV'],\
                    stock['EPS'], stock['PER'], stock['BPS'],\
                    stock['PBR'], stock['DPS'], stock['DVD_YLD'])
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
                    value = (adj_date, stock['ISU_SRT_CD'],\
                        stock['MKT_NM'], stock['FLUC_RT'],\
                        stock['TDD_OPNPRC'], stock['TDD_HGPRC'],\
                        stock['TDD_LWPRC'], stock['TDD_CLSPRC'],\
                        stock['ACC_TRDVOL'], stock['ACC_TRDVAL'],\
                        stock['MKTCAP'])
                    values.append(value)
            db.multiInsertDB('stock_price', values)

            txt = f'| stock_price | Run'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'| stock_price | * Error * : {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
