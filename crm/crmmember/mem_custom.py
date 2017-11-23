# -*- coding: utf-8 -*-
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site
from users.forms import MemberCreationForm
from django.utils.translation import ugettext_lazy as _
from pikachu import settings
from django.shortcuts import redirect




class AccountMxin(object):
    login_template = 'siteuser/login.html'  # 你项目的登录页面模板
    register_template = 'siteuser/register.html'  # 你项目的注册页面模板
    reset_passwd_template = 'reset_password.html'  # 忘记密码的重置密码模板
    change_passwd_template = 'change_password.html'  # 登录用户修改密码的模板
    notify_template = 'siteuser/notify.html'
    reset_passwd_email_title = u'重置密码'  # 重置密码发送电子邮件的标题
    reset_passwd_link_expired_in = 24  # 重置密码链接多少小时后失效

    def get_login_context(self, request):
        pass
        return {}

    def post(self, request, *args, **kwargs):
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            '''
            if settings.USERS_AUTO_LOGIN_AFTER_REGISTRATION:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
            elif not user.is_active and settings.USERS_VERIFY_EMAIL:
                opts = {
                    'user': user,
                    'request': request,
                }
            '''
            #return redirect(None)
            request.session['uid'] = user.id

    def get_register_context(self, request):
        form = MemberCreationForm()

        current_site = get_current_site(request)

        context = {
            'form': form,
            'site': current_site,
            'site_name': current_site.name,
            'title': _('Register'),
        }
        return context