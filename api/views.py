from api.models import (
    Organization,
    Gate,
    Vehicle
)
from api.serializers import (
    OrganizationSerializer,
    GateSerializer,
    VehicleSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class GateViewSet(ModelViewSet):
    queryset = Gate.objects.all()
    serializer_class = GateSerializer

class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer