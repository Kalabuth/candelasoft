from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.models import User

from apps.common.exceptions import UserAlreadyExists


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists() \
           or User.objects.filter(email=data['email']).exists():
            raise UserAlreadyExists()
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    