from django.shortcuts import render, redirect
from apps.api.models import UserScore
from apps.authentication.models import User
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import login as auth_login ,authenticate

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

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            newPassword = form.cleaned_data
            if newPassword['newPassword'] == newPassword['passwordConfirm']:
                user = User.objects.get(username=username)
                if user.check_password(newPassword['oldPassword']):
                    if newPassword['newPassword'] != newPassword['oldPassword']:
                        user.set_password(newPassword['newPassword'])
                        user.save()
                        auth_login(request, authenticate(username=username,password=newPassword['newPassword']))
                        messages.success(request, 'Пароль успешно изменён!')
                        return redirect('profile')
                    else:
                        messages.error(request, 'Новый пароль не может совпадать со старым!')
                else:
                    messages.error(request, 'Неверный старый пароль!')
            else:
                messages.error(request,'Пароли не совпадают!')
        return redirect('profile')
    else:
        form = ChangePasswordForm()

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
        'form': form,
    }

    return render(request, 'profile.html', context=content)