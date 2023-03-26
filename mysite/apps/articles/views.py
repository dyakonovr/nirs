from urllib import parse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Topic, Question, QuestionOption, TopicMaterials, Photos
from apps.userProfile.models import UserScores


@login_required
def article(request):
    topicNum = request.GET.get('topic')

    if Topic.objects.filter(id=topicNum).exists():

        # Основые переменные, которые передаются на страницу
        mainPhotos = TopicMaterials.objects.get(
            topic=topicNum).mainPhoto.split(',')
        allPhotos = {}
        presentation = TopicMaterials.objects.get(
            topic=topicNum).presentation
        movies = TopicMaterials.objects.get(topic=topicNum).videos.split(',')
        topicName = Topic.objects.get(id=topicNum).topic.strip()
        questionChoices = {}
        textRdy = TopicMaterials.objects.get(topic=topicNum).text
        topicNamesLinks = {}
        nextTopicLink = f'article?topic={int(topicNum)+1}'

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
        
        # Получение всех картинок
        photos = Photos.objects.filter(topic=topicNum)
        for photo in photos:
            allPhotos[photo.paragraph] = photo.photo

        countOfMainPhotos = textRdy.count('^^')
        for photo in mainPhotos:
            if not photo == '':
                textRdy = textRdy.replace("^^", rf'<img src="{photo}" width="300" height="400" alt="" class="float-end ms-3 d-block">',1)
        text = textRdy.split('\n')
        counter = 2
        print(allPhotos)
        for paragraph, photo in allPhotos.items():
            print(paragraph - countOfMainPhotos + counter)
            text.insert(paragraph - countOfMainPhotos + counter, rf'<img src="{photo}" alt="" class="my-3 d-block mx-auto">')
            counter += 1
        # Получение всех вопросов + вариантов ответов для данной темы
        questions = [
            question for question in Question.objects.filter(topic=topicNum)]

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
                f'user_score_{topicNum}']

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
                                                    f"user_score_{topicNum}": testScore})

            return HttpResponseRedirect(f'article?topic={topicNum}')

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
