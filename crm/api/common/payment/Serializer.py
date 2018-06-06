# -*- coding: utf-8 -*-
from rest_framework import serializers, validators
from crm.models import RentalOrder,PaymentOrder
from crm.server_utils.customerField.Field import *
from crm.server_utils.base import FSM as fsm
from django.db import transaction
from crm.server_utils.base.DQS import SingletonFactory
from collections import Counter, OrderedDict
from decimal import Decimal


class PaymentSerializer(serializers.ModelSerializer):
    orderno = serializers.ListField(child=serializers.CharField(max_length=25), write_only=True)
    pay_id = serializers.CharField(required=False)
    payedamount = AmountField(read_only=True)

    class Meta:
        model = PaymentOrder
        exclude = ('gmt_create', 'gmt_modified', 'orderNo')
        read_only_fields = ()

    def validate(self, attrs):
        realattrs = OrderedDict()
        realattrs.setdefault('orderno', attrs['orderno'])
        return realattrs

    def create(self, validated_data):
        orderlist = validated_data.pop('orderno', [])#self.context['request'].POST.getlist('orderNo[]', None)
        if not orderlist:
            raise serializers.ValidationError("orderNo缺失")
        else:
            #根据订单生产支付订单
            olist = []
            payamount = Decimal(0)
            obj_list = []
            for orderNo in orderlist:
                try:
                    order = RentalOrder.objects.get(orderNo=orderNo)
                    if order.orderStatus != fsm.ORDER_START:
                        raise serializers.ValidationError("订单已关闭 不可支付")
                    if order.payment_status != 0: #未支付才可以支付
                        raise serializers.ValidationError("订单正在支付,不可继续操作")
                except RentalOrder.DoesNotExist:
                    raise serializers.ValidationError("订单不存在")
                olist.append(order.orderNo)
                order.paymentorder
                payamount += order.payedamount
                obj_list.append(order)

            #validated_data['orderNo'] = str(olist)
            validated_data['payedamount'] = payamount
            with transaction.atomic():
                if not validated_data.has_key('payedamount'):
                    validated_data['payedamount'] = order.amount
                validated_data['memberId'] = self.context['request'].siteuser.memberId
                inst = super(PaymentSerializer, self).create(validated_data)
                for obj in obj_list:
                    obj.payment_status = 1 #订单状态更改为支付中
                    obj.payid = inst.pay_id
                    obj.paymentorder.add(inst)
                    obj.save()
            assert type(inst) == PaymentOrder
            SingletonFactory.getPaymentQueue().putitem(inst.pay_id)
            return inst
