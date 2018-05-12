# -*- coding: utf-8 -*-
from rest_framework import routers
from .view import UserViewset, UserLogView
from django.conf.urls import url, include
from .member.view import MemberViewset
from .product.view import ProductViewset, ProductUpdateView, ProductFileView
from .service.view import RentalServiceViewset

router = routers.DefaultRouter()

router.register(r'User', UserViewset)# 管理员用户
router.register(r'member', MemberViewset)# 会员
router.register(r'product', ProductViewset)# 商品
router.register(r'RentalService', RentalServiceViewset) #租赁服务
#router.register(r'UserLogin', UserLogView)


urlpatterns = [
    url(r'UserLogin/$', UserLogView.as_view(), name='User login'),
    url(r'productupdate/$', ProductUpdateView.as_view(), name='update product'),
    url(r'productfile/$', ProductFileView.as_view(), name='batch update product'),
]


urlpatterns += router.urls #+=