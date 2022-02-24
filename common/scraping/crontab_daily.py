import os
from pathlib import Path
import json
import requests
from qm.db.connect import POSTGRESCRUD
from qm import scraping


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


### functions
def non_traiding_days():
    '''
    휴장일 갱신을 위해 매일 update 수행
    '''
    try:
        data = scraping.get_non_trading_days(Type='db')
        db = POSTGRESCRUD(pgdb_properties)

        for row in data:
            date = ''.join(row['calnd_dd'].split('-'))
            value = date, row['dy_tp_cd'], row['kr_dy_tp'], row['holdy_nm']

            db.insertDB('non_trading_days', '', value)

        txt = f'| non_traiding_days | Run'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'| non_traiding_days | * Error * : {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def fundamental_v1():
    try:
        data = scraping.get_fundamental(Type='db')
        # mongodb = db.connect.mongodb_connect(host).kr

        for stock in data:
            doc = {
                'STCD': stock['ISU_SRT_CD'],
                'STNM': stock['ISU_ABBRV'],
                'EPS': stock['EPS'],
                'PER': stock['PER'],
                'FWD_EPS': stock['FWD_EPS'],
                'FWD_PER': stock['FWD_PER'],
                'BPS': stock['BPS'],
                'PBR': stock['PBR'],
                'DPS': stock['DPS'],
                'DVD_YLD': stock['DVD_YLD']
            }
            # mongodb.stock_fundamental.insert_one(doc)

        txt = f'Run: fundamental_v1'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except:
        txt = f'*** ERROR ***: fundamental_v1'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)
