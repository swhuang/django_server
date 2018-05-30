# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductDetail
from crm.server_utils.customerField.Field import *



class ProductSerializer(serializers.ModelSerializer):
    MainImage0 = PdImageField(source='image1', required=False, read_only=True)
    MainImage1 = PdImageField(source='image2', required=False, read_only=True)
    MainImage2 = PdImageField(source='image3', required=False, read_only=True)
    MainImage3 = PdImageField(source='image4', required=False, read_only=True)
    MainImage4 = PdImageField(source='image5', required=False, read_only=True)
    MainImage5 = PdImageField(source='image6', required=False, read_only=True)
    detailImages = PdImageField(required=False, read_only=True)
    createdDate = ModifiedDateTimeField(source='gmt_create', read_only=True)
    createdBy = serializers.CharField(read_only=True)
    lastModifiedBy = serializers.CharField(read_only=True)
    lastModified = serializers.DateTimeField(source='gmt_modified', read_only=True)
    sellingPrice = AmountField()
    diamondWeight = StrfloatField(required=False)

    class Meta:
        model = ProductDetail
        exclude = ('reserved', 'gmt_create','gmt_modified',
                   'image1', 'image2', 'image3', 'image4', 'image5', 'image6')
        read_only_fields = ('productid', )
        write_only_fields = ('image1',)
