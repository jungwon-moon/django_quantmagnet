from django.shortcuts import render
from api.models import *
from api.serializers import *

# Create your views here.

def index(request):
    return render(request, 'strategy/strategy.html')

def Screener(request, code):
    using = 'gcp'
    query = FundamentalV1.objects.using(
        using).all().filter(stcd__contains=code)[:5]
    serializer = FundamentalSerializer(query, many=True)
    data = serializer.data
    return render(request, 'index.html', {'data': data})