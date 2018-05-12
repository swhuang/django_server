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
from .product.Serializer import ProductFileSerializer
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
            return Response({"detail": "登录失败"}, HTTP_400_BAD_REQUEST)




# 取货完成接口
class CompClaimView(APIView):
    permissions_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        serv_id = request.data.get("projid", None)
        serv_type = request.data.get("type", None)

        if serv_type == 'zl':#租赁
            cur_serv = ProductRental.objects.get(serviceNo=serv_id)
        elif serv_type == 'tc':#套餐
            cur_serv = ComboRental.objects.get(serviceNo=serv_id)

        cur_serv.set_state(RentalProcessing())
        pass
