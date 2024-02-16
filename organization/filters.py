from backend.filters import ParkVisionDateFilter
from vehicle.models import Vehicle

class VehicleFilter(ParkVisionDateFilter):
    class Meta:
        model = Vehicle
        fields = (
            'fromDate',
            'toDate',
            'entry_time',
            'exit_time',
            'entry_gate__organization',
            'exit_gate__organization'
        )