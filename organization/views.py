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
from users.models import ParkomateUser
from users.serializers import ParkomateUserSerializer   
from django.db import transaction
import random
from utils.emails import send_email


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
        request.data.update({'admins': []})
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
                    password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8))
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
                    return Response({"success": "Admin added successfully."})
            else:
                return Response({"error": "You are not authorized to add admin to this organization."})
        except Exception as e:
            return Response({"error": str(e)})
        
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
                return Response({"success": "Admin removed successfully."})
        else:
            return Response({"error": "You are not authorized to remove admin from this organization."})
        
    def list(self, request):
        id = request.data['organization']
        organization = Organization.objects.get(id=id)
        user = request.user
        if organization.owner == user:
            admins = organization.admins
            serializer = ParkomateUserSerializer(admins, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "You are not authorized to view admins of this organization."})
        
    def retrieve(self, request):
        id = request.data['organization']
        organization = Organization.objects.get(id=id)
        user = request.user
        if organization.owner == user:
            email = request.data['email']
            admin = ParkomateUser.objects.get(email=email)
            serializer = ParkomateUserSerializer(admin)
            return Response(serializer.data)
        else:
            return Response({"error": "You are not authorized to view admins of this organization."})
        
    def update(self, request, pk=None):
        return Response({"error": "You are not authorized to update admins of this organization."})
        
    def partial_update(self, request, pk=None):
        return Response({"error": "You are not authorized to update admins of this organization."})