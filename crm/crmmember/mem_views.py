#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import csv
from crm.models import *
import os
import hashlib
import crm.util as mUtil
from django.views.decorators.csrf import csrf_exempt
import json
# import users.models.User as Usermodel
from users.models import User as Usermodel
from django.template.response import TemplateResponse
from users.forms import MemberCreationForm
from pikachu import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, resolve_url
from django.utils.translation import ugettext_lazy as _
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site


def member_reg(request, template_name = "user/member.html",
               registration_form = MemberCreationForm,
               post_registration_redirect = None):
    r'''

    :param request:
    :param template_name:
    :param registration_form:
    :param post_registration_redirect:
    :return:
    '''
    if post_registration_redirect is None:
        post_registration_redirect = reverse('users_registration_complete')

    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            if settings.USERS_AUTO_LOGIN_AFTER_REGISTRATION:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
            elif not user.is_active and settings.USERS_VERIFY_EMAIL:
                opts = {
                    'user': user,
                    'request': request,
                }
            return redirect(post_registration_redirect)
    else:
        form = registration_form()

    current_site = get_current_site(request)

    context = {
        'form': form,
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Register'),
    }

    return TemplateResponse(request, template_name, context)

    #return HttpResponse('hswok')