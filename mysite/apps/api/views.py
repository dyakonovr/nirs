from django.forms import ValidationError
from django.shortcuts import render
from apps.userProfile.models import TeachersGroup, Student
from rest_framework import generics
from .serializers import GroupSerializer, UserSerializer, StudentSerializer
from apps.authentication.models import User





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