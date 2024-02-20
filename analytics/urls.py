from django.urls import path
from analytics.views import VehicleDetails

urlpatterns = [
    path('vehicle-details/', VehicleDetails.as_view(), name='vehicle-details'),
]