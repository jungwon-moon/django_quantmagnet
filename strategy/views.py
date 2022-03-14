from django.shortcuts import render
from api.models import *
from api.serializers import *

# Create your views here.


def strategy(request):
    return render(request, 'strategy/strategy.html')


def screener(request):
    # using = 'gcp'
    # query = FundamentalV1.objects.using(
    #     using).all()[:5]
    # serializer = FundamentalSerializer(query, many=True)
    # data = serializer.data
    # return render(request, 'strategy/screener.html', {'data': data})
    return render(request, 'strategy/screener.html')
