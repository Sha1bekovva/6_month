from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ConfirmationCode
import random

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'birthday')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data['password'],
            birthday=validated_data.get('birthday'),
            is_active=False
        )
        code = f"{random.randint(100000, 999999)}"
        ConfirmationCode.objects.create(user=user, code=code)
        return user

class ConfirmCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            if not hasattr(user, 'confirmation'):
                raise serializers.ValidationError("Код не найден.")
            if user.confirmation.code != data['code']:
                raise serializers.ValidationError("Неверный код.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")
        return data

    def save(self, **kwargs):
        user = User.objects.get(username=self.validated_data['username'])
        user.is_active = True
        user.save()
        user.confirmation.delete()

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['birthday'] = user.birthday.isoformat() if user.birthday else None
        return token
