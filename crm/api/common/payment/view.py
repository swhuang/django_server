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
        inst = self.perform_create(serializer)
        # 根据inst吊起微信支付
        # TODO
        headers = self.get_success_headers(serializer.data)
        if isinstance(inst, PaymentOrder):
            ret = wepay.pay_jsapi(inst.payedamount, inst.pay_id)
            if TESTMODE:
                return Response("支付结束")
            else:
                return Response(ret, status=HTTP_201_CREATED, headers=headers)
        else:
            logging.getLogger('django').error(u"订单创建失败%s"% request.data)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        v = {}
        if hasattr(self.request, 'siteuser'):
            v['memberId'] = self.request.siteuser.memberId
        return PaymentOrder.objects.filter(**v)


#管理端接口
class BackendPaymentViewset(PaymentViewset):

    def get_queryset(self):
        return PaymentOrder.objects.all()


# 微信支付结果通知
class PaymentNotify(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        pass


