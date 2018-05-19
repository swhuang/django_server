# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental
from crm.server_utils.customerField.Field import *


class ClientRentalServiceSerializer(serializers.ModelSerializer):
    serviceStatus = StatusField()
    createDate = ModifiedDateTimeField(source='gmt_create', read_only=True)

    class Meta:
        model = ProductRental
        exclude = ('gmt_create', 'gmt_modified', 'product', 'isCompleted', 'curProcOrder')
        read_only_fields = (
        'deliveryOperator', 'serviceCloseOpertator', 'finishDate', 'commodityEntry', 'serviceCompletion'
                                                                                     'store', 'completeMode',
        'retStore')

    def create(self, validated_data):
        sNo = validated_data.pop('serviceNo', None)
        if not sNo:
            return super(ClientRentalServiceSerializer, self).create(validated_data)
        else:
            try:
                instance = ProductRental.objects.get(serviceNo=sNo)
            except ProductRental.DoesNotExist:
                raise serializers.ValidationError(detail={"message": "无效的serviceNo"})

            return self.update(instance, validated_data)
