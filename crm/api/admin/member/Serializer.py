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
    '''
    email = serializers.EmailField()
    userid = serializers.CharField(max_length=15, validators=[UniqueValidator(queryset=User.objects.all())])
    #mid = serializers.CharField(max_length=15, validators=[merchant_valid])
    #mid = serializers.SlugRelatedField(queryset=Merchant.objects.all(), slug_field='merchantid')
    merchantid = serializers.CharField(source='mid.merchantid', validators=[merchant_valid])
    password1 = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)
    '''
    class Meta:
        model = SiteUser
        fields = "__all__"
    # register
    '''
    def create(self, validated_data):
        try:
            p = Merchant.objects.get(merchantid=validated_data['mid'])
        except Merchant.DoesNotExist:
            p = Merchant.objects.get(merchantid=settings.DEFAULT_MERCHANT)
        validated_data['mid'] = p
        validated_data['username'] = unicode(validated_data['username'].encode("raw_unicode_escape"), 'UTF-8')
        form = RegistrationForm(self.context['request'].POST)
        user = form.save()
        return user
    '''

