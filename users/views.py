from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .serializers import UserRegisterSerializer, ConfirmCodeSerializer, UserAuthSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class ConfirmUserView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь подтвержден!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Колдонуучу логини (token алуу).
    POST /api/v1/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'key': token.key})
        return Response({'error': 'Неверные данные или пользователь не активирован'}, status=status.HTTP_401_UNAUTHORIZED)
