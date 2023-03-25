from django.shortcuts import render
from .models import Dictionary


def dict(request):
    terms = Dictionary.objects.all()
    content = {
        'terms': terms,
    }
    return render(request, 'dict.html', context=content)


def dates(request):
    return render(request, 'dates.html')
