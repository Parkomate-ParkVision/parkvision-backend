from django.db import models
from organization.models import Organization
from vehicle.models import Vehicle
import uuid


class PerHourVehicleCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='per_hour_vehicle_count')
    vehicleType = models.CharField(max_length=50)
    vehicleCount = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'per_hour_vehicle_count'
        verbose_name_plural = 'Per Hour Vehicle Count'
        ordering = ['-createdAt']

    def __str__(self):
        return str(self.vehicle_count)


class VehicleDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicleDetails')
    vehicleType = models.CharField(max_length=50, blank=True, null=True)
    ownerAddress = models.CharField(max_length=500, blank=True, null=True)
    permitNo = models.CharField(max_length=150, blank=True, null=True)
    permitType = models.CharField(max_length=150, blank=True, null=True)
    permitValidityFrom = models.DateField(blank=True, null=True)
    permitValidityTo = models.DateField(blank=True, null=True)
    registrationDate = models.DateField(blank=True, null=True)
    registrationNumber = models.CharField(max_length=250, blank=True, null=True)
    insurancePolicyNo = models.CharField(max_length=250, blank=True, null=True)
    ownerMobileNo = models.CharField(max_length=250, blank=True, null=True)
    insuranceName = models.CharField(max_length=250, blank=True, null=True)
    permanentAddress = models.CharField(max_length=500, blank=True, null=True)
    ownerName = models.CharField(max_length=250, blank=True, null=True)
    manufacturer = models.CharField(max_length=250, blank=True, null=True)
    manufacturerModel = models.CharField(max_length=250, blank=True, null=True)
    pucValidUpto = models.DateField(blank=True, null=True)
    fuelType = models.CharField(max_length=250, blank=True, null=True)
    seatingCapacity = models.CharField(max_length=250, blank=True, null=True)
    registeredPlace = models.CharField(max_length=250, blank=True, null=True)
    fatherName = models.CharField(max_length=250, blank=True, null=True)
    currentAddress = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'vehicle_details'
        verbose_name_plural = 'Vehicle Details'
        ordering = ['-registrationDate']

    def __str__(self):
        return str(self.vehicle)
