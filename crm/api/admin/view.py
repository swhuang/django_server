# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics
from rest_framework.status import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .Serializer import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save()


class UserLogView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LogSerializer

    def get(self, request, format=None):
        d = {}
        d['name'] = 'hsw'
        d['money'] = 1000000
        return Response(d)

    # login
    def post(self, request, *args, **kwargs):
        v = {}
        v["password"] = request.data.get("password")
        v["username"] = request.data.get("userid")
        form = AuthenticationForm(request, data=v)
        if form.is_valid():
            login(request, form.get_user())
            return Response("success")
        else:
            return Response({"detail":"登录失败"}, HTTP_400_BAD_REQUEST)

    '''
    def perform_create(self, serializer):
        pass
    '''
    # serializer.save()
