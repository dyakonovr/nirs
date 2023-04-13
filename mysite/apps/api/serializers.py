from rest_framework import serializers
from apps.userProfile.models import TeachersGroup, Student
from apps.authentication.models import User
from rest_framework.authtoken.models import Token

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachersGroup
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('user_id','key',)

class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=True, read_only=True)
    token = TokenSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'group')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
