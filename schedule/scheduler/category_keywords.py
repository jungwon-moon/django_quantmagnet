import json
import requests
from qm import utils, scraping
from qm.connect import postgres_connect, slack_url, headers


def run():

    time = utils._time

    try:
        data = scraping.category_keywords()
        db = postgres_connect()
        values = []
        for row in data:
            value = (
                time,
                row['CATEGORY_CODE'],
                row['CATEGORY_NAME'],
                row['NAMED_ENTITY'],
                row['NAMED_ENTITY_TYPE'],
                row['NAMED_ENTITY_COUNT'],
            )
            values.append(value)
        db.multiInsertDB('category_keywords', values)
        txt = f'[SUCCESS] Category_Keywords\n실행: SCHEDULER'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'[FAILURE] Category_Keywords\n실행: SCHEDULER\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)
