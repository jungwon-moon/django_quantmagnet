from django.db import models


# # STOCK
class Holiday(models.Model):
    """
    휴장일 정보
    """
    calnd_dd = models.CharField(primary_key=True, max_length=8)
    dy_tp_cd = models.CharField(max_length=3, blank=True, null=True)
    kr_dy_tp = models.CharField(max_length=3, blank=True, null=True)
    holdy_nm = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'holiday'
        verbose_name_plural = "휴장일"


class StockPrice(models.Model):
    """
    주가 
    """
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
    value = models.FloatField(blank=True, null=True)
    capital = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_price'
        unique_together = (('date', 'stcd'),)


class Valuation(models.Model):
    """
    가치평가(밸류에이션)
    """
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


class Stocks(models.Model):
    """
    주식의 종목코드 및 종목명
    """
    stcd = models.CharField(max_length=6)
    stnm = models.TextField(primary_key=True)
    market = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocks'


##
class CategoryKeywords(models.Model):
    """
    워드클라우드
    """
    date = models.CharField(max_length=12, primary_key=True)
    category_code = models.CharField(max_length=9)
    category_name = models.TextField()
    named_entity = models.TextField()
    named_entity_type = models.TextField()
    named_entity_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'category_keywords'
        # unique_together = (('date', 'stcd'),)


class GainsAndLosers(models.Model):
    """
    급등주 및 급락주
    """
    date = models.CharField(max_length=8, primary_key=True)
    stcd = models.CharField(max_length=6)
    stnm = models.TextField()
    rate = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cache_gains_and_losers'
        unique_together = (('date', 'stcd'))


class SoaringValue(models.Model):
    """
    거래대금 상승종목
    """
    date = models.CharField(max_length=8, primary_key=True)
    stcd = models.CharField(max_length=6)
    stnm = models.TextField()
    rate = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cache_soaring_value'
        unique_together = (('date', 'stcd'))


##
class ValuationReturns(models.Model):
    """
    기본 valuation의 수익률 결과값
    """
    name = models.TextField()
    date = models.CharField(max_length=12, primary_key=True)
    return_3m = models.FloatField()
    return_6m = models.FloatField()
    return_1y = models.FloatField()
    annualized_HPR = models.FloatField()
    cumulative_return = models.FloatField()
    stddev = models.FloatField()
    mdd = models.FloatField()
    cagr = models.FloatField()
    sharp_rate = models.FloatField()
    period = models.FloatField()

    class Meta:
        managed = False
        db_table = 'valuation_returns'
        # unique_together = (('name', 'date'),)
