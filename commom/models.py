# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class BaseModel(models.Model):

    gmt_create = models.DateTimeField(_('添加时间'), default=timezone.now)
    gmt_modified = models.DateTimeField(_('修改时间'), default=timezone.now)
    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.gmt_modified = timezone.now()
        super(BaseModel, self).save()
