from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ParkingInfo(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    max_parkingCapacity = models.IntegerField()
    parkingCount = models.IntegerField()
    address = models.CharField(max_length=200)
    prices = models.CharField(max_length=200)
    workingtime = models.CharField(max_length=50)
    def __unicode__(self):
        return self.pid