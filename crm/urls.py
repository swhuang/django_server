from django.conf.urls import url
import views
import crmmember.mem_views as mem_views

urlpatterns = [
    url(r'form/$', views.crm_main, name='content_manager'),
    url(r'interfacetest/$', views.test),
    url(r'getsessiontoken/$', views.getSessionToken),
    url(r'getuserdata/$', views.getUserData),
    url(r'generatetestmerchant', views.generatetestmerchant),
    url(r'djtest', views.djtest),
    url(r'form/projectmanager/$', views.panel_projectform, name='prj_manager'),
    url(r'member_reg/$', mem_views.member_reg, name='member_reg'),
    url(r'preferences/$', views.panel_preferences, name='preferences'),
    url(r'form/ordermanager', views.panel_ordermanager, name='ordermanager')
]