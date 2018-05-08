# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import *
from siteuser.member.models import SiteUser
from crm.models import Merchant
from pikachu import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

import sys


def merchant_valid(mid):
    try:
        p = Merchant.objects.get(merchantid=mid)
    except Merchant.DoesNotExist:
        raise serializers.ValidationError('商户不存在')


class MemberSerializer(serializers.ModelSerializer):


    class Meta:
        model = SiteUser
        # fields = "__all__"
        exclude = ('is_social', 'is_active', 'username', 'avatar_url', 'avatar_name', 'mid', 'date_joined')
        read_only_fields = ('name', 'idNo', 'idType', 'gender', 'phone', 'birthday', 'source', 'createdDate')

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.address = validated_data['address']
        instance.save()
        return instance

    # register
    def validate(self, attrs):
        try:
            p = SiteUser.objects.get(memberid=attrs['memberid'])
        except SiteUser.DoesNotExist:
            raise serializers.ValidationError("memberid 错误")
        return attrs

    def create(self, validated_data):
        p = SiteUser.objects.get(memberid=validated_data['memberid'])
        p.email = validated_data['email']
        p.address = validated_data['address']
        return p
