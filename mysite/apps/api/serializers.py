from rest_framework import serializers
from apps.userProfile.models import StudentsGroup
from apps.authentication.models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsGroup
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'group')
