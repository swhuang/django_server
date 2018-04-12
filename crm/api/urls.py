# -*- coding: utf-8 -*-
from rest_framework import routers
from .view import MerchantViewset
from django.conf.urls import url

router = routers.DefaultRouter()

router.register(r'merchant', MerchantViewset)

urlpatterns = router.urls