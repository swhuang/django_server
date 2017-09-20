"""pikachu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from pikachutest import views as app_view
from crm import views as crm_view
from django.contrib.auth import urls as auth_urls
from users import views as userview

urlpatterns = [
    url(r'^$', app_view.index, name="home"),
    url(r'^test', userview.mmmtest),
    url(r'^getmodel', app_view.getmodel),
    url(r'^GetParkingInfo', app_view.GetParkingInfo),
    url(r'^admin/', admin.site.urls),
    url(r'^initatable', app_view.initatable),
    url(r'^UpdateParkingData', app_view.UpdateParkingData),
    url(r'^TimeTable', app_view.TimeTable),
    url(r'^SortTable', app_view.SortTable),
    url(r'^accounts/', include('users.urls')),
    url(r'^userform/', include('crm.urls')),
]
