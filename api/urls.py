from django.urls import path
from api.views import *

app_name = "api"

urlpatterns = [
    ### 한국 주식 ###
    path("kr/holiday/", HolidayList.as_view(), name='holiday'),
    path("kr/tradingday/", TradingdayAPI.as_view(), name='tradingday'),
    path("kr/valuation/", ValuationList.as_view(), name='valuation'),
    path("kr/val-det/", ValuationDetail.as_view(), name='val-det'),
    path("kr/stockprice/", StockPriceList.as_view(), name='stockprice'),

    ### ###
    path("kr/gainers-losers/", GainersAndlosersList.as_view(), name='gainers-losers'),
    path("kr/soaringvalue/", SoaringValueList.as_view(), name='soaringvalue'),

    ###  ###
    path("val-ret-li", ValuationReturnsList.as_view(), name='val-ret-li'),
    path("val-ret-det", ValuationReturnsDetailList.as_view(), name='val-ret-det'),

    ###  ###
    path("searchstock/", SearchStockList.as_view(), name='searchstock'),
    path("categorykeywords/", CategoryKeywordsList.as_view(),
         name='categorykeywords'),
]
