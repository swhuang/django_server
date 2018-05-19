# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental
from crm.server_utils.customerField.Field import *


class OrderSerializer(serializers.ModelSerializer):

    createDate = ModifiedDateTimeField(source='gmt_create', read_only=True)

    class Meta:
        model = ProductRental
        exclude = ('gmt_create', 'gmt_modified', 'product', 'isCompleted', 'curProcOrder')
        read_only_fields = ()

    def create(self, validated_data):
        pass
