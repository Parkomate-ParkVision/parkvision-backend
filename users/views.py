from users.models import ParkomateUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    ParkomateUserSerializer,
    LogoutSerializer,
)
from rest_framework import status


class ParkomateUserRegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_id = ParkomateUser.objects.get(email=user['email']).id
        user_data = serializer.data
        user_data['id'] = user_id
        return Response(user_data, status=status.HTTP_201_CREATED)


class ParkomateUserLoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParkomateUserLogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ParkomateUserView(ModelViewSet):
    queryset = ParkomateUser.objects.all()
    serializer_class = ParkomateUserSerializer
