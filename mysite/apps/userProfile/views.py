from django.shortcuts import render, redirect
from apps.api.models import UserScore
from apps.authentication.models import User
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import login as auth_login ,authenticate, update_session_auth_hash
from django.http import JsonResponse

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def profile(request):
    currentUser = request.user

    username = currentUser.username
    email = currentUser.email
    phoneNumber = currentUser.phoneNumber

    userScoreEasy = UserScore.objects.get(
        user_id=currentUser.id).user_score_easy
    userScoreMedium = UserScore.objects.get(
        user_id=currentUser.id).user_score_medium
    userScoreHard = UserScore.objects.get(
        user_id=currentUser.id).user_score_hard

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
        if username == username_:
            currentPlaceEasy = count

    count = 0
    for user in allScoresMedium:
        count += 1
        user_id = user.user_id
        username_ = User.objects.get(id=user_id).username
        if username == username_:
            currentPlaceMedium = count

    count = 0
    for user in allScoresHard:
        count += 1
        user_id = user.user_id
        username_ = User.objects.get(id=user_id).username
        if username == username_:
            currentPlaceHard = count

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

    content = {
        'username': username,
        'email': email,
        'phoneNumber': phoneNumber,
        'userScoreEasy': userScoreEasy,
        'userScoreMedium': userScoreMedium,
        'userScoreHard': userScoreHard,
        'currentPlaceEasy': currentPlaceEasy,
        'currentPlaceMedium': currentPlaceMedium,
        'currentPlaceHard': currentPlaceHard,
        'form': changePasswordForm,
    }

    return render(request, 'profile.html', context=content)