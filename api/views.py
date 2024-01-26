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
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def list(self, request):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            serializer = OrganizationSerializer(organization)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to view this organization."})

    def create(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def update(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            serializer = OrganizationSerializer(
                organization, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this organization."})

    def destroy(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            organization.delete()
            return Response({"success": "Organization deleted successfully."})
        else:
            return Response({"error": "You are not authorized to delete this organization."})

    def partial_update(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            serializer = OrganizationSerializer(
                organization, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this organization."})


class GateViewSet(ModelViewSet):
    queryset = Gate.objects.all()
    serializer_class = GateSerializer

    def list(self, request):
        gates = Gate.objects.all()
        user = request.user
        for gate in gates:
            if gate.organization.owner != user:
                gates.remove(gate)
        serializer = GateSerializer(gates, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        gate = Gate.objects.get(id=pk)
        organization = gate.organization
        user = request.user
        if organization.owner == user:
            serializer = GateSerializer(gate)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to view this gate."})

    def create(self, request):
        serializer = GateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def update(self, request, pk=None):
        gate = Gate.objects.get(id=pk)
        organization = gate.organization
        user = request.user
        if organization.owner == user:
            serializer = GateSerializer(gate, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this gate."})

    def destroy(self, request, pk=None):
        gate = Gate.objects.get(id=pk)
        organization = gate.organization
        user = request.user
        if organization.owner == user:
            gate.delete()
            return Response({"success": "Gate deleted successfully."})
        else:
            return Response({"error": "You are not authorized to delete this gate."})

    def partial_update(self, request, pk=None):
        gate = Gate.objects.get(id=pk)
        organization = gate.organization
        user = request.user
        if organization.owner == user:
            serializer = GateSerializer(gate, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this gate."})


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def list(self, request):
        vehicles = Vehicle.objects.all()
        user = request.user
        for vehicle in vehicles:
            if vehicle.entry_gate.organization.owner != user:
                vehicles.remove(vehicle)
        serializer = VehicleSerializer(vehicles, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        vehicle = Vehicle.objects.get(id=pk)
        user = request.user
        if vehicle.entry_gate.organization.owner == user:
            serializer = VehicleSerializer(vehicle)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to view this vehicle."})

    def create(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def update(self, request, pk=None):
        vehicle = Vehicle.objects.get(id=pk)
        user = request.user
        if vehicle.entry_gate.organization.owner == user:
            serializer = VehicleSerializer(vehicle, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this vehicle."})

    def destroy(self, request, pk=None):
        vehicle = Vehicle.objects.get(id=pk)
        user = request.user
        if vehicle.entry_gate.organization.owner == user:
            vehicle.delete()
            return Response({"success": "Vehicle deleted successfully."})
        else:
            return Response({"error": "You are not authorized to delete this vehicle."})

    def partial_update(self, request, pk=None):
        vehicle = Vehicle.objects.get(id=pk)
        user = request.user
        if vehicle.entry_gate.organization.owner == user:
            serializer = VehicleSerializer(
                vehicle, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this vehicle."})
