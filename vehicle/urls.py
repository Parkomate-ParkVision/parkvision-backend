from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from vehicle.views import (
    VehicleView
)

router = DefaultRouter()
router.register('vehicles', VehicleView, basename='vehicles')


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Main API',
            'endpoints': [
                '/vehicles/',
            ]
        })


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
] + router.urls
