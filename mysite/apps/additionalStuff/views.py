from django.shortcuts import render


def dict(request):
    return render(request, 'dict.html')


def dates(request):
    return render(request, 'dates.html')
