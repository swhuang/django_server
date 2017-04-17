from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ParkingInfo(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=100)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    max_parkingCapacity = models.IntegerField()
    parkingCount = models.IntegerField()
    def __unicode__(self):
        return self.pid