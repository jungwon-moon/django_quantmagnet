from rest_framework import serializers
from api.models import NonTradingDays


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = NonTradingDays
        fields = '__all__'
