from organization.models import (
    Organization,
    Gate,
)
from organization.serializers import (
    OrganizationSerializer,
    GateSerializer
)
from organization.permissions import (
    OrganizationPermission,
    GatePermission,
    DashboardPermission
)

from vehicle.models import Vehicle
from organization.filters import VehicleFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from users.models import ParkomateUser
from users.serializers import ParkomateUserSerializer
from django.db import transaction
from django.db.models import Count, Q
from django.db.models.functions import TruncWeek, TruncMonth, TruncDay
import random
from utils.emails import send_email
from rest_framework import status
from rest_framework.generics import ListAPIView
from datetime import datetime, timedelta


class DashboardView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filterset_class = VehicleFilter

    def list(self, request, pk=None):
        user = request.user
        try:
            organization = Organization.objects.get(id=pk)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
        vehicles = Vehicle.objects.filter(
            entry_gate__organization=organization)
        if user.email not in organization.admins or organization.owner != user:
            return Response({"error": "You are not authorized to view this organization's dashboard."}, status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                daily_entries = vehicles.filter(entry_time__gte=datetime.now() - timedelta(days=1)).count()
                weekly_entries = vehicles.filter(entry_time__gte=datetime.now() - timedelta(days=7)).count()
                monthly_entries = vehicles.filter(entry_time__gte=datetime.now() - timedelta(days=30)).count()
                daily_exits = vehicles.filter(exit_time__gte=datetime.now() - timedelta(days=1)).count()
                weekly_exits = vehicles.filter(exit_time__gte=datetime.now() - timedelta(days=7)).count()
                monthly_exits = vehicles.filter(exit_time__gte=datetime.now() - timedelta(days=30)).count()

                total_slots = organization.total_slots
                filled_slots = organization.filled_slots
                percentage_occupied = (filled_slots / total_slots) * 100

                average_occupancy = 0
                for vehicle in vehicles:
                    if vehicle.exit_time is not None:
                        average_occupancy += (vehicle.exit_time -
                                              vehicle.entry_time).seconds / 3600
                average_occupancy = average_occupancy / vehicles.count()

                DAYS = {
                    0: "Monday",
                    1: "Tuesday",
                    2: "Wednesday",
                    3: "Thursday",
                    4: "Friday",
                    5: "Saturday",
                    6: "Saturday",
                }
                daily_data_dict = {
                    'Monday': 0,
                    'Tuesday': 0,
                    'Wednesday': 0,
                    'Thursday': 0,
                    'Friday': 0,
                    'Saturday': 0,
                    'Sunday': 0
                }
                daily_data = vehicles.exclude(exit_time=None).annotate(
                    day_start=TruncDay('entry_time')
                ).values('day_start').annotate(count=Count('id')).order_by(
                    'day_start'
                )
                for data in daily_data:
                    day = data['day_start'].weekday()
                    daily_data_dict[DAYS[int(day)]] += data['count']

                weekly_data = vehicles.exclude(exit_time=None).annotate(
                    week_start=TruncWeek('entry_time')
                ).values('week_start').annotate(count=Count('id')).order_by(
                    'week_start'
                )
                monthly_data = vehicles.exclude(exit_time=None).annotate(
                    month_start=TruncMonth('entry_time')
                ).values('month_start').annotate(count=Count('id')).order_by(
                    'month_start'
                )

                vehicle_types = vehicles.exclude(exit_time=None).values(
                    'vehicle_type'
                ).annotate(
                    count=Count('id')
                ).order_by(
                    'vehicle_type'
                )

                average_occupancy_by_vehicle_type = {}
                for vehicle_type in vehicle_types:
                    average_occupancy_by_vehicle_type[vehicle_type['vehicle_type']] = 0
                    for vehicle in vehicles:
                        if vehicle.vehicle_type == vehicle_type['vehicle_type']:
                            if vehicle.exit_time is not None:
                                average_occupancy_by_vehicle_type[vehicle_type['vehicle_type']] += (
                                    vehicle.exit_time - vehicle.entry_time).seconds / 3600
                    average_occupancy_by_vehicle_type[vehicle_type['vehicle_type']
                                                      ] = average_occupancy_by_vehicle_type[vehicle_type['vehicle_type']] / vehicle_type['count']

                return Response({
                    "organization": organization.name,
                    "daily_entries": daily_entries,
                    "weekly_entries": weekly_entries,
                    "monthly_entries": monthly_entries,
                    "daily_exits": daily_exits,
                    "weekly_exits": weekly_exits,
                    "monthly_exits": monthly_exits,
                    "total_slots": total_slots,
                    "filled_slots": filled_slots,
                    "percentage_occupied": percentage_occupied,
                    "average_occupancy": average_occupancy,
                    "daily_distribution": daily_data_dict,
                    "daily_data": daily_data,
                    "weekly_data": weekly_data,
                    "monthly_data": monthly_data,
                    "vehicle_types": vehicle_types,
                    "average_occupancy_by_vehicle_type": average_occupancy_by_vehicle_type
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganizationView(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        current_user = request.user
        if current_user.is_superuser:
            organizations = Organization.objects.all()
            page = self.paginate_queryset(organizations)
            if page is not None:
                serializer = OrganizationSerializer(
                    page, context={'request': request}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        organizations = Organization.objects.filter(
            Q(owner=current_user) | Q(admins__contains=[current_user.email]))
        page = self.paginate_queryset(organizations)
        if page is not None:
            serializer = OrganizationSerializer(
                page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            serializer = OrganizationSerializer(organization)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to view this organization."}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        request.data.update({'admins': []})
        serializer = OrganizationSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            serializer = OrganizationSerializer(
                organization, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update this organization."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            organization.delete()
            return Response({"success": "Organization deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You are not authorized to delete this organization."}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            serializer = OrganizationSerializer(
                organization, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update this organization."}, status=status.HTTP_403_FORBIDDEN)


class GateView(ModelViewSet):
    queryset = Gate.objects.all()
    serializer_class = GateSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        gates = Gate.objects.all()
        user = request.user
        for gate in gates:
            if gate.organization.owner != user and user.email not in gate.organization.admins:
                gates.remove(gate)
        page = self.paginate_queryset(gates)
        if page is not None:
            serializer = GateSerializer(
                page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        gate = Gate.objects.get(id=pk)
        organization = gate.organization
        user = request.user
        if organization.owner == user or user.email in organization.admins:
            serializer = GateSerializer(gate)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to view this gate."}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        serializer = GateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        gate = Gate.objects.get(id=pk)
        organization = gate.organization
        user = request.user
        if organization.owner == user or user.email in organization.admins:
            serializer = GateSerializer(gate, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update this gate."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        gate = Gate.objects.get(id=pk)
        organization = gate.organization
        user = request.user
        if organization.owner == user:
            gate.delete()
            return Response({"success": "Gate deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You are not authorized to delete this gate."}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        gate = Gate.objects.get(id=pk)
        organization = gate.organization
        user = request.user
        if organization.owner == user or user.email in organization.admins:
            serializer = GateSerializer(gate, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update this gate."}, status=status.HTTP_403_FORBIDDEN)


class AdminView(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            id = request.data['organization']
            organization = Organization.objects.get(id=id)
            user = request.user
            if organization.owner == user:
                email = request.data['email']
                if email is None:
                    return Response({"error": "Email is required."})
                with transaction.atomic():
                    existing_user = ParkomateUser.objects.filter(email=email)
                    if existing_user.exists():
                        return Response({"error": "User with this email already exists."})
                    password = ''.join(random.choices(
                        'abcdefghijklmnopqrstuvwxyz1234567890', k=8))
                    user = ParkomateUser.objects.create(name=request.data['email'],
                                                        email=email,
                                                        phone=request.data['phone'])
                    user.set_password(password)
                    user.save()
                    send_email(
                        receiver=email,
                        subject='Parkomate Account Password',
                        message=f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Welcome to ParkVision</title>
                        </head>
                        <body style="font-family: Arial, sans-serif; text-align: center;">
                            <div class="container" style="max-width: 600px; margin: 0 auto; background-color: #f4f2ee; padding: 25px; border-radius: 10px;">
                                <h1 style="margin-top: 2.5rem; color: #8DBF41;">Welcome to ParkVision!</h1>
                                <p style="margin-top: 1.25rem; font-size: 16px; line-height: 1.5;">
                                    Dear user, welcome to ParkVision, a dashboard for managing and analyzing your organization's parking needs.
                                </p>
                                <p style="margin-top: 1.25rem; font-size: 16px; line-height: 1.5;">
                                    Here are your credentials:
                                </p>
                                <p style="font-size: 16px; line-height: 1.5;">
                                    Email: <strong>{email}</strong><br>
                                    Password: <strong>{password}</strong>
                                </p>
                                <p style="margin-top: 1.25rem; font-size: 16px; line-height: 1.5;">
                                    Login to your ParkVision dashboard and start managing your organization's parking needs!
                                </p>
                            </div>
                        </body>
                        </html>
                        """
                    )
                    organization.admins.append(email)
                    organization.save()
                    return Response({"success": "Admin added successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "You are not authorized to add admin to this organization."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        organization = Organization.objects.get(id=pk)
        user = request.user
        if organization.owner == user:
            with transaction.atomic():
                email = request.data['email']
                if email is None:
                    return Response({"error": "Email is required."})
                organization.admins.remove(email)
                organization.save()
                user = ParkomateUser.objects.get(email=email)
                user.delete()
                return Response({"success": "Admin removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to remove admin from this organization."}, status=status.HTTP_403_FORBIDDEN)

    def list(self, request):
        id = request.data['organization']
        organization = Organization.objects.get(id=id)
        user = request.user
        if organization.owner == user:
            admins = organization.admins
            serializer = ParkomateUserSerializer(admins, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to view admins of this organization."}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request):
        id = request.data['organization']
        organization = Organization.objects.get(id=id)
        user = request.user
        if organization.owner == user:
            email = request.data['email']
            admin = ParkomateUser.objects.get(email=email)
            serializer = ParkomateUserSerializer(admin)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to view admins of this organization."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        return Response({"error": "You are not authorized to update admins of this organization."}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        return Response({"error": "You are not authorized to update admins of this organization."}, status=status.HTTP_403_FORBIDDEN)
