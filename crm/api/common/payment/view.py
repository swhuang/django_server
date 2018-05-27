# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from crm.models import PaymentOrder
from .Serializer import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import *

import datetime
import logging
from crm.api.admin.service.view import RentalServiceViewset
from rest_framework import generics, mixins


class PaymentViewset(viewsets.ModelViewSet):
    queryset = PaymentOrder.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = PaymentSerializer

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


