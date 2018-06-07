# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
import pikachu.settings
from commom.models import BaseModel, BillamountField, initModel
import logging
from django.db import transaction
from crm.models import RentalOrder
from FP_risk.base.utils import synchronized
from django.utils.functional import SimpleLazyObject





# Create your models here.
# 用户账户
class Account(BaseModel):
    acctid = models.CharField(_(u'账户编号'), max_length=10, unique=True, db_index=True, null=True)
    #user = models.OneToOneField(SiteUser, related_name='account')
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


# 商户层面账务明细表
class Baseacct(BaseModel):
    seq = models.CharField(_(u'账户编号'), max_length=15, db_index=True, null=True)
    debit_credit = models.BooleanField(_(u'借贷方向'), help_text='True:相对商户入账【】False:相对商户出账')
    acid = models.CharField(_(u'科目编号'), max_length=16, blank=True)
    projid = models.CharField(_(u'服务项目编号'), max_length=25)
    serviceType = models.PositiveSmallIntegerField(_(u'服务类型'), default=0, choices=RentalOrder.serv_type)
    merchantid = models.CharField(_(u'商户编号'), default=pikachu.settings.DEFAULT_MERCHANT, max_length=18)
    balance = BillamountField(_(u'当时账户余额'), help_text='该笔账务产生前账户余额')
    billingamt = BillamountField(_(u'账务金额'), default=0.0)
    relatedNumber = models.CharField(_(u'相关编号'), max_length=30, default='')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        m = super(Baseacct, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)
        if not self.seq or self.seq == '':
            self.seq = "%015d" % self.id
            super(Baseacct, self).save(force_update=True, update_fields=['acctid'])

    class Meta:
        unique_together = ('seq', 'acid', 'billingamt', 'relatedNumber')

# 个人账务明细
class Individualacct(Baseacct):
    pass



class FrozenBalance(BaseModel):
    seq = models.CharField(_(u'账户编号'), max_length=15, db_index=True, null=True)
    amount = BillamountField(_(u'冻结金额'), default=0.0)
    orderNo = models.CharField(_(u'订单号'), max_length=25, db_index=True, default='', unique=True)
    isreleased = models.BooleanField(_(u'是否释放'), default=False)




class BillingTran(object):

    def __init__(self, **kwargs):
        assert kwargs.has_key('serviceType')

        self.serviceNo = kwargs.pop('projid', None)
        self.member = kwargs.pop('member')
        self.logger = logging.getLogger('django')
        self.serviceType = kwargs.pop('serviceType', 0)
        try:
            self.acct = Account.objects.get(user=self.member)
        except Exception ,e:
            self.logger.error(e)
            raise ValueError("Error user: "+ self.member.memberId)

    def billingrent(self, amt):
        "租金入账"
        with transaction.atomic():
            DailyBilling = Baseacct(debit_credit=True, acid='DAILYBILL001', projid=self.serviceNo, merchantid=self.acct.mid,
                                balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid, serviceType=self.serviceType)
            DailyBilling.save(force_insert=True)


    def billingdeposit(self, amt):
        "扣减押金入账"
        with transaction.atomic():
            DailyBilling = Baseacct(debit_credit=True, acid='DAILYBILL002', projid=self.serviceNo,
                                    merchantid=self.acct.mid,
                                    balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid, serviceType=self.serviceType)
            DailyBilling.save(force_insert=True)


    def billingdeduct(self, amt):
        "补扣款"
        with transaction.atomic():
            DailyBilling = Baseacct(debit_credit=True, acid='DAILYBILL009', projid=self.serviceNo,
                                    merchantid=self.acct.mid, serviceType=self.serviceType,
                                    balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid)
            DailyBilling.save(force_insert=True)

    def billingfilling(self, amt):
        "余额入账"

        with transaction.atomic():
            DailyBilling = Individualacct(debit_credit=False, acid='BALANBILL101', projid=self.serviceNo,
                                merchantid=self.acct.mid, serviceType=self.serviceType,
                                balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid)
            DailyBilling.save(force_insert=True)


    def billingOuting(self, amt, relatedNo=''):
        "余额出账"
        with transaction.atomic():
            DailyBilling = Individualacct(debit_credit=True, acid='BALANBILL101', projid=self.serviceNo,
                                merchantid=self.acct.mid, serviceType=self.serviceType,
                                balance=self.acct.balance, billingamt=amt, seq=self.acct.acctid, relatedNumber=relatedNo)
            DailyBilling.save(force_insert=True)


class BalanceManager(object):
    """
    余额管理
    """
    def __init__(self, acct=None):
        assert type(acct) == Account or type(acct) == SimpleLazyObject
        self.acct = acct

        def getbillobj(self):
            return BillingTran(member=self.acct.user.memberId, serviceType=0)

        self.billobj = SimpleLazyObject(getbillobj)



    @synchronized   # TODO 解决对象锁的问题
    def freeze(self, amt, orderno):
        assert amt <= self.acct.balance
        FrozenBalance.objects.create(seq=self.acct.acctid, amount=amt, orderNo=orderno)
        self.acct.balance -= amt
        self.acct.save(force_update=True, update_fields=['balance'])

    @synchronized
    def defreeze(self, orderno, isbill=False):
        from crm.models import RentalOrder
        try:
            order = RentalOrder.objects.get(orderNo=orderno)
        except RentalOrder.DoesNotExist:
            logging.getLogger('django').error('订单号错误!')
            raise ValueError('Invaild order number!')
        else:
            billobj = BillingTran(serviceType=order.serviceType, projid=order.serviceNo, member=order.memberId)
        try:
            inst = FrozenBalance.objects.get(orderNo=orderno)
        except FrozenBalance.DoesNotExist:
            logging.getLogger('django').error('没有冻结余额可以释放')
            if isbill:

                if order.amount > order.payedamount:
                    deltaAmt = order.amount - order.payedamount
                    try:
                        Individualacct.objects.get(acid='BALANBILL101', seq=self.acct.acctid, relatedNumber=order.orderNo, billingamt=deltaAmt)
                    except Individualacct.DoesNotExist:
                        # 补账
                        if deltaAmt < self.acct.balance:
                            billobj.billingOuting(deltaAmt, relatedNo=orderno)
                            self.acct.balance -= deltaAmt
                            self.acct.save()
                        else:
                            # 该补账时 余额已经不足以抵扣
                            logging.getLogger('django').error("该补账时 余额已经不足以抵扣, 订单号:%s, 余额补扣金额: %d" % (orderno, deltaAmt))
                            return False
            return True
        else:
            with transaction.atomic():
                if not isbill:
                    self.acct.balance += inst.amount
                    self.acct.save(force_update=True, update_fields=['balance'])
                else:
                    billobj.billingOuting(inst.amount, relatedNo=orderno,)
                inst.isreleased = True
                inst.save()
            return True

    @synchronized
    def withdraw(self, amt):
        assert self.acct.balance >= amt
        with transaction.atomic():
            self.billobj.billingOuting(amt,)
            self.acct.balance -= amt
            self.acct.save(force_update=True, update_fields=['balance'])


    @synchronized
    def recharge(self, amt):
        assert amt > 0
        with transaction.atomic():
            self.billobj.billingfilling(amt)
            self.acct.balance += amt
            self.acct.save(force_update=True, update_fields=['balance'])


