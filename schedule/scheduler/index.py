import json
import requests
from qm import scraping, utils
from qm.connect import postgres_connect, slack_url, headers


def kospi():

    today = utils._today

    if utils.check_trading_day(today):
        try:
            data = scraping.kospi(today)
            db = postgres_connect()

            value = (
                today, '코스피', 'KOSPI',
                utils.replace_zero(data['UPDN_RATE']),    # 등락률
                utils.replace_zero(data['PRV_DD_CMPR']),  # 대비
                utils.replace_zero(data['OPNPRC_IDX']),   # 시가
                utils.replace_zero(data['HGPRC_IDX']),    # 고가
                utils.replace_zero(data['LWPRC_IDX']),    # 저가
                utils.replace_zero(data['CLSPRC_IDX']),   # 종가
                utils.replace_zero(data['ACC_TRDVOL']),   # 거래량
                utils.replace_zero(data['ACC_TRDVAL']),    # 거래대금
            )
            db.insertDB('index_', value)

            txt = f'[SUCCESS] INDEX_KOSPI\n실행: SCHEDULER'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'[FAILURE] INDEX_KOSPI\n실행: SCHEDULER\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)


def kosdaq():

    today = utils._today

    if utils.check_trading_day(today):
        try:
            data = scraping.kosdaq(today)
            db = postgres_connect()

            value = (
                today, '코스닥', 'KOSDAQ',
                utils.replace_zero(data['UPDN_RATE']),    # 등락률
                utils.replace_zero(data['PRV_DD_CMPR']),  # 대비
                utils.replace_zero(data['OPNPRC_IDX']),   # 시가
                utils.replace_zero(data['HGPRC_IDX']),    # 고가
                utils.replace_zero(data['LWPRC_IDX']),    # 저가
                utils.replace_zero(data['CLSPRC_IDX']),   # 종가
                utils.replace_zero(data['ACC_TRDVOL']),   # 거래량
                utils.replace_zero(data['ACC_TRDVAL']),    # 거래대금
            )
            db.insertDB('index_', value)

            txt = f'[SUCCESS] INDEX_KOSDAQ\n실행: SCHEDULER'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'[FAILURE] INDEX_KOSDAQ\n실행: SCHEDULER\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
