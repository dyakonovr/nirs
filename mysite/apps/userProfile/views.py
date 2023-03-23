from django.shortcuts import render, redirect
from .models import UserScores
from apps.articles.models import Topic
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from apps.authentication.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages


@login_required
def profile(request):
    # Получение данных юзера
    current_user = request.user
    username = current_user.username
    email = current_user.email
    phoneNumber = current_user.phoneNumber
    try:
        userScores = UserScores.objects.get(user=current_user).__dict__
    except:
        userScores = UserScores.objects.create(user=current_user).__dict__
    del userScores['_state'], userScores['user_id']

    scores = list(userScores.copy().values())
    topics = Topic.objects.all()

    scoresData = {}
    for i in range(len(topics)):
        scoresData[topics[i]] = scores[i]

    # Смена пароля
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
                        auth_login(request, authenticate(
                            username=username, password=newPassword['newPassword']))
                        messages.success(request, "Пароль успешно изменён!")
                    else:
                        messages.error(request, "Ваш старый пароль совпадает с новым!")
                else:
                    messages.error(request, 'Неверный старый пароль')
            else:
                messages.error(request, "Пароли не совпадают!")
        return redirect('profile')
    else:
        form = ChangePasswordForm()

    content = {
        'username': username,
        'email': email,
        'phoneNumber': phoneNumber,
        'scores': scoresData,
        'form': form,
    }
    return render(request, 'profile.html', context=content)
