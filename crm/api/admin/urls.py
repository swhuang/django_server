# -*- coding: utf-8 -*-
from rest_framework import routers
from .view import UserViewset, UserLogView
from django.conf.urls import url, include
from .member.view import MemberViewset
from .product.view import ProductViewset, ProductUpdateView, ProductFileView

router = routers.DefaultRouter()

router.register(r'User', UserViewset)
router.register(r'member', MemberViewset)
router.register(r'product', ProductViewset)
#router.register(r'UserLogin', UserLogView)


urlpatterns = [
    url(r'UserLogin/$', UserLogView.as_view()),
    url(r'productupdate/$', ProductUpdateView.as_view()),
    url(r'productfile/$', ProductFileView.as_view()),
]


urlpatterns += router.urls #+=