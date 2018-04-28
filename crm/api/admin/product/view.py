# -*- coding: utf-8 -*-
from rest_framework import viewsets
from crm.models import ProductDetail
from .Serializer import ProductSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewset(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save()


