import json
import requests
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from qm import utils
from qm.db.query.simple_backtesting_query import *


time = utils.dt2str(datetime.today(), 'time')
date = utils.dt2str(datetime.today())


def date_range(start, end):
  start = datetime.strptime(start, "%Y%m%d")
  end = datetime.strptime(end, "%Y%m%d")
  dates = [(start + relativedelta(days=i)).strftime("%Y%m%d")
           for i in range((end-start).days+1)]
  return dates


def simple_yields_PER(date):
  if utils.check_trading_day(date):
    query_model = Simple_backtesting_PER()
    query_model.start = utils.dt2str(
        utils.str2dt(date) - relativedelta(months=9))
    query_model.end = date
    query_model.limit = 10
    columns = ['date', 'stcd', 'market', 'close', 'volume']
    stcd = query_model.select_stock_code()
    print(len(stcd))
    df = pd.DataFrame(query_model.stock_price(),
                      columns=columns)

    new_df = pd.DataFrame(columns=['date', 'stcd', 'close', 'balance'])
    for cd in stcd:
      tmp = df.loc[df['stcd'] == cd[0]][['date', 'stcd', 'close']]
      buy_price = tmp.iloc[0, 2]
      balance = 1000
      tmp['balance'] = (1+(tmp['close']-buy_price)/buy_price)*balance
      new_df = pd.concat([new_df, tmp], ignore_index=True)
    group_date_df = new_df[['date', 'balance']].groupby(['date']).mean()
    group_date_df['전고점'] = group_date_df['balance'].cummax()
    print(group_date_df)
    print(query_model.start)


### RUN
# print(date_range('20200101', '20201231'))
# simple_yields_PER(date)
