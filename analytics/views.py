from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from analytics.utils import get_vehicle_details, get_idfy_request_id
from analytics.serializers import IDFYRequestSerializer, VehicleDetailsSerializer
from rest_framework.permissions import IsAuthenticated


class VehicleDetails(GenericAPIView):
    serializer_class = IDFYRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            rc_number = request.data['rc_number']
            challan_blacklist_details = request.data['challan_blacklist_details']
            if challan_blacklist_details == 'true':
                challan_blacklist_details = True
            else:
                challan_blacklist_details = False
            request_id = request.data['request_id'] if 'request_id' in request.data else None
            if request_id is None:
                request_id = get_idfy_request_id(rc_number, challan_blacklist_details)['request_id']
                print(request_id, flush=True)
            response = get_vehicle_details(request_id)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)