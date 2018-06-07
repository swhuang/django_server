# -*- coding: utf-8 -*-
# 处理所有微信访问的地址
from django.conf.urls import url
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.views import (login, logout, password_change,
                                       password_change_done, password_reset,
                                       password_reset_complete,
                                       password_reset_confirm,
                                       password_reset_done, logout_then_login)

from crm import views as crmviews
from django.urls import reverse
from wechat.views import authorize

urlpatterns = [
    url(r'^authorize/$', authorize, name='wechat_authorized'),
    url(r'^login/$', login, name='wechat_login'),
]

reverse(viewname='users_reigister')