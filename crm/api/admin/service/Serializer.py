# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental
from crm.server_utils.customerField.Field import *
from crm.server_utils.base import FSM as fsm
import logging


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
    claimResult = serializers.SerializerMethodField()
    #serializers.CharField(max_length=1, default='1', read_only=True)
    serviceStatus = StatusField(read_only=True)

    def get_claimResult(self, obj):
        if hasattr(self, 'result'):
            return self.result
        else:
            return '1'

    class Meta:
        fields = ('serviceNo', 'productid', 'deliveryOperator', 'deliveryStore', 'deliveryMode', 'serialNumber',
                  'logisticsCompany', 'trackingNumber', 'claimResult', 'serviceStatus')

    def create(self, validated_data):
        servtype = validated_data.pop('serviceType', None)
        # ignore deliveryOperator deliveryStore
        validated_data.pop('deliveryOperator', None)
        validated_data.pop('deliveryStore', None)


        if servtype not in self.servtype.keys():
            raise serializers.ValidationError("服务类型错误")
        try:
            servid = validated_data.pop('serviceNo', None)
            if servtype == 'r':
                serv = ProductRental.objects.get(serviceNo=servid)
            else:
                #TODO
                raise NotImplementedError
        except Exception, e:
            logging.getLogger('django').error(e)
            raise serializers.ValidationError(u'服务不存在')

        for attr, value in validated_data.items():
            setattr(serv, attr, value)
        serv.deliveryOperator = self.context['request'].user.userid
        serv.deliveryStore = self.context['request'].user.submerchant_id
        if not serv.deliveryOperator:
            serv.deliveryOperator = ''
        if not serv.deliveryStore:
            serv.deliveryStore = ''

        try:
            serv.updatestate(fsm.DeliveryCompleteEvent())
        except Exception ,e:
            logging.getLogger('django').error(e)

        try:
            serv.save()
            self.result = '0'
        except Exception, e:
            logging.getLogger('django').error(e)
        return serv
