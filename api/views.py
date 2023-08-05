from api.models import *
from api.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .pagination import PaginationHandlerMixin
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# # STOCK
# 휴장일
class HolidayList(generics.ListAPIView):
    """
    휴장일 데이터
    ---
    조회연도의 휴장일을 조회
    """

    using = 'lightsail_db'
    queryset = Holiday.objects.using(using).all()
    serializer_class = HolidaySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^calnd_dd']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="조회연도",
                type=openapi.TYPE_STRING,
                default="2023"
            )])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# 밸류에이션
class ValuationPagination(LimitOffsetPagination):
    default_limit = 3000
    max_limit = 5000


class ValuationList(generics.ListAPIView):
    using = "lightsail_db"
    cur_date = Valuation.objects.using(using).raw('''
        select max(date) as date from valuation
    ''')[0].date
    queryset = Valuation.objects.using(using).all().filter(
        date=cur_date)
    serializer_class = ValuationSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_fields = {
        "pbr": ["gte", "lte"],
        "per": ["gte", "lte"],
        "eps": ["gte", "lte"],
        "bps": ["gte", "lte"],
        "roe": ["gte", "lte"],
    }
    pagination_class = ValuationPagination


class ValuationDetail(APIView):
    def get(self, request):
        using = 'lightsail_db'
        stcd__contains = request.GET.get('stcd__contains')
        cur_date = Valuation.objects.using(using).raw(f'''
            select max(date) as date from valuation 
            where stcd like '{stcd__contains}'
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

# class StockPriceList(generics.ListAPIView):
#     using = 'lightsail_db'
#     queryset = StockPrice.objects.using(using).all()
#     serializer_class = StockPriceSerializer
#     pagination_class = StockPricePagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.OrderingFilter,
#     ]
#     filterset_fields = {
#         'date': ['contains'],
#         'stcd': ['contains'],
#     }
#     ordering_fields = ['date']
#     ordering = ['-date']


class StockPriceList(APIView, PaginationHandlerMixin):
    pagination_class = StockPricePagination
    serializer_class = StockPriceSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "stcd",
                openapi.IN_QUERY,
                description="종목코드",
                type=openapi.TYPE_STRING,
                default="005930"
            )])
    def get(self, request):
        using = "lightsail_db"
        stcd = request.GET.get("stcd")
        query = StockPrice.objects.using(
            using).filter(stcd=stcd).order_by('-date')
        page = self.paginate_queryset(query)
        if page is not None:
            serializers = self.get_paginated_response(
                self.serializer_class(page, many=True).data)
        else:
            serializers = self.get_paginated_response(query, many=True)
        return Response(serializers.data)


# 종목 검색
class SearchStockList(generics.ListAPIView):
    """
    ~~검색창에서 검색을 위한 API~~
    ---
    종목코드 또는 종목명에 해당하는 값을 반환한다.
    """
    using = 'lightsail_db'
    queryset = Stocks.objects.using(using).all()
    serializer_class = SearchStockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^stcd', '^stnm']


class CategoryKeywordsList(APIView):
    """
    워드 클라우드 데이터
    ---
    워드 클라우드에 사용할 데이터 조회
    호출 시 가장 최근의 데이터를 조회
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="분류코드",
                type=openapi.TYPE_STRING,
                default="002000000"
            )])
    def get(self, request):
        using = 'lightsail_db'
        code = request.GET.get('code')
        cur_date = CategoryKeywords.objects.using(using).raw('''
            select max(date) as date from category_keywords
        ''')[0].date
        query = CategoryKeywords.objects.using(
            using).filter(date=cur_date, category_code=code)
        serializers = CategoryKeywordsSerializer(query, many=True)
        return Response(serializers.data)


class ValuationReturnsList(APIView):
    def get(self, request):
        using = 'lightsail_db'
        cur_date = ValuationReturns.objects.using(using).raw('''
            select max(date) as date from valuation_returns
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
