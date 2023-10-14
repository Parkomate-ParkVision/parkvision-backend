from django.db import models
from api.models import Organization
import uuid

class Floor(models.Model):
    number = models.IntegerField(primary_key=True, unique=True, auto_created=True, default=1)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return "Floor " + str(self.number)
    
class Section(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True, auto_created=True, default='A')
    floor = models.ForeignKey(Floor, related_name='sections', on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return "Floor " + str(self.floor.number) + ' - Section ' + self.name
    
class Location(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, auto_created=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=True, null=True)
    section = models.ForeignKey(Section, to_field='name', related_name='locations', on_delete=models.CASCADE)
    isOccupied = models.BooleanField(default=False)
    isAllocated = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.section.floor.number) + '-' + str(self.section.name) + '-' + str(self.pk)
