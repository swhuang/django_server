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
        key_category = request.GET.get('category', None)
        if not key_model and not key_category:
            return super(ProductViewset, self).list(self.request, *args, **kwargs)
        else:
            filterargs = request.GET.copy().dict()
            if key_model:
                try:
                    model_list = json.loads(filterargs.pop('model'))
                except Exception, e:
                    return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
                if not isinstance(model_list, list):
                    return Response({"detail": 'Invalid parameter model'}, HTTP_400_BAD_REQUEST)
                else:
                    if len(model_list) == 1:
                        filterargs['model'] = model_list[0]
                    else:
                        filterargs['model__in'] = model_list

            if key_category:
                try:
                    v = filterargs.pop('category')
                    category_list = json.loads(v)
                except Exception, e:
                    return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
                if not isinstance(category_list, list):
                    return Response({"detail": 'Invalid parameter category'}, HTTP_400_BAD_REQUEST)
                else:
                    if len(category_list) == 1:
                        filterargs['category'] = category_list[0]
                    else:
                        filterargs['category__in'] = category_list
            try:
                filterargs.pop('limit')
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
            p = ProductDetail.objects.get(productid=pid)
        except ProductDetail.DoesNotExist:
            return Response({"detail": "无效的productid"}, HTTP_400_BAD_REQUEST)
        try:
            self.get_serializer(instance=p, data=request.data).update(p, validated_data)
        except Exception, e:
            return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
        return Response("sucess")


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
