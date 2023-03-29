from urllib import parse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Topic, Question, QuestionOption, TopicMaterials
from apps.userProfile.models import UserScores
from apps.additionalStuff.models import Dictionary


@login_required
def article(request):
    topicId = request.GET.get('topic')

    if Topic.objects.filter(id=topicId).exists():

        # Основые переменные, которые передаются на страницу
        allPhotos = TopicMaterials.objects.get(
            topic=topicId).photos.split('\n')
        try:
            movies = TopicMaterials.objects.get(topic=topicId).videos.split(',')
            presentation = TopicMaterials.objects.get(topic=topicId).presentation
            mainPhotos = TopicMaterials.objects.get(topic=topicId).mainPhoto.split(',')
        except:
            movies = []
            presentation = ''
            mainPhotos = []
        topicName = Topic.objects.get(id=topicId).topic.strip()
        questionChoices = {}
        text = ''
        topicNamesLinks = {}
        nextTopicLink = f'article?topic={int(topicId)+1}'

        # Смена переменных в сессии юзера для рендера результатов теста
        if request.session.get('testFlag') is None:
            request.session['testFlag'] = False
            request.session['onResultPage'] = False
            request.session['userTestScore'] = -1
        elif request.session['onResultPage'] == True:
            request.session['testFlag'] = True
        else:
            request.session['testFlag'] = False

        if request.session['onResultPage'] == True:
            request.session['onResultPage'] = False
        # Вставка в текст фото, видео, ссылок
        textRdy = TopicMaterials.objects.get(topic=topicId).text
        for photo in mainPhotos:
            if photo != '':
                textRdy = textRdy.replace(
                    "^^", rf'<img src="{photo}" width="300" height="400" alt="" class="float-end ms-3 d-block">', 1)
        for photo in allPhotos:
            if photo != '':
                textRdy = textRdy.replace(
                    "$", rf'<img src="{photo}" alt="" class="my-3 d-block mx-auto w-100">', 1)
        for movie in movies:
            if movie != '':
                textRdy = textRdy.replace(
                    "@", rf'<iframe src="{ movie }" title="YouTube video player" class="d-flex mx-auto my-3" style="width: 864px; height: 500px" frameborder="0"allow="accelerometer; autoplay; clipboard-write; encrypted-media;gyroscope; picture-in-picture; web-share"allowfullscreen></iframe>', 1)
        dict = Dictionary.objects.filter(topic=topicId)
        for term in dict:
            if term != '':
                textRdy = textRdy.replace(
                    "%", rf'<a href="directory#{term.id}" id="{term.id}">{term.id}<a/>', 1)
        text = textRdy.split('\n')

        # Получение всех вопросов + вариантов ответов для данной темы
        questions = [
            question for question in Question.objects.filter(topic=topicId)]

        allChoices = []

        for question in questions:

            questionId = question.id
            optionsToId = [
                option for option in QuestionOption.objects.filter(question=questionId)]
            allChoices.append(optionsToId)

        for i in range(len(questions)):
            questionChoices[questions[i]] = allChoices[i]

        # Получение всех тем + их ссылок
        topicObjects = Topic.objects.all()
        for topic in topicObjects:
            topicNamesLinks[topic.topic] = f'article?topic={topic.id}'

        # Обработка теста
        if request.method == 'POST':
            userScore = UserScores.objects.get(user=request.user).__dict__[
                f'user_score_{topicId}']

            userchoices = request.POST.copy()
            del userchoices['csrfmiddlewaretoken']

            testScore = 0
            for answer in userchoices.values():
                currentAnswer = QuestionOption.objects.get(
                    id=answer).is_correct
                if currentAnswer:
                    testScore += 1
            request.session['userTestScore'] = testScore
            request.session['testFlag'] = True
            request.session['onResultPage'] = True

            if testScore > userScore:
                UserScores.objects.update_or_create(user=request.user, defaults={
                                                    f"user_score_{topicId}": testScore})

            return HttpResponseRedirect(f'article?topic={topicId}')

        userTestScore = request.session['userTestScore']
        testFlag = request.session['testFlag']
        
        content = {
            'topicName': topicName,
            'test': questionChoices,
            'textRdy': text,
            'movies': movies,
            'topicNamesLinks': topicNamesLinks,
            'presentation': presentation,
            'mainPhotos': mainPhotos,
            'allPhotos': allPhotos,
            'userTestScore': userTestScore,
            'testFlag': testFlag,
            'nextTopicLink': nextTopicLink,
        }
        return render(request, 'article.html', context=content)
    else:
        return HttpResponseNotFound("Not found")
