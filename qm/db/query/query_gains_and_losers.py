class Gains_and_losers:

    def __init__(self):

        self.query = f" select p.date, p.stcd, s.stnm, p.rate, p.open, p.high, p.low, p.close, p.volume, p.value "
        self.query += f"from stock_price as p "
        self.query += f"inner join stocks as s "
        self.query += f"on p.stcd = s.stcd "
        self.query += f"where p.date = (select max(date) as date "
        self.query += f"                from stock_price) "
        self.query += f"order by p.rate desc"
