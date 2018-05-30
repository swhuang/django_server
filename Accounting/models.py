# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from siteuser.member.models import SiteUser
from django.utils.translation import ugettext_lazy as _
import pikachu.settings
from commom.models import BaseModel, BillamountField, initModel
import logging
from django.db import transaction



# Create your models here.
# 用户账户
class Account(BaseModel):
    acctid = models.CharField(_(u'账户编号'), max_length=10, unique=True, db_index=True, null=True)
    user = models.ForeignKey(SiteUser, related_name='account')
    balance = BillamountField(_(u'账户余额'), default=0.0)
    deposit = BillamountField(_(u'在用押金'), default=0.0)
    rent = BillamountField(_(u'在用租金'), default=0.0)

    @property
    def cashable(self):
        return self.balance - self.deposit - self.rent

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        m = super(Account, self).save()
        if not self.acctid or self.acctid == '':
            self.acctid = "%010d" % self.id
            super(Account, self).save(force_update=True, update_fields=['acctid'])

    def __unicode__(self):
        return self.acctid


# 会计科目
class AccountClassifaction(models.Model):
    c2d = {
        (True, '相对商户入账'),
        (False, '相对商户出账')
    }
    acid = models.CharField(_(u'科目编号'), unique=True, max_length=15)
    desc = models.CharField(_('描述'), max_length=255, blank=True)
    debit_credit = models.BooleanField(_(u'借贷方向'), help_text='True:相对商户入账【】False:相对商户出账', default=True, choices=c2d)


# 账务明细表
class Baseacct(BaseModel):
    seq = models.CharField(_(u'账户编号'), max_length=15, unique=True, db_index=True, null=True)
    debit_credit = models.BooleanField(_(u'借贷方向'), help_text='True:相对商户入账【】False:相对商户出账')
    acid = models.CharField(_(u'科目编号'), max_length=6, blank=True)
    projid = models.CharField(_(u'服务项目编号'), max_length=10)
    merchantid = models.CharField(_(u'商户编号'), default=pikachu.settings.DEFAULT_MERCHANT, max_length=18)
    balance = BillamountField(_(u'当时账户余额'), help_text='该笔账务产生前账户余额')
    billingamt = BillamountField(_(u'账务金额'), default=0.0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        m = super(Baseacct, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)
        if not self.acctid or self.acctid == '':
            self.acctid = "%015d" % self.id
            super(Baseacct, self).save(force_update=True, update_fields=['acctid'])


class BillingTran(object):

    def __init__(self, **kwargs):
        self.serviceNo = kwargs.pop('projid', None)
        self.member = kwargs.pop('member')
        self.logger = logging.getLogger('django')
        try:
            self.acct = Account.objects.get(user=self.member)
        except Exception ,e:
            self.logger.error(e)
            raise ValueError("Error user: "+ self.member.memberId)

    def billingrent(self, amt):
        "租金入账"
        with transaction.atomic:
            DailyBilling = Baseacct(debit_credit=True, acid='DAILYBILL001', projid=self.serviceNo, merchantid=self.acct.mid,
                                balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid)
            DailyBilling.save(force_insert=True)
            self.acct.balance -= amt
            self.acct.rent -= amt
            self.acct.save()
        pass

    def billingdeposit(self, amt):
        "扣减押金入账"
        with transaction.atomic:
            DailyBilling = Baseacct(debit_credit=True, acid='DAILYBILL002', projid=self.serviceNo,
                                    merchantid=self.acct.mid,
                                    balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid)
            DailyBilling.save(force_insert=True)
            self.acct.balance -= amt
            self.acct.deposit -= amt
            self.acct.save()
        pass

    def billingdeduct(self, amt, servrent, servdeposit):
        if amt != (servrent + servdeposit):
            self.logger.error("amt not equals servrent&servdeposit!")
            raise ValueError("amt not equals servrent&servdeposit!")

        "补扣款"
        with transaction.atomic:
            DailyBilling = Baseacct(debit_credit=True, acid='DAILYBILL009', projid=self.serviceNo,
                                    merchantid=self.acct.mid,
                                    balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid)
            DailyBilling.save(force_insert=True)
            self.acct.balance -= amt
            self.acct.rent -= servrent
            self.acct.rent -= servdeposit
            self.acct.save()

    def billingfilling(self, amt):
        with transaction.atomic:
            DailyBilling = Baseacct(debit_credit=False, acid='DAILYBILL101', projid=self.serviceNo,
                                merchantid=self.acct.mid,
                                balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid)
            DailyBilling.save(force_insert=True)
            self.acct.balance += amt
            self.acct.save()
