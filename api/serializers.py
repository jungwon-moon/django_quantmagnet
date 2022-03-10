from rest_framework import serializers
from api.models import *


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['calnd_dd', 'kr_dy_tp', 'holdy_nm']


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'


class FundamentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundamentalV1
        fields = '__all__'