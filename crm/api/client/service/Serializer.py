# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental, RentalOrder
from crm.server_utils.customerField.Field import *
from crm.server_utils.base.DQS import SingletonFactory
from crm.server_utils.customerField.structure import *
from collections import Counter, OrderedDict


def serviceType_valid(value):
    if value not in ['0', '1', '2']:
        raise serializers.ValidationError('服务方式错误')


class ClientRentalServiceSerializer(serializers.ModelSerializer):
    serviceStatus = StatusField(read_only=True)
    reservedProduct = JsonField(read_only=True)
    product = JsonField(read_only=True)
    #serviceType = serializers.CharField(validators=serviceType_valid, write_only=True, max_length=1)

    class Meta:
        model = ProductRental
        exclude = ('gmt_create', 'gmt_modified', 'isCompleted', 'curProcOrder', 'daily_amount', )
        #read_only_fields = '__all__'


    def create(self, validated_data):
        """
        生成租赁服务
        :param validated_data:
        :return:
        """
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

    def validate(self, attrs):
        realattrs = OrderedDict()
        try:
            realattrs.setdefault('reservedProductid', attrs['reservedProductid'])
            realattrs.setdefault('rentPeriod', attrs['rentPeriod'])
        except Exception ,e:
            raise serializers.ValidationError("缺少参数")
        if attrs.has_key('memberId'):
            memberid = attrs['memberId']
        else:
            memberid = self.context['request'].siteuser.memberId
        realattrs.setdefault('memberId', memberid)
        realattrs.setdefault('create_user', memberid)

        return realattrs

class ClientRentalListSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()
    serviceStatus = StatusField(read_only=True)
    reservedProduct = JsonField(read_only=True)
    product = JsonField(read_only=True)

    class Meta:
        model = ProductRental
        fields = '__all__'

    def get_order(self, obj):
        assert type(obj) == ProductRental
        orderlist = [i['orderNo'] for i in RentalOrder.objects.filter(serviceNo=obj.serviceNo).values('orderNo')]
        return orderlist