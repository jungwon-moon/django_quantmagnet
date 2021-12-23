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

def ivestment_inflation(request):
    '''
    Investment_Inflation, 
    '''
    return render(request, 'calculator/investment_inflation.html')