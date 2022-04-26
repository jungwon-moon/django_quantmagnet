import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from api.models import *
from api.serializers import *

# # STOCK
# 휴장일
class HolidayPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100

class HolidayList(generics.ListAPIView):
    using = 'gcp'
    queryset = Holiday.objects.using(using).all()
    serializer_class = HolidaySerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = HolidayPagination
    search_fields = ['^calnd_dd']

# 밸류에이션
class FundamentalFilter(django_filters.FilterSet):
    class Meta:
        model = FundamentalV1
        fields = {
            'date': ['contains'],
            'eps': ['gte', 'lte'],
            'per': ['gte', 'lte'],
            'bps': ['gte', 'lte'],
            'pbr': ['gte', 'lte'],
            'dps': ['gte', 'lte'],
            'roe': ['gte', 'lte'],
            'dvd_yld': ['gte', 'lte'],
        }

class FundamentalPagination(LimitOffsetPagination):
    default_limit = 2500
    max_limit = 2500

class FundamentalList(generics.ListAPIView):
    using = 'gcp'
    queryset = FundamentalV1.objects.using(using).all()
    serializer_class = FundamentalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filter_class = FundamentalFilter
    pagination_class= FundamentalPagination
    ordering_fields = ['stcd']
    ordering = ['stcd']
