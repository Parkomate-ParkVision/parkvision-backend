from django.db import models
from uuid import uuid4
from users.models import ParkomateUser
from django.contrib.postgres.fields import ArrayField


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(ParkomateUser, on_delete=models.CASCADE, related_name='organizations', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    entry_gates = models.IntegerField(blank=True, null=True)
    exit_gates = models.IntegerField(blank=True, null=True)
    total_slots = models.IntegerField(blank=True, null=True)
    filled_slots = models.IntegerField(blank=True, null=True)
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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='gates')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Gates"
        managed = True

    def __str__(self):
        return self.id
