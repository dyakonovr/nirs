from django.shortcuts import render, redirect
from apps.api.models import UserScore
from apps.authentication.models import User
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import login as auth_login ,authenticate, update_session_auth_hash
from django.http import JsonResponse



@login_required
def profile(request):
    currentUser = request.user

    userScoreEasy = UserScore.objects.get_or_create(
        user_id=currentUser.id)[0].user_score_easy
    userScoreMedium = UserScore.objects.get_or_create(
        user_id=currentUser.id)[0].user_score_medium
    userScoreHard = UserScore.objects.get_or_create(
        user_id=currentUser.id)[0].user_score_hard

    allScoresEasy = UserScore.objects.order_by("-user_score_easy")
    allScoresMedium = UserScore.objects.order_by("-user_score_medium")
    allScoresHard = UserScore.objects.order_by("-user_score_hard")

    currentPlaceEasy = -1
    currentPlaceMedium = -1
    currentPlaceHard = -1

    count = 0
    for user in allScoresEasy:
        count += 1
        user_id = user.user_id
        username_ = User.objects.get(id=user_id).username
        if currentUser.username == username_:
            currentPlaceEasy = count

    count = 0
    for user in allScoresMedium:
        count += 1
        user_id = user.user_id
        username_ = User.objects.get(id=user_id).username
        if currentUser.username == username_:
            currentPlaceMedium = count

    count = 0
    for user in allScoresHard:
        count += 1
        user_id = user.user_id
        username_ = User.objects.get(id=user_id).username
        if currentUser.username == username_:
            currentPlaceHard = count

    # Смена пароля
    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
    changePasswordForm = ChangePasswordForm(request.user)
    if is_ajax(request=request):
        changePasswordForm = ChangePasswordForm(request.user,request.POST)
        if changePasswordForm.is_valid():

            newPassword = changePasswordForm.cleaned_data['newPassword']

            user = User.objects.get(username=currentUser.username)
            user.set_password(newPassword)
            user.save()

            update_session_auth_hash(request, user)

            return JsonResponse({'success': 'Пароль успешно изменён'})
        else:
            return JsonResponse({'errors': changePasswordForm.errors})

    content = {
        'currentUser': currentUser,
        'userScoreEasy': userScoreEasy,
        'userScoreMedium': userScoreMedium,
        'userScoreHard': userScoreHard,
        'currentPlaceEasy': currentPlaceEasy,
        'currentPlaceMedium': currentPlaceMedium,
        'currentPlaceHard': currentPlaceHard,
        'changePasswordForm': changePasswordForm,
    }

    return render(request, 'profile.html', context=content)