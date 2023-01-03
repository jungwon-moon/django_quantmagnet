from api.models import *
from rest_framework import serializers


# # STOCK
class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['calnd_dd', 'kr_dy_tp', 'holdy_nm']

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'

class ValuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valuation
        fields = '__all__'

class SearchStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = '__all__'

class CategoryKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryKeywords
        fields = ['date', 'category_code', 'named_entity', 'named_entity_count']

class ValuationReturnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValuationReturns
        fields = '__all__'