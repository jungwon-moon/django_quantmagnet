from django.urls import path
from api.views import *

app_name = "api"

urlpatterns = [
    ### 한국 주식 ###
    path("kr/holiday/", HolidayList.as_view(), name='holiday'),
    path("kr/valuation/", ValuationList.as_view(), name='valuation'),
    path("kr/stockprice/", StockPriceList.as_view(), name='stockprice'),
    ###  ###
    path("searchstock/", SearchStockList.as_view(), name='searchstock'),
    path("categorykeywords/", CategoryKeywordsList.as_view(), name='categorykeywords'),
    ###  ###
    path("val-ret-li", ValuationReturnsList.as_view(), name='val-ret-li'),
    path("val-ret-det", ValuationReturnsDetailList.as_view(), name='val-ret-det'),
]