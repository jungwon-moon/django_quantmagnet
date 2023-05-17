import json
import requests
from qm import utils, scraping
from qm.connect import postgres_connect, slack_url, headers


def run():

    today = utils._today

    if utils.check_trading_day(today):
        try:
            data = scraping.valuation(today)
            db = postgres_connect()
            values = []
            for stock in data:
                value = (
                    today, stock['ISU_SRT_CD'],
                    stock['ISU_ABBRV'],
                    utils.replace_zero(stock['EPS']),
                    utils.replace_zero(stock['PER']),
                    utils.replace_zero(stock['BPS']),
                    utils.replace_zero(stock['PBR']),
                    utils.replace_zero(stock['DPS']),
                    utils.replace_zero(stock['DVD_YLD']),
                    utils.calc_roe(stock['EPS'], stock['BPS'])   # ROE
                )
                values.append(value)
            db.multiInsertDB('valuation', values)

            txt = f'[SUCCESS] Valuation\n실행: SCHEDULER'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'[FAILURE] Valuation\n실행: SCHEDULER\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
