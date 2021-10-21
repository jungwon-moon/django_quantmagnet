from django.urls import path
from . import views


app_name = 'common'

urlpatterns = [
    path('test/', views.test, name='test'),
]