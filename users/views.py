from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import ConfirmationCode, CustomUser
from .serializers import (
    UserRegisterSerializer,
    UserAuthSerializer,
    ConfirmCodeSerializer,
    CustomTokenObtainSerializer
)
from .tasks import send_otp_email
import random
import string


class RegistrationAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()

            # Генерируем и отправляем код
            code = ''.join(random.choices(string.digits, k=6))
            ConfirmationCode.objects.update_or_create(user=user, defaults={"code": code})
            send_otp_email.delay(user.email, code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={'user_id': user.id, 'message': 'Пользователь зарегистрирован. Код отправлен на почту.'}
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data={'message': 'Пользователь успешно активирован.'}
        )


class AuthorizationAPIView(CreateAPIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'Аккаунт ещё не активирован.'}
                )
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'Неверные учетные данные.'}
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer