from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from organization.views import (
    OrganizationView,
    GateView,
    AdminView
)

router = DefaultRouter()
router.register('organizations', OrganizationView, basename='organizations')
router.register('gates', GateView, basename='gates')
router.register('admins', AdminView, basename='admins')


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Main API',
            'endpoints': [
                '/organizations/',
                '/gates/',
                '/admins/',
            ]
        })


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
] + router.urls
