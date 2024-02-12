from rest_framework.response import Response
from .models import Parking, CCTV
from organization.models import Organization
from .serializers import ParkingSerializer, CCTVSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class ParkingView(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Parking.objects.filter(isActive=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ParkingSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        parking = Parking.objects.get(id=pk)
        user = request.user
        if parking.organization.owner == user:
            serializer = ParkingSerializer(parking)
            return Response(serializer.data)
        else:
            return Response({"error": "You are not authorized to view this parking."})

    def create(self, request):
        user = request.user
        organizationId = request.data['organization']
        organization = Organization.objects.get(id=organizationId)
        if organizationId is None:
            return Response({"error": "Organization is required."})
        if organization.owner != user:
            return Response({"error": "You are not authorized to create parking for this organization."})
        if user.is_active == False:
            return Response({"error": "Your account is not active."})
        serializer = ParkingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def update(self, request, pk=None):
        parking = Parking.objects.get(id=pk)
        user = request.user
        if parking.organization.owner == user:
            serializer = ParkingSerializer(parking, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this parking."})
        
    def destroy(self, request, pk=None):
        parking = Parking.objects.get(id=pk)
        user = request.user
        if parking.organization.owner == user:
            parking.delete()
            return Response({"success": "Parking deleted successfully."})
        else:
            return Response({"error": "You are not authorized to delete this parking."})

    def partial_update(self, request, pk=None):
        parking = Parking.objects.get(id=pk)
        user = request.user
        if parking.organization.owner == user:
            serializer = ParkingSerializer(parking, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this parking."})


class CCTVView(viewsets.ModelViewSet):
    queryset = CCTV.objects.all()
    serializer_class = CCTVSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = CCTV.objects.filter(isActive=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CCTVSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        cctv = CCTV.objects.get(id=pk)
        user = request.user
        if cctv.parking.organization.owner == user:
            serializer = CCTVSerializer(cctv)
            return Response(serializer.data)
        else:
            return Response({"error": "You are not authorized to view this CCTV."})

    def create(self, request):
        user = request.user
        parkingId = request.data['parking']
        parking = Parking.objects.get(id=parkingId)
        if parkingId is None:
            return Response({"error": "Parking is required."})
        if parking.organization.owner != user:
            return Response({"error": "You are not authorized to create CCTV for this parking."})
        if user.is_active == False:
            return Response({"error": "Your account is not active."})
        serializer = CCTVSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def update(self, request, pk=None):
        cctv = CCTV.objects.get(id=pk)
        user = request.user
        if cctv.parking.organization.owner == user:
            serializer = CCTVSerializer(cctv, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this CCTV."})
        
    def destroy(self, request, pk=None):
        cctv = CCTV.objects.get(id=pk)
        user = request.user
        if cctv.parking.organization.owner == user:
            cctv.delete()
            return Response({"success": "CCTV deleted successfully."})
        else:
            return Response({"error": "You are not authorized to delete this CCTV."})

    def partial_update(self, request, pk=None):
        cctv = CCTV.objects.get(id=pk)
        user = request.user
        if cctv.parking.organization.owner == user:
            serializer = CCTVSerializer(cctv, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "You are not authorized to update this CCTV."})