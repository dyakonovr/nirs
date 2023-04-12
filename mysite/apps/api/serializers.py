from rest_framework import serializers
from apps.userProfile.models import TeachersGroup, Student
from apps.authentication.models import User
import random
import string

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachersGroup
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'group')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
