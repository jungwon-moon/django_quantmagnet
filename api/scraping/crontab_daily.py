import json
import requests
from pathlib import Path
from datetime import datetime
from qm.db.connect import postgres_connect
from qm import scraping, utils


headers = {
    "Content-type": "application/json"
}

SECRET_PATH = Path(__file__).resolve().parent.parent.parent
SECRET_FILE = SECRET_PATH / 'config/.config_secret/db.json'
secrets = json.loads(open(SECRET_FILE).read())

for key, value in secrets.items():
    ### postgresql connect
    if key == 'lightsail_db':
        pgdb_properties = value
    ### slack webhook connect
    if key == 'slack_scraping':
        slack_url = value

today = utils.dt2str(datetime.today())


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


### functions
def holiday():

    # 실행일과 거래일이 일치하는지 확인
    global today
    if utils.check_trading_day(today):
        try:
            data = scraping.get_holiday()
            db = postgres_connect(pgdb_properties)

            for row in data:
                date = ''.join(row['calnd_dd'].split('-'))
                value = date, row['dy_tp_cd'], row['kr_dy_tp'], row['holdy_nm']
                db.upsertDB('holiday', value, 'calnd_dd')

            txt = f'Holiday | Success'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'Holiday | * Failed * : {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)


def valiation():
    # 실행일과 거래일이 일치하는지 확인
    global today
    if utils.check_trading_day(today):
        try:
            data = scraping.get_valuation(today)
            db = postgres_connect(pgdb_properties)
            values = []
            for stock in data:
                value = (
                    today,
                    stock['ISU_SRT_CD'], stock['ISU_ABBRV'],
                    replace_zero(stock['EPS']),
                    replace_zero(stock['PER']),
                    replace_zero(stock['BPS']),
                    replace_zero(stock['PBR']),
                    replace_zero(stock['DPS']),
                    replace_zero(stock['DVD_YLD']),
                    calc_roe(stock['EPS'], stock['BPS'])   # ROE 계산
                )
                values.append(value)
            db.multiInsertDB('valiation', values)

            txt = f'Valiation | Success'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'Valiation | * Failed * : {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)


def stock_price():
    # 실행일과 거래일이 일치하는지 확인
    global today
    if utils.check_trading_day(today):
        try:
            data = scraping.get_all_stock_price(today)
            db = postgres_connect(pgdb_properties)

            values = []
            for stock in data:
                if stock['MKT_NM'] != 'KONEX':
                    # 거래량이 0일때 시,고,저가 데이터를 종가로 변경
                    if stock['ACC_TRDVOL'] == '0':
                        value = (
                            today, stock['ISU_SRT_CD'], stock['MKT_NM'],
                            replace_zero(stock['FLUC_RT']),  # 등락률
                            replace_zero(stock['CMPPREVDD_PRC']),  # 대비
                            replace_zero(stock['TDD_CLSPRC']),
                            replace_zero(stock['TDD_CLSPRC']),
                            replace_zero(stock['TDD_CLSPRC']),
                            replace_zero(stock['TDD_CLSPRC']),
                            replace_zero(stock['ACC_TRDVOL']),
                            replace_zero(stock['ACC_TRDVAL']),
                            replace_zero(stock['MKTCAP'])
                        )
                    else:
                        value = (
                            today, stock['ISU_SRT_CD'], stock['MKT_NM'],
                            replace_zero(stock['FLUC_RT']),  # 등락률
                            replace_zero(stock['CMPPREVDD_PRC']),  # 대비
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

            txt = f'Stock_price | Success'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'Stock_price | * Failed * : {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
