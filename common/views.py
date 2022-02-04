from datetime import datetime
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect

from common.forms import UserForm

# from py import prac_bokeh
# from qmscraping import krx, utils


def test(request):
    """
    test 페이지
    """
    # now = datetime.today()
    # now = now.strftime('%Y-%m-%d')
    # now = utils.check_trading_day(now)
    # js = krx.fundamental_json(now)

    return render(request, 'test2.html')
    # return render(request, 'test copy.html', {'js': js, 'now': now})
    # return render(request, 'test.html', {'s1': script1, 'd1': div1})


def index(request):
    """
    첫 페이지
    """
    return render(request, 'index.html')

def register(request):
    """
    계정생성
    """
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        form  = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
        
    return render(request, 'common/register.html', {'form': form})


# def krxx(request):
#     dddd = krx.ipo()

#     return render(request, 'common/krx.html', {'dddd': dddd})