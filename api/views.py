from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from api.models import *
from api.serializers import *


# # STOCK
# 휴장일
class HolidayPagination(LimitOffsetPagination):
    default_limit = 1000
    max_limit = 1000


class HolidayList(generics.ListAPIView):
    using = 'lightsail_db'
    queryset = Holiday.objects.using(using).all()
    serializer_class = HolidaySerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = HolidayPagination
    search_fields = ['^calnd_dd']


# 밸류에이션
class ValuationList(APIView):
    def get(self, request):
        using = 'lightsail_db'
        pbr__gte = request.GET.get('pbr__gte')
        pbr__lte = request.GET.get('pbr__lte')
        per__gte = request.GET.get('per__gte')
        per__lte = request.GET.get('per__lte')
        eps__gte = request.GET.get('eps__gte')
        eps__lte = request.GET.get('eps__lte')
        bps__gte = request.GET.get('bps__gte')
        bps__lte = request.GET.get('bps__lte')
        roe__gte = request.GET.get('roe__gte')
        roe__lte = request.GET.get('roe__lte')
        cur_date = Valuation.objects.using(using).raw('''
            select date from valuation
                order by date desc limit 1
        ''')[0].date
        query = Valuation.objects.using(
            using).all().filter(
                date=cur_date,
                pbr__gte=pbr__gte,
                pbr__lte=pbr__lte,
                per__gte=per__gte,
                per__lte=per__lte,
                eps__gte=eps__gte,
                eps__lte=eps__lte,
                bps__gte=bps__gte,
                bps__lte=bps__lte,
                roe__gte=roe__gte,
                roe__lte=roe__lte
                )
        serializers = ValuationSerializer(query, many=True)
        return Response(serializers.data)

class ValuationDetail(APIView):
    def get(self, request):
        using = 'lightsail_db'
        stcd__contains = request.GET.get('stcd__contains')
        cur_date = Valuation.objects.using(using).raw('''
            select date from valuation
                order by date desc limit 1
        ''')[0].date
        query = Valuation.objects.using(
            using).all().filter(
                date=cur_date,
                stcd__contains=stcd__contains
            )
        serializers = ValuationSerializer(query, many=True)
        return Response(serializers.data)


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
