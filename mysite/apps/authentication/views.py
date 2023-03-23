from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib import messages
from .models import User
from apps.api.models import UserScore


def logIn(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LogInForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data
                username = user.get('username')
                password = user.get('password')
                flag_auth = authenticate(username=username, password=password)
                if flag_auth is not None:
                    auth_login(request, flag_auth)
                    return redirect('quiz')
                else:
                    messages.error(
                        request, 'Неправильное имя пользователя или пароль')
                    return redirect('logIn')
        else:
            form = LogInForm()
        return render(request, 'logIn.html', context={'form': form})
    else:
        return redirect('quiz')


def signUp(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()

                user_id = User.objects.get(username=user.username).id
                userScore = UserScore(user_id=user_id)
                userScore.save()

                auth_login(request, user)
                return redirect('quiz')
        else:
            form = SignUpForm()
        return render(request, 'signUp.html', context={'form': form})
    else:
        return redirect('quiz')


def logout_view(request):
    logout(request)
    return redirect('logIn')
