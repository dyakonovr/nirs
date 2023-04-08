from django.forms import ValidationError
from django.shortcuts import render, redirect
from .models import UserScores, StudentsGroup, StudentGroupUser
from apps.articles.models import Topic
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm, AddGroupForm
from apps.authentication.models import User
from django.contrib.auth import login as auth_login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def profile(request):

    # Получение данных юзера
    currentUser = request.user

    # Получение результатов
    try:
        userScores = UserScores.objects.get(user=currentUser).__dict__
    except:
        userScores = UserScores.objects.create(user=currentUser).__dict__
    del userScores['_state'], userScores['user_id']

    scores = list(userScores.copy().values())
    topics = Topic.objects.all()

    scoresData = {}
    for i in range(len(topics)):
        scoresData[topics[i]] = scores[i]

    # Смена пароля
    changePasswordForm = ChangePasswordForm(request.user)
    if is_ajax(request=request):
        changePasswordForm = ChangePasswordForm(request.user,request.POST)
        if changePasswordForm.is_valid():
            oldPassword = changePasswordForm.cleaned_data['oldPassword']
            newPassword = changePasswordForm.cleaned_data['newPassword']
            passwordConfirm = changePasswordForm.cleaned_data['passwordConfirm']
            user = User.objects.get(username=currentUser.username)
            user.set_password(newPassword)
            user.save()
            update_session_auth_hash(request, user)
            data = {
                'oldPassword': oldPassword,
                'newPassword': newPassword,
                'passwordConfirm': passwordConfirm,
            }
            return JsonResponse({'success': 'Пароль успешно изменён'})
        else:
            return JsonResponse({'errors': changePasswordForm.errors})

    # Привязка учеников
    groups = StudentsGroup.objects.all()
    addGroupForm = AddGroupForm()

    content = {
        'currentUser': currentUser,
        'scores': scoresData,
        'changePasswordForm': changePasswordForm,
        'groups': groups,
        'addGroupForm': addGroupForm,
    }
    return render(request, 'profile.html', context=content)
