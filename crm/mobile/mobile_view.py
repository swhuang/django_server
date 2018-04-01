# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
import csv
from crm.models import *
import os
import hashlib
import crm.util as mUtil
from django.views.decorators.csrf import csrf_exempt
import json
from crm.forms import QueryForm, OrderPaymentForm, OrderGenForm
from django.template.response import TemplateResponse
from users.models import Member
from crm.models import Merchant,Project

from django.core.urlresolvers import reverse
from crm.mobile.settings import ErrorInfo
from crm.util import mlogin_required
import copy


def index(request):
    #print "got in index"
    if not request.siteuser:
        return HttpResponseRedirect(reverse('siteuser_login'))
    context = {}
    context['projects'] = []
    try:
        p = Project.objects.get(id=1)
        context['projects'].append(p.getDict())
    except Project.DoesNotExist:
        print "Not found project"
        pass
    return TemplateResponse(request, "mobile/mindex.html", context)

def error_info(request, *args, **kwargs):
    print args[0]
    error_msg = ''
    context = {}
    if ErrorInfo.errors.has_key(args[0]):
        error_msg = ErrorInfo.errors[args[0]]
        context['error_msg'] = error_msg
        return TemplateResponse(request, "mobile/merror.html", context)
    else:
        return TemplateResponse(request, "mobile/merror.html", {'error_msg': u'未知错误'})

@mlogin_required
def orderinfo(request):
    print "got here"
    _merchant = None
    if request.merchant:
        _merchant = request.merchant
    context = {}
    context['project'] = {}
    context['form'] = OrderGenForm(_merchant)
    return TemplateResponse(request, "mobile/mproductinfo.html", context)


def ordersubmit(request):
    r'''
    生成订单
    :param request:
    :return:
    '''
    if request.method == 'POST':
        context = {}
        context['project'] = {}
        try:
            p = Project.objects.get(id=1)
            context['projects'] = p.getDict()
            context['form'] = OrderPaymentForm()
        except p.DoesNotExist:
            print "Not found project"
        #add new order
        #new_order = Order()
        return TemplateResponse(request, "mobile/morder.html", context)
    else:
        pass

    return HttpResponse('ok')


def doPayment(request):
    r'''
    执行支付
    :param request:
    :return:
    '''
    return HttpResponse('ok')
