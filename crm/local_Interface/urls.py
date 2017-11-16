from django.conf.urls import url
import view

urlpatterns = [
    url(r'GetMemberData/$', view.GetMemberData, name='GetMemberData'),
    url(r'GetOrderData/$', view.GetOrderData, name='GetOrderData')
]