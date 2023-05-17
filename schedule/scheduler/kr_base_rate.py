import json
import requests
from qm import scraping
from qm.connect import postgres_connect, slack_url, headers


def run():
    try:
        datas = scraping.kr_base_rate()
        db = postgres_connect()
        for data in datas:
            db.upsertDB("kr_base_rate", tuple(data), "date")

        txt = f'[SUCCESS] Base_rate\n실행: SCHEDULER'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'[FAILURE] Base_rate\n실행: SCHEDULER\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)
