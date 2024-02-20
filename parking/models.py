from django.db import models
from organization.models import Organization
import uuid


class Parking(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='parkings')
    name = models.CharField(max_length=255)
    totalSlots = models.IntegerField(default=0)
    availableSlots = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.organization} - {self.name}"


class CCTV(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    parking = models.ForeignKey(
        Parking, on_delete=models.CASCADE, related_name='cctvs')
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.parking.name} - {self.name}"
