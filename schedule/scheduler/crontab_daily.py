import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
from qm.db.connect import postgres_connect
from qm import scraping, utils
from qm.db.query.strategy_query import *
from qm.db.query.crontab_daily_query import *


headers = {
    "Content-type": "application/json"
}

SECRET_PATH = Path(__file__).resolve().parent.parent.parent
SECRET_FILE = SECRET_PATH / 'config/.config_secret/db.json'
secrets = json.loads(open(SECRET_FILE).read())

for key, value in secrets.items():
    # postgresql connect
    if key == 'lightsail_db':
        pgdb_properties = value
    # slack webhook connect
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


# functions
def holiday():
    # 실행일과 거래일이 일치하는지 확인
    if utils.check_trading_day(today):
        try:
            data = scraping.get_holiday()
            db = postgres_connect(pgdb_properties)

            for row in data:
                date = ''.join(row['calnd_dd'].split('-'))
                value = date, row['dy_tp_cd'], row['kr_dy_tp'], row['holdy_nm']
                db.upsertDB('holiday', value, 'calnd_dd')

            txt = f'Holiday\n실행: SCHEDULER\n실행일: {today}\n상태: SUCCESS'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'Holiday\n실행: SCHEDULER\n실행일: {today}\n상태: ※ FAILURE ※\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)


def kr_base_rate_restore():
    try:
        values = scraping.get_kr_base_rate()
        db = postgres_connect(pgdb_properties)
        for value in values:
            db.upsertDB('kr_base_rate', tuple(value), 'date')

        txt = f'Base_rate\n실행: SCHEDULER\n실행일: {today}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Base_rate\n실행: SCHEDULER\n실행일: {today}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def valuation():
    # 실행일과 거래일이 일치하는지 확인
    if utils.check_trading_day(today):
        try:
            data = scraping.get_valuation(today)
            db = postgres_connect(pgdb_properties)
            values = []
            for stock in data:
                value = (
                    today, stock['ISU_SRT_CD'],
                    stock['ISU_ABBRV'],
                    replace_zero(stock['EPS']),
                    replace_zero(stock['PER']),
                    replace_zero(stock['BPS']),
                    replace_zero(stock['PBR']),
                    replace_zero(stock['DPS']),
                    replace_zero(stock['DVD_YLD']),
                    calc_roe(stock['EPS'], stock['BPS'])   # ROE
                )
                values.append(value)
            db.multiInsertDB('valuation', values)

            txt = f'Valuation\n실행: SCHEDULER\n실행일: {today}\n상태: SUCCESS'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'Valuation\n실행: SCHEDULER\n실행일: {today}\n상태: ※ FAILURE ※\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)


def stock_price():
    # 실행일과 거래일이 일치하는지 확인
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

            txt = f'Stock_price\n실행: SCHEDULER\n실행일: {today}\n상태: SUCCESS'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'Stock_price\n실행: SCHEDULER\n실행일: {today}\n상태: ※ FAILURE ※\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
    else:
        return False


def disparity():
    start = utils.dt2str(utils.str2dt(today) - timedelta(days=100))
    data = {}
    try:
        db = postgres_connect(pgdb_properties)
        values = []
        rows = db.readDB(table='stock_price',
                         columns='*',
                         where=f"date between '{start}' and '{today}'",
                         orderby='stcd, date')
        # data 데이터 생성
        # '000020': [[date1, ..., ...], [date2, ..., ...], ...]
        # '000040': [[date1, ..., ...], [date2, ..., ...], ...]
        # ...
        for row in rows:
            if data.get(row[1]):
                data[row[1]].append(row)
            else:
                data[row[1]] = [row]

        for _, v in data.items():
            # _: '000020', ...
            # v: [[date1, ..., ...], [date2, ..., ...], ...]
            df = pd.DataFrame(v)
            df.columns = ['date', 'stcd', 'market', 'rate', 'prevd',
                          'open', 'high', 'low', 'close', 'volume', 'values', 'capital']
            df['ma10'] = df['close'].rolling(10).mean().round(1)
            df['ma20'] = df['close'].rolling(20).mean().round(1)
            df['ma60'] = df['close'].rolling(60).mean().round(1)
            df['dp10'] = ((df['close'] / df['ma10']) * 100).round(1)
            df['dp20'] = ((df['close'] / df['ma20']) * 100).round(1)
            df['dp60'] = ((df['close'] / df['ma60']) * 100).round(1)
            value = tuple(
                df.iloc[[-1], [0, 1, 12, 13, 14, 15, 16, 17]].values.tolist()[0])
            if today == value[0]:
                values.append(value)

        run = db.multiInsertDB('disparity', values)
        if run[0] == False:
            raise Exception(run[1])

        txt = f'Disparity\n실행: SCHEDULER\n실행일: {today}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Disparity\n실행: SCHEDULER\n실행일: {today}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def update_stock_code():
    query_model = Update_stock_code()
    query_model.date = today
    query_model.update_code()


def run_flows():
    # 주가 정보 수집(stock_price) ->
    # 종목 코드 업데이트(update_stock_code) ->
    # 이격도 계산(disparity)
    if stock_price() != False:
        update_stock_code()
        disparity()


def strategy_per_return():
    if utils.check_trading_day(today):
        try:
            model = Per_return()
            model.date = today
            name = 'valuation_per'
            ret_3m, ret_6m, ret_1y, \
                ret_an, ret_cum, period = model.returns()
            stddev, cagr, sharp = model.stddev_cagr_sharp()
            mdd = model.mdd()
            values = (name, today, ret_3m, ret_6m, ret_1y,
                      ret_an, ret_cum, stddev, mdd, 
                      cagr, sharp, period)
            model.db.insertDB('valuation_returns', values)

            txt = f'strategy_per_return\n실행: SCHEDULER\n복원일: {today}\n상태: SUCCESS'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'strategy_per_return\n실행: SCHEDULER\n복원일: {today}\n상태: ※ FAILURE ※\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)


def valuation_returns():
    strategy_per_return()
