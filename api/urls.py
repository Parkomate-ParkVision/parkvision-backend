from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from api.views import (
    OrganizationViewSet,
    GateViewSet,
    VehicleViewSet
)

router = DefaultRouter()
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register('gates', GateViewSet, basename='gates')
router.register('vehicles', VehicleViewSet, basename='vehicles')

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Main API',
            'endpoints': [
                '/organizations/',
                '/gates/',
                '/vehicles/',
            ]
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
] + router.urls