from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache
import random
import string

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

        # Генерация и сохранение кода в Redis
        code = ''.join(random.choices(string.digits, k=6))
        cache_key = f"confirmation_code:{user.username}"
        cache.delete(cache_key)
        cache.set(cache_key, code, timeout=300)  # 5 минут

        return user

class ConfirmCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        cache_key = f"confirmation_code:{user.username}"
        cached_code = cache.get(cache_key)
        if not cached_code or cached_code != data['code']:
            raise serializers.ValidationError("Неверный или просроченный код.")

        self.user = user
        return data

    def save(self, **kwargs):
        self.user.is_active = True
        self.user.save()
        cache.delete(f"confirmation_code:{self.user.username}")
