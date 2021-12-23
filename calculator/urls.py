from django.urls import path
from . import views


app_name = 'calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('cagr/', views.cagr, name='cagr'),
    path('investment_inflation/', views.ivestment_inflation,
         name='investment_inflation'),
]
