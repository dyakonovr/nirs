from rest_framework import serializers
from apps.userProfile.models import StudentsGroup
from apps.authentication.models import User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentsGroup
        fields = ('user_id', 'group')


class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = User
        fields = ('user_id', 'username', 'group')
