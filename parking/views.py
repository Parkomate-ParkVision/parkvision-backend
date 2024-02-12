from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response

from .models import Floor, Section, Location
from .serializers import FloorSerializer, SectionSerializer, LocationSerializer

from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Floor.objects.filter(isActive=True)
        serializer = FloorSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response({'message': 'Floor cannot be updated! Delete and create a new one instead.'})

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'Floor cannot be updated! Delete and create a new one instead.'})

    def destroy(self, request, *args, **kwargs):
        floor = Floor.objects.get(number=kwargs['pk'])
        floor.isActive = False
        floor.save()
        return Response({'message': 'Floor was deleted successfully!'})


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Section.objects.filter(isActive=True)
        serializer = SectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response({'message': 'Section cannot be updated! Delete and create a new one instead!'})

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'Section cannot be updated! Delete and create a new one instead!'})

    def destroy(self, request, *args, **kwargs):
        section = Section.objects.get(name=kwargs['pk'])
        section.is_active = False
        section.save()
        return Response({'message': 'Section was deleted successfully!'})


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Location.objects.filter(isActive=True)
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        jsonData = JSONParser().parse(request)
        location = Location.objects.get(pk=jsonData['pk'])
        location.isActive = False
        location.save()
        return Response({'message': 'Location was deleted successfully!'})
