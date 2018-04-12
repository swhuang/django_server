# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import Merchant

class MerchantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchant
        fields = ('merchantid', 'name', 'date_joined', 'key', 'expiretime','daily_maxcount')