from django.shortcuts import render
from apps.userProfile.models import StudentsGroup
from rest_framework import generics
from .serializers import GroupSerializer, UserSerializer
from apps.authentication.models import User


class GetGroupList(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DeleteGroup(generics.DestroyAPIView):
    queryset = StudentsGroup.objects.all()
    serializer_class = GroupSerializer

class CreateGroup(generics.CreateAPIView):
    queryset = StudentsGroup.objects.all()
    serializer_class = GroupSerializer