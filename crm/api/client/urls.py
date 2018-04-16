# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from rest_framework import routers
from .view import SiteUserLoginView, GetVerifyCode
from django.conf.urls import url, include

router = routers.DefaultRouter()

#router.register(r'UserLogin', UserLogView)


urlpatterns = [
    url(r'UserLogin/$', SiteUserLoginView.as_view()),
    url(r'GetVerifyCode', GetVerifyCode.as_view()),
]


#urlpatterns += router.urls #+=