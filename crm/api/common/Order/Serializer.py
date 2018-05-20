# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import *
from crm.server_utils.customerField.Field import *
from django.db import transaction
from crm.server_utils.base import FSM as fsm
from crm.server_utils.base.DQS import SingletonFactory



class OrderSerializer(serializers.ModelSerializer):

    createDate = ModifiedDateTimeField(source='gmt_create', read_only=True)

    class Meta:
        model = RentalOrder
        exclude = ('gmt_create', 'gmt_modified',)
        read_only_fields = ()

    #创建订单
    def create(self, validated_data):
        if not validated_data.has_key('serviceNo'):
            validated_data['type'] = 2

            with transaction.atomic:
                inst = super(OrderSerializer, self).create(validated_data)
            return inst
        else:
            serv = None

            try:
                if validated_data['type'] == 0:
                    serv = ProductRental.objects.get(serviceNo=validated_data['serviceNo'])
                elif validated_data['type'] == 1:
                    serv = ComboRental.objects.get(serviceNo=validated_data['serviceNo'])
            except ProductRental.DoesNotExist:
                raise serializers.ValidationError("服务单号错误")

            with transaction.atomic:
                inst = super(OrderSerializer, self).create(validated_data)
                serv.curProcOrder = inst.orderid
                serv.set_state(fsm.RentalConfirmed())
                serv.save()
            SingletonFactory.getCycleQueue().putitem(inst.orderid)#加入倒计时队列
            return inst
