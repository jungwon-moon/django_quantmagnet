import json
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup
from qm.db.connect import postgres_connect
from qm import scraping, utils
from qm.db.query.strategy_query import *
from qm.db.query.crontab_daily_query import *
from qm.db.query.simple_backtesting_query import *


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

db = postgres_connect(pgdb_properties)
time = utils.dt2str(datetime.today(), 'time')
date = utils.dt2str(datetime.today())


# Utils function
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


# Main function
def stock_price_restore(*dates):
    try:
        # db = postgres_connect(pgdb_properties)
        for date in dates[0]:
            # 실행일과 거래일이 일치하는지 확인
            if utils.check_trading_day(date):
                data = scraping.get_all_stock_price(date)

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
                                replace_zero(stock['MKTCAP']))
                        else:
                            value = (
                                date, stock['ISU_SRT_CD'], stock['MKT_NM'],
                                replace_zero(stock['FLUC_RT']),  # 등락률
                                replace_zero(stock['CMPPREVDD_PRC']),
                                replace_zero(stock['TDD_OPNPRC']),
                                replace_zero(stock['TDD_HGPRC']),
                                replace_zero(stock['TDD_LWPRC']),
                                replace_zero(stock['TDD_CLSPRC']),
                                replace_zero(stock['ACC_TRDVOL']),
                                replace_zero(stock['ACC_TRDVAL']),
                                replace_zero(stock['MKTCAP']))
                        values.append(value)
                run = db.multiInsertDB('stock_price', values)
                if run[0] == False:
                    raise Exception(run[1])

        txt = f'Stock_price\n실행: RESTORE\n복원일: {dates[0][0]} ~ {dates[0][-1]}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Stock_price\n실행: RESTORE\n복원일: {dates[0][0]} ~ {dates[0][-1]}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def valuation_restore(*dates):
    try:
        for date in dates[0]:
            # 실행일과 거래일이 일치하는지 확인
            if utils.check_trading_day(date):
                data = scraping.get_valuation(date)
                # db = postgres_connect(pgdb_properties)
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

        txt = f'Valiation\n실행: RESTORE\n복원일: {dates[0][0]} ~ {dates[0][-1]}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Valiation\n실행: RESTORE\n복원일: {dates[0][0]} ~ {dates[0][-1]}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def holiday_restore(yy=None):
    try:
        data = scraping.get_holiday(yy)
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


def kr_base_rate_restore():
    try:
        values = scraping.get_kr_base_rate()
        for value in values:
            db.upsertDB('kr_base_rate', tuple(value), 'date')

        txt = f'Base_rate\n실행: RESTORE\n복원일: {date}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'Base_rate\n실행: RESTORE\n복원일: {date}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def category_keywords_restore(time):
    try:
        data = scraping.get_category_keywords()['categoryKeyword']
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
        # db = postgres_connect(pgdb_properties)
        values = []
        rows = db.readDB(table='stock_price',
                         columns='*',
                         where=f"date between '{start}' and '{date}'",
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


def simple_yields_PER(date):
    if utils.check_trading_day(date):
        try:
            query_model = Simple_backtesting_PER()
            query_model.start = utils.dt2str(
                utils.str2dt(date) - relativedelta(months=12))
            query_model.end = date
            # query_model.limit = 1
            columns = ['date', 'stcd', 'market', 'close', 'volume']
            stcd = query_model.select_stock_code()
            print(len(stcd))
            query_model.select_stock_code()
            df = pd.DataFrame(
                query_model.stock_price(), columns=columns)
            # df['balance'] = df['stcd']
            # new_df = pd.DataFrame(columns=['date', 'stcd', 'close', '전고점', 'DD'])
            new_df = pd.DataFrame(columns=['date', 'stcd', 'close', 'balance'])
            for cd in stcd:
                tmp = df.loc[df['stcd'] == cd[0]][['date', 'stcd', 'close']]
                buy_price = tmp.iloc[0, 2]
                balance = 100
                tmp['balance'] = (
                    1 + (tmp['close'] - buy_price) / buy_price) * balance
                new_df = pd.concat([new_df, tmp], ignore_index=True)
            group_date_df = new_df[['date', 'balance']
                                   ].groupby(['date']).mean()
            group_date_df['전고점'] = group_date_df['balance'].cummax()
            print(group_date_df)
            print(query_model.start)

        except Exception as e:
            print(e)


def restore_update_stock_code():
    query_model = Update_stock_code()
    query_model.date = date
    query_model.update_code()


def restore_strategy_per_return(*dates):
    try:
        for date in dates[0]:
            if utils.check_trading_day(date):
                model = Per_return()
                model.date = date
                name = 'valuation_per'
                ret_3m, ret_6m, ret_1y, \
                    ret_an, ret_cum, period = model.returns()
                stddev, cagr, sharp = model.stddev_cagr_sharp()
                mdd = model.mdd()
                value = (name, date, ret_3m, ret_6m, ret_1y,
                         ret_an, ret_cum, stddev, mdd,
                         cagr, sharp, period)
                model.db.insertDB('valuation_returns', value)

        txt = f'strategy_per_return\n실행: RESTORE\n복원일: {dates[0][0]} ~ {dates[0][-1]}\n상태: SUCCESS'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'strategy_per_return\n실행: RESTORE\n복원일: {dates[0][0]} ~ {dates[0][-1]}\n상태: ※ FAILURE ※\n에러: {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)


def strategy_per_buy(day):
    # 파라미터 설정
    model = Strategy_per()
    model.start = day
    model.set_view()
    # 종목 산출
    stcds = model.select_stocks()

    df = pd.DataFrame(model.stock_price(), columns=[
        'date', 'stcd', 'market', 'close'])
    new_df = pd.DataFrame(columns=['date', 'stcd', 'close', 'balance'])

    # 종목별 balance 계산
    balance = model.current_balance()
    if balance is None:
        balance = 100

    for stcd in stcds:
        tmp = df.loc[df['stcd'] == stcd[0]][['date', 'stcd', 'close']]
        tmp['balance'] = balance
        new_df = pd.concat([new_df, tmp], ignore_index=True)

    # DB 저장
    # date, stcd, balance, price, limit, per_gte, per_lte, new_position
    values = new_df[['date', 'stcd', 'balance', 'close']].values.tolist()
    values = [tuple(value + [model.limit, model.per_gte, model.per_lte, 't'])
              for value in values]
    model.db.multiInsertDB('strategy_per', values)


def restore_strategy_per_begin():
    trading_day = '20180101'
    strategy_per_buy(trading_day)


def restore_strategy_per(tdate):
    model = Strategy_per()
    # 최근 계산일
    current_date = model.current_date()
    # DB 데이터 확인
    if current_date is None:
        restore_strategy_per_begin()
        current_date = model.current_position_date()
    # 포지션 매수일
    current_position_date = model.current_position_date()
    # 포지션 매도일
    end_position_date = utils.dt2str(utils.str2dt(
    	current_position_date) + relativedelta(months=3))
    # # 리밸런싱 기준일
    next_rebalancing_date = utils.dt2str(
    	utils.str2dt(end_position_date) + relativedelta(days=1))

    # 실행일이 DB 마지막 데이터보다 이후면? -> 최근데이터 갱신
    if tdate > current_date:
        # 마지막 데이터가 포지션 만료일보다 이전이면? 데이터 갱신
        if current_date < end_position_date:
            model.start = current_date
            model.end = end_position_date
            price_df = pd.DataFrame(model.period_stock_price(), columns=[
                'date', 'stcd', 'close'])
            save_df = pd.DataFrame(
            	columns=['date', 'stcd', 'close', 'balance'])
            position_info = model.position_info()
            for stcd, price, balance in position_info:
                row = price_df.loc[price_df['stcd']
                                   == stcd][['date', 'stcd', 'close']]
                tmp_df = row[['date', 'stcd', 'close']]
                tmp_df['price'] = price
                tmp_df['balance'] = (
                    1+((tmp_df['close']-price)/price)) * balance
                # tmp_df[1:] -> current_date 제거
                save_df = pd.concat([save_df, tmp_df[1:]])
            values = save_df[['date', 'stcd',
                              'balance', 'price']].values.tolist()
            values = [tuple(value + [model.limit, model.per_gte, model.per_lte, 'f'])
                      for value in values]
            model.db.multiInsertDB('strategy_per', values)

        # 리밸런싱 조건
        if next_rebalancing_date <= tdate:
            strategy_per_buy(next_rebalancing_date)


### Run
# dates = [date]
# dates = ['20210702']
# simple_yields_PER('20220302')
# simple_yields_PER('20221202')
# restore_update_stock_code(date)
# holiday_restore('2018')
# dates = date_range('20190101', '20211231')
# dates = date_range('20220101', '20221231')
# stock_price_restore(dates)
# valuation_restore(dates)
# category_keywords(time)
# disparity_restore(date)
# restore_strategy_per('20221212')
# restore_strategy_per_return(dates)
