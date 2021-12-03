from django.shortcuts import render, redirect


def index(request):
    '''
    calculator 메인
    '''
    return render(request, 'calculator/calculator.html')

def cagr(request):
    '''
    CAGR, 복합 연간 성장률
    '''
    return render(request, 'calculator/cagr.html')