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
  model = Strategy_per()
  model.start = day
  model.set_view()
  stcds = model.select_stocks()
  df = pd.DataFrame(model.stock_price(), columns=[
      'date', 'stcd', 'market', 'close'])
  new_df = pd.DataFrame(columns=['date', 'stcd', 'close', 'balance'])
  balance = model.current_balance()
  if balance is None:
    balance = 100

  for stcd in stcds:
    tmp = df.loc[df['stcd'] == stcd[0]][['date', 'stcd', 'close']]
    tmp['balance'] = balance
    new_df = pd.concat([new_df, tmp], ignore_index=True)

  values = new_df[['date', 'stcd', 'balance', 'close']].values.tolist()
  values = [tuple(value + [model.limit, model.per_gte, model.per_lte, 't'])
            for value in values]
  model.db.multiInsertDB('strategy_per', values)


def strategy_per_crontab():
  if utils.check_trading_day(date):
    try:
      model = Strategy_per()
      current_date = model.current_date()
      current_position_date = model.current_position_date()
      end_position_date = utils.dt2str(utils.str2dt(
          current_position_date) + relativedelta(months=3))
      next_rebalancing_date = utils.dt2str(
          utils.str2dt(end_position_date) + relativedelta(days=1))

      if date > current_date:
        if current_date < end_position_date:
          model.start = current_date
          model.end = end_position_date
          price_df = pd.DataFrame(model.period_stock_price(), columns=[
              'date', 'stcd', 'close'])
          save_df = pd.DataFrame(
              columns=['date', 'stcd', 'close', 'balance'])
          position_info = model.position_info()
          for stcd, bid, balance in position_info:
            row = price_df.loc[price_df['stcd']
                                == stcd][['date', 'stcd', 'close']]
            tmp_df = row[['date', 'stcd', 'close']]
            tmp_df['bid'] = bid
            tmp_df['balance'] = (1+((tmp_df['close']-bid)/bid)) * balance
            save_df = pd.concat([save_df, tmp_df[1:]])
          values = save_df[['date', 'stcd',
                            'balance', 'bid']].values.tolist()
          values = [tuple(value + [model.limit, model.per_gte, model.per_lte, 'f'])
                    for value in values]
          model.db.multiInsertDB('strategy_per', values)
        
        txt = f"Strategy_per_crontab\n실행: SCHEDULER\n실행일: {date}\n상태: SUCCESS"

        if next_rebalancing_date <= date:
          strategy_per_buy(next_rebalancing_date)
          txt +=f"\n리밸런싱"

        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
      txt = f"Strategy_per_crontab\n실행: SCHEDULER\n실행일: {date}\n상태: ※ FAILURE ※\n에러: {e}"
      txt = json.dumps({"text": txt})
      requests.post(slack_url, headers=headers, data=txt)
