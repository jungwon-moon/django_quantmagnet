from django.db import models


# # STOCK
class Valuation(models.Model):
    date = models.CharField(max_length=8, primary_key=True)
    stcd = models.CharField(max_length=6)
    stnm = models.TextField(blank=True, null=True)
    eps = models.FloatField(blank=True, null=True)
    per = models.FloatField(blank=True, null=True)
    bps = models.FloatField(blank=True, null=True)
    pbr = models.FloatField(blank=True, null=True)
    dps = models.FloatField(blank=True, null=True)
    dvd_yld = models.FloatField(blank=True, null=True)
    roe = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'valuation'
        unique_together = (('date', 'stcd'),)


class Holiday(models.Model):
    calnd_dd = models.CharField(primary_key=True, max_length=8)
    dy_tp_cd = models.CharField(max_length=3, blank=True, null=True)
    kr_dy_tp = models.CharField(max_length=3, blank=True, null=True)
    holdy_nm = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'holiday'
        verbose_name_plural = "휴장일"


class StockPrice(models.Model):
    date = models.CharField(max_length=8, primary_key=True)
    stcd = models.CharField(max_length=6)
    market = models.TextField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    prevd = models.FloatField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    values = models.FloatField(blank=True, null=True)
    capital = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_price'
        unique_together = (('date', 'stcd'),)


class Stocks(models.Model):
    stcd = models.CharField(max_length=6)
    stnm = models.TextField(primary_key=True)
    market = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocks'
