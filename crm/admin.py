from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(ComboRental, ProductRental, RentalOrder, PaymentOrder, Package, ProductDetail, Submerchant, Merchant, ProductItem)
class CrmAdmin(admin.ModelAdmin):
    pass
