# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductDetail


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDetail
        exclude = ('reserved', 'gmt_create', 'gmt_modified', 'createdBy', 'lastModifiedBy')
        #read_only_fields = ('productid', )

    #def post(self):

    def create(self, validated_data):
        if validated_data.has_key('productid'):
            #update
            pid = validated_data.pop('productid')
            try:
                p = ProductDetail.objects.get(productid=pid)
            except ProductDetail.DoesNotExist:
                raise serializers.ValidationError(detail={"message": "无效的productid"})

            self.update(p, validated_data)
        else:#new
            return self.save()

