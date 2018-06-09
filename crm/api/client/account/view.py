# -*- coding: utf-8 -*-
import logging
from rest_framework import viewsets
from ..permission.UserPermission import AuthenticateUserPermission
from Serializer import AccountSerializer
from Accounting.models import Account

class AccountViewset(viewsets.ModelViewSet):
    permission_classes = (AuthenticateUserPermission, )
    serializer_class = AccountSerializer

    def get_queryset(self):
        v = {}
        if hasattr(self.request, 'siteuser'):
            v['id'] = self.request.siteuser.account.id
        return Account.objects.filter(**v)