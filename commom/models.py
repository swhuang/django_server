# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from pikachu import settings
import datetime
import random


# Create your models here.
class initModel(models.Model):
    gmt_create = models.DateTimeField(_('添加时间'), default=timezone.now)
    gmt_modified = models.DateTimeField(_('修改时间'), default=timezone.now)

    class Meta:
        abstract = True
        ordering = ('gmt_create', 'gmt_modified',)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.gmt_modified = timezone.now()
        super(initModel, self).save()

    def getDict(self):
        d = {}
        d['gmt_create'] = self.gmt_create.strftime('%y-%m-%d %H:%M:%S')
        d['gmt_modified'] = self.gmt_modified.strftime('%y-%m-%d %H:%M:%S')
        return d


class BaseModel(initModel):
    mid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT, db_index=True)

    class Meta:
        abstract = True


def randomtril():
    seed = "1234567890"
    sa = []
    for i in range(4):
        sa.append(random.choice(seed))
    return ''.join(sa)


def gettimestamp():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')


def Ordertimestamp():
    return 'O' + gettimestamp() + randomtril()


def Paytimestamp():
    return 'P' + gettimestamp() + randomtril()
