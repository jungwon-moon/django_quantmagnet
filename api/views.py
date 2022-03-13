from django.shortcuts import render
from rest_framework import generics, filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from api.models import *
from api.serializers import *


# Create your views here.
class HolidayList(generics.ListAPIView):
    using = 'gcp'
    queryset = Holiday.objects.using(using).all()
    serializer_class = HolidaySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^calnd_dd']


class FundamentalFilter(django_filters.FilterSet):
    class Meta:
        model = FundamentalV1
        fields = {
            'date': ['contains'],
            'per': ['gte', 'lte']
        }
        

class FundamentalList(generics.ListAPIView):
    using = 'gcp'
    queryset = FundamentalV1.objects.using(using).all()
    serializer_class = FundamentalSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['date', 'stcd', ]
    filter_class = FundamentalFilter

