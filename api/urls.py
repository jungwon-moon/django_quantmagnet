from django.urls import path
from api.views import *

app_name = "api"

urlpatterns = [
    ### 한국 주식 ###
    path("kr/holiday/", HolidayList.as_view(), name='holiday'),
    path("kr/fundamental/", FundamentalList.as_view(), name='fundamental'),
    ###  ###
]