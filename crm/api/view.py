# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.generics import GenericAPIView
from crm.models import Merchant
from .Serializer import *


class MerchantViewset(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

    def perform_create(self, serializer):
        serializer.save()


class RestTest(APIView):
    # queryset = Merchant.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        d = {}
        d['name'] = 'hsw'
        d['money'] = 1000000
        return Response(d)
