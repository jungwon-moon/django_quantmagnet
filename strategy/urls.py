from django.urls import path
from strategy.views import *

urlpatterns = [
    path("fundamental/<code>/", Screener)
]
