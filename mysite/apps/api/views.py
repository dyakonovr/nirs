from django.shortcuts import render
from .models import UserScore
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import UserScoreSerializer, UserDataSerialiazer, TokenSerializer
from apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token


class UserScoreView(generics.RetrieveAPIView):
    queryset = UserScore.objects.all()
    serializer_class = UserScoreSerializer


class UserScoreUpdate(generics.UpdateAPIView):
    queryset = UserScore.objects.all()
    serializer_class = UserScoreSerializer
    permission_classes = (IsAuthenticated,)


class UserDataView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserDataSerialiazer


class UserDataList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDataSerialiazer
    permission_classes = (IsAdminUser,)


class UserTokenView(generics.RetrieveAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'user_id'
