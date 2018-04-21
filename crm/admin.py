# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(ComboRental, ProductRental, PaymentOrder, Package, ProductDetail, Submerchant, Merchant,
                ProductItem)
class CrmAdmin(admin.ModelAdmin):
    # list_display = ['subid', 'merchantid', 'productid','']
    pass


@admin.register(RentalOrder)
class RentalOrderAdmin(admin.ModelAdmin):
    list_display = ['orderid', 'orderamount', 'user_id', 'proj', 'comboproj']
    pass


admin.site.site_header = '珠宝租赁管理系统'
admin.site.site_title = '租宝'

