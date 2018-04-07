# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from commom.models import BaseModel
from pikachu import settings
from decimal import Decimal
from users.utils import gettimestamp
import random
import json
import datetime

# Create your models here.
# @python_2_unicode_compatible
class OrderInfo(BaseModel):
    orderid = models.CharField(_(u'订单信息'), max_length=30)
    description = models.CharField(_(u'描述信息'), max_length=500, null=True)
    class Meta:
        permissions = (
            ("view", "can view the available order"),
            ("change", "can change the status")
        )


class autonumber(object):
    # @staticmethod
    def getunion(self):
        return '10000'


class MerchantManager(models.Manager):
    r'''

    '''

# @python_2_unicode_compatible
#主商户
class Merchant(BaseModel):
    _uuid = autonumber
    merchantid = models.CharField(_(u'商户号'), max_length=15, unique=True, db_index=True, default='10000000123')
    name = models.CharField(_(u'商户名称'), max_length=200)
    date_joined = models.DateTimeField(_('添加时间'), default=timezone.now)
    key = models.CharField(_(u'密钥'), max_length=200, default='')
    expiretime = models.CharField(_(u'有效时间'), max_length=6, default='3600')
    daily_maxcount = models.IntegerField(_(u'每日最大访问次数'), default=100)
    class Meta:
        verbose_name = _('Merchant')
        verbose_name_plural = _('Merchant')

    def save(self, *args, **kwargs):
        _m = super(Merchant, self).save(*args, **kwargs)
        #_m = self.save()
        if self.merchantid == None or self.merchantid == '':
            self.merchantid = "%015d" % self.id
        super(Merchant, self).save(force_update=True, update_fields=['merchantid'])

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
        return json.dumps(d)

    def getDict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
        return d

DEFAULT_MERCHANT_OBJ = Merchant(merchantid=settings.DEFAULT_MERCHANT)#
# 门店
class Submerchant(BaseModel):
    subid = models.CharField(_(u'门店编号'), max_length=15, db_index=True, unique=True) #primary key
    basemerchantid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT)
    class Meta:
        verbose_name = _('Submerchant')
        verbose_name_plural = _('Submerchant')


#商品
class ProductDetail(BaseModel):
    productid = models.CharField(_(u'产品编号'), max_length=18, db_index=True, unique=True) #primary key
    productname = models.CharField(_(u'产品名称'), max_length=30)
    productprice = models.DecimalField(_(u'产品售价'), max_digits=12, decimal_places=2)
    proddesc = models.CharField(_(u'产品描述'), max_length=500)
    mid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT)

    class Meta:
        ordering = ('productid', )

    def __str__(self):
        return self.productid

#租赁服务
class Project(BaseModel):
    r"""

    """
    proj_id = models.CharField(max_length=10, default='', db_index=True)
    proj_name = models.CharField(max_length=128, default='')
    #mid = models.ForeignKey(Merchant, null=True, default=Merchant(merchantid=settings.DEFAULT_MERCHANT))
    mid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT)

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        self.proj_id = "%010d" % self.id
        super(Project, self).save(force_update=True, update_fields=['proj_id'])

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), Merchant):
                dic = json.loads(getattr(self, attr).toJSON())
                d.update(dic)
            elif isinstance(getattr(self, attr), Decimal):
                d[attr] = str(getattr(self, attr))
            else:
                d[attr] = getattr(self, attr)
        return json.dumps(d)

    def getDict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), Merchant):
                d.update(getattr(self, attr).getDict())
            elif isinstance(getattr(self, attr), Decimal):
                d[attr] = str(getattr(self, attr))
            else:
                d[attr] = getattr(self, attr)
        return d

class Order(BaseModel):
    r"""

    """
    from users.models import Member
    userinfo = models.ForeignKey(Member, null=True)
    proj = models.ForeignKey(Project, null=True)
    paytime = models.DateTimeField(_(u'支付时间'), default=timezone.now)
    orderamount = models.DecimalField(_(u'订单金额'), max_digits=12, decimal_places=2)
    payedamount = models.DecimalField(_(u'支付金额'), max_digits=12, decimal_places=2)
    payment_status = models.SmallIntegerField(_(u'支付状态'))
    #mid = models.ForeignKey(Merchant, db_index=True, null=True, default=Merchant(merchantid=settings.DEFAULT_MERCHANT))
    mid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT)
    orderid = models.CharField(max_length=20, default=gettimestamp, db_index=True, unique=True)

    class Meta:
        ordering = ('orderid',)

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}

        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            elif isinstance(getattr(self, attr), Merchant):
                dic = json.loads(getattr(self, attr).toJSON())
                d.update(dic)
            elif isinstance(getattr(self, attr), Project):
                dic = json.loads(getattr(self, attr).toJSON())
                d.update(dic)
            elif isinstance(getattr(self, attr), Member):
                dic = json.loads(getattr(self, attr).toJSON())
                d.update(dic)
            elif isinstance(getattr(self, attr), Decimal):
                d[attr] = str(getattr(self, attr))
            else:
                d[attr] = getattr(self, attr)
        return json.dumps(d)

    def getDict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            elif isinstance(getattr(self, attr), Merchant):
                d.update(getattr(self, attr).getDict())
            elif isinstance(getattr(self, attr), Project):
                d.update(getattr(self, attr).getDict())
            elif isinstance(getattr(self, attr), Member):
                d.update(getattr(self, attr).getDict())
            elif isinstance(getattr(self, attr), Decimal):
                d[attr] = str(getattr(self, attr))
            else:
                d[attr] = getattr(self, attr)
        return d


class PaymentOrder(BaseModel):
    payment_id = models.CharField(max_length=20, default=gettimestamp, db_index=True, unique=True)
    mid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT)

class Userdata(models.Model):
    username = models.CharField(_(u'用户名'), max_length=200)
    date_joined = models.DateTimeField(_(u'添加时间'), default=timezone.now)
    phone = models.CharField(_(u'联系电话'), max_length=20)
    vertime = models.CharField(_(u'验证时间'), max_length=200, default='')

    # data_section = models.IntegerField(_(u'数据区块'))
    # merchantid = models.ForeignKey(Merchant)
    def getinfo(self):
        retmsg = {}
        retmsg['username'] = self.username
        retmsg['phone'] = self.phone
        retmsg['vertime'] = self.vertime
        retmsg['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return retmsg

    class Meta:
        verbose_name = _('Userdata')
        verbose_name_plural = _('Merchant')


class Datapool(models.Model):
    r"""
    每1000个编号的userdata数据为一条记录；
    每新增一个商户增加 记录数/1000 条数据
    """
    merchantid = models.CharField(_(u'商户编号'), max_length=15, db_index=True, default='')
    mid = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    datapool = models.TextField(_(u'数据池'))

    # merchantid = models.CharField()
    @staticmethod
    def get_single_data(merchantid):
        dp = Datapool.objects.filter(merchantid=merchantid).values()
        try:
            r1 = random.randint(0, dp.count())
            _l = str(dp[r1]['datapool']).split(',')
            r2 = random.randint(0, len(_l))

            key = int(_l[r2])
            del _l[r2]

            if len(_l) != 0:
                p = Datapool.objects.get(id=dp[r1]['id'])
                p.datapool = ','.join(_l)
                p.save()
            else:
                dp[r1].delete()

            return key
        except:
            raise ValueError


class TokenManager(models.Model):
    r"""
    针对每个token进行限制管理
    """
    token = models.CharField(_(u'用户token'), max_length=100, db_index=True)
    count = models.IntegerField(_(u'已访问次数'), default=0)
    max_count = models.IntegerField(_(u'最大访问次数'), default=100)

