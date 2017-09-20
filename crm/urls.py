from django.conf.urls import url
import views

urlpatterns = [
    url(r'form/$', views.crmtest, name='content_manager')
]