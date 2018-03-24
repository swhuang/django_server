from django.conf.urls import url
import view

urlpatterns = [
    url(r'GetTableData', view.GetTableData, name='GetTableData'),
    url(r'CreateProject/$', view.CreateProject, name='CreateProject'),
    url(r'CreateOrder/$', view.OrderNewForm, name='GetOrderData'),
    url(r'userVerify/$', view.userVerification, name='UserVerificaiton')
]