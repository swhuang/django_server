# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import transaction
from django.db.models.signals import post_delete
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from commom.models import *
from pikachu import settings
from decimal import Decimal
from django.forms.models import model_to_dict
from server_utils.base.FSM import *
from django_model_changes import ChangesMixin
from django.db.models import signals
from django.dispatch import receiver
import random
import json
import datetime
from easy_thumbnails.fields import ThumbnailerImageField
import logging
import os


# Create your models here.
# @python_2_unicode_compatible
class OrderInfo(BaseModel):
    orderNo = models.CharField(_(u'订单信息'), max_length=30)
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
CATEGORY['ALL'] = '0'
CATEGORY['项链'] = '1'
CATEGORY['戒指'] = '2'


def getuploadpath(model, filename):
    return 'img/product/%s/%s' % (model.model, filename)


# 商品
class ProductDetail(BaseModel):
    productid = models.CharField(_(u'产品编号'), max_length=15, db_index=True, unique=True, default='0')  # primary key
    model = models.CharField(_(u'商品型号'), max_length=10, unique=True, null=True, blank=True)
    title = models.CharField(_(u'产品名称'), max_length=30, default='')
    category = models.CharField(_(u'商品分类'), default=CATEGORY['ALL'], max_length=2)
    goldType = models.CharField(_(u'商品材质'), max_length=10, default='', blank=True)
    goldPurity = models.CharField(_(u'材质纯度'), max_length=5, default='', blank=True)
    goldContent = models.CharField(_(u'含金量(克)'), max_length=10, default='', blank=True)
    diamondWeight = models.FloatField(_(u'钻石重量(克)'),
                                      default=0.0)  # models.CharField(_(u'钻石重量(克)'), max_length=10, default='')
    sellingPrice = BillamountField(_(u'产品售价'))  # models.DecimalField(_(u'产品售价'), max_digits=12, decimal_places=2)
    releaseStatus = models.CharField(_(u'是否发布'), default='0', max_length=1)
    brand = models.CharField(_(u'品牌'), max_length=20, default='', blank=True)
    desc = models.CharField(_(u'产品描述'), max_length=500, default='', blank=True)
    series = models.CharField(_(u'系列'), max_length=10, default='', blank=True)
    certificate = models.CharField(_(u'证书'), max_length=30, default='', blank=True)
    inventory = models.IntegerField(_(u'库存数量'), default=INVENTORY)
    deposit = BillamountField(_(u'押金'), default=0.0)
    size = models.CharField(_(u'尺寸'), max_length=5, default='', blank=True)
    remark = models.CharField(_(u'备注'), max_length=100, default='', blank=True)
    rent = BillamountField(_(u'租赁单价'), default=0.0)
    rentType = models.CharField(_(u'租赁类型'), default=0, max_length=1)  # 0：日租，1：周租，2：月租
    rentcycle = models.PositiveSmallIntegerField(_(u'租赁起始天数'), default=1)
    reletcycle = models.PositiveSmallIntegerField(_(u'租赁周期'), default=1)

    attributes = JSONField(_(u'产品参数'), default={})

    detailImages = ThumbnailerImageField(verbose_name=_(u'详情图片'), upload_to=getuploadpath, default='', blank=True)

    image1 = ThumbnailerImageField(verbose_name=_(u'图片1'), upload_to=getuploadpath, default='', blank=True)
    # image1 = models.ImageField(_(u'图片1'), null=True, upload_to='img/product', default='')
    image2 = ThumbnailerImageField(verbose_name=_(u'图片2'), blank=True, upload_to=getuploadpath, default='')
    image3 = ThumbnailerImageField(verbose_name=_(u'图片3'), blank=True, upload_to=getuploadpath, default='')
    image4 = ThumbnailerImageField(verbose_name=_(u'图片4'), blank=True, upload_to=getuploadpath, default='')
    image5 = ThumbnailerImageField(verbose_name=_(u'图片5'), blank=True, upload_to=getuploadpath, default='')
    image6 = ThumbnailerImageField(verbose_name=_(u'图片6'), blank=True, upload_to=getuploadpath, default='')

    reserved = models.CharField(_(u'reserved'), default='', max_length=200, blank=True)

    def delete_image_obj(self, obj):
        path = os.path.join(settings.MEDIA_ROOT, obj.name)
        logging.getLogger('django').info('Deleting file:' + path)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception, e:
                logging.getLogger('django').error(e)

    def delete_image(self):
        for i in range(6):
            img = getattr(self, "image" + str(i + 1), None)
            if img:
                self.delete_image_obj(img)
        self.delete_image_obj(self.detailImages)

    class Meta:
        ordering = ('productid', 'mid')
        verbose_name = '商品管理'
        verbose_name_plural = '商品管理'

    def __str__(self):
        return self.productid

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, userid=None):

        _m = super(ProductDetail, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                             update_fields=update_fields)
        if not userid:
            self.lastModifiedBy = userid
        if self.productid == '0':
            self.productid = "%015d" % self.id
            if not userid:
                self.createdBy = userid
            super(ProductDetail, self).save(force_update=True, update_fields=['productid'])


# 删除图片hook
def _delete_image_on_disk(sender, instance, *args, **kwargs):
    instance.delete_image()


post_delete.connect(_delete_image_on_disk, sender=ProductDetail)


# SKU商品
class ProductItem(BaseModel):
    itemid = models.CharField(_(u'真实产品ID'), max_length=18, db_index=True, unique=True, default='0', editable=False)
    name = models.CharField(_(u'产品名字'), max_length=50)
    inventory = models.IntegerField(_(u'库存数量'), default=INVENTORY)
    attributes = JSONField(_(u'产品参数'), default={})
    sellingPrice = BillamountField(_(u'产品售价'))
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
        marg['sellingPrice__gte'] = self.low_bound
        marg['sellingPrice__lte'] = self.high_bound
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


class ServiceManager(models.Manager):
    def create(self, *args, **kwargs):
        pass


# 租赁服务
class Project(ChangesMixin, BaseModel):
    r"""

    """
    Credit_Level = {
        ('0', '正常'),
        ('1', '逾期'),
        ('2', '超限'),
    }

    service_status = {
        (0, '租赁服务已创建'),
        (1, '待支付'),
        (2, '待取货'),
        (3, '服务关闭'),
        (4, '租赁中'),
        (5, '租赁完成'),
        (6, '租转售完成'),
    }

    delivery_dic = {
        ('0', '自提'),
        ('1', '邮寄')
    }

    serviceNo = models.CharField(_(u'服务编号'), max_length=25, default='', db_index=True, editable=False)
    isCompleted = models.BooleanField(_(u'服务单是否完成'), default=False, db_index=True)
    proj_name = models.CharField(max_length=128, default='')
    serviceType = models.CharField(_(u'服务状态'), max_length=1, default='')
    # productid = models.CharField(_(u'产品编号'), max_length=15, null=False, default='0')
    memberId = models.CharField(_(u'用户编号'), max_length=15, null=False, default='0')
    name = models.CharField(_(u'姓名'), max_length=100, default='')
    phone = models.CharField(_(u'手机号'), max_length=50, default='', db_index=True)
    receiverName = models.CharField(_(u'收货人姓名'), max_length=50, default='')
    receiverPhone = models.CharField(_(u'收货人手机'), max_length=50, default='', help_text=u'客户端填写的收货人信息')
    address = models.CharField(_(u'地址'), max_length=200, default='', blank=True, help_text=u'客户端填写的地址,覆盖原地址')
    serviceStatus = StatusField(_(u'服务状态'), default=Start,
                                choices=service_status)  # models.IntegerField(_(u'服务状态'), default=0)
    create_user = models.CharField(_(u'创建者'), max_length=10, default='user')  # 创建者:店员or用户
    rentStartDate = models.DateField(_(u'开始时间'),
                                     auto_now=True)  # models.DateTimeField(_(u'开始时间'), default=timezone.now)
    rentDueDate = models.DateField(_(u'结束时间'), default=timezone.now().strftime('%Y-%m-%d'))
    cycle_day = models.IntegerField(_(u'租赁周期'), default=1)
    rentPeriod = models.IntegerField(_(u'租赁时长'), default=1)
    initialRent = BillamountField(_(u'初始租金'), default=0.0)
    initialDeposit = BillamountField(_(u'初始押金'), default=0.0)
    payed_amount = BillamountField(_(u'总共支付的金额'), default=0.0)
    current_payamount = BillamountField(_(u'当前需要支付金额'), default=0.0)
    realChargingTime = models.PositiveIntegerField(_(u'实际计费时长'), default=0)
    residualRent = BillamountField(_(u'剩余租金'), default=0.0)
    residualDeposit = BillamountField(_(u'剩余押金'), default=0.0)
    creditStatus = models.CharField(_(u'服务信用状态'), choices=Credit_Level, default='0', max_length=1)
    deliveryStore = models.CharField(_(u'提货门店'), max_length=15, default='')
    deliveryOperator = models.CharField(_(u'提货经办人'), max_length=100, help_text=u'店员账号', default='')
    serviceCloseOpertator = models.CharField(_(u'服务完成人'), max_length=100, help_text=u'店员账号', default='')
    deliveryMode = models.CharField(_(u'物流方式'), max_length=1, choices=delivery_dic, default='0')
    logisticsCompany = models.CharField(_(u'物流公司'), max_length=20, default='')
    trackingNumber = models.CharField(_(u'运单号'), max_length=20, default='')
    remarks = models.CharField(_(u'备注'), max_length=500, default='')
    finishDate = models.DateField(_(u'服务结束时间'), default=None, null=True)
    # commodityEntry = models.CharField(_(u'提货经办人'), max_length=10, default='')
    serviceCloseOpertator = models.CharField(_(u'服务完成人'), max_length=10, default='')
    # store = models.CharField(_(u'取货门店'), max_length=15, default=0)
    completeMode = models.IntegerField(_(u'服务完成方式'), default=0)
    realChargingRent = BillamountField(_(u'已付租金'), default=0.0)
    returnDeposit = BillamountField(_(u'应退款'), default=0.0)
    serialNumber = models.CharField(_(u'SKU商品编号'), max_length=10, default='')
    # deliveryStore = models.CharField(_(u'取货门店'), max_length=15, default='')
    returnStore = models.CharField(_(u'还货门店'), max_length=15, default='')
    curProcOrder = models.CharField(_(u'当前处理订单号'), max_length=20, default='')
    adjustmentAmount = BillamountField(_(u'租转售补差金额'), default=0.0)
    daily_amount = BillamountField(_(u'日租金'), default=0.0)

    class Meta:
        ordering = ('serviceNo', 'mid')
        abstract = True

    def __init__(self, *args, **kwargs):

        super(Project, self).__init__(*args, **kwargs)
        # m = Merchant.objects.get(merchantid=self.mid)

        if self.initialDeposit == 0.0:
            pass
            # raise ValueError("初始租金为0")
            # self.initialDeposit = round((m.guarantee_pct / 100) * self.product.rent, 2)

        if self.current_payamount == 0.0:
            self.current_payamount = self.initialDeposit + self.initialRent
            '''
            self.current_payamount = round(
                Decimal(self.deposit) + Decimal(
                    self.rentPeriod * self.product.rent), 2)
            '''

        if self.residualDeposit == 0.0:
            self.residualDeposit = self.initialDeposit

        if self.residualRent == 0.0:
            self.residualRent = self.initialRent

        if not self.serviceStatus:
            self.serviceStatus = Start()
            # self.__state = START_STATE

    def set_state(self, s):
        self.serviceStatus = s

    def updatestate(self, state):
        self.serviceStatus.updatestate(self, state)

    def save(self, *args, **kwargs):
        if self.name == '' or self.phone == '':
            from siteuser.member.models import SiteUser
            try:
                usr = SiteUser.objects.get(memberId=self.memberId)
            except Exception, e:
                logger = logging.getLogger('django')
                logger.error(e)
            else:
                self.name = usr.name
                self.phone = usr.phone

        # with transaction.atomic:
        super(Project, self).save(*args, **kwargs)
        if self.serviceNo == '':
            self.serviceNo = 'S' + gettimestamp()
            super(Project, self).save(force_update=True, update_fields=['serviceNo'])

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
    productid = models.CharField(_(u'租赁产品编号'), max_length=15, default='')
    product = JSONField(_(u'商品快照'), max_length=1000, default='')

    reservedProductid = models.CharField(_(u'预约产品编号'), max_length=15, default='')
    reservedProduct = JSONField(_(u'预约商品快照'), max_length=1000, default='')

    def __unicode__(self):
        return self.serviceNo

    def __init__(self, *args, **kwargs):
        super(ProductRental, self).__init__(*args, **kwargs)
        if not self.productid:
            raise TypeError("error for null productid")
            logging.getLogger('django').error("error for null productid")

        self.set_state(Start())

    def save(self, *args, **kwargs):
        if self.product == '' and self.productid:
            try:
                pd = ProductDetail.objects.get(productid=self.productid)
            except ProductDetail.DoesNotExist:
                raise ValueError("productid 错误")
            self.product = model_to_dict(pd, fields=['category', 'model', 'title', 'brand', 'series', 'sellingPrice'])
        if self.reservedProduct == '' and self.reservedProductid:
            try:
                pd = ProductDetail.objects.get(productid=self.reservedProductid)
            except ProductDetail.DoesNotExist:
                raise ValueError("productid 错误")
            self.reservedProduct = model_to_dict(pd, fields=['category', 'model', 'title', 'brand', 'series',
                                                             'sellingPrice'])

        return super(ProductRental, self).save(*args, **kwargs)

    def genRentalOrder(self):
        ro = RentalOrder(proj=self, memberId=self.memberId)  # to_be_done

    class Meta:
        verbose_name = _('租赁服务')
        verbose_name_plural = _('租赁服务')

    pass


# 租赁服务hook
@receiver(signal=signals.pre_save, sender=ProductRental)
def snap_save(sender, instance, **kwargs):
    if 'productid' in instance.changes():
        try:
            pd = ProductDetail.objects.get(productid=instance.productid)
        except ProductDetail.DoesNotExist:
            raise ValueError("productid 错误")
        instance.product = model_to_dict(pd, fields=['category', 'model', 'title', 'brand', 'series', 'sellingPrice'])
    if 'reservedProductid' in instance.changes():
        try:
            pd = ProductDetail.objects.get(productid=instance.reservedProductid)
        except ProductDetail.DoesNotExist:
            raise ValueError("reservedProductid 错误")
        instance.product = model_to_dict(pd, fields=['category', 'model', 'title', 'brand', 'series', 'sellingPrice'])


# 套餐租赁服务
class ComboRental(Project):
    product = models.ForeignKey(Package)
    packageshot = JSONField(_(u'套餐快照'), max_length=1000, default='')
    productid = models.CharField(_(u'租赁产品编号'), max_length=15, default='')
    product = JSONField(_(u'商品快照'), max_length=1000, default='')
    changelist = models.CharField(_(u'租品变化情况'), default='', max_length=3000)

    def __unicode__(self):
        return self.serviceNo

    def save(self, *args, **kwargs):
        return super(ComboRental, self).save(*args, **kwargs)
        pass

    class Meta:
        verbose_name = _('套餐租赁服务')
        verbose_name_plural = _('套餐租赁服务')

class SellService(Project):
    """
    """
    pass
        


# 订单
class Order(BaseModel):
    r"""

    """
    paytype = {
        ('0', u'微信'),
        ('1', u'其他')
    }

    ordersts = {
        ('0', u'待支付'),
        ('1', u'已支付'),
        ('2', u'退款中'),
        ('3', u'已退款'),
        ('4', u'订单关闭')
    }



    memberId = models.CharField(_(u'用户编号'), max_length=15, null=False)

    # proj = models.CharField(_(u'服务编号'), max_length=10, null=False, default='0')
    paymentDatetime = models.DateTimeField(_(u'支付时间'), null=True, blank=True)
    paymentType = models.CharField(_(u'支付方式'), max_length=1, default='0', choices=paytype)
    amount = BillamountField(_(u'订单金额'))  # models.DecimalField(_(u'订单金额'), max_digits=12, decimal_places=2)
    payedamount = BillamountField(_(u'支付金额'),
                                  default=0.0)  # models.DecimalField(_(u'支付金额'), max_digits=12, decimal_places=2)
    payment_status = models.SmallIntegerField(_(u'支付状态'), default=0)  # 0:未支付 1:支付中 2:支付成功
    orderNo = models.CharField(max_length=20, default=gettimestamp, db_index=True, unique=True, editable=False)

    orderStatus = models.IntegerField(_('订单状态'), default=fsm.ORDER_START)
    payid = models.CharField(_('支付订单号'), max_length=20, default='')

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)

    def save(self, userid=None, *args, **kwargs):
        if self.orderNo == '' or self.orderNo == None:
            self.orderNo = Ordertimestamp()
        super(Order, self).save(force_insert=False, force_update=False, using=None,
                                update_fields=None)

    class Meta:
        ordering = ('orderNo',)
        abstract = True

    def getType(self):
        return self.type

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
    order_type = {
        (0, '租赁订单'),
        (1, '套餐订单'),
        (2, '销售订单'),
        (3, '赔偿订单'),
        (4, '补押订单'),
        (5, '补差订单'),
        (7, '套餐租赁转售订单'),
        (8, '单品租赁转售订单')
    }
    serviceNo = models.CharField(_(u'服务单号'), max_length=20, default='')
    type = models.PositiveSmallIntegerField(_(u'订单类型'), choices=order_type, default=0)
    desc = models.CharField(_(u'订单描述'), max_length=100, default='')

    class Meta:
        verbose_name = _('租赁订单')
        verbose_name_plural = _('租赁订单')

    def clean(self):
        pass


# 支付订单
class PaymentOrder(BaseModel):
    order = models.ForeignKey(RentalOrder, related_name='relatedPaymentOrders')
    pay_id = models.CharField(max_length=20, db_index=True, unique=True)
    orderNo = models.CharField(max_length=200, default='0')
    memberId = models.CharField(_(u'用户编号'), max_length=15, null=False, default='0')
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
