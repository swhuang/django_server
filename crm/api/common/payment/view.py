# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from crm.models import PaymentOrder
from .Serializer import PaymentSerializer
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import *
from crm.server_utils.payment import wepay
from pikachu.settings import TESTMODE
from rest_framework import serializers

import datetime
import logging
from crm.api.admin.service.view import RentalServiceViewset
from rest_framework import generics, mixins


class PaymentViewset(viewsets.ModelViewSet):
    queryset = PaymentOrder.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            inst = self.perform_create(serializer)
        except serializers.ValidationError, e:
            headers = self.get_success_headers(serializer.data)
            logging.getLogger('django').error(u"订单创建失败%s" % request.data)
            return Response(str(e.detail[0]), status=HTTP_400_BAD_REQUEST, headers=headers)
        except Exception, e:
            headers = self.get_success_headers(serializer.data)
            logging.getLogger('django').error(u"订单创建失败%s" % request.data)
            return Response(e.message, status=HTTP_400_BAD_REQUEST, headers=headers)
        # 根据inst吊起微信支付
        # TODO
        headers = self.get_success_headers(serializer.data)
        productname = u'多项订单联合'
        if inst.order.count() == 1:
            flg = inst.order.first().serviceType
            if flg == 0:
                productname = u'单品租赁服务'
            elif flg == 1:
                productname = u'套餐租赁服务'
            elif flg == 2:
                productname = u'销售服务'

        if isinstance(inst, PaymentOrder):
            ret = wepay.pay_jsapi(amount=inst.payedamount, out_trade_no=inst.pay_id,
                                  body=request.merchant.name + '-' + productname)
            if TESTMODE:
                return Response("支付结束")
            else:
                return Response(ret, status=HTTP_201_CREATED, headers=headers)
        else:
            logging.getLogger('django').error(u"订单创建失败%s" % request.data)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        v = {}
        if hasattr(self.request, 'siteuser'):
            v['memberId'] = self.request.siteuser.memberId
        return PaymentOrder.objects.filter(**v)


# 管理端接口
class BackendPaymentViewset(PaymentViewset):
    def get_queryset(self):
        return PaymentOrder.objects.all()


# 微信支付结果通知
class PaymentNotify(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        pass
