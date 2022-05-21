import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import LimitOffsetPagination
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
class ValuationFilter(django_filters.FilterSet):
    class Meta:
        model = Valuation
        fields = {
            'date': ['contains'],
            'stcd': ['contains'],
            'eps': ['gte', 'lte'],
            'per': ['gte', 'lte'],
            'bps': ['gte', 'lte'],
            'pbr': ['gte', 'lte'],
            'dps': ['gte', 'lte'],
            'roe': ['gte', 'lte'],
            'dvd_yld': ['gte', 'lte'],
        }


class ValuationPagination(LimitOffsetPagination):
    default_limit = 2500
    max_limit = 2500


class ValuationList(generics.ListAPIView):
    using = 'gcp'
    queryset = Valuation.objects.using(using).all()
    serializer_class = ValuationSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filter_class = ValuationFilter
    pagination_class = ValuationPagination
    ordering_fields = ['stcd']
    ordering = ['stcd']


# 주가 조회
class StockPriceFilter(django_filters.FilterSet):
    class Meta:
        model = StockPrice
        fields = {
            'date': ['contains'],
            'stcd': ['contains'],
        }

class StockPricePagination(LimitOffsetPagination):
    default_limit = 300
    max_limit = 3000

class StockPriceList(generics.ListAPIView):
    using = 'gcp'
    queryset = StockPrice.objects.using(using).all()
    serializer_class = StockPriceSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filter_class = StockPriceFilter
    pagination_class = StockPricePagination
    ordering_fields = ['stcd']
    ordering = ['stcd']