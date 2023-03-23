from rest_framework import serializers
from .models import UserScore
from apps.authentication.models import User
from rest_framework.authtoken.models import Token


class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = ['user', 'user_score_easy',
                  'user_score_medium', 'user_score_hard',]


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['user_id', 'key']


class UserDataSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]
