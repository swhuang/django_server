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
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class MemberViewset(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save()
