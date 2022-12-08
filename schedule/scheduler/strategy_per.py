import json
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
from qm import utils
from qm.db.query.strategy_query import *


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


def strategy_per_buy(day):
  # 파라미터 설정
  model = Strategy_per()
  model.start = day
  model.set_view()
  # 종목 산출
  stcds = model.select_stocks()

  df = pd.DataFrame(model.stock_price_begin(), columns=[
                    'date', 'stcd', 'market', 'close'])
  new_df = pd.DataFrame(columns=['date', 'stcd', 'close', 'balance'])

  # 종목별 balance 계산
  balance = model.current_balance()
  if balance is None:
    balance = 1000

  for stcd in stcds:
    tmp = df.loc[df['stcd'] == stcd[0]][['date', 'stcd', 'close']]
    tmp['balance'] = balance
    new_df = pd.concat([new_df, tmp], ignore_index=True)

  # DB 저장
  values = new_df[['date', 'stcd', 'balance']].values.tolist()
  values = [tuple(value + [model.limit, model.per_gte, model.per_lte])
            for value in values]
  model.db.multiInsertDB('strategy_per', values)


def strategy_per_begin():
  trading_day = '20180301'
  strategy_per_buy(trading_day)


def strategy_per_crontab():
  try:
    model = Strategy_per()
    model.limit = 10
    model.start = utils.dt2str(utils.str2dt(
        model.current_date()))
    next = utils.dt2str(utils.str2dt(
        model.current_date()) + relativedelta(months=3))
    model.end = utils.dt2str(utils.str2dt(
        next) - relativedelta(days=1))

    # 실행하려는 next가 오늘보다 과거여야함
    if utils.dt2str(next) <= utils.dt2str(date):
      model.set_view()
      # 종목 산출
      stcds = model.select_stocks()
      # df
      stocks_df = pd.DataFrame(model.stock_price(), columns=[
          'date', 'stcd', 'market', 'close'])
      save_df = pd.DataFrame(columns=['date', 'stcd', 'close', 'balance'])
      # balance 조회
      balance = model.current_balance()
      for stcd in stcds:
        tmp = stocks_df.loc[stocks_df['stcd']
                            == stcd[0]][['date', 'stcd', 'close']]
        buy_price = tmp.iloc[0, 2]
        tmp['balance'] = (1+((tmp['close'] - buy_price)/buy_price)) * balance
        save_df = pd.concat([save_df, tmp[1:]], ignore_index=True)
      values = save_df[['date', 'stcd', 'balance']].values.tolist()
      values = [tuple(value + [model.limit, model.per_gte, model.per_lte])
                for value in values]
      model.db.multiInsertDB('strategy_per', values)
      # 신규 매수
      strategy_per_buy(next)

      txt = f"Strategy_per_crontab\n실행: SCHEDULER\n실행일: {date}\n상태: SUCCESS\n기간: {model.start} ~ {next}\n{next} 리밸런싱"
      txt = json.dumps({"text": txt})
      requests.post(slack_url, headers=headers, data=txt)

    else:
      txt = f"Strategy_per_crontab\n실행: SCHEDULER\n실행일: {date}\n상태: SUCCESS"
      txt = json.dumps({"text": txt})
      requests.post(slack_url, headers=headers, data=txt)

  except Exception as e:
    txt = f"Strategy_per_crontab\n실행: SCHEDULER\n실행일: {date}\n상태: ※ FAILURE ※\n에러: {e}"
    txt = json.dumps({"text": txt})
    requests.post(slack_url, headers=headers, data=txt)

# strategy_per_begin()
# strategy_per_crontab()
