import json
from pathlib import Path
from qm.db.DB import POSTGRESCRUD

SECRET_PATH = Path(__file__).resolve().parent.parent
SECRET_FILE = SECRET_PATH / "config/.config_secret/db.json"
secrets = json.loads(open(SECRET_FILE).read())

for key, value in secrets.items():
  # postgresql connect
  if key == "lightsail_db":
    pgdb_properties = value


def postgres_connect():
  return POSTGRESCRUD(pgdb_properties)
