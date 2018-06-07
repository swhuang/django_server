# -*- coding: utf-8 -*-
# 处理所有微信访问的地址
from django.conf.urls import url
from wechat.views import authorize, login

urlpatterns = [
    url(r'^authorize/$', authorize, name='wechat_authorized'),
    url(r'^login/$', login, name='wechat_login'),
]
