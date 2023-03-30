from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from apps.articles.models import Topic



def mainPage(request):
    if request.user.is_authenticated:
        allTopics = Topic.objects.all()
        content = {
            'allTopics': allTopics,
        }
    else:
        return redirect('about')

    return render(request, 'mainPage.html', context=content)

def aboutPage(request):
    return render(request, 'about.html')