from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from analytics.serializers import IDFYRequestSerializer, VehicleDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from analytics.models import VehicleDetails
from utils.idfy import get_idfy_request_id, get_vehicle_details
import time
from backend.settings import log_db_queries
from django.core.cache import cache
import redis 


redis_instance = redis.StrictRedis(host='redis', port=6379, db=1)


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

            while True:
                response = get_vehicle_details(request_id)
                if response[0]['status'] == 'completed':
                    break
                time.sleep(1)

            request.data['owner_name'] = response[0]['result']['extraction_output']['owner_name']
            request.data['vehicle_class'] = response[0]['result']['extraction_output']['vehicle_class']
            request.data['norms_type'] = response[0]['result']['extraction_output']['norms_type']
            request.data['manufacturer_model'] = response[0]['result']['extraction_output']['manufacturer_model']
            request.data['insurance_validity'] = response[0]['result']['extraction_output']['insurance_validity']
            request.data['address'] = response[0]['result']['extraction_output']['current_address']
            request.data['seating_capacity'] = response[0]['result']['extraction_output']['seating_capacity']
            request.data['manufacturing_year'] = response[0]['result']['extraction_output']['m_y_manufacturing']
            request.data['manufacturer'] = response[0]['result']['extraction_output']['manufacturer']
            request.data['state'] = response[0]['result']['extraction_output']['state']
            request.data['fuel_type'] = response[0]['result']['extraction_output']['fuel_type']
            request.data['puc_valid_upto'] = response[0]['result']['extraction_output']['puc_valid_upto']
            request.data['insurance_name'] = response[0]['result']['extraction_output']['insurance_name']
            try:
                return VehicleDetailsView().create(request)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        

class VehicleDetailsView(ModelViewSet):
    serializer_class = VehicleDetailsSerializer
    permission_classes = [IsAuthenticated]
    queryset = VehicleDetails.objects.all()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        try:
            cache_key = f"vehicle_details_user_{request.user.id}"
            
            if cache_key in cache:
                data = cache.get(cache_key)
            else:
                serializer = self.serializer_class(self.queryset, many=True)
                data = serializer.data
                cache.set(cache_key, data, timeout=3600)  # Cache for 1 hour
            
            return Response(data, status=status.HTTP_200_OK)
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
                "puc_valid_upto": request.data['puc_valid_upto'],
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