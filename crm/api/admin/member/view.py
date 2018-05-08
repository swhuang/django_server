# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics
from rest_framework.status import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .Serializer import *
from crm.models import *
from siteuser.member.models import SiteUser
from django_filters.rest_framework import DjangoFilterBackend
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class MemberViewset(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    # 定义需要使用过滤器的字段
    filter_fields = ('memberId','name', 'idType', 'idNo', 'phone')

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializers.save()

