# -*- coding: utf-8 -*-
from rest_framework import viewsets
from crm.models import Merchant
from .Serializer import *

class MerchantViewset(viewsets.ModelViewSet):

    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

    def perform_create(self, serializer):
        serializer.save()