import json
import requests
from pathlib import Path
from datetime import datetime
from qm.db.connect import postgres_connect
from qm import scraping, utils


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

today = utils.dt2str(datetime.today())
time = utils.dt2str(datetime.today(), 'time')


def category_keywords():
    global time
    try:
        data = scraping.get_category_keywords()['categoryKeyword']
        db = postgres_connect(pgdb_properties)
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
        db.multiInsertDB('category_keywords', values)
        txt = f'category_keyword | Success'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

    except Exception as e:
        txt = f'category_keyword | * Failed * : {e}'
        txt = json.dumps({"text": txt})
        requests.post(slack_url, headers=headers, data=txt)

category_keywords()