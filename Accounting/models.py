# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from siteuser.member.models import SiteUser
from django.utils.translation import ugettext_lazy as _

from commom.models import BaseModel, BillamountField, initModel


# Create your models here.
# 用户账户
class Account(BaseModel):
    acctid = models.CharField(_(u'账户编号'), max_length=10, unique=True, db_index=True, null=True)
    user = models.ForeignKey(SiteUser)
    balance = BillamountField(_(u'账户余额'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        m = super(Account, self).save()
        if not self.acctid or self.acctid == '':
            self.acctid = "%010d" % self.id
            super(Account, self).save(force_update=True, update_fields=['acctid'])

#会计科目
class AccountClassifaction(models.Model):
    acid = models.CharField(_(u'科目编号'), unique=True, max_length=6)
    desc = models.CharField(_('描述'))


class Baseacct(BaseModel):
    seq = models.CharField(_(u'账户编号'), max_length=15, unique=True, db_index=True, null=True)
    debit_credit = models.BooleanField(_(u'借贷方向'))
    acid = models.CharField(_(u'科目编号'))
    user = models.ForeignKey(SiteUser)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        m = super(Baseacct, self).save()
        if not self.acctid or self.acctid == '':
            self.acctid = "%015d" % self.id
            super(Baseacct, self).save(force_update=True, update_fields=['acctid'])