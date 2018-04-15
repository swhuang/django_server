# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import *
from users.models import User
from crm.models import Merchant
from pikachu import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

import sys
if settings.USERS_SPAM_PROTECTION:  # pragma: no cover
    from users.forms import RegistrationFormHoneypot as RegistrationForm
else:
    from users.forms import RegistrationForm



def merchant_valid(mid):
    try:
        p = Merchant.objects.get(merchantid=mid)
    except Merchant.DoesNotExist:
        raise serializers.ValidationError('商户不存在')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    userid = serializers.CharField(max_length=15, validators=[UniqueValidator(queryset=User.objects.all())])
    mid = serializers.CharField(max_length=15, validators=[merchant_valid])
    password1 = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'identification', 'userid', 'mid', 'email', 'password1', 'password2')#, 'password')

    #register
    def create(self, validated_data):
        p = Merchant.objects.get(merchantid=validated_data['mid'])
        validated_data['mid'] = p
        validated_data['username'] = unicode(validated_data['username'].encode("raw_unicode_escape"), 'UTF-8')
        form = RegistrationForm(self.context['request'].POST)
        user = form.save()
        return user


def Login(mid):
    try:
        p = Merchant.objects.get(merchantid=mid)
    except Merchant.DoesNotExist:
        raise serializers.ValidationError('商户不存在')

class LogSerializer(serializers.Serializer):
    userid = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=100, read_only=True)
    class Meta:
        model = User
        fields = ('userid', 'username', 'password')


        # def validate_identification(self,):
