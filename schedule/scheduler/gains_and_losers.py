import json
import requests
from qm import utils
from qm.db.query.query_gains_and_losers import Gains_and_losers
from qm.connect import postgres_connect, slack_url, headers


def run():
    # 급등주 및 급락주
    today = utils._today
    limit = 50

    if utils.check_trading_day(today):
        try:
            db = postgres_connect()
            query = Gains_and_losers().query
            db.cursor.execute(query)
            data = db.cursor.fetchall()
            gains = list(map(lambda x: tuple(x), data[:limit]))
            losers = list(map(lambda x: tuple(x), data[-limit:]))
            db.multiInsertDB('cache_gains_and_losers', gains)
            db.multiInsertDB('cache_gains_and_losers', losers)

            txt = f'[SUCC] gains_and_losers\n실행: SCHEDULER'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'[FAIL] gains_and_losers\n실행: SCHEDULER\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
    else:
        return False
