from django.shortcuts import render
from apps.api.models import UserScore
from apps.authentication.models import User
from django.contrib.auth.decorators import login_required

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
    }

    return render(request, 'profile.html', context=content)