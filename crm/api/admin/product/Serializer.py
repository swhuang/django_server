# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductDetail


class ProductSerializer(serializers.ModelSerializer):
    #createdDate = serializers.DateTimeField(source='gmt_create', read_only=True)


    class Meta:
        model = ProductDetail
        exclude = ('reserved', 'gmt_create', 'gmt_modified', 'createdBy', 'lastModifiedBy')
