# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from crm.models import ProductRental
from .Serializer import RentalServiceSerializer
from django_filters.rest_framework import DjangoFilterBackend


class RentalServiceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ProductRental.objects.all()
    serializer_class = RentalServiceSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
