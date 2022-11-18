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
    using = 'lightsail_db'
    queryset = Holiday.objects.using(using).all()
    serializer_class = HolidaySerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = HolidayPagination
    search_fields = ['^calnd_dd']


# 밸류에이션
class ValuationPagination(LimitOffsetPagination):
    default_limit = 2500
    max_limit = 2500


class ValuationList(generics.ListAPIView):
    using = 'lightsail_db'
    queryset = Valuation.objects.using(using).all()
    serializer_class = ValuationSerializer
    pagination_class = ValuationPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = {
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
    ordering_fields = ['date']
    ordering = ['-date']


# 주가 조회
class StockPricePagination(LimitOffsetPagination):
    default_limit = 300
    max_limit = 3000


class StockPriceList(generics.ListAPIView):
    using = 'lightsail_db'
    queryset = StockPrice.objects.using(using).all()
    serializer_class = StockPriceSerializer
    pagination_class = StockPricePagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        'date': ['contains'],
        'stcd': ['contains'],
    }
    ordering_fields = ['date']
    ordering = ['-date']


# 종목 검색
class SearchStockList(generics.ListAPIView):
    using = 'lightsail_db'
    queryset = Stocks.objects.using(using).all()
    serializer_class = SearchStockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^stcd', '^stnm']


# 클라우드 워드 키워드 조회
class CategoryKeywordsPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


class CategoryKeywordsList(generics.ListAPIView):
    using = 'lightsail_db'
    queryset = CategoryKeywords.objects.using(using).all()
    serializer_class = CategoryKeywordsSerializer
    pagination_class = CategoryKeywordsPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        'date': ['contains'],
        'category_code': ['contains']
    }
    ordering_fields = ['date']
    ordering = ['-date']
