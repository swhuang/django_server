# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from commom.models import *
from pikachu import settings
from decimal import Decimal
from server_utils.base.FSM import *
import random
import json
import datetime
from easy_thumbnails.fields import ThumbnailerImageField



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


INVENTORY = 1000


class MerchantManager(models.Manager):
    r'''

    '''


# @python_2_unicode_compatible
# 主商户
class Merchant(initModel):
    _uuid = autonumber
    merchantid = models.CharField(_(u'商户号'), max_length=15, unique=True, db_index=True, default='10000000123',
                                  editable=False)
    name = models.CharField(_(u'商户名称'), max_length=200)
    date_joined = models.DateTimeField(_('添加时间'), default=timezone.now)
    key = models.CharField(_(u'密钥'), max_length=200, default='')
    expiretime = models.CharField(_(u'有效时间'), max_length=6, default='3600')
    daily_maxcount = models.IntegerField(_(u'每日最大访问次数'), default=100)

    guarantee_pct = models.PositiveIntegerField(_(u'押金比例'), default=70)  # 70 = 70%
    daily_amount_pct = models.PositiveIntegerField(_(u'日租金比例'), default=5)  # 5 = 5%

    class Meta:
        verbose_name = _('商户管理')
        verbose_name_plural = _('商户管理')

    def save(self, *args, **kwargs):
        _m = super(Merchant, self).save(*args, **kwargs)
        # _m = self.save()
        if self.merchantid == None or self.merchantid == '10000000123':
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
        d.update(super(Merchant, self).getDict())
        return d


DEFAULT_MERCHANT_OBJ = Merchant(merchantid=settings.DEFAULT_MERCHANT)  #


# 门店
class Submerchant(SubBaseModel):
    subid = models.CharField(_(u'门店编号'), max_length=15, db_index=True, unique=True, default='0',
                             editable=False)  # primary key

    class Meta:
        verbose_name = _('门店管理')
        verbose_name_plural = _('门店管理')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        _m = super(Submerchant, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                           update_fields=update_fields)
        if self.subid == '0':
            self.subid = "%015d" % self.id
            super(Submerchant, self).save(force_update=True, update_fields=['subid'])


CATEGORY = {}
CATEGORY['ALL'] = 0
CATEGORY['项链'] = 1
CATEGORY['戒指'] = 2


# 商品
class ProductDetail(BaseModel):
    productid = models.CharField(_(u'产品编号'), max_length=15, db_index=True, unique=True, default='0')  # primary key
    model = models.CharField(_(u'商品型号'), max_length=10, unique=True, null=True)
    productname = models.CharField(_(u'产品名称'), max_length=30, default='')
    category = models.PositiveIntegerField(_(u'商品分类'), default=CATEGORY['ALL'])
    goldType = models.CharField(_(u'商品材质'), max_length=10, default='')
    goldpurity = models.CharField(_(u'材质纯度'), max_length=5, default='')
    goldContent = models.CharField(_(u'含金量(克)'), max_length=10, default='')
    diamondWeight = models.FloatField(_(u'钻石重量(克)'), default=0.0)#models.CharField(_(u'钻石重量(克)'), max_length=10, default='')
    productprice = BillamountField(_(u'产品售价'))  # models.DecimalField(_(u'产品售价'), max_digits=12, decimal_places=2)
    releaseStatus = models.BooleanField(_(u'是否发布'), default=False)
    proddesc = models.CharField(_(u'产品描述'), max_length=500, default='')
    series = models.CharField(_(u'系列'), max_length=10, default='')
    certificate = models.CharField(_(u'证书'), max_length=30, default='')
    inventory = models.IntegerField(_(u'库存数量'), default=INVENTORY)
    guarantee = BillamountField(_(u'押金'), default=0.0)
    size = models.CharField(_(u'尺寸'), max_length=5, default='')
    remark = models.CharField(_(u'备注'), max_length=100, default='')
    rentalprice = BillamountField(_(u'租赁单价'), default=0.0)
    rentType = models.CharField(_(u'租赁类型'), default=0, max_length=1) #0：日租，1：周租，2：月租
    rentcycle = models.PositiveSmallIntegerField(_(u'租赁起始天数'), default=1)
    reletcycle = models.PositiveSmallIntegerField(_(u'租赁周期'), default=1)

    attributes = JSONField(_(u'产品参数'), default={})

    detailImages = ThumbnailerImageField(verbose_name=_(u'详情图片'), upload_to='img/product', default='', blank=True)

    image1 = ThumbnailerImageField(verbose_name=_(u'图片1'), upload_to='img/product', default='', blank=True)
    #image1 = models.ImageField(_(u'图片1'), null=True, upload_to='img/product', default='')
    image2 = ThumbnailerImageField(verbose_name =_(u'图片2'), blank=True, upload_to='img/product', default='')
    image3 = ThumbnailerImageField(verbose_name =_(u'图片3'), blank=True, upload_to='img/product', default='')
    image4 = ThumbnailerImageField(verbose_name =_(u'图片4'), blank=True, upload_to='img/product', default='')
    image5 = ThumbnailerImageField(verbose_name =_(u'图片5'), blank=True, upload_to='img/product', default='')
    image6 = ThumbnailerImageField(verbose_name =_(u'图片6'), blank=True, upload_to='img/product', default='')

    reserved = models.CharField(_(u'reserved'), default='', max_length=200)

    class Meta:
        ordering = ('productid', 'mid')
        verbose_name = '商品管理'
        verbose_name_plural = '商品管理'

    def __str__(self):
        return self.productid

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        _m = super(ProductDetail, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                             update_fields=update_fields)
        if self.productid == '0':
            self.productid = "%015d" % self.id
            super(ProductDetail, self).save(force_update=True, update_fields=['productid'])


# SKU商品
class ProductItem(BaseModel):
    itemid = models.CharField(_(u'真实产品ID'), max_length=18, db_index=True, unique=True, default='0', editable=False)
    name = models.CharField(_(u'产品名字'), max_length=50)
    inventory = models.IntegerField(_(u'库存数量'), default=INVENTORY)
    attributes = JSONField(_(u'产品参数'), default={})
    productprice = BillamountField(_(u'产品售价'))
    pdetail = models.ForeignKey(ProductDetail, related_name='proditem')

    class Meta:
        ordering = ('itemid',)
        verbose_name = 'SKU商品'
        verbose_name_plural = 'SKU商品'


# 套餐
class Package(BaseModel):
    name = models.CharField(_('套餐名字'), max_length=10, default='')
    low_bound = BillamountField(_('价格下限'))  # models.DecimalField(_('价格下限'), max_digits=12, decimal_places=2)
    high_bound = BillamountField(_('价格上限'))  # models.DecimalField(_('价格上限'), max_digits=12, decimal_places=2)

    def getProductList(self, offset=0, limit=0):
        marg = {}
        marg['productprice__gte'] = self.low_bound
        marg['productprice__lte'] = self.high_bound
        if offset == 0 and limit == 0:
            productinfo = list(ProductDetail.objects.filter(**marg))
        else:
            productinfo = list(ProductDetail.objects.filter(**marg)[offset:offset + limit])

        return productinfo

    class Meta:
        verbose_name_plural = _('套餐管理')
        verbose_name = _('套餐管理')


START_STATE = 0
RENTALPROC_STATE = 1
SELLPROC_STATE = 2
COMPLETE = 3


# 租赁服务
class Project(BaseModel):
    r"""

    """
    proj_id = models.CharField(_(u'服务编号'), max_length=10, default='', db_index=True, editable=False)
    proj_name = models.CharField(max_length=128, default='')
    # productid = models.CharField(_(u'产品编号'), max_length=15, null=False, default='0')
    user_id = models.CharField(_(u'用户编号'), max_length=15, null=False, default='0')
    currsts = StatusField(_(u'服务状态'), default=Start)# models.IntegerField(_(u'服务状态'), default=0)
    create_user = models.CharField(_(u'创建者'), max_length=10, default='user')  # 创建者:店员or用户
    start_time = models.DateField(_(u'开始时间'), auto_now=True) #models.DateTimeField(_(u'开始时间'), default=timezone.now)
    end_time = models.DateField(_(u'结束时间'), default=timezone.now().strftime('%Y-%m-%d'))
    cycle_day = models.IntegerField(_(u'租赁周期'), default=1)
    process_day = models.IntegerField(_(u'租赁时长'), default=1)
    guarantee = BillamountField(_(u'押金'), default=0.0)
    payed_amount = BillamountField(_(u'总共支付的金额'), default=0.0)
    current_payamount = BillamountField(_(u'当前需要支付金额'), default=0.0)

    class Meta:
        ordering = ('proj_id', 'mid')
        abstract = True

    def __init__(self, *args, **kwargs):

        super(Project, self).__init__(*args, **kwargs)
        m = Merchant.objects.get(merchantid=self.mid)
        if not self.product:
            print ("error for null product")
            return

        if self.guarantee == 0.0:
            self.guarantee = round((m.guarantee_pct / 100) * self.product.rentalprice, 2)

        if self.current_payamount == 0.0:
            self.current_payamount = round(
                Decimal(self.guarantee) + Decimal(self.process_day * self.product.rentalprice * (m.daily_amount_pct / 100)), 2)

        if not self.currsts:
            self.currsts = Start()
            #self.__state = START_STATE

    def set_state(self, s):
        self.currsts = s

    def updatestate(self):
        self.currsts.updatestate(self)

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        if self.proj_id == '':
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
        d.update(super(Project, self).getDict())
        return d


# 商品租赁服务
class ProductRental(Project):
    product = models.ForeignKey(ProductDetail)

    def __unicode__(self):
        return self.proj_id

    def __init__(self, *args, **kwargs):
        super(ProductRental, self).__init__(*args, **kwargs)

        if self.product != None:
            v = self.product
            self.proj_name = v.productname
            self.guarantee = v.guarantee
        self.set_state(Start())

    def genRentalOrder(self):
        ro = RentalOrder(proj=self, user_id=self.user_id)  # to_be_done

    class Meta:
        verbose_name = _('租赁服务')
        verbose_name_plural = _('租赁服务')

    pass


# 套餐租赁服务
class ComboRental(Project):
    product = models.ForeignKey(Package)
    current_product = models.ForeignKey(ProductDetail, null=True)
    changelist = models.CharField(_(u'租品变化情况'), default='', max_length=3000)

    def __unicode__(self):
        return self.proj_id

    def save(self, *args, **kwargs):
        super(ComboRental, self).save(*args, **kwargs)
        pass

    class Meta:
        verbose_name = _('套餐租赁服务')
        verbose_name_plural = _('套餐租赁服务')

    pass


# 订单
class Order(BaseModel):
    r"""

    """
    # from users.models import Member
    # userinfo = models.ForeignKey(Member, null=True)
    user_id = models.CharField(_(u'用户编号'), max_length=15, null=False)

    # proj = models.CharField(_(u'服务编号'), max_length=10, null=False, default='0')
    paytime = models.DateTimeField(_(u'支付时间'), default=timezone.now)
    orderamount = BillamountField(_(u'订单金额'))  # models.DecimalField(_(u'订单金额'), max_digits=12, decimal_places=2)
    payedamount = BillamountField(_(u'支付金额'),
                                  default=0.0)  # models.DecimalField(_(u'支付金额'), max_digits=12, decimal_places=2)
    payment_status = models.SmallIntegerField(_(u'支付状态'), default=0)  # 0:未支付 1:支付成功
    orderid = models.CharField(max_length=20, default=gettimestamp, db_index=True, unique=True, editable=False)

    status = models.IntegerField(_('订单状态'),default = fsm.ORDER_START)

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        if self.proj_id and self.comboproj:
            raise ValidationError(_('proj 和 comboproj 无法同时存在'))
        if not self.proj_id and not self.comboproj:
            raise ValidationError(_('proj 和 comboproj 无法同时为空'))
        if self.proj:
            self.orderamount = self.proj.current_payamount
        if self.comboproj:
            self.orderamount = self.comboproj.current_payamount


    class Meta:
        ordering = ('orderid',)
        abstract = True

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
        d.update(super(Order, self).getDict())
        return d


class RentalOrder(Order):
    proj = models.ForeignKey(ProductRental, null=True, related_name="RentalOrderid")
    comboproj = models.ForeignKey(ComboRental, null=True, related_name="RentalOrderid")

    class Meta:
        verbose_name = _('租赁订单')
        verbose_name_plural = _('租赁订单')

    def clean(self):
        if self.proj_id and self.comboproj:
            raise ValidationError(_('proj 和 comboproj 无法同时存在'))
        if not self.proj_id and not self.comboproj:
            raise ValidationError(_('proj 和 comboproj 无法同时为空'))


class SaleOrder(Order):
    proj = models.ForeignKey(ProductRental, null=True, related_name='SaleOrderid')
    comboproj = models.ForeignKey(ComboRental, null=True, related_name='SaleOrderid')

    class Meta:
        verbose_name = _('销售订单')
        verbose_name_plural = _('销售订单')

    def clean(self):
        if self.proj_id and self.comboproj:
            raise ValidationError(_('proj 和 comboproj 无法同时存在'))
        if not self.proj_id and not self.comboproj:
            raise ValidationError(_('proj 和 comboproj 无法同时为空'))


# 支付订单
class PaymentOrder(BaseModel):
    pay_id = models.CharField(max_length=20, db_index=True, unique=True)
    order_id = models.CharField(max_length=20, default='0')
    user_id = models.CharField(_(u'用户编号'), max_length=15, null=False, default='0')
    payedamount = BillamountField(
        _(u'支付金额'))  # models.DecimalField(_(u'支付金额'), max_digits=12, decimal_places=2, null=True)

    # mid = models.CharField(_(u'总店编号'), max_length=15, default=settings.DEFAULT_MERCHANT)
    class Meta:
        verbose_name = _('支付订单')
        verbose_name_plural = _('支付订单')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.payment_id == '' or self.payment_id == None:
            self.payment_id = Paytimestamp()
        super(PaymentOrder, self).save(force_insert=False, force_update=False, using=None,
                                       update_fields=None)


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
