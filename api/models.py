# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FundamentalV1(models.Model):
    date = models.CharField(primary_key=True, max_length=8)
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
        db_table = 'fundamental_v1'
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
    date = models.CharField(primary_key=True, max_length=8)
    stcd = models.CharField(max_length=6)
    market = models.TextField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
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
