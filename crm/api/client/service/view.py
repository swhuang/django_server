# -*- coding: utf-8 -*-
from rest_framework import viewsets
from crm.api.client.permission import UserPermission
from crm.models import ProductRental
from .Serializer import ClientRentalServiceSerializer, ClientRentalListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import *

import datetime
import logging
from crm.api.admin.service.view import RentalServiceViewset
from rest_framework import generics, mixins
from rest_framework import permissions


class ClientRentalServiceViewset(RentalServiceViewset, mixins.CreateModelMixin):

    serializer_class = ClientRentalServiceSerializer
    #permission_classes = (permissions.AllowAny, )
    permission_classes = (UserPermission.AuthenticateUserPermission, )

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        v = {}
        if hasattr(self.request, 'siteuser'):
            v['memberId'] = self.request.siteuser.memberId
        return ProductRental.objects.filter(**v).order_by('-gmt_create')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inst = self.perform_create(serializer)
        # 根据inst吊起微信支付
        # TODO
        headers = self.get_success_headers(serializer.data)
        if isinstance(inst, ProductRental):
            return Response({'serviceNo': inst.serviceNo}, status=HTTP_201_CREATED, headers=headers)
        else:
            logging.getLogger('django').error(u"服务创建失败%s"% request.data)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST, headers=headers)


class ClientRentalList(RentalServiceViewset):
    permission_classes = (UserPermission.AuthenticateUserPermission,)
    serializer_class = ClientRentalListSerializer

    def get_queryset(self):
        v = {}
        if hasattr(self.request, 'siteuser'):
            v['memberId'] = self.request.siteuser.memberId
        return ProductRental.objects.filter(**v)





