from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from analytics.serializers import IDFYRequestSerializer, VehicleDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from analytics.models import VehicleDetails
from utils.idfy import get_idfy_request_id, get_vehicle_details
import time


class IDFYDetails(GenericAPIView):
    serializer_class = IDFYRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.data['challan_blacklist_details'] == "false":
                request.data['challan_blacklist_details'] = False
            else:
                request.data['challan_blacklist_details'] = True
            request_id = get_idfy_request_id(
                request.data['rc_number'], 
                request.data['challan_blacklist_details']
            )
            print(request_id, flush=True)
            time.sleep(2)
            response = get_vehicle_details(
                request_id
            )
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        

class VehicleDetailsView(ModelViewSet):
    serializer_class = VehicleDetailsSerializer
    permission_classes = [IsAuthenticated]
    queryset = VehicleDetails.objects.all()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk):
        try:
            details = VehicleDetails.objects.get(vehicle__id=pk)
            serializer = self.serializer_class(details)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request):
        try:
            fields = {
                "vehicle": request.data['vehicle'],
                "owner_name": request.data['owner_name'],
                "vehicle_class": request.data['vehicle_class'],
                "norms_type": request.data['norms_type'],
                "manufacturer_model": request.data['manufacturer_model'],
                "insurance_validity": request.data['insurance_validity'],
                "address": request.data['address'],
                "seating_capacity": request.data['seating_capacity'],
                "manufacturing_year": request.data['manufacturing_year'],
                "manufacturer": request.data['manufacturer'],
                "state": request.data['state'],
                "fuel_type": request.data['fuel_type'],
                "puc_valid_type": request.data['puc_valid_type'],
                "insurance_name": request.data['insurance_name']
            }
            serializer = self.serializer_class(data=fields)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk):
        return Response('Update not allowed', status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        return Response('Partial update not allowed', status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        return Response('Delete not allowed', status=status.HTTP_400_BAD_REQUEST)