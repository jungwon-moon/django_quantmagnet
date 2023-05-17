from django.test import TestCase
from qm import utils, scraping
from qm.scraping import web_bigkind, web_data_krx, web_bok, web_krx
from datetime import datetime
from qm.connect import postgres_connect


class UtilsTests(TestCase):

    def test_dt2str(self):
        dt = datetime(1993, 11, 14)
        result = utils.dt2str(dt, "day")
        self.assertEqual(result, "19931114")

    def test_str2dt(self):
        dt = datetime(1993, 11, 14)
        result = utils.str2dt("19931114")
        self.assertEqual(result, dt)

    def test_replace_zero(self):
        result = utils.replace_zero("10,000")
        self.assertEqual(result, "10000")
        result = utils.replace_zero("-")
        self.assertIsNone(result)

    def test_calc_roe(self):
        result = utils.calc_roe("-", "1,000")
        self.assertIsNone(result)
        result = utils.calc_roe("100", "-")
        self.assertIsNone(result)
        result = utils.calc_roe("721", "5,323")
        self.assertEqual(result, "13.54")

    def test_chech_trading_day_api(self):
        # 토요일 -> False
        result = utils.check_trading_day("20230513")
        self.assertFalse(result)
        # db 호출
        # 신정 -> False
        db = postgres_connect()
        result = utils.check_trading_day("20230101", db)
        self.assertFalse(result)
        # api 호출
        # 신정 -> False
        result = utils.check_trading_day("20230101")
        self.assertFalse(result)


class ScrapingTests(TestCase):

    def test_get_holiday(self):
        result = web_krx.get_holiday()
        # status code 200 반환
        self.assertEqual(result.status_code, 200)

    def test_holiday(self):
        result = scraping.holiday()
        # 데이터의 개수가 0이 아니어야 함
        self.assertNotEqual(len(result), 0)

    def test_get_kr_base_rate(self):
        result = web_bok.get_kr_base_rate()
        # 데이터의 개수가 0이 아니어야 함
        self.assertNotEqual(len(result), 0)

    def test_kr_base_rate(self):
        result = scraping.kr_base_rate()
        # 해당 데이터를 포함
        self.assertIn(['20230113', '3.50'], result)

    def test_get_valuation(self):
        result = web_data_krx.get_valuation("20230517")
        self.assertEqual(result.status_code, 200)

    def test_valuation(self):
        result = scraping.valuation("20230517")
        self.assertNotEqual(len(result), 0)

    def test_get_stock_price(self):
        result = web_data_krx.get_stock_price("20230517")
        self.assertEqual(result.status_code, 200)

    def test_stock_price(self):
        result = scraping.stock_price("20230517")
        self.assertNotEqual(len(result), 0)

    def test_get_stock_index(self):
        result = web_data_krx.get_stock_index(indIdx=1)
        self.assertEqual(result.status_code, 200)

    def test_kospi(self):
        result = scraping.kospi("20230517")
        self.assertNotEqual(len(result), 0)

    def test_kosdaq(self):
        result = scraping.kosdaq("20230517")
        self.assertNotEqual(len(result), 0)

    def test_get_category_keywords(self):
        result = web_bigkind.get_category_keywords()
        self.assertEqual(result.status_code, 200)

    def test_category_keywords(self):
        result = scraping.category_keywords()
        self.assertNotEqual(len(result), 0)
