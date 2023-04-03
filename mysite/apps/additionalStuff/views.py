from django.shortcuts import render
from .models import Dictionary, Dates
from apps.articles.models import Topic

def dict(request):
    topicDict = {}
    for topic in Topic.objects.all():
        if topic.id == 23:
            continue
        topicDict[topic.topic] = (Dictionary.objects.filter(topic=topic.id).order_by("order"), Dates.objects.filter(topic=topic.id))
    content = {
        'topicDict': topicDict,
    }
    return render(request, 'dir.html', context=content)


def dates(request):
    return render(request, 'dates.html')
