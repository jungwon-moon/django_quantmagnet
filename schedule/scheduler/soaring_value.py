import json
import requests
import numpy as np
import pandas as pd
from qm import utils
from qm.connect import postgres_connect, slack_url, headers


def run():
    today = utils._today

    if utils.check_trading_day(today):
        db = postgres_connect()
        query = ''


run()
