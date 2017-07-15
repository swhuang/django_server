from __future__ import unicode_literals

from django.db import models


# Create your models here.
class ParkingInfo(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()#DecimalField(max_digits=10, decimal_places=7)
    max_parkingCapacity = models.IntegerField()
    parkingCount = models.IntegerField()
    address = models.CharField(max_length=200)
    prices = models.CharField(max_length=200)
    workingtime = models.CharField(max_length=50)

    def __unicode__(self):
        return self.pid

class TimeTable(models.Model):
    primary_key = models.IntegerField(default=0)
    teacherid = models.IntegerField(default=0)
    courseid = models.IntegerField(default=0)
    classid = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)
    def __unicode__(self):
        return  self.primary_key

class Teacher(models.Model):
    pid = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.id

class Course(models.Model):
    pid = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.id