from django.urls import path, include
from api.views import HolidayAPI

urlpatterns = [
    path("holiday/", HolidayAPI),
    
]