from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from vehicle.views import (
    VehicleView,
    VerificationView,
    UnverifiedVehicleView,
    GetVehicleByOrganizationView
)

router = DefaultRouter()
router.register('vehicles', VehicleView, basename='vehicles')


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Main API',
            'endpoints': [
                '/vehicles/',
                '/verify-vehicle/<str:pk>/<str:number_plate>/',
                '/unverified-vehicles/',
            ]
        })


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('verify-vehicle/<str:pk>/<str:number_plate>/',
         VerificationView.as_view(), name="verify-vehicle"),
    path('unverified-vehicles/', UnverifiedVehicleView.as_view(),
         name="unverified-vehicles"),
    path('organization-vehicles/<str:organization_id>/',
         GetVehicleByOrganizationView.as_view(),
         name="organization-vehicles")
] + router.urls
