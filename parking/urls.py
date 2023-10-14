from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FloorViewSet, SectionViewSet, LocationViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

router = DefaultRouter()
router.register(r'floors', FloorViewSet, basename='floors')
router.register(r'sections', SectionViewSet, basename='sections')
router.register(r'locations', LocationViewSet, basename='locations')

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Parking API',
            'endpoints': [
                '/floors/',
                '/sections/',
                '/locations/',
            ]
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
] + router.urls