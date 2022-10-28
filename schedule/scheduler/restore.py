import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
from qm.db.connect import postgres_connect
from qm import scraping, utils


headers = {
    "Content-type": "application/json"
}

SECRET_PATH = Path(__file__).resolve().parent.parent.parent
SECRET_FILE = SECRET_PATH / 'config/.config_secret/db.json'
secrets = json.loads(open(SECRET_FILE).read())

for key, value in secrets.items():
    ### postgresql connect
    if key == 'lightsail_db':
        pgdb_properties = value
    ### slack webhook connect
    if key == 'slack_scraping':
        slack_url = value

time = utils.dt2str(datetime.today(), 'time')
date = utils.dt2str(datetime.today())


### Utils function
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


def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d")
             for i in range((end-start).days+1)]
    return dates


### Main function
def stock_price_restore(*dates):
    try:
        for date in dates[0]:
            # 실행일과 거래일이 일치하는지 확인
            if utils.check_trading_day(date):
                data = scraping.get_all_stock_price(date)
                db = postgres_connect(pgdb_properties)
                values = []
                for stock in data:
                    if stock['MKT_NM'] != 'KONEX':
                        # 거래량이 0일때 시,고,저가 데이터를 종가로 변경
                        if stock['ACC_TRDVOL'] == '0':
                            value = (
                                date, stock['ISU_SRT_CD'], stock['MKT_NM'],
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
                                date, stock['ISU_SRT_CD'], stock['MKT_NM'],
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

                run = db.multiInsertDB('stock_price', values)
                if run[0] == False:
                    raise Exception(run[1])

        txt = f'Stock_price\n실행: RESTORE\n복원일: {date}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Stock_price\n실행: RESTORE\n복원일: {date}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def valuation_restore(*dates):
    try:
        for date in dates[0]:
            # 실행일과 거래일이 일치하는지 확인
            if utils.check_trading_day(date):
                data = scraping.get_valuation(date)
                db = postgres_connect(pgdb_properties)
                values = []
                for stock in data:
                    value = (
                        date, stock['ISU_SRT_CD'],
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

                run = db.multiInsertDB('valuation', values)
                if run[0] == False:
                    raise Exception(run[1])

        txt = f'Valiation\n실행: RESTORE\n복원일: {date}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Valiation\n실행: RESTORE\n복원일: {date}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def holiday_restore(yy=None):
    try:
        data = scraping.get_holiday(yy)
        db = postgres_connect(pgdb_properties)
        values = []
        for row in data:
            date = ''.join(row['calnd_dd'].split('-'))
            value = date, row['dy_tp_cd'], row['kr_dy_tp'], row['holdy_nm']
            values.append(value)

        run = db.multiInsertDB('holiday', values)
        if run[0] == False:
            raise Exception(run[1])

        txt = f'Holiday\n실행: RESTORE\n복원일: {yy}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Holiday\n실행: RESTORE\n복원일: {yy}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def category_keywords_restore(time):
    try:
        data = scraping.get_category_keywords()['categoryKeyword']
        db = postgres_connect(pgdb_properties)
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

        run = db.multiInsertDB('category_keywords', values)
        if run[0] == False:
            raise Exception(run[1])

        txt = f'Category_keyword\n실행: RESTORE\n복원일: {time}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Category_keyword\n실행: RESTORE\n복원일: {time}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def disparity_restore(date):
    """
    이격도(disparity) 함수입니다.\n
    stock_price가 수집되는 16시 이후 최신 데이터를 계산할 수 있습니다.\n
        Args:
            date(str): 분석 기준일 `20220101`
    """
    start = utils.dt2str(utils.str2dt(date) - timedelta(days=100))
    data = {}
    try:
        db = postgres_connect(pgdb_properties)
        values = []
        rows = db.readDB(table='stock_price',
                         columns='*',
                         where=f"date between '{start}' and '{date}'",
                         orderby='stcd, date')
        ### data 데이터 생성
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
            if date == value[0]:
                values.append(value)

        run = db.multiInsertDB('disparity', values)
        if run[0] == False:
            raise Exception(run[1])

        txt = f'disparity\n실행: RESTORE\n복원일: {date}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'disparity\n실행: RESTORE\n복원일: {date}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


### Run
# holiday_restore('2022')
# dates = date_range('20220601', '20220628')
# dates = ['20221005']
# stock_price_restore(dates)
# valuation_restore(dates)
# category_keywords(time)
# disparity(date)
