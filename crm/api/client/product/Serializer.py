# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductDetail
from crm.server_utils.customerField.Field import *



class ProductSerializer(serializers.ModelSerializer):
    #MainImage = PdImageField(source='image1', required=False, read_only=True)
    mainimage = serializers.SerializerMethodField()
    #createdDate = ModifiedDateTimeField(source='gmt_create', read_only=True)
    sellingPrice = AmountField()

    class Meta:
        model = ProductDetail
        fields = ('productid', 'title', 'sellingPrice', 'rent', 'series', 'mainimage')

    def get_mainimage(self, obj):
        currobj = None
        if isinstance(obj, ProductDetail):
            for i in range(6):
                name = 'image%s'%(str(i+1))
                if getattr(obj, name).name != '':
                    currobj = getattr(obj, name)
                    break
            if not currobj:
                return None
        else:
            return None
        if not getattr(currobj, 'url', None):
            return None
        request = self.context.get('request', None)
        if request is not None:
            url = '{scheme}://{host}/{path}'.format(scheme=request.scheme,
                                                    host=request.get_host(),
                                                    path=currobj['avatar'].url)
        else:
            url = currobj.url
        return url