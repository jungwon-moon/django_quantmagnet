import json
import requests
import numpy as np
import pandas as pd
from qm import utils
from qm.connect import postgres_connect, slack_url, headers


def run():
    today = utils._today

    if utils.check_trading_day(today):
        try:
            ### DB connect ### 
            db = postgres_connect()
            start = utils.change_date(today, "months", -2)

            ### Stock Codes ###
            query = f"""
                select stcd from stock_price 
                where date='{start}' 
                order by stcd
            """
            db.cursor.execute(query)
            stcds = tuple(map(lambda x: x[0], db.cursor.fetchall()))

            ### DataFrame ###
            query = f"""
                select date, stcd, value
                from stock_price 
                where stcd in {stcds} 
                    and date between '{start}' and '{today}' 
                    and volume != 0 
                order by stcd desc, date desc
            """
            db.cursor.execute(query)
            df = pd.DataFrame(db.cursor.fetchall())
            df = df[::-1].reset_index(drop=True)
            df.columns = [
                "date", "stcd", "value"
            ]

            ### Condition ###
            search_stock_list = []
            for stcd in stcds:
                tmp_df = df[df["stcd"]==stcd]
                tmp_value = tmp_df["value"]
                if len(tmp_df) <= 2: continue
                if tmp_df["date"].values[-1] != today: continue
                
                cond1 = tmp_value.max() == tmp_value.values[-1]
                cond2 = tmp_value.values[-2] * 10 < tmp_value.values[-1]
                cond3 = tmp_value.values[-1] >= 10000000000

                if ((cond1 is np.True_) and
                    (cond2 is np.True_) and
                    (cond3 is np.True_)):
                    search_stock_list.append(stcd)

            ### Insert DB ###
            query = f"""
                select p.date, p.stcd, s.stnm, p.rate, p.open, p.high, p.low, p.close, p.volume, p.value 
                from stock_price as p 
                inner join stocks as s 
                on p.stcd = s.stcd 
                where p.date = '{today}' 
                    and p.stcd in {tuple(search_stock_list)}
                order by p.value desc
            """
            db.cursor.execute(query)
            data  = list(map(lambda x: tuple(x), db.cursor.fetchall()))
            db.multiInsertDB("cache_soaring_value", data)

            txt = f'[SUCC] soaring_value\n실행: SCHEDULER'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)

        except Exception as e:
            txt = f'[FAIL] soaring_value\n실행: SCHEDULER\n에러: {e}'
            txt = json.dumps({"text": txt})
            requests.post(slack_url, headers=headers, data=txt)
    else:
        return False
