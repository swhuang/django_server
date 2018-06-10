# -*- coding: utf-8 -*-
from ...admin.product.view import ProductViewset
from crm.models import ProductDetail
from rest_framework import viewsets
from rest_framework.status import *
from .Serializer import ProductSerializer
from crm.api.client.permission import UserPermission
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from crm.server_utils.base.httpProcess import get_parameter_dic
from django.db.models import Q
import logging


class ClientProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('productid', 'category', 'model', 'goldType', 'diamondWeight',)
    queryset = ProductDetail.objects.filter(releaseStatus='1')

    def list(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        params = get_parameter_dic(request)
        params.pop('offset', None)
        params.pop('limit', None)
        orderByPrice = params.pop('orderByPrice', None)
        keyword = params.pop('keyword', None)
        filterargs = {}
        for k, v in params.items():
            if k == 'sellingPrice':
                if type(v) != list:
                    raise ValueError("sellingPrice error")
            else:
                if isinstance(v, list):
                    if len(v) == 1:
                        filterargs[k[0:-2]] = v[0]
                    else:
                        filterargs[k[0:-2] + '__in'] = v
                else:
                    filterargs[k] = v

        try:
            if keyword:
                keyword = str(keyword[0])
                queryset = self.get_queryset().filter(
                    Q(title__icontains=keyword) | Q(model__icontains=keyword) | Q(brand__icontains=keyword) | Q(
                        series__icontains=keyword) | Q(goldType__icontains=keyword))
            else:
                queryset = self.get_queryset()

            if orderByPrice == '1':
                queryset = queryset.filter(**filterargs).order_by('sellingPrice')
            elif orderByPrice == '-1':
                queryset = queryset.filter(**filterargs).order_by('-sellingPrice')
            else:
                queryset = queryset.filter(**filterargs)
            queryset = self.filter_queryset(queryset)
        except Exception, e:
            logger.error(e)
            return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
