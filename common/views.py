from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from common.forms import UserForm


def test(request):
    """
    test 페이지
    """
    return render(request, 'test.html')

def index(request):
    """
    첫 페이지
    """
    return render(request, 'index.html')

def signup(request):
    """
    계정생성
    """
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
    return render(request, 'common/signup.html', {'form': form})