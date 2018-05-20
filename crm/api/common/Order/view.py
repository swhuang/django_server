# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from crm.models import RentalOrder
from .Serializer import OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import *

import datetime
import logging
from crm.api.admin.service.view import RentalServiceViewset
from rest_framework import generics, mixins

#客户端
class OrderViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        v = {}
        if hasattr(self.request, 'siteuser'):
            v['memberId'] = self.request.siteuser.memberId
        return RentalOrder.objects.filter(**v)

    def list(self, request, *args, **kwargs):
        return super(OrderViewset, self).list(request, *args, **kwargs)
        # TODO


# 管理端接口
class BackendOrderViewset(OrderViewset):
    def get_queryset(self):
        return RentalOrder.objects.all()
