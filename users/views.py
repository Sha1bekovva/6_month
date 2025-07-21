from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate
from .serializers import (
    UserRegisterSerializer,
    ConfirmCodeSerializer,
    UserAuthSerializer,
    CustomTokenObtainSerializer
)
from .models import ConfirmationCode
import random
import string

class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
            code = ''.join(random.choices(string.digits, k=6))
            ConfirmationCode.objects.update_or_create(user=user, defaults={"code": code})
        return Response({'user_id': user.id, 'message': 'Пользователь зарегистрирован. Код отправлен на почту.'}, status=status.HTTP_201_CREATED)

class ConfirmUserView(CreateAPIView):
    serializer_class = ConfirmCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Пользователь успешно активирован.'}, status=status.HTTP_200_OK)

class LoginView(CreateAPIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user:
            if not user.is_active:
                return Response({'error': 'Аккаунт ещё не активирован.'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': 'Успешный вход'}, status=status.HTTP_200_OK)
        return Response({'error': 'Неверные учетные данные.'}, status=status.HTTP_401_UNAUTHORIZED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
