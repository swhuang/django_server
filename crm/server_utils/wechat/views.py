# -*- coding: utf-8 -*-
from ..payment.wepay import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import url
from django.urls import reverse
from datetime import datetime, timedelta


# 微信认证
def authorize(request):
    """登陆回调函数"""
    code = request.args.get("code")
    if not code:
        return "ERR_INVALID_CODE", 400
    next = request.args.get("next", "/")
    data = weixin.access_token(code)
    openid = data.openid
    resp = HttpResponseRedirect(next)
    expires = datetime.now() + timedelta(days=1)
    resp.set_cookie("openid", openid, expires=expires)
    return resp


# 微信登录
def login(request):
    """登陆跳转地址"""
    openid = request.cookies.get("openid")
    _next = request.args.get("next") or request.referrer or "/",
    if openid:
        return HttpResponseRedirect(_next)

    callback = reverse("wechat_authorized", kwargs={'next': _next})
    url = weixin.authorize(callback, "snsapi_base")
    return HttpResponseRedirect(url)
