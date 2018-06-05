# -*- coding: utf-8 -*-
from rest_framework import routers
from django.conf.urls import url, include
from Order.view import OrderViewset
from payment.view import PaymentViewset

router = routers.DefaultRouter()

router.register(r'order', OrderViewset, base_name='order')
router.register(r'payment', PaymentViewset, base_name='payment')


urlpatterns = [
]


urlpatterns += router.urls #+=