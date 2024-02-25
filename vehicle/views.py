from vehicle.models import (
    Vehicle,
)
from vehicle.serializers import (
    VehicleSerializer
)
from vehicle.permissions import (
    VehiclePermission
)
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from vehicle.filters import VehicleFilter


class VehicleView(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_class = VehicleFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, VehiclePermission]

    def list(self, request, *args, **kwargs):
        try:
            vehicles = Vehicle.objects.all()
            vehicles = self.filter_queryset(vehicles)
            isPaginated = request.query_params.get('isPaginated')
            user = request.user
            vehicles = vehicles.filter(
                entry_gate__organization__owner=user)
            # for vehicle in vehicles:
            #     if vehicle.entry_gate.organization.owner != user:
            #         vehicles = vehicles.exclude(id=vehicle.id)
            if isPaginated == "false" or isPaginated is None:
                serializer = VehicleSerializer(vehicles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            page = self.paginate_queryset(vehicles)
            if page is not None:
                serializer = VehicleSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = VehicleSerializer(vehicles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Vehicle.DoesNotExist:
            return Response({"error": "No vehicles found."}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        vehicle = Vehicle.objects.get(id=pk)
        user = request.user
        if vehicle.entry_gate.organization.owner == user:
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to view this vehicle."}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        vehicle = Vehicle.objects.get(id=pk)
        user = request.user
        if vehicle.entry_gate.organization.owner == user:
            serializer = VehicleSerializer(vehicle, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update this vehicle."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        vehicle = Vehicle.objects.get(id=pk)
        user = request.user
        if vehicle.entry_gate.organization.owner == user:
            vehicle.delete()
            return Response({"success": "Vehicle deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to delete this vehicle."}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        vehicle = Vehicle.objects.get(id=pk)
        user = request.user
        if vehicle.entry_gate.organization.owner == user:
            serializer = VehicleSerializer(
                vehicle, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update this vehicle."}, status=status.HTTP_403_FORBIDDEN)


class UnverifiedVehicleView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        try:
            vehicles = Vehicle.objects.filter(verified_by=None)
            for vehicle in vehicles:
                if vehicle.entry_gate.organization.owner != user and user.email not in vehicle.entry_gate.organization.admins:
                    vehicles = vehicles.exclude(id=vehicle.id)
            page = self.paginate_queryset(vehicles)
            if page is not None:
                serializer = VehicleSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = VehicleSerializer(vehicles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Vehicle.DoesNotExist:
            return Response({"error": "No unverified vehicles found."}, status=status.HTTP_404_NOT_FOUND)


class VerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, number_plate=None):
        try:
            vehicle = Vehicle.objects.get(id=pk)
            user = request.user
            if vehicle.entry_gate.organization.owner == user or user.email in vehicle.entry_gate.organization.admins:
                vehicle.verified_by = user
                if number_plate is not None:
                    vehicle.verified_number_plate = number_plate
                if number_plate == "null":
                    vehicle.verified_number_plate = vehicle.number_plate
                vehicle.save()
                return Response({"success": "Vehicle verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You are not authorized to verify this vehicle."}, status=status.HTTP_403_FORBIDDEN)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)


class GetVehicleByOrganizationView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, organization_id=None):
        user = request.user
        try:
            vehicles = Vehicle.objects.filter(
                entry_gate__organization=organization_id)
            vehicles = vehicles.filter(
                Q(entry_gate__organization__owner=user) |
                ~Q(entry_gate__organization__admins__contains=[user.email]))
            serializer = VehicleSerializer(vehicles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vehicle.DoesNotExist:
            return Response({"error": "No vehicles found."}, status=status.HTTP_404_NOT_FOUND)
