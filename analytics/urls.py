from django.urls import path
from analytics.views import VehicleDetailsView, IDFYDetails
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vehicle-details', VehicleDetailsView, basename='vehicle-details')


urlpatterns = [
    path('idfy-details/', IDFYDetails.as_view(), name='idfy-details'),
] + router.urls