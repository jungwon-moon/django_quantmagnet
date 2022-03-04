from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Holiday
from api.serializers import HolidaySerializer


# Create your views here.
@api_view(['GET'])
def HolidayAPI(request):
    using = 'gcp'
    query = Holiday.objects.using(using).all()
    serializer = HolidaySerializer(query, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def HolidayDetailAPI(request, year):
    using = 'gcp'
    query = Holiday.objects.using(using).all().filter(calnd_dd__contains=year)
    serializer = HolidaySerializer(query, many=True)
    return Response(serializer.data)
