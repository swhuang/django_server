# -*- coding: utf-8 -*-
from rest_framework import viewsets
from crm.api.client.permission import UserPermission
from crm.models import ProductRental
from .Serializer import ClientRentalServiceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import *

import datetime
import logging
from crm.api.admin.service.view import RentalServiceViewset
from rest_framework import generics, mixins


class ClientRentalServiceViewset(RentalServiceViewset, mixins.CreateModelMixin):

    serializer_class = ClientRentalServiceSerializer
    permission_classes = (UserPermission.AuthenticateUserPermission, )

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        v = {}
        if hasattr(self.request, 'siteuser'):
            v['memberId'] = self.request.siteuser.memberId
        return ProductRental.objects.filter(**v)






