# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from pikachu import settings
from crm.server_utils.base import FSM as fsm
import datetime
import random
import json


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


class SubBaseModel(initModel):
    mid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT, db_index=True)
    #submid = models.CharField(_(u'门店编号'), max_length, db_index=True)

    class Meta:
        abstract = True

class BaseModel(initModel):
    mid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT, db_index=True)
    submid = models.CharField(_(u'门店编号'), max_length=15, db_index=True, default='')

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


class BillamountField(models.DecimalField):
    def __init__(self, verbose_name=None, name=None, max_digits=None,
                 decimal_places=None, **kwargs):
        super(BillamountField, self).__init__(verbose_name=verbose_name, max_digits=12, decimal_places=2, **kwargs)


class JSONField(models.TextField):  

    def from_db_value(self, value, expression, connection, context):
        v = models.TextField.to_python(self, value)
        try:
            return json.loads(v)['v']
        except:
            pass
        return v

    def get_prep_value(self, value):  
        return json.dumps({'v':value})



class StatusField(models.IntegerField):

    def from_db_value(self, value, expression, connection, context):
        v = models.IntegerField.to_python(self, value)
        ret = None
        if v == fsm.START_STATE:
            ret = fsm.Start()
        elif v == fsm.RENTAL_CONFIRM:
            ret = fsm.RentalConfirmed()
        elif v == fsm.RENTALPROC_STATE:
            ret = fsm.RentalProcessing()
        elif v == fsm.COMPLETE:
            ret = fsm.Completed()
        try:
            return ret
        except:
            pass
        return ret

    def get_prep_value(self, value):
        return value.statevalue

