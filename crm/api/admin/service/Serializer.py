# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental
from crm.server_utils.customerField.Field import *
from crm.server_utils.base import FSM as fsm
from collections import Counter, OrderedDict
import logging


class RentalServiceSerializer(serializers.ModelSerializer):
    serviceStatus = StatusField()
    createDate = ModifiedDateTimeField(source='gmt_create')
    product = JsonField()

    class Meta:
        model = ProductRental
        exclude = (
        'gmt_create', 'gmt_modified', 'createdBy', 'create_user', 'completeMode', 'isCompleted', 'daily_amount')


class ClaimGoodSerializer(serializers.Serializer):
    result = {
        '1': '失败',
        '2': '成功'
    }

    servtype = {
        '0': '租赁',
        '1': '销售',
        '2': '套餐',
    }

    serviceNo = serializers.CharField(max_length=25, write_only=True)
    serviceType = serializers.CharField(max_length=1, write_only=True)
    productid = serializers.CharField(max_length=15, write_only=True)
    deliveryOperator = serializers.CharField(max_length=100, write_only=True, required=False)
    deliveryStore = serializers.CharField(max_length=15, write_only=True, required=False)
    deliveryMode = serializers.CharField(max_length=1, write_only=True, required=False)
    serialNumber = serializers.CharField(max_length=10, write_only=True, required=False)
    logisticsCompany = serializers.CharField(max_length=20, write_only=True, required=False)
    trackingNumber = serializers.CharField(max_length=20, write_only=True, required=False)
    claimResult = serializers.SerializerMethodField()
    # serializers.CharField(max_length=1, default='1', read_only=True)
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
        return validated_data['key']

    def validate(self, attrs):
        realattrs = OrderedDict()
        try:
            servtype = attrs.get('serviceType')
            serviceNo = attrs.get('serviceNo')
        except:
            raise serializers.ValidationError("参数错误")

        if servtype not in self.servtype.keys():
            raise serializers.ValidationError("服务类型错误")
        try:
            servid = serviceNo
            if servtype == '0':
                serv = ProductRental.objects.get(serviceNo=servid)
            else:
                # TODO 增加其余服务类型
                raise NotImplementedError
        except Exception, e:
            logging.getLogger('django').error(e)
            raise serializers.ValidationError(u'服务不存在')

        for attr, value in attrs.items():
            setattr(serv, attr, value)
        serv.deliveryOperator = self.context['request'].user.userid
        serv.deliveryStore = self.context['request'].user.submerchant_id
        if not serv.deliveryOperator:
            serv.deliveryOperator = ''
        if not serv.deliveryStore:
            serv.deliveryStore = ''

        try:
            serv.updatestate(fsm.DeliveryCompleteEvent())
            serv.save()
            self.result = '0'
        except Exception, e:
            logging.getLogger('django').error(e)
            raise serializers.ValidationError("状态修改失败")
        else:
            realattrs['key'] = serv
            return realattrs
