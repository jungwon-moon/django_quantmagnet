from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from api.models import *
from api.serializers import *
from django import db
from django.db import connection 
from django.db import transaction
from django.utils.connection import ConnectionProxy


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


class CategoryKeywordsList(APIView):
    """
    워드 클라우드
    """
    def get(self, request):
        using = 'lightsail_db'
        code = request.GET.get('code')
        cur_date = CategoryKeywords.objects.using(using).raw('''
            select date from category_keywords
                order by date desc limit 1
        ''')[0].date
        query = CategoryKeywords.objects.using(
            using).all().filter(date=cur_date, category_code=code).order_by('-date')
        serializers = CategoryKeywordsSerializer(query, many=True)
        return Response(serializers.data)


class ValuationReturnsList(APIView):
    def get(self, request):
        using = 'lightsail_db'
        cur_date = ValuationReturns.objects.using(using).raw('''
            select date from valuation_returns
                order by date desc limit 1
            ''')[0].date
        query = ValuationReturns.objects.using(
            using).all().filter(date=cur_date)
        # data = [[row.date, row.name, row.return_3m, row.return_6m, row.return_1y] for row in query]
        serializers = ValuationReturnsSerializer(query, many=True)
        return Response(serializers.data)


class ValuationReturnsDetailList(APIView):
    def get(self, request):
        name = request.GET.get('name')
        using = 'lightsail_db'
        query = ValuationReturns.objects.using(
            using).all().filter(name=name).order_by('-date')
        serializers = ValuationReturnsSerializer(query, many=True)
        return Response(serializers.data)
