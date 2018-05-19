# -*- coding: utf-8 -*-
from rest_framework import routers
from .view import SiteUserLoginView, GetVerifyCode
from django.conf.urls import url, include
from .service.view import *

router = routers.DefaultRouter()

#router.register(r'UserLogin', UserLogView)
router.register(r'service', ClientRentalServiceViewset)


urlpatterns = [
    url(r'UserLogin/$', SiteUserLoginView.as_view()),
    url(r'GetVerifyCode', GetVerifyCode.as_view()),
]


urlpatterns += router.urls #+=