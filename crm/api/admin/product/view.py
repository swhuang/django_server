# -*- coding: utf-8 -*-
from rest_framework import viewsets
from crm.models import ProductDetail
from .Serializer import ProductSerializer, ProductFileSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
import django_filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import GenericAPIView
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ValidationError
from crm.server_utils.base.httpProcess import get_parameter_dic

import json



class ProductFilter(FilterSet):
    """
    自定义过滤类
    """
    price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    """
    icontains前面的i表示忽视大小写
    """
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = ProductDetail
        fields = ['price_min', 'price_max', 'name']


class ProductViewset(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)

    filter_fields = ('productid', 'category', 'model', 'goldType', 'diamondWeight',)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):

        logger = logging.getLogger('django')
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
                #queryset = ProductDetail.objects.filter(**filterargs)
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


# 产品更新接口
class ProductUpdateView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer
    queryset = ProductDetail.objects.all()
    _ignore_model_permissions = True

    def post(self, request, *args, **kwargs):
        validated_data = request.data

        if not validated_data.has_key('productid'):
            return Response({"detail": "productid 缺失"}, HTTP_400_BAD_REQUEST)

        pid = validated_data.pop('productid')

        try:
            p = ProductDetail.objects.get(productid=pid[0])
        except ProductDetail.DoesNotExist:
            try:
                p = ProductDetail.objects.get(productid=pid)
            except ProductDetail.DoesNotExist:
                return Response({"detail": "无效的productid"}, HTTP_400_BAD_REQUEST)
        #try:
        translate_dict = {
            'MainImage0': 'image1',
            'MainImage1': 'image2',
            'MainImage2': 'image3',
            'MainImage3': 'image4',
            'MainImage4': 'image5',
            'MainImage5': 'image6',
        }
        validated_data[u'lastModifiedBy'] = 'sabi' #request.user.userid
        for key, value in validated_data.items():
            old_key = key
            if translate_dict.has_key(key):
                key = translate_dict[key]
                validated_data[key] = value
                del validated_data[old_key]

        try:
            with transaction.atomic():
                mSerializer = self.get_serializer(instance=p, data=request.data)
                if mSerializer.is_valid(raise_exception=True):
                    mSerializer.update(p, validated_data)
                    if getattr(p, '_prefetched_objects_cache', None):
                        # If 'prefetch_related' has been applied to a queryset, we need to
                        # forcibly invalidate the prefetch cache on the instance.
                        p._prefetched_objects_cache = {}
                    return Response(mSerializer.data)
        except Exception, e:
            if hasattr(e, 'detail'):
                return Response(e.detail, HTTP_400_BAD_REQUEST)
            return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)




# 文件上传接口
class ProductFileView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductFileSerializer
    _ignore_model_permissions = True

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = ProductFileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception, e:
                print e
                logger = logging.getLogger('django')
                logger.error(e)
                return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
            else:
                return Response('success', status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
