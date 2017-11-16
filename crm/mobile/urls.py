# -*- coding: utf-8 -*-
from django.conf.urls import url
import mobile_view

urlpatterns = [
    url(r'^$', mobile_view.index, name='MobileIndex'),
    url(r'^orderinfo/$', mobile_view.orderinfo, name='MobileOrderInfo'),
    url(r'^ordersubmit/$', mobile_view.ordersubmit, name='MobileOrderSubmit')
]
