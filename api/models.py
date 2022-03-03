# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NonTradingDays(models.Model):
    calnd_dd = models.CharField(primary_key=True, max_length=8)
    dy_tp_cd = models.CharField(max_length=3, blank=True, null=True)
    kr_dy_tp = models.CharField(max_length=3, blank=True, null=True)
    holdy_nm = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'non_trading_days'
        verbose_name_plural = '휴장일'
