# -*- coding: utf-8 -*-
from rest_framework import routers
from .view import MerchantViewset, RestTest
from django.conf.urls import url, include

router = routers.DefaultRouter()

router.register(r'merchant', MerchantViewset)
#router.register(r'test', RestTest.as_view())

urlpatterns = [
    url(r'admin/', include('crm.api.admin.urls')),
    url(r'client/', include('crm.api.client.urls')),
]

urlpatterns += router.urls