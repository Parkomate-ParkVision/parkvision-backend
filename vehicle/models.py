from django.db import models
from uuid import uuid4
from organization.models import Gate


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    number_plate = models.CharField(max_length=255, blank=True, null=True, unique=True)
    cropped_image = models.URLField(blank=True, null=True, unique=True)
    vehicle_image = models.URLField(blank=True, null=True, unique=True)
    prediction = models.CharField(max_length=255, blank=True, null=True)
    entry_gate = models.ForeignKey(Gate, on_delete=models.CASCADE, related_name='entry_vehicle', blank=True, null=True)
    exit_gate = models.ForeignKey(Gate, on_delete=models.CASCADE, related_name='exit_vehicle', blank=True, null=True)
    entry_time = models.DateTimeField(blank=True, null=True)
    exit_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
