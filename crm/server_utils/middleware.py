# -*- coding: utf-8 -*-
from django.middleware.cache import FetchFromCacheMiddleware
from django.contrib.auth import get_user_model


class CrmFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    """
    管理端用户不使用缓存
    """
    def process_request(self, request):
        if isinstance(request.user, get_user_model()):
            return None
        else:
            return super(CrmFetchFromCacheMiddleware, self).process_request(request)