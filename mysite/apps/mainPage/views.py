from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.articles.models import Topic


@login_required
def mainPage(request):
    allTopics = Topic.objects.all()
    content = {
        'allTopics': allTopics,
    }

    return render(request, 'mainPage.html', context=content)
