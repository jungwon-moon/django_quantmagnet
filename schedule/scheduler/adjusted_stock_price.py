import time
import json
import requests
from qm import scraping
from qm.connect import postgres_connect, slack_url, headers


def run():
    try:
        db = postgres_connect()
        query = f"""
            select distinct stcd from stock_price
            """
        db.cursor.execute(query)
        stcds = tuple(map(lambda x: x[0], db.cursor.fetchall()))
        for stcd in stcds:
            time.sleep(0.1)
            data = scraping.adjusted_stock_price(stcd)
            data = tuple(map(lambda x: tuple(
                (x[0], stcd, x[1], x[2], x[3], x[4], x[5])), data))
            action = """
                update set
                open=excluded.open,
                high=excluded.high,
                low=excluded.low,
                close=excluded.close,
                volume=excluded.volume
                """
            db.multiUpsertDB(
                "stock_price",
                column="(date, stcd, open, high, low, close, volume)",
                values=data,
                target="date, stcd",
                action=action
            )

        txt = f"[SUCCESS] Adjust_stock_price\n실행: SCHEDULER"
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f"[FAILURE] Adjust_stock_price\n실행: SCHEDULER\n에러: {e}"
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)
