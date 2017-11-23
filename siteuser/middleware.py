# -*- coding: utf-8 -*-

from django.utils.functional import SimpleLazyObject

from siteuser.member.models import SiteUser
from users.models import Merchant

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

from django.utils.deprecation import MiddlewareMixin

class User(MiddlewareMixin):
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
                return None

            try:
                _merchant = Merchant.objects.get(id=int(mid))
            except _merchant.DoesNotExist:
                return None

            return _merchant

        request.siteuser = SimpleLazyObject(get_user)
        request.merchant = SimpleLazyObject(get_merchant)
