from django.shortcuts import render, get_object_or_404, redirect

def test(request):
    """
    test 페이지
    """
    return render(request, 'test.html')