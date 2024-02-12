from users.models import ParkomateUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    ParkomateUserSerializer,
    LogoutSerializer,
)
from rest_framework import status
from utils.emails import send_email
import random
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BaseAuthentication

class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None

class ParkomateUserRegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    authentication_classes = [NoAuthentication]

    def post(self, request):
        user = request.data
        user['password'] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8))
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_id = ParkomateUser.objects.get(email=user['email']).id
        user_data = serializer.data
        user_data['id'] = user_id
        user_data['password'] = user['password']
        send_email(
            user['email'],
            'Parkomate Account Password',
            f'Your password is {user["password"]}. Login to your account on the ParkVision Dashboard',
        )
        return Response(user_data, status=status.HTTP_201_CREATED)


class ParkomateUserLoginView(GenericAPIView):
    serializer_class = LoginSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    authentication_classes = [NoAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParkomateUserLogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ParkomateUserView(ModelViewSet):
    queryset = ParkomateUser.objects.all()
    serializer_class = ParkomateUserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]