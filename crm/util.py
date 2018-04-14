# -*- coding: utf-8 -*-
import time
import base64
import hmac
import hashlib
import string
from random import *
from crm.models import TokenManager
from functools import wraps
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from abc import ABCMeta, abstractmethod


def generate_token(key, expire=3600):
    r"""
    :param key:
    :param expire:
    :return:
        state:str
    """
    ts_str = str(time.time() + float(expire))
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, hashlib.sha1).hexdigest()
    token = ts_str + ":" + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode('utf-8'))
    return b64_token.decode("utf-8")


def certify_token(key, token):
    r'''

    :param key:
    :param token:
    :return:
    boolean
    '''
    print "This token is :" + token
    token_str = base64.urlsafe_b64decode(str(token)).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        try:
            _token = TokenManager.objects.get(token=token)
            if _token:
                _token.delete()
        except:
            pass
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode('utf-8'), ts_str.encode('utf-8'), hashlib.sha1)
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        return False
    return True


def generate_key():
    r"""
    生成随机16位长秘钥
    :return:
    """

    characters = string.ascii_letters + string.digits
    password = "".join(choice(characters) for x in range(randint(16, 16)))
    return password


class autonumber(object):
    @staticmethod
    def getunion():
        return '10000'


class Rspinfo(object):
    r'''

    '''
    status = 0
    reason = ''
    version = 'v1.0'
    errorcode = ''

    class Meta:
        abstract = True

    def __init__(self):
        status = 0
        reason = ''
        version = 'v1.0'
        errorcode = ''


class SessionTokenRsp(Rspinfo):
    def __init__(self, status='Success', errorcode='00', reason='', sessiontoken='', merchantid=''):
        self.status = status
        self.reason = reason
        self.errorcode = errorcode
        self.sessiontoken = sessiontoken
        self.merchantid = merchantid

        self.retmsg = {}
        self.retmsg['sessiontoken'] = self.sessiontoken
        self.retmsg['merchantid'] = self.merchantid
        self.retmsg['status'] = self.status  # 成功
        self.retmsg['errorcode'] = self.errorcode
        self.retmsg['reason'] = self.reason
        self.retmsg['version'] = 'v1.0'

    @property
    def dict(self):
        return self.retmsg


class UserDataRsp(Rspinfo):
    r'''

    '''

    def __init__(self, status=0, errorcode='00', reason='', merchantid='', datainfo={}):
        self.status = status
        self.reason = reason
        self.errorcode = errorcode
        self.merchantid = merchantid

        self.retmsg = {}
        self.retmsg['merchantid'] = self.merchantid
        self.retmsg['status'] = self.status  # 成功
        self.retmsg['errorcode'] = self.errorcode
        self.retmsg['reason'] = self.reason
        self.retmsg['version'] = 'v1.0'
        self.retmsg['datainfo'] = datainfo

    @property
    def dict(self):
        return self.retmsg

#siteuser 登录验证
def mlogin_required(func):
    @wraps(func)
    def deco(request, *args, **kwargs):
        if not request.siteuser:
            print reverse('siteuser_login')
            return HttpResponseRedirect(reverse('siteuser_login'))
        return func(request, *args, **kwargs)
    return deco

def crmlogin_check(func):
    @wraps(func)
    def deco(request, *args, **kwargs):
        if not request.user.mid:
            print reverse('MobileErrorInfo')
            return HttpResponseRedirect(reverse('MobileErrorInfo')+'/error02')
        return func(request, *args, **kwargs)
    return deco

class Structure(object):
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        for name,value in zip(self._fields, args):
            setattr(self, name, value)

        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        if kwargs:
            raise TypeError('Invaild argument(s):{}'.format(','.join(kwargs)))

if __name__ == '__main__':
    key = '123456789'
    token = generate_token(key)
    print token
    print certify_token(key, token)
    generate_key()
    import os

    r'''
    for i in xrange(10000000):
        file_obj = open('merchant_data', 'a')
        file_obj.write(str(i)+',')
        file_obj.close()

    print 'file create completed'
    '''
    file_obj = open('merchant_data', 'wa')
    file_obj.read(100)
    print
