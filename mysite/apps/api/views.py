from django.shortcuts import render
from apps.userProfile.models import StudentsGroup
from rest_framework import generics
from .serializers import GroupSerializer 

class GetGroupList(generics.RetrieveAPIView):
    queryset = StudentsGroup.objects.all()
    lookup_field = 'user'
    serializer_class = GroupSerializer
