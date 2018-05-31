# -*- coding: utf-8 -*-
from ...admin.product.view import ProductViewset
from crm.models import ProductDetail
from rest_framework import viewsets
from rest_framework.status import *
from .Serializer import ProductSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from crm.server_utils.base.httpProcess import get_parameter_dic
import logging



class ClientProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('productid', 'category', 'model', 'goldType', 'diamondWeight',)

    def get_queryset(self):
        return ProductDetail.objects.filter(releaseStatus='1')

    def list(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        params = get_parameter_dic(request)
        filterargs = {}
        for k,v in params:
            if isinstance(v, list):
                if len(v) == 1:
                    filterargs[k[0:-2]] = v[0]
                else:
                    filterargs[k[0:-2] + '__in'] = v
            else:
                filterargs[k] = v









        key_model = request.GET.get('model', None)
        key_goldType = request.GET.getlist('goldType[]', None)
        if key_goldType == []:
            key_goldType = None

        key_category = request.GET.getlist('category[]', None)
        if key_category == []:
            key_goldType = None

        key_title = request.GET.get('title', None)

        if not key_model and not key_category and not key_goldType and not key_title:
            return super(ProductViewset, self).list(self.request, *args, **kwargs)
        else:
            filterargs = request.GET.copy().dict()
            if key_model:
                try:
                    _model = filterargs.pop('model')
                except Exception, e:
                    return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)

                filterargs['model__contains'] = _model

            if key_title:
                try:
                    _title = filterargs.pop('title')
                except Exception, e:
                    return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
                filterargs['title__contains'] = _title

            if key_category:
                try:
                    vlist = filterargs.pop('category[]')
                except Exception, e:
                    return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
                if not isinstance(key_category, list):
                    return Response({"detail": 'Invalid parameter category'}, HTTP_400_BAD_REQUEST)
                else:
                    if len(key_category) == 1:
                        filterargs['category'] = key_category[0]
                    else:
                        filterargs['category__in'] = key_category

            if key_goldType:
                try:
                    vlist = filterargs.pop('goldType[]')
                except Exception, e:
                    return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)

                if not isinstance(key_goldType, list):
                    return Response({"detail": 'Invalid parameter goldType'}, HTTP_400_BAD_REQUEST)
                else:
                    if len(key_goldType) == 1:
                        filterargs['goldType'] = key_goldType[0]
                    else:
                        filterargs['goldType__in'] = key_goldType

            try:
                filterargs.pop('limit')
            except:
                pass
            try:
                filterargs.pop('offset')
            except:
                pass

            try:
                # queryset = ProductDetail.objects.filter(**filterargs)
                queryset = self.get_queryset().filter(**filterargs)
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
