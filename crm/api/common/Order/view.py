# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from crm.models import ProductRental
from .Serializer import OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import *

import datetime
import logging
from crm.api.admin.service.view import RentalServiceViewset
from rest_framework import generics, mixins


class OrderViewset(viewsets.ModelViewSet):

    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save()
    #TODO






