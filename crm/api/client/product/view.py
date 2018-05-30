# -*- coding: utf-8 -*-
from ...admin.product.view import ProductViewset
from crm.models import ProductDetail

class ClientProductViewset(ProductViewset):

    def get_queryset(self):
        return ProductDetail.objects.filter(releaseStatus='1')