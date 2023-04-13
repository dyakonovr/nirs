from urllib import parse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Topic, Question, QuestionOption, TopicMaterials
from apps.userProfile.models import UserScores
from apps.additionalStuff.models import Dictionary


# Форматирование статьи:
# ### - интересный блок
# ** - h2 тег, подтема
# *** - h3 тег подтема "меньше"
# ^^ - фото правителя
# $ - фото в тексте
# @ - видео
# && - ссылка


@login_required
def article(request):
    topicId = request.GET.get('topic')

    if Topic.objects.filter(id=topicId).exists():

        currentTopic = TopicMaterials.objects.get(topic=topicId)

        # Основые переменные, которые передаются на страницу
        currentUser = request.user
        allPhotos = currentTopic.photos.split('\n')
        try:
            movies = currentTopic.videos.split(',')
            presentation = currentTopic.presentation
            mainPhotos = currentTopic.mainPhoto.split(',')
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
        info = currentTopic.personInfo.split(';\n')
        rdyInfo = []
        for i in range(len(info)):
            info[i] = info[i].split('\n')
        # Rus: почему то появляетс пустой тег <p>
        for item in info:
            lst = []
            for x in range(len(item)):
                if x == 0:
                    lst.append(
                        '<p class="mt-1 mb-3 text-center border-bottom border-2 border-info fw-bold fs-5">' + item[x] + '</p>')
                else:
                    lst.append('<p class="mb-1 mb-0 px-1">' + item[x] + '</p>')
            rdyInfo.append(lst)
        # Rus: для span'оу поставить класс fw-bold/fw-semibold
        textRdy = currentTopic.text
        counter = 0
        for photo in mainPhotos:
            if photo != '':
                textRdy = textRdy.replace(
                    "^^", rf'''
                    <div class="d-flex flex-column float-end ms-3 d-block border border-3 border-info rounded-4" style="max-width: 300px">
                        <img src="{photo}" width="295" height="400" alt="" class="d-block" style="border-radius:14px 13px 0 0">{"".join(rdyInfo[counter])}
                    </div>
                    ''', 1)
            counter += 1
        for photo in allPhotos:
            if photo != '':
                textRdy = textRdy.replace(
                    "$", rf'<img src="{photo}" alt="" class="my-3 d-block mx-auto w-100">', 1)
        for movie in movies:
            if movie != '':
                textRdy = textRdy.replace(
                    "@", rf'<iframe src="{ movie }" title="YouTube video player" class="d-flex mx-auto my-3" style="width: 864px; height: 500px" frameborder="0"allow="accelerometer; autoplay; clipboard-write; encrypted-media;gyroscope; picture-in-picture; web-share"allowfullscreen></iframe>', 1)
        dict = Dictionary.objects.filter(topic=topicId).order_by("order")
        for term in dict:
            if term != '':
                textRdy = textRdy.replace(
                    "&&", rf'<a href="directory#{term.id}" id="{term.id}" class="text-decoration-none"><sup>[{term.id}]</sup></a>', 1)

        text = textRdy.split('\n')

        # Форматирование текста
        for i in range(len(text)):
            if "***" in text[i]:
                text[i] = text[i].replace(
                    '***', '<h3 class="fs-3 fw-500 mt-4">', 1).replace('***', '</h3>', 1)
            if '**' in text[i]:
                text[i] = text[i].replace(
                    '**', '<h2 class="fs-3 fw-500 mt-4">', 1).replace('**', '</h2>', 1)
            if "###" in text[i]:
                text[i] = text[i].replace(
                    '###', '<div class="bg-info-subtle d-flex align-items-center p-3 rounded-4 my-4"><p class="text-black mb-0 fs-4">', 1).replace('###', '</p></div>', 1)

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

            if currentUser.role != 'Teacher':

                if testScore > userScore:
                    UserScores.objects.update_or_create(user=request.user, defaults={
                                                        f"user_score_{topicId}": testScore})

            return HttpResponseRedirect(f'article?topic={topicId}')

        userTestScore = request.session['userTestScore']
        testFlag = request.session['testFlag']
        content = {
            'topicName': topicName,
            'test': questionChoices,
            'text': text,
            'movies': movies,
            'topicNamesLinks': topicNamesLinks,
            'presentation': presentation,
            'mainPhotos': mainPhotos,
            'allPhotos': allPhotos,
            'userTestScore': userTestScore,
            'testFlag': testFlag,
            'nextTopicLink': nextTopicLink,
            'currentUser': currentUser,
        }
        return render(request, 'article.html', context=content)
    else:
        return HttpResponseNotFound("Not found")
