# -*- coding: utf-8 -*-
from rest_framework import routers
from .view import SiteUserLoginView, GetVerifyCode
from django.conf.urls import url, include
from .service.view import *
from .product.view import *
from .account.view import *
from django.views.decorators.cache import cache_page, never_cache

router = routers.DefaultRouter()

#router.register(r'UserLogin', UserLogView)
router.register(r'RentalService', ClientRentalServiceViewset)
router.register(r'RentalServiceList', ClientRentalList)
router.register(r'product', ClientProductViewset)
router.register(r'account', AccountViewset, base_name='account')


urlpatterns = [
    url(r'UserLogin/$', SiteUserLoginView.as_view()),
    url(r'GetVerifyCode', GetVerifyCode.as_view()),
]


urlpatterns += router.urls #+=