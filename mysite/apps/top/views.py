from django.shortcuts import render
from apps.api.models import UserScore
from apps.authentication.models import User
from django.contrib.auth.decorators import login_required


@login_required
def top(request):
    currentUser = request.user.username
    user_id = request.user.id

    allScoresEasy = UserScore.objects.order_by("-user_score_easy")
    allScoresMedium = UserScore.objects.order_by("-user_score_medium")
    allScoresHard = UserScore.objects.order_by("-user_score_hard")

    topPlayersEasy = {}
    topPlayersMedium = {}
    topPlayersHard = {}

    currentPlayerEasyScore = UserScore.objects.get(
        user_id=user_id).user_score_easy
    currentPlayerMediumScore = UserScore.objects.get(
        user_id=user_id).user_score_medium
    currentPlayerHardScore = UserScore.objects.get(
        user_id=user_id).user_score_hard

    count = 0
    currentPlayerEasyPlace = -1
    currentPlayerMediumPlace = -1
    currentPlayerHardPlace = -1

    for user in allScoresEasy:
        count += 1
        if len(topPlayersEasy) <= 9:
            user_id = user.user_id
            username = User.objects.get(id=user_id).username
            topPlayersEasy[username] = user.user_score_easy
            if username == currentUser:
                currentPlayerEasyPlace = count
        else:
            user_id = user.user_id
            username = User.objects.get(id=user_id).username
            if username == currentUser:
                currentPlayerEasyPlace = count

    count = 0
    for user in allScoresMedium:
        count += 1
        if len(topPlayersMedium) <= 9:
            user_id = user.user_id
            username = User.objects.get(id=user_id).username
            topPlayersMedium[username] = user.user_score_medium
            if username == currentUser:
                currentPlayerMediumPlace = count
        else:
            user_id = user.user_id
            username = User.objects.get(id=user_id).username
            if username == currentUser:
                currentPlayerMediumPlace = count

    count = 0
    for user in allScoresHard:
        count += 1
        if len(topPlayersHard) <= 9:
            user_id = user.user_id
            username = User.objects.get(id=user_id).username
            topPlayersHard[username] = user.user_score_hard
            if username == currentUser:
                currentPlayerHardPlace = count
        else:
            user_id = user.user_id
            username = User.objects.get(id=user_id).username
            if username == currentUser:
                currentPlayerHardPlace = count

    content = {
        'topPlayersEasy': topPlayersEasy.items(),
        'topPlayersMedium': topPlayersMedium.items(),
        'topPlayersHard': topPlayersHard.items(),
        'currentUser': currentUser,
        'currentPlayerEasyScore': currentPlayerEasyScore,
        'currentPlayerMediumScore': currentPlayerMediumScore,
        'currentPlayerHardScore': currentPlayerHardScore,
        'currentPlayerEasyPlace': currentPlayerEasyPlace,
        'currentPlayerMediumPlace': currentPlayerMediumPlace,
        'currentPlayerHardPlace': currentPlayerHardPlace,
    }

    return render(request, 'top.html', context=content)


def about(request):
    return render(request, 'about.html')