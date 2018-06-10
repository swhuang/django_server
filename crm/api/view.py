# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from siteuser.functional import send_html_mail as _send_mail
from periodic.MiscTask.reserve_notify import reservedproductnotify
from .Serializer import *


class MerchantViewset(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

    def perform_create(self, serializer):
        serializer.save()


class RestTest(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        d = {}
        d['name'] = 'hsw'
        d['money'] = 1000000
        reservedproductnotify()
        return Response(d)
