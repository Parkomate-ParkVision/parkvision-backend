from django.db import models
from uuid import uuid4

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    address = models.TextField(blank=False, null=False)
    entry_gates = models.IntegerField(blank=False, null=False)
    exit_gates = models.IntegerField(blank=False, null=False)
    total_slots = models.IntegerField(blank=False, null=False)
    filled_slots = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

class Gate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='gates')

    def __str__(self):
        return self.id

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    number_plate = models.CharField(max_length=255, blank=False, null=False, unique=True)
    cropped_image = models.URLField(blank=False, null=False, unique=True)
    vehicle_image = models.URLField(blank=False, null=False, unique=True)
    prediction = models.CharField(max_length=255, blank=False, null=False)
    entry_gate = models.OneToOneField(Gate, on_delete=models.CASCADE, related_name='entry_gate', blank=True, null=True)
    exit_gate = models.OneToOneField(Gate, on_delete=models.CASCADE, related_name='exit_gate', blank=True, null=True)
    entry_time = models.DateTimeField(blank=True, null=True)
    exit_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.id