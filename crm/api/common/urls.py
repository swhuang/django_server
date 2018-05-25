# -*- coding: utf-8 -*-
from rest_framework import routers
from django.conf.urls import url, include
from Order.view import OrderViewset

router = routers.DefaultRouter()

router.register(r'order', OrderViewset, base_name='order')


urlpatterns = [
]


urlpatterns += router.urls #+=