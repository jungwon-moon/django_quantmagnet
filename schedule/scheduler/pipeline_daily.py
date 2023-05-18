import json
import requests
import pandas as pd
from datetime import timedelta
from qm import utils, scraping
from qm.db.query.query_pipeline_daily import Update_stock_list
from qm.connect import postgres_connect, slack_url, headers


today = utils._today


def stock_price():
    # 실행일과 거래일이 일치하는지 확인
    if utils.check_trading_day(today):
        try:
            data = scraping.stock_price(today)
            db = postgres_connect()

            values = []
            for stock in data:
                if stock['MKT_NM'] != 'KONEX':
                    # 거래량이 0일때 시,고,저가 데이터를 종가로 변경
                    if stock['ACC_TRDVOL'] == '0':
                        value = (
                            today, stock['ISU_SRT_CD'], stock['MKT_NM'],
                            utils.replace_zero(stock['FLUC_RT']),  # 등락률
                            utils.replace_zero(stock['CMPPREVDD_PRC']),  # 대비
                            utils.replace_zero(stock['TDD_CLSPRC']),
                            utils.replace_zero(stock['TDD_CLSPRC']),
                            utils.replace_zero(stock['TDD_CLSPRC']),
                            utils.replace_zero(stock['TDD_CLSPRC']),
                            utils.replace_zero(stock['ACC_TRDVOL']),
                            utils.replace_zero(stock['ACC_TRDVAL']),
                            utils.replace_zero(stock['MKTCAP'])
                        )
                    else:
                        value = (
                            today, stock['ISU_SRT_CD'], stock['MKT_NM'],
                            utils.replace_zero(stock['FLUC_RT']),  # 등락률
                            utils.replace_zero(stock['CMPPREVDD_PRC']),  # 대비
                            utils.replace_zero(stock['TDD_OPNPRC']),
                            utils.replace_zero(stock['TDD_HGPRC']),
                            utils.replace_zero(stock['TDD_LWPRC']),
                            utils.replace_zero(stock['TDD_CLSPRC']),
                            utils.replace_zero(stock['ACC_TRDVOL']),
                            utils.replace_zero(stock['ACC_TRDVAL']),
                            utils.replace_zero(stock['MKTCAP'])
                        )
                    values.append(value)
            db.multiInsertDB('stock_price', values)

            txt = f'[SUCCESS] Stock_price\n실행: SCHEDULER'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'[FAILURE] Stock_price\n실행: SCHEDULER\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
    else:
        return False


def disparity():
    start = utils.dt2str(utils.str2dt(today) - timedelta(days=100))
    data = {}
    try:
        db = postgres_connect()
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

        txt = f'[SUCCESS] Disparity\n실행: SCHEDULER'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'[SUCCESS] Disparity\n실행: SCHEDULER\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

import os
from pathlib import Path

def update_stock_list():
    """
    종목 검색에 사용되는 종목 코드
    """
    try:
        db = postgres_connect()
        query = Update_stock_list(today).query
        db.cursor.execute(query)

        url = "https://quantmag.net/api/searchstock/?format=json&limit=4000"
        data = requests.get(url).json()['results']
        file_path = "store/json/stockList.json"
        base_path = Path(__file__).resolve().parent.parent.parent
        path = base_path / file_path
        
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent="\t", ensure_ascii=False)

        txt = f'[SUCCESS] Update_Stock_List\n실행: SCHEDULER'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'[SUCCESS] Update_Stock_List\n실행: SCHEDULER\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def run():
    # 주가 정보(stock_price)
    # if stock_price() is not False:
        # 종목 코드 업데이트
    update_stock_list()
        # 이격도(disparity)
        # disparity()   
