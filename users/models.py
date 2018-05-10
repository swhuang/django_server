# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .managers import UserInheritanceManager, UserManager
from crm.models import Merchant, Submerchant
from commom.models import JSONField
from decimal import Decimal
from django.db import transaction
import json


# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.tokens import default_token_generator


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    USERS_AUTO_ACTIVATE = not settings.USERS_VERIFY_EMAIL

    email = models.EmailField(
        _('email address'), max_length=255)  # , db_index=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(
        _('active'), default=USERS_AUTO_ACTIVATE,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    user_type = models.ForeignKey(ContentType, null=True, editable=False)

    objects = UserInheritanceManager()
    base_objects = UserManager()

    # userid = models.TextField(_(u'用户名'),default='',unique=True, db_index=True,max_length=50)
    userid = models.CharField(_(u'用户名'), default='', unique=True, db_index=True, max_length=50)

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def get_full_name(self):
        """ Return the userid."""
        return self.userid  # email

    def get_short_name(self):
        """ Return the userid."""
        return self.userid  # email

    def email_user(self, subject, message, from_email=None):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    def activate(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.user_type_id:
            self.user_type = ContentType.objects.get_for_model(self, for_concrete_model=False)
        super(AbstractUser, self).save(*args, **kwargs)


class User(AbstractUser):
    """
    Concrete class of AbstractUser.
    Use this if you don't need to extend User.
    """
    username = models.TextField(max_length=100, default=u"黄圣伟")

    identification = models.IntegerField(default=0)

    usertoken = models.CharField(max_length=100, default='')

    mid = models.ForeignKey(Merchant, null=True)  # , default=settings.DEFAULT_MERCHANT_ID)

    submerchant = models.ForeignKey(Submerchant, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        if not self.mid:
            self.mid = Merchant.objects.all().first()
        super(User, self).save(*args, **kwargs)


class Member(AbstractBaseUser):
    username = models.TextField(max_length=100, default=u'hsw')
    memberId = models.CharField(max_length=15, default='')
    id_name = models.CharField(max_length=15, null=True)
    id_no = models.CharField(max_length=15, null=True)
    id_type = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, default='0')
    phone = models.CharField(_(u'用户名'), default='', unique=True, db_index=True, max_length=50)
    mid = models.ForeignKey(Merchant, null=True, db_index=True)  # , default=settings.DEFAULT_MERCHANT_ID)
    email = models.EmailField(_(u'邮箱'), max_length=255, null=True)
    '''
    class Meta:
        abstract = True
    '''
    USERNAME_FIELD = 'phone'

    def save(self, *args, **kwargs):
        if not self.mid:
            pass  # self.mid = settings.DEFAULT_MERCHANT_ID
        super(Member, self).save(*args, **kwargs)
        self.memberid = "%010d" % self.id
        super(Member, self).save(force_update=True, update_fields=['memberid'])

    def default_init(self):
        self.username = 'hsw'

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
            elif attr == 'id_type':
                if getattr(self, attr) == 0:
                    d[attr] = u'身份证'
                else:
                    d[attr] = u'其他'
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
            elif attr == 'id_type':
                if getattr(self, attr) == 0:
                    d[attr] = u'身份证'
                else:
                    d[attr] = u'其他'
            else:
                d[attr] = getattr(self, attr)
        return d


class ExtendMember(models.Model):
    # username = models.TextField(max_length=100, default=u'hsw')
    memberId = models.CharField(_(u'会员ID号'), max_length=15, default='')
    name = models.CharField(_(u'用户真名'), max_length=15, default='')
    idNo = models.CharField(_(u'证件号码'), max_length=15, default='')
    idType = models.CharField(_(u'证件类型'), default='0', max_length=15)
    gender = models.CharField(_(u'性别'), max_length=1, default='0')
    phone = models.CharField(_(u'手机号'), default='', unique=True, db_index=True, max_length=50)
    mid = models.ForeignKey(Merchant, null=True, db_index=True)  # , default=settings.DEFAULT_MERCHANT_ID)
    email = models.EmailField(_(u'邮箱'), max_length=255, default='')
    address = models.CharField(_(u'地址'), default="[]", max_length=500)
    birthday = models.DateField(_(u'生日'), blank=True, default='1990-01-01')
    source = models.CharField(_(u'创建来源'), blank=True, default='0', max_length=1)
    createdDate = models.DateField(_(u'创建日期'), blank=True, default=timezone.now().strftime("%Y-%m-%d"))

    class Meta:
        abstract = True

    USERNAME_FIELD = 'phone'

    def __unicode__(self):
        return self.memberid

    def save(self, *args, **kwargs):
        if not self.mid:
            try:
                self.mid = Merchant.objects.get(merchantid=settings.DEFAULT_MERCHANT)  # settings.DEFAULT_MERCHANT_ID
            except:
                self.mid = None
        with transaction.atomic():
            super(ExtendMember, self).save(*args, **kwargs)
            if self.memberId == '':
                self.memberId = "%010d" % self.id
                super(ExtendMember, self).save(force_update=True, update_fields=['memberId'])

    def default_init(self):
        self.username = 'hsw'

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
            elif attr == 'id_type':
                if getattr(self, attr) == 0:
                    d[attr] = u'身份证'
                else:
                    d[attr] = u'其他'
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
            elif attr == 'id_type':
                if getattr(self, attr) == 0:
                    d[attr] = u'身份证'
                else:
                    d[attr] = u'其他'
            else:
                d[attr] = getattr(self, attr)
        return d


'''
class Permission(models.Model):

    name = models.CharField(u'权限名称', max_length=64)
    url = models.CharField(u'URL名称', max_length=255)
    choices = ((1, 'GET'), (2, 'POST'))
'''


class SessionToken(models.Model):
    pass
