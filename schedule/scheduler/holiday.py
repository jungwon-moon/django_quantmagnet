import json
import requests
from qm import utils, scraping
from qm.connect import postgres_connect, slack_url, headers


def run():

    today = utils._today

    if utils.check_trading_day(today):
        try:
            data = scraping.holiday()
            db = postgres_connect()

            for row in data:
                date = ''.join(row['calnd_dd'].split('-'))
                value = date, row['dy_tp_cd'], row['kr_dy_tp'], row['holdy_nm']
                db.upsertDB('holiday', value, 'calnd_dd')

            txt = f'[SUCCESS] Holiday\n실행: SCHEDULER'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'[FAILURE] Holiday\n실행: SCHEDULER\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
