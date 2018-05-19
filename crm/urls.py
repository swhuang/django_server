from django.conf.urls import url
import views
import crmmember.mem_views as mem_views
from weixin import Weixin

config = dict(WEXIN_APP_ID='wx1c88e225b036f07a', WEIXIN_APP_SECRET='6fd6d2e8e7b3df81361d7bfb5521a9de')
weixin = Weixin(config)

urlpatterns = [
    url(r'^$', views.crm_main, name='content_manager'),
    url(r'weixin/$', weixin.django_view_func(), name='index'),
    url(r'getsessiontoken/$', views.getSessionToken),
    url(r'getuserdata/$', views.getUserData),
    url(r'generatetestmerchant', views.generatetestmerchant),
    url(r'djtest', views.djtest),
    url(r'projectmanager/$', views.panel_projectform, name='prj_manager'),
    url(r'member_reg/$', mem_views.member_reg, name='member_reg'),
    url(r'preferences/$', views.panel_preferences, name='preferences'),
    url(r'ordermanager', views.panel_ordermanager, name='ordermanager'),
    url(r'membermanager', views.crm_main, name='membermgr'),
    url(r'submanager', views.panel_submanager, name='submanager')
]