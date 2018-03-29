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
from crm import views as crm_view
from django.contrib.auth import urls as auth_urls
from users import views as userview

urlpatterns = [
    url(r'^$', crm_view.crm_main, name="home"),
    url(r'^test', userview.mmmtest),
    url(r'^admin/', admin.site.urls),
    url(r'', include('siteuser.urls')),
    url(r'^accounts/', include('users.urls')),
    url(r'^userform/', include('crm.urls')),
    url(r'^local/', include('crm.local_Interface.urls')),
    url(r'^mobile/', include('crm.mobile.urls'))
]
