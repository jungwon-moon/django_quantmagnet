import json
import requests
from qm import utils, scraping
from qm.connect import postgres_connect, slack_url, headers


today = utils._today


def run():
    if utils.check_trading_day(today):
        try:

            kospi = scraping.industry_classification(1)
            kosdaq = scraping.industry_classification(2)
            data = kospi + kosdaq
            db = postgres_connect()

            for row in data:
                value = (
                    row["ISU_SRT_CD"],      # 종목 코드
                    row["IDX_IND_NM"],      # 업종 구분
                )
                db.upsertDB("industry", value, "stcd")

            txt = f'[SUCCESS] Industry_classification\n실행: SCHEDULER'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'[FAILURE] Industry_classification\n실행: SCHEDULER\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
