from django.db import models
from vehicle.models import Vehicle
import uuid


class VehicleDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_details')
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    vehicle_class = models.CharField(max_length=255, blank=True, null=True)
    norms_type = models.CharField(max_length=255, blank=True, null=True)
    manufacturer_model = models.CharField(max_length=255, blank=True, null=True)
    insurance_validity = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    seating_capacity = models.IntegerField(blank=True, null=True)
    manufacturing_year = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    fuel_type = models.CharField(max_length=255, blank=True, null=True)
    puc_valid_upto = models.CharField(max_length=255, blank=True, null=True)
    insurance_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'vehicle_details'
        verbose_name_plural = 'Vehicle Details'
        ordering = ['-insurance_validity', '-puc_valid_upto', '-id']

    def __str__(self):
        return str(self.vehicle)
