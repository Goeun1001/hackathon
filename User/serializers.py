from rest_framework import serializers
from django.contrib.auth import get_user_model
from .services import HashService

User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=45)
    password = serializers.CharField(required=True, max_length=64)
    nickname = serializers.CharField(required=True, max_length=45)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            password=HashService.hash_string_to_password(
                validated_data.get('password')),
            nickname=validated_data.get('nickname'),
        )

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=45)
    password = serializers.CharField(required=True, max_length=64)
