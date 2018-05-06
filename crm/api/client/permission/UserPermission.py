# -*- coding: utf-8 -*-
from rest_framework import permissions

class AnyUserPermission(permissions.BasePermission):
    pass


class LogedUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.siteuser and True