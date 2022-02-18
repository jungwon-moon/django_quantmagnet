import os
from pathlib import Path
import json
import requests
from qm import db, scraping

### slack webhook connect
slack_url = 'https://hooks.slack.com/services/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'
headers = {
    "Content-type": "application/json"
}

### mongodb connect
SECRET_PATH = Path(__file__).resolve().parent.parent.parent
SECRET_FILE = SECRET_PATH / 'config/.config_secret/db.json'

secrets = json.loads(open(SECRET_FILE).read())
for key, value in secrets.items():
    if key == 'host':
        host = value

### functions
def non_traiding_days():
    '''
    휴장일 갱신을 위해 매일 update 수행
    '''
    try:
        data = scraping.get_non_trading_days()
        mongodb = db.connect.mongodb_connect(host).qmdb
        for row in data:
            doc = {
                'calnd_dd': ''.join(row['calnd_dd'].split('-')),
                'dy_tp_cd': row['dy_tp_cd'],
                'kr_dy_tp': row['kr_dy_tp'],
                'holdy_nm': row['holdy_nm'],
            }
            mongodb.non_trading_days.update_one(doc, {"$set": doc}, upsert=True)

        txt = f'Run: non_traiding_days'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except:
        txt = f'*** ERROR ***: non_traiding_days'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)
