# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import *
from .Serializer import SiteUserSerializer, LoginSerializer
from crm.server_utils.Authentication import MsgAuthentication
from siteuser.member.models import SiteUser, InnerUser
from Accounting.models import Account
from django.db import transaction
from django.views.decorators.cache import cache_page, never_cache



class SiteUserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    # login & register
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        verifycode = request.data.get("verifycode")
        stored_code = request.session.get('VerifyCode', None)
        if MsgAuthentication.verifyPhoneCode(request.session, verifycode):
            try:
                usr = SiteUser.objects.get(username=username)
            except SiteUser.DoesNotExist:
                try:
                    with transaction.atomic():
                        usr = InnerUser.objects.create(username=username, phone=username)
                        request.session['uid'] = usr.user.id
                        act = Account.objects.create(user=usr.user, balance=0.0)
                except Exception,e:
                    print e
                    return Response({"detail": "注册/登录失败"}, HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail", "success"})
        else:
            return Response({"detail": "验证码错误"}, HTTP_400_BAD_REQUEST)

        return Response({"username": username, "verifycode": verifycode})


class GetVerifyCode(APIView):
    permission_classes = (permissions.AllowAny,)

    @never_cache
    def get(self, request, *args, **kwargs):
        a = MsgAuthentication.createPhoneCode(request.session)
        return Response({"verifycode": a})
