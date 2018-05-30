# -*- coding: utf-8 -*-

from django.utils.functional import SimpleLazyObject

from siteuser.member.models import SiteUser
from users.models import Merchant
from crm.models import DEFAULT_MERCHANT_OBJ
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import sys

# add 'siteuser.middleware.User' in MIDDLEWARE_CLASSES
# then the request object will has a `siteuser` property
#
# you can using it like this:
# if request.siteuser:
#     # there has a logged user,
#     uid = request.siteuser.id
# else:
#     # no one is logged
#
# Don't worry about the performance,
# `siteuser` is a lazy object, it readly called just access the `request.siteuser`

from django.views.debug import technical_500_response
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import cookie_date
import time
from django.conf import settings


class User(MiddlewareMixin):
    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())

    def process_request(self, request):
        def get_user():
            uid = request.session.get('uid', None)
            if not uid:
                return None

            try:
                user = SiteUser.objects.get(id=int(uid))
            except SiteUser.DoesNotExist:
                return None

            if not user.is_active:
                user = None
            return user

        def get_merchant():
            mid = request.session.get('mid', None)
            if not mid:
                mid = 1

            try:
                _merchant = Merchant.objects.get(id=int(mid))
            except _merchant.DoesNotExist:
                return None

            return _merchant

        # disable csrf
        setattr(request, '_dont_enforce_csrf_checks', True)
        request.siteuser = SimpleLazyObject(get_user)
        if not request.session.has_key('merchant'):
            request.session['merchant'] = DEFAULT_MERCHANT_OBJ.merchantid
        request.merchant = SimpleLazyObject(get_merchant)

    def process_response(self, request, response):

        def currentlogin(user):  # 当前未登录:true 当前已登录:false
            if isinstance(user, AnonymousUser):
                return True
            elif isinstance(user, SiteUser):
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = cookie_date(expires_time)

                isAuth = '1'
                if user.isauthenticated:
                    isAuth = '0'
                if request.COOKIES.get('IsAuthenticated', None) != isAuth:
                    response.set_cookie(
                        'IsAuthenticated:', isAuth, max_age=max_age, expires=expires,
                        domain=settings.SESSION_COOKIE_DOMAIN,
                        path=settings.SESSION_COOKIE_PATH,
                        secure=settings.SESSION_COOKIE_SECURE or None,
                        httponly=False,
                    )
                return False
            elif isinstance(user, get_user_model()):
                return False
            else:
                return True

        current_user = request.user

        if hasattr(request, 'siteuser'):
            if isinstance(request.siteuser, SiteUser):
                current_user = request.siteuser

        loginfo = request.COOKIES.get('logged', None)
        if not loginfo:
            if request.session.get_expire_at_browser_close():
                max_age = None
                expires = None
            else:
                max_age = request.session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = cookie_date(expires_time)

            response.set_cookie(
                'logged', '1', max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                path=settings.SESSION_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=False,
            )
            loginfo = '1'

        if currentlogin(current_user) and loginfo == '0':  # 当前未登录,原来已登录
            if request.session.get_expire_at_browser_close():
                max_age = None
                expires = None
            else:
                max_age = request.session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = cookie_date(expires_time)

            response.set_cookie(
                'logged', '1', max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                path=settings.SESSION_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=False,
            )
        elif not currentlogin(current_user) and loginfo == '1':  # 当前已登录,原来未登录
            if request.session.get_expire_at_browser_close():
                max_age = None
                expires = None
            else:
                max_age = request.session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = cookie_date(expires_time)

            response.set_cookie(
                'logged', '0', max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                path=settings.SESSION_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=False,
            )
        return response
