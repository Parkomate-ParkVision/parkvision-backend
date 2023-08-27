from django.db import models
from uuid import uuid4

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    entry_gates = models.IntegerField(blank=True, null=True)
    exit_gates = models.IntegerField(blank=True, null=True)
    total_slots = models.IntegerField(blank=True, null=True)
    filled_slots = models.IntegerField(blank=True, null=True)

    def __str__(self):
            return self.name