# -*- coding: utf-8 -*-
from rest_framework import routers
from .view import UserViewset, UserLogView
from django.conf.urls import url, include

router = routers.DefaultRouter()

router.register(r'User', UserViewset)
#router.register(r'UserLogin', UserLogView)


urlpatterns = [
    url(r'UserLogin/$', UserLogView.as_view()),
]


urlpatterns += router.urls #+=