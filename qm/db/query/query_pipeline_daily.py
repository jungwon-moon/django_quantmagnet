class Update_stock_list:

    def __init__(self, date):
        self.query = f"insert into stocks "
        self.query += f"select v.stcd, v.stnm, s.market "
        self.query += f"from valuation as v join stock_price as s "
        self.query += f"on (v.date = s.date) and (v.stcd = s.stcd) "
        self.query += f"where (v.date='{date}') "
        self.query += f"on conflict (stnm) "
        self.query += f"DO NOTHING"
