from django.urls import path
from api.views import *


urlpatterns = [
    ### 한국 주식 ###
    path("kr/holiday/", HolidayAPI),
    path("kr/holiday/<year>/", HolidayDetailAPI),
    path("kr/stockprice/<day>/", StockPriceAPI),
    ###  ###
]