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
                filterargs['title_contains'] = _title

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
                queryset = ProductDetail.objects.filter(**filterargs)
            except Exception, e:
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
    permissions_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer
    queryset = ProductDetail.objects.all()
    _ignore_model_permissions = True

    def post(self, request, *args, **kwargs):
        validated_data = request.data
        pid = validated_data.pop('productid')
        try:
            p = ProductDetail.objects.get(productid=pid[0])
        except ProductDetail.DoesNotExist:
            return Response({"detail": "无效的productid"}, HTTP_400_BAD_REQUEST)
        try:
            validated_data[u'lastModifiedBy'] = request.user.userid
            self.get_serializer(instance=p, data=request.data).update(p, validated_data)
        except Exception, e:
            return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
        return Response("success")


# 文件上传接口
class ProductFileView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductFileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception, e:
                return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
            else:
                return Response('success', status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
