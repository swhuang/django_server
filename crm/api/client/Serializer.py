# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import *
from siteuser.member.models import SiteUser
from siteuser.settings import MAX_USERNAME_LENGTH


class SiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = '__all__'


class LoginSerializer(serializers.Serializer):

    memberid = serializers.CharField(max_length=15, read_only=True)
    username = serializers.CharField(max_length=MAX_USERNAME_LENGTH)
    verifycode = serializers.CharField(max_length=4, write_only=True)

    class Meta:
        model = SiteUser
        fields = ('username', 'memberid')

    def validate(self, attrs):
        pass
