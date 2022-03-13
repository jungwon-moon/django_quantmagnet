import json
from qm import scraping
from bokeh.plotting import figure
from bokeh.embed import components
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect

from common.forms import UserForm

# from py import prac_bokeh
# from qmscraping import krx, utils

from math import pi
import pandas as pd 

def main(request):
    """
    첫 페이지
    """
    return render(request, 'common/main.html')


def register(request):
    """
    계정생성
    """
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == "POST":
        form  = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = UserForm()
        
    return render(request, 'common/register.html', {'form': form})

