# -*- coding: utf-8 -*-

from django.conf.urls import url

from siteuser.upload_avatar import views

urlpatterns = [
    url(r'^uploadavatar_upload/?$', views.upload_avatar, name="uploadavatar_upload"),
    url(r'^uploadavatar_crop/?$', views.crop_avatar, name="uploadavatar_crop"),
]