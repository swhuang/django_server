# -*- coding: utf-8 -*-
from rest_framework import viewsets
from crm.models import ProductDetail
from .Serializer import ProductSerializer, ProductFileSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import GenericAPIView


class ProductViewset(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)

    filter_fields = ('productid', 'category', 'model', 'goldType', 'diamondWeight',)

    def perform_create(self, serializer):
        serializer.save()


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

#文件上传接口
class ProductFileView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductFileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception,e:
                return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
            else:
                return Response('success', status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)