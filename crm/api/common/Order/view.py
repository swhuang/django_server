# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from crm.models import RentalOrder
from .Serializer import OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import *
from crm.api.client.permission.UserPermission import AuthenticateUserPermission

import datetime
import logging
from crm.api.admin.service.view import RentalServiceViewset
from rest_framework import generics, mixins


# 客户端
class OrderViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, AuthenticateUserPermission)
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend,)

    filter_fields = ('orderNo',)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        v = {}
        if hasattr(self.request, 'siteuser') and self.request.siteuser:
            v['memberId'] = self.request.siteuser.memberId
        return RentalOrder.objects.filter(**v)

    def list(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        orderType = request.GET.getlist('orderType[]', None)
        orderStatus = request.GET.getlist('orderStatus[]', None)
        createDate = request.GET.getlist('createDate[]', None)
        if orderType == []:
            orderType = None
        if orderStatus == []:
            orderStatus = None
        if createDate == []:
            createDate = None

        if not orderType and not orderStatus and not createDate:
            return super(OrderViewset, self).list(request, *args, **kwargs)
        else:
            filterargs = request.GET.copy().dict()
            if orderType:
                vlist = filterargs.pop('orderType[]')
                if not isinstance(orderType, list):
                    return Response({"detail": '错误的参数: orderType'}, HTTP_400_BAD_REQUEST)
                else:
                    if len(orderType) == 1:
                        filterargs['orderType'] = orderType[0]
                    else:
                        filterargs['orderType__in'] = orderType

            if orderStatus:
                vlist = filterargs.pop('orderStatus[]')
                if not isinstance(orderType, list):
                    return Response({"detail": '错误的参数: orderStatus'}, HTTP_400_BAD_REQUEST)
                else:
                    if len(orderType) == 1:
                        filterargs['orderStatus'] = orderType[0]
                    else:
                        filterargs['orderStatus__in'] = orderType

            if createDate and isinstance(createDate, list):
                timeformat = "%Y-%m-%d %H:%M:%S"
                if createDate[0] == createDate[1]:
                    dt = datetime.datetime.strptime(createDate[0], timeformat)
                    filterargs['gmt_create__date'] = dt  # .date()
                else:
                    dtstart = datetime.datetime.strptime(createDate[0], timeformat)  # .date()
                    dtend = datetime.datetime.strptime(createDate[1], timeformat)  # .date()
                    filterargs['gmt_create__date__gte'] = dtstart
                    filterargs['gmt_create__date__lte'] = dtend
            filterargs.pop('limit', None)
            filterargs.pop('offset', None)

            try:
                queryset = RentalOrder.objects.filter(**filterargs)
            except Exception, e:
                logger.error(e)
                return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
            else:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
            serializer = RentalOrder(queryset, many=True)
            return Response(serializer.data)


# 管理端接口
class BackendOrderViewset(OrderViewset):
    def get_queryset(self):
        return RentalOrder.objects.all()
