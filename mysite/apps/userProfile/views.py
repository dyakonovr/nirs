from django.forms import ValidationError
from django.shortcuts import render, redirect
from .models import UserScores, TeachersGroup, Student
from apps.articles.models import Topic
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm, AddGroupForm
from apps.authentication.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse


@login_required
def profile(request):

    # Получение данных юзера
    currentUser = request.user
    teacherGroup = {}
    for groupMember in Student.objects.filter(student=currentUser):
        teacherGroup[groupMember] = TeachersGroup.objects.get(
            id=groupMember.group.id)

    # Вспомогательные функции

    # Получение результатов
    def getResults(user):
        studentScores = {}
        try:
            userScores = UserScores.objects.get(user=user).__dict__
        except:
            userScores = UserScores.objects.create(user=user).__dict__
        del userScores['_state'], userScores['user_id']

        scores = list(userScores.copy().values())
        topics = Topic.objects.all()

        for i in range(len(topics)):
            studentScores[topics[i]] = scores[i]

        return studentScores

    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
    # Смена пароля
    changePasswordForm = ChangePasswordForm(request.user)
    if is_ajax(request=request):
        changePasswordForm = ChangePasswordForm(request.user, request.POST)
        if changePasswordForm.is_valid():

            newPassword = changePasswordForm.cleaned_data['newPassword']
            user = User.objects.get(username=currentUser.username)
            user.set_password(newPassword)
            user.save()

            update_session_auth_hash(request, user)

            return JsonResponse({'success': 'Пароль успешно изменён'})
        else:
            return JsonResponse({'errors': changePasswordForm.errors})

    # Получение групп с учениками или результатов юзера
    if currentUser.role == 'Teacher':
        groups = TeachersGroup.objects.filter(user=currentUser)
        addGroupForm = AddGroupForm()
        groupStudents = {}
        scoresData = {}
        for group in groups:

            students = {}

            for student in Student.objects.filter(group=group.id):

                scores = getResults(student.student)

                students[student] = scores

            groupStudents[group] = students

    else:
        addGroupForm = None
        scoresData = getResults(currentUser)
        groupStudents = {}

    content = {
        'currentUser': currentUser,
        'scores': scoresData,
        'changePasswordForm': changePasswordForm,
        'groupStudents': groupStudents,
        'addGroupForm': addGroupForm,
        'userGroups': teacherGroup,
    }

    return render(request, 'profile.html', context=content)


@login_required
def addGroup(request):

    teacher_id = request.GET.get('user_id')
    group_id = request.GET.get('group_id')
    code = request.GET.get('code')

    if User.objects.filter(id=teacher_id).exists() and TeachersGroup.objects.filter(id=group_id).exists() and TeachersGroup.objects.filter(code=code).exists():
        if int(teacher_id) != request.user.id:
            if request.user.role != 'Teacher':
                if not Student.objects.filter(group_id=group_id, student=request.user).exists():

                    Student.objects.create(
                        student=request.user, group=TeachersGroup.objects.get(id=group_id))

                    content = {
                        'teacher': User.objects.get(id=teacher_id),
                        'group': TeachersGroup.objects.get(id=group_id),
                    }

                    return render(request, 'addGroup.html', context=content)
                else:
                    return HttpResponse("<h1>ERROR! You're already this group member!</h1>")
            else:
                return HttpResponse("<h1>ERROR! You can't be student, because you're a teacher!</h1>")
        else:
            return HttpResponse("<h1>ERROR! You can't be your student</h1>")
    return HttpResponseNotFound("<h1>Page not found</h1>")
