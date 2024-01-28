from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from users.views import (
    ParkomateUserLoginView,
    ParkomateUserRegisterView,
    ParkomateUserLogoutView,
    ParkomateUserView,
)

router = DefaultRouter()
router.register(r'users', ParkomateUserView, basename='users')


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Users API',
            'endpoints': [
                '/login/',
                '/register/',
                '/logout/',
                '/users/',
            ]
        })


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', ParkomateUserLoginView.as_view(), name="login"),
    path('register/', ParkomateUserRegisterView.as_view(), name="register"),
    path('logout/', ParkomateUserLogoutView.as_view(), name="logout"),
] + router.urls
