from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib import messages
from apps.userProfile.models import UserScores


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
                    return redirect('mainPage')
                else:
                    messages.error(
                        request, 'Неправильное имя пользователя или пароль')
                    return redirect('login')
        else:
            form = LogInForm()
        return render(request, 'logIn.html', context={'form': form})
    else:
        return redirect('mainPage')


def signUp(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()

                userScore = UserScores(user=user)
                userScore.save()

                auth_login(request, user)
                return redirect('mainPage')
        else:
            form = SignUpForm()
        return render(request, 'signUp.html', context={'form': form})
    else:
        return redirect('mainPage')


def logout_view(request):
    logout(request)
    return redirect('login')
