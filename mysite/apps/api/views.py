from django.forms import ValidationError
from django.shortcuts import render
from apps.userProfile.models import TeachersGroup, Student
from rest_framework import generics
from .serializers import GroupSerializer, UserSerializer, StudentSerializer, TokenSerializer
from apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class GetGroupList(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeleteGroup(generics.DestroyAPIView):
    queryset = TeachersGroup.objects.all()
    serializer_class = GroupSerializer


class CreateGroup(generics.CreateAPIView):
    queryset = TeachersGroup.objects.all()
    serializer_class = GroupSerializer


class DeleteStudent(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'student_id'


class GetTokenUser(generics.RetrieveAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'user_id'
