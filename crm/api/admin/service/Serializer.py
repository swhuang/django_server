# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental
from crm.server_utils.customerField.Field import *


class RentalServiceSerializer(serializers.ModelSerializer):
    serviceStatus = StatusField()
    createDate = ModifiedDateTimeField(source='gmt_create')
    product = JsonField()

    class Meta:
        model = ProductRental
        exclude = ('gmt_create', 'gmt_modified', 'createdBy', 'create_user', 'completeMode', 'isCompleted')


class ClaimGoodSerializer(serializers.Serializer):
    result = {
        '1': '失败',
        '2': '成功'
    }

    servtype = {
        'r': '租赁',
        's': '销售',
        'p': '套餐',
    }

    serviceNo = serializers.CharField(max_length=25, write_only=True)
    serviceType = serializers.CharField(max_length=1, write_only=True)
    productid = serializers.CharField(max_length=15, write_only=True)
    deliveryOperator = serializers.CharField(max_length=100, write_only=True)
    deliveryStore = serializers.CharField(max_length=15, write_only=True)
    deliveryMode = serializers.CharField(max_length=1, write_only=True)
    serialNumber = serializers.CharField(max_length=10, write_only=True)
    logisticsCompany = serializers.CharField(max_length=20, write_only=True)
    trackingNumber = serializers.CharField(max_length=20, write_only=True)
    claimResult = serializers.CharField(max_length=1, default='1', read_only=True)
    serviceStatus = StatusField(read_only=True)

    class Meta:
        fields = ('serviceNo', 'productid', 'deliveryOperator', 'deliveryStore', 'deliveryMode', 'serialNumber',
                  'logisticsCompany', 'trackingNumber', 'claimResult', 'serviceStatus')

    def create(self, validated_data):
        try:
            pass
        pass
