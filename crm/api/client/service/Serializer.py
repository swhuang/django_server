# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental
from crm.server_utils.customerField.Field import *
from crm.server_utils.base.DQS import SingletonFactory
from crm.server_utils.customerField.structure import *


class ClientRentalServiceSerializer(serializers.ModelSerializer):
    serviceStatus = StatusField()
    createDate = ModifiedDateTimeField(source='gmt_create', read_only=True)

    class Meta:
        model = ProductRental
        exclude = ('gmt_create', 'gmt_modified', 'product', 'isCompleted', 'curProcOrder', 'daily_amount')
        read_only_fields = (
        'deliveryOperator', 'serviceCloseOpertator', 'finishDate', 'commodityEntry', 'serviceCompletion'
                                                                                     'store', 'completeMode',
        'retStore')

    def create(self, validated_data):
        sNo = validated_data.pop('serviceNo', None)
        if not sNo:

            inst = super(ClientRentalServiceSerializer, self).create(validated_data)
            SingletonFactory.getServiceQueue().putitem((inst.serviceNo, SERVICE_RENTAL))
            return inst
        else:
            try:
                instance = ProductRental.objects.get(serviceNo=sNo)
            except ProductRental.DoesNotExist:
                raise serializers.ValidationError(detail={"message": "无效的serviceNo"})

            return self.update(instance, validated_data)
