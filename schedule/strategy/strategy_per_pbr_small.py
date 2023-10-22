import json
import time
import pandas as pd
from qm import utils
from qm.connect import postgres_connect

s = time.time()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def cumulative_calc(x):
    result = 1
    for i in x:
        result *= (1 + i)

    return result


def df_return_calc(prev, last):
    return last / prev - 1


def df_cumulative(base, m1, commision):
    sum = 0
    for stcd in base["stcd"]:
        if (base[base["stcd"] == stcd].empty) or \
                (m1[m1["stcd"] == stcd].empty) or \
                (m1[m1["stcd"] == stcd]["volume"].values[0] == 0):
            sum += 0
        else:
            m0_c = base[base["stcd"] == stcd]["close"].values[0]
            m1_c = m1[m1["stcd"] == stcd]["close"].values[0]
            sum += (m1_c * (1 - commision) / m0_c)

    return sum / len(base)


def extraction_df(data):
    window = len(data)
    df = pd.DataFrame(data)
    df.columns = ["date", "return"]
    df["cumulative"] = df["return"].rolling(
        window, min_periods=1).apply(cumulative_calc)
    df["return_max"] = df["cumulative"].rolling(
        window, min_periods=1).max()
    df["drawndown"] = (df["cumulative"] /
                       df["return_max"] - 1.) * 100.
    # df["mdd"] = df["drawndown"].rolling(window, min_periods=1).min()

    return df


class Strategy_PER_PBR_SMALL:
    """
    저PER 저PBR 소형주
    """

    def __init__(self):
        self.db = postgres_connect()
        # 약 1% = 증권사 수수료 0.015% X 2 + 증권 거래세 0.2% + 슬리피지 1%
        self.commission = 0.0123
        self.monthly_last = utils.load_monthly_last()

    def get_rebalancing_stcd(self):
        self.rebalancing_stcd = list()
        for date in self.monthly_last[:-1:3]:
            query = f"""
                select stcd from stock_price
                where date = '{date}'
                    and stcd in (
                        select stcd from valuation
                        where date = '{date}'
                            and (0 < per and per <= 20)
                            and (0 < pbr and pbr <= 5)
                    )
                    and value >= 50000000
                order by capital
                limit 30
            """
            self.db.cursor.execute(query)
            data = list(map(lambda x: x[0], self.db.cursor.fetchall()))
            self.rebalancing_stcd.append(data)

    def calculate(self):
        self.get_rebalancing_stcd()
        stock_data = list()
        monthly_return = list()
        quarterly_return = list()
        yearly_return = list()

        q_w = 0
        q_l = 0
        m_w = 0
        m_l = 0

        for i in range(len(self.rebalancing_stcd)):
            query = f"""
                select date, stcd, open, high, low, close, volume from stock_price
                where date in ('{self.monthly_last[i * 3]}', 
                        '{self.monthly_last[i * 3 + 1]}',
                        '{self.monthly_last[i * 3 + 2]}',
                        '{self.monthly_last[i * 3 + 3]}')
                    and stcd in {tuple(self.rebalancing_stcd[i])}
                    and volume != 0
                order by date, stcd
            """
            self.db.cursor.execute(query)
            data = self.db.cursor.fetchall()
            stock_data += [data]

            m_df = pd.DataFrame(data)
            m_df.columns = ["date", "stcd", "open",
                            "high", "low", "close", "volume"]

            m0 = m_df[m_df["date"] == self.monthly_last[i * 3]].reset_index()
            m1 = m_df[m_df["date"] ==
                      self.monthly_last[i * 3 + 1]].reset_index()
            m2 = m_df[m_df["date"] ==
                      self.monthly_last[i * 3 + 2]].reset_index()
            m3 = m_df[m_df["date"] ==
                      self.monthly_last[i * 3 + 3]].reset_index()

            rc1 = df_cumulative(m0, m1, 0)
            rc2 = df_cumulative(m0, m2, 0)
            rc3 = df_cumulative(m0, m3, self.commission)

            r1 = df_return_calc(1, rc1)
            r2 = df_return_calc(rc1, rc2)
            r3 = df_return_calc(rc2, rc3)

            three_month_return = df_cumulative(
                m0, m3, self.commission) - 1

            if three_month_return > 0:
                q_w += 1
            else:
                q_l += 1

            monthly_return.append([self.monthly_last[i * 3 + 1], r1])
            monthly_return.append([self.monthly_last[i * 3 + 2], r2])
            monthly_return.append([self.monthly_last[i * 3 + 3], r3])
            quarterly_return.append(
                [self.monthly_last[i * 3 + 3], three_month_return])

        for i in range(len(quarterly_return)):
            if i % 4 == 0:
                tmp = (1 + quarterly_return[i][1]) * \
                    (1 + quarterly_return[i+1][1]) * \
                    (1 + quarterly_return[i+2][1]) * \
                    (1 + quarterly_return[i+3][1]) - 1
                yearly_return.append([quarterly_return[i+3][0], tmp])

        for _, r in monthly_return:
            if r > 0:
                m_w += 1
            else:
                m_l += 1

        m_df = extraction_df([[self.monthly_last[0], 0.]] + monthly_return)
        q_df = extraction_df([[self.monthly_last[0], 0.]] + quarterly_return)
        y_df = extraction_df([[self.monthly_last[0], 0.]] + yearly_return)

        # json 계산
        cmgr = (((m_df['cumulative'].iloc[-1])) ** (1 / len(m_df)) - 1)
        cqgr = (((q_df['cumulative'].iloc[-1])) ** (1 / len(q_df)) - 1)
        cagr = (((y_df['cumulative'].iloc[-1])) ** (1 / len(y_df)) - 1)
        sm_avg = m_df['return'].mean()
        sq_avg = q_df['return'].mean()
        sy_avg = y_df['return'].mean()
        last_return = y_df['cumulative'].iloc[-1] - 1
        std = y_df['return'].std()
        sharp = cagr / std

        # json 추출
        monthly_data = {
            'dates': list(m_df['date']),
            'drawndown': list(m_df['drawndown']),
            'return_ratios': list(m_df['return']),
            'cumulative': list(m_df['cumulative'])
        }
        quarterly_data = {
            'dates': list(q_df['date']),
            'drawndown': list(q_df['drawndown']),
            'return_ratios': list(q_df['return']),
            'cumulative': list(q_df['cumulative'])
        }
        yearly_data = {
            'dates': list(y_df['date']),
            'drawndown': list(y_df['drawndown']),
            'return_ratios': list(y_df['return']),
            'cumulative': list(y_df['cumulative'])
        }
        summary = {
            'last_return': last_return,
            'std': std,
            'sharp': sharp,
            'mdd': m_df['drawndown'].min(),
            'cmgr': cmgr,
            'cqgr': cqgr,
            'cagr': cagr,
            'smvg': sm_avg,
            'sqvg': sq_avg,
            'savg': sy_avg,
            'odds': {'qw': q_w, 'ql': q_l, 'mw': m_w, 'ml': m_l}
        }

        output_data = {
            'summary': summary,
            'stock_info': stock_data,
            'monthly': monthly_data,
            'quarterly': quarterly_data,
            'yearly': yearly_data
        }

        with open("../react_quantmagnet/src/store/json/strategy_per_pbr_small.json", "w") as f:
            json.dump(output_data, f, indent=4)

        print(
            f"최종 수익률: {round(last_return * 100, 2)} %")
        print(
            f"분기 단순 평균 수익률: {round(sq_avg * 100, 2)} %")
        print(
            f"분기 환산 평균: {round(cqgr * 100, 2)} %")
        print(
            f"연 환산 평균: {round(cagr * 100, 2)} %")
        print(
            f"분기 승률 승: {q_w} / 패: {q_l} / 승률: {round((q_w / (q_w + q_l)) * 100, 2)} %")
        print(
            f"월 승률 승: {m_w} / 패: {m_l} / 승률: {round((m_w / (m_w + m_l)) * 100,2)} %")
        print(
            f"MDD: {round(m_df['drawndown'].min(), 2)} %")
        print(
            f"STD: {round(std, 2)}")
        print(
            f"Sharp: {round(sharp, 2)}"
        )


def run():
    strategy = Strategy_PER_PBR_SMALL()
    strategy.calculate()


run()


print(f"\n===== {round(time.time() - s, 4)} s =====")
