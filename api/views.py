from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import NonTradingDays
from api.serializers import HolidaySerializer


# Create your views here.
@api_view(['GET'])
def HolidayAPI(request):
    using = 'gcp'
    total = NonTradingDays.objects.using(using).all()
    serializer = HolidaySerializer(total, many=True)

    return Response(serializer.data)