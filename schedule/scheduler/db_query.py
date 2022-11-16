import json
from pathlib import Path
from qm.db.connect import postgres_connect
from qm import scraping, utils


class Connect_DB():
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

	db = postgres_connect(pgdb_properties)


class Simple_yields_PER(Connect_DB):

	def __init__(self):
		# 3 <= per <= 5
		self.per_gte = 3
		self.per_lte = 5
		self.start = ""
		self.end = ""
		self.orderby = "capital"
		self.limit = 30

	def set_view(self):
		query = f"create or replace view public.per "
		query += f"as select p.date, p.stcd, p.close, v.per, p.capital, p.volume "
		query += f"from valuation as v join stock_price as p "
		query += f"on (v.date = p.date) and (v.stcd = p.stcd) "
		query += f"where p.volume != 0 and v.date='{self.start}' and "
		query += f"v.per >= {self.per_gte} and v.per <= {self.per_lte} "
		query += f"order by p.{self.orderby} asc "
		query += f"limit {self.limit} "
		self.db.cursor.execute(query)

	def show_view(self):
		query = f"select * from public.per"
		self.db.cursor.execute(query)
		result = self.db.cursor.fetchall()
		return result

	def select_stock_code(self):
		self.set_view()
		query = f"select stcd from public.per"
		self.db.cursor.execute(query)
		result = self.db.cursor.fetchall()
		return result

	def stock_price(self):
		query = f"select date, stcd, market, close, volume from stock_price "
		query += f"where stcd = any(select stcd from public.per) "
		query += f"and date between (select distinct date from stock_price where date >= '{self.start}' order by date asc limit 1) "
		query += f"and (select distinct date from stock_price where date <= '{self.end}' order by date desc limit 1)"
		query += f"order by stcd, date"
		self.db.cursor.execute(query)
		result = self.db.cursor.fetchall()
		return result


class Update_stock_code(Connect_DB):

	def __init__(self):
		self.date = ''

	def delete_lock(self):
		query = f"delete from stocks where stnm like '%[락]'"
		self.db.cursor.execute(query)

	def update_code(self):
		query = f"insert into stocks "
		query += f"select v.stcd, v.stnm, s.market "
		query += f"from valuation as v join stock_price as s "
		query += f"on (v.date = s.date) and (v.stcd = s.stcd) "
		query += f"where (v.date='{self.date}')"
		query += f"on conflict (stnm) "
		query += f"DO NOTHING"
		self.db.cursor.execute(query)
