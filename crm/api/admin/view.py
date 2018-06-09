# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics
from rest_framework.status import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .Serializer import *
from crm.models import *
from .product.Serializer import ProductFileSerializer
from django.http import QueryDict
import sys
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import update_session_auth_hash
import logging
import urllib

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
        print "here"
        return Response(d)

    # login
    def post(self, request, *args, **kwargs):
        v = {}
        v["password"] = request.data.get("password")
        v["username"] = request.data.get("userid")
        form = AuthenticationForm(request, data=v)
        if form.is_valid():
            login(request, form.get_user())
            return Response({"name": form.get_user().username})
        else:
            return Response({"detail": form.errors}, HTTP_400_BAD_REQUEST)


class UserLogOut(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LogOutSerializer

    # logout
    def post(self, request, format=None):
        if not isinstance(request.user, AnonymousUser):
            logout(request)
        return Response({"detail": "已退出"})


class UserChangePWD(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    # change password
    def post(self, request, format=None):
        data = QueryDict(urllib.urlencode(request.data))
        form = PasswordChangeForm(user=request.user, data=data)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one.
            update_session_auth_hash(request, form.user)
            return Response({"detail": "重置成功"})
        else:
            logging.getLogger('django').warning(form.errors)
            return Response({"detail": form.errors}, HTTP_400_BAD_REQUEST)



