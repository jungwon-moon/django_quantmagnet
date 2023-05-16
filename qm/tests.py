from django.test import TestCase
from qm import utils
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

    def test_check_trading_day_weekend(self):
        result = utils.check_trading_day("20230513")
        self.assertEqual(result, False)

    def test_chech_trading_day_api(self):
        result = utils.check_trading_day("20230101")
        self.assertEqual(result, False)

    def test_chech_trading_day_db(self):
        db = postgres_connect()
        result = utils.check_trading_day("20230101", db)
        self.assertEqual(result, False)
