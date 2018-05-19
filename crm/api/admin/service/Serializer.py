# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental
from crm.server_utils.customerField.Field import *




class RentalServiceSerializer(serializers.ModelSerializer):

    serviceStatus = StatusField()
    createDate = ModifiedDateTimeField(source='gmt_create')

    class Meta:
        model = ProductRental
        exclude = ('gmt_create', 'gmt_modified', 'product')