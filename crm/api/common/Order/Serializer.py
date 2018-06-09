# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import *
from crm.server_utils.customerField.Field import *
from django.db import transaction
from crm.server_utils.base import FSM as fsm
from crm.server_utils.base.DQS import SingletonFactory
from collections import Counter, OrderedDict
from Accounting.models import BillingTran, BalanceManager


class OrderSerializer(serializers.ModelSerializer):
    createDate = ModifiedDateTimeField(source='gmt_create', read_only=True)
    paymentDatetime = ModifiedDateTimeField(read_only=True)
    useBalance = serializers.CharField(max_length=1, write_only=True, required=False)
    deliveryMode = serializers.CharField(max_length=1, write_only=True, required=False)
    orderType = serializers.IntegerField(source='type')
    name = serializers.CharField(max_length=100, write_only=True, required=False)
    phone = serializers.CharField(max_length=13, write_only=True, required=False)
    address = serializers.CharField(max_length=100, write_only=True, required=False)
    gender = serializers.CharField(max_length=1, write_only=True, required=False)
    remark = serializers.CharField(max_length=100, write_only=True, required=False)

    class Meta:
        model = RentalOrder
        exclude = ('gmt_create', 'gmt_modified', 'paymentorder',)
        read_only_fields = (
        'payid', 'paymentType', 'paymentDatetime', 'memberId', 'orderStatus', 'payment_status', 'amount', 'payedamount')

    # 创建订单
    def create(self, validated_data):

        serv = validated_data.pop('serv')

        # 准备创建订单
        validated_data['amount'] = serv.initialDeposit + serv.initialRent
        currentbalance = self.context['request'].acct.balance
        freezeamt = 0
        if int(validated_data.pop('useBalance')) and currentbalance > 0.0:
            if validated_data['amount'] <= currentbalance:
                validated_data['payedamount'] = 0
            else:
                validated_data['payedamount'] = validated_data['amount'] - currentbalance

            # 冻结余额
            freezeamt = validated_data['amount'] - validated_data['payedamount']
        else:
            validated_data['payedamount'] = validated_data['amount']

        deliveryMode = validated_data.pop('deliveryMode', None)
        deliveryInfo = validated_data.pop('deliveryinfo', {})


        with transaction.atomic():
            inst = super(OrderSerializer, self).create(validated_data)
            if int(deliveryMode) == 0:
                serv.reservedProduct.update(deliveryInfo)

            serv.curProcOrder = inst.orderNo
            serv.deliveryMode = deliveryMode
            serv.updatestate(fsm.GenOrderEvent(orderNo=inst.orderNo))
            serv.save()
            if freezeamt > 0:
                BalanceManager(acctid=self.context['request'].acct.id, memberId=serv.memberId).freeze(amt=freezeamt, orderno=inst.orderNo)
        SingletonFactory.getCycleQueue().putitem(inst.orderNo)  # 加入倒计时队列
        return inst

    def validate(self, attrs):
        realattrs = OrderedDict()
        usebalance = attrs.get('useBalance', None)
        realattrs.setdefault('useBalance', usebalance)
        try:
            realattrs.setdefault('serviceNo', attrs['serviceNo'])
            realattrs.setdefault('deliveryMode', attrs['deliveryMode'])
            realattrs.setdefault('serviceType', attrs['serviceType'])
            realattrs.setdefault('type', int(attrs['type']))
        except Exception, e:
            raise serializers.ValidationError("缺少参数")
        else:
            # 准备创建订单
            realattrs['createdBy'] = self.context['request'].siteuser.username
            if attrs['serviceType'] not in [0, 1, 2]:
                raise serializers.ValidationError("serviceType参数错误")
            realattrs['memberId'] = self.context['request'].siteuser.memberId
            if int(realattrs['deliveryMode']) == 0 or not realattrs.has_key('deliveryMode'):
                deliveryinfo = dict()
                deliveryinfo.setdefault('gender', attrs.get('gender', ''))
                deliveryinfo.setdefault('name', attrs.get('name', ''))
                deliveryinfo.setdefault('phone', attrs.get('phone', ''))
                deliveryinfo.setdefault('address', attrs.get('address', ''))
                deliveryinfo.setdefault('remark', attrs.get('remark', ''))
                realattrs['deliveryinfo'] = deliveryinfo

        try:
            if realattrs['serviceType'] == 0:
                serv = ProductRental.objects.get(serviceNo=realattrs['serviceNo'])
            elif realattrs['serviceType'] == 1:
                serv = ComboRental.objects.get(serviceNo=realattrs['serviceNo'])
        except ProductRental.DoesNotExist:
            raise serializers.ValidationError("服务单号错误")
        else:
            realattrs['serv'] = serv

        return realattrs
