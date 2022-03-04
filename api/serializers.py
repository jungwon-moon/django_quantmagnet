from rest_framework import serializers
from api.models import Holiday


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['calnd_dd', 'kr_dy_tp', 'holdy_nm']
