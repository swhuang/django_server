# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

# Create your models here.
#@python_2_unicode_compatible
class OrderInfo(models.Model):

    orderid = models.CharField(_(u'订单信息'), max_length=30)
    class Meta:
        permissions = (
            ("view", "can view the available order"),
            ("change", "can change the status")
        )

#@python_2_unicode_compatible
class Merchant(models.Model):
    pass