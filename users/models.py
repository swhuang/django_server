# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .managers import UserInheritanceManager, UserManager
from crm.models import Merchant
from utils import gettimestamp
import datetime
from decimal import Decimal
import json
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator


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

    identifcation = models.IntegerField(default=0)

    usertoken = models.CharField(max_length=100, default='')

    mid = models.ForeignKey(Merchant, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Member(AbstractBaseUser):
    username = models.TextField(max_length=100, default=u'hsw')
    memberid = models.CharField(max_length=15, default='')
    id_name = models.CharField(max_length=15, null=True)
    id_no = models.CharField(max_length=15, null=True)
    id_type = models.IntegerField(default=0)
    gender = models.BooleanField(default=True)
    phone = models.CharField(_(u'用户名'), default='', unique=True, db_index=True, max_length=50)
    mid = models.ForeignKey(Merchant, null=True, db_index=True)
    email = models.EmailField(_(u'邮箱'), max_length=255, null=True)
    '''
    class Meta:
        abstract = True
    '''
    USERNAME_FIELD = 'phone'

    def save(self, *args, **kwargs):
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


class ExtendMember(AbstractBaseUser):
    #username = models.TextField(max_length=100, default=u'hsw')
    memberid = models.CharField(max_length=15, default='')
    id_name = models.CharField(max_length=15, null=True)
    id_no = models.CharField(max_length=15, null=True)
    id_type = models.IntegerField(default=0)
    gender = models.BooleanField(default=True)
    phone = models.CharField(_(u'用户名'), default='', unique=True, db_index=True, max_length=50)
    mid = models.ForeignKey(Merchant, null=True, db_index=True)
    email = models.EmailField(_(u'邮箱'), max_length=255, null=True)

    class Meta:
        abstract = True

    USERNAME_FIELD = 'phone'

    def save(self, *args, **kwargs):
        super(ExtendMember, self).save(*args, **kwargs)
        self.memberid = "%010d" % self.id
        super(ExtendMember, self).save(force_update=True, update_fields=['memberid'])

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


class Project(models.Model):
    r"""

    """
    proj_id = models.CharField(max_length=10, default='', db_index=True)
    proj_name = models.CharField(max_length=128, default='')
    mid = models.ForeignKey(Merchant, null=True)

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


class Order(models.Model):
    r"""

    """
    userinfo = models.ForeignKey(Member, null=True)
    proj = models.ForeignKey(Project, null=True)
    paytime = models.DateTimeField(_(u'支付时间'), default=timezone.now)
    orderamount = models.DecimalField(_(u'订单金额'), max_digits=12, decimal_places=2)
    payedamount = models.DecimalField(_(u'支付金额'), max_digits=12, decimal_places=2)
    payment_status = models.SmallIntegerField(_(u'支付状态'))
    mid = models.ForeignKey(Merchant, db_index=True, null=True)
    orderid = models.CharField(max_length=20, default=gettimestamp, db_index=True, unique=True)

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


'''
class Permission(models.Model):

    name = models.CharField(u'权限名称', max_length=64)
    url = models.CharField(u'URL名称', max_length=255)
    choices = ((1, 'GET'), (2, 'POST'))
'''


class SessionToken(models.Model):
    pass
