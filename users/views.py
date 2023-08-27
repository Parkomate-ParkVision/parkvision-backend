from django.shortcuts import render
from users.models import ParkomateUser
from users.serializers import ParkomateUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class ParkomateUserRegisterView(APIView):
    def post(self, request):
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        organization = request.data.get('organization', None)
        password = request.data.get('password', None)
        privilege = request.data.get('privilege', None)

        user = ParkomateUser.objects.filter(email=email)
        if user:
            return Response({'error': 'User already exists'}, status=400)
        else:
            user = ParkomateUser.objects.create(email=email, name=name, phone=phone, organization=organization, password=password, privilege=privilege)
            serializer = ParkomateUserSerializer(user)
            return Response(
                {'status': 'User created', 'data': serializer.data}, 
                status=201
            )

class ParkomateUserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = ParkomateUser.objects.filter(email=email, password=password)
        if user:
            serializer = ParkomateUserSerializer(user)
            return Response(
                {'status': 'User logged in', 'data': serializer.data}, 
                status=200
            )

class ParkomateUserLogoutView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        user = ParkomateUser.objects.filter(email=email)
        if user:
            serializer = ParkomateUserSerializer(user)
            return Response(
                {'status': 'User logged out', 'data': serializer.data}, 
                status=200
            )
        
class ParkomateUserViewSet(ModelViewSet):
    queryset = ParkomateUser.objects.all()
    serializer_class = ParkomateUserSerializer