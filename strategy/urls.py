from django.urls import path
from strategy.views import *

app_name = 'strategy'

urlpatterns = [
    path("", strategy, name='strategy'),
    path("screener/", screener, name='screener')
]
