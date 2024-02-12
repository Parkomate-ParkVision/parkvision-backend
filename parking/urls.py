from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ParkingView, CCTVView
from rest_framework.views import APIView
from rest_framework.response import Response

router = DefaultRouter()
router.register(r'parkings', ParkingView, basename='parkings')
router.register(r'cctvs', CCTVView, basename='cctvs')

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Parking API',
            'endpoints': [
                '/parkings/',
                '/cctvs/',
            ]
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
] + router.urls