from organization.models import (
    Organization,
    Gate,
)
from organization.serializers import (
    OrganizationSerializer,
    GateSerializer
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class OrganizationView(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        organizations = Organization.objects.all()
        page = self.paginate_queryset(organizations)
        if page is not None:
            serializer = OrganizationSerializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            serializer = OrganizationSerializer(organization)
            return Response(serializer.data)
        else:
            return Response({"error": "You are not authorized to view this organization."})

    def create(self, request):
        user = request.user
        request.data.update({'owner': user.id})
        serializer = OrganizationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
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


class GateView(ModelViewSet):
    queryset = Gate.objects.all()
    serializer_class = GateSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        gates = Gate.objects.all()
        user = request.user
        for gate in gates:
            if gate.organization.owner != user:
                gates.remove(gate)
        page = self.paginate_queryset(gates)
        if page is not None:
            serializer = GateSerializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

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