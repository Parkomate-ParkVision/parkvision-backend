from django.db import models
from uuid import uuid4
from users.models import ParkomateUser
from django.contrib.postgres.fields import ArrayField


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(ParkomateUser, on_delete=models.CASCADE,
                              related_name='organizations', blank=True, null=True)
    admins = ArrayField(models.EmailField(
        name='adminEmail', unique=True), blank=True, null=True, default=list)
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    entry_gates = models.IntegerField(blank=True, null=True)
    exit_gates = models.IntegerField(blank=True, null=True)
    total_slots = models.IntegerField(blank=True, null=True)
    filled_slots = models.IntegerField(blank=True, null=True)
    parking_threshold = models.IntegerField(
        blank=True, null=True)
    occupancy_limit = models.IntegerField(
        blank=True, null=True)  # in minutes
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    penalty_charges = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)  # per hour after occupancy_threshold
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Organizations"
        managed = True

    def __str__(self):
        return self.name


class Gate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='gates')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Gates"
        managed = True

    def __str__(self):
        return str(self.id)
