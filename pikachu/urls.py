# -*- coding: utf-8 -*-
"""pikachu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .settings import MEDIA_ROOT
from django.views.static import serve
from crm.views import RenderIndex
from django.contrib.auth import urls as auth_urls
from crm.server_utils.base.DQS import Order_timer
import threading

urlpatterns = [
    url(r'^api-auth/', include('crm.api.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('siteuser.urls')),
    url(r'^accounts/', include('users.urls')),
    #url(r'^', include('crm.urls')),
    url(r'^', RenderIndex),
    url(r'^local/', include('crm.local_Interface.urls')),
    url(r'^mobile/', include('crm.mobile.urls')),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),
    #url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),
]

# 增加定时任务用于
'''
ORDERTIMER = threading.Timer(2.0, Order_timer)
ORDERTIMER.start()
'''