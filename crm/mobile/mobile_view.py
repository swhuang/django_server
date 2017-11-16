# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import csv
from crm.models import *
import os
import hashlib
import crm.util as mUtil
from django.views.decorators.csrf import csrf_exempt
import json
from crm.forms import QueryForm, OrderPaymentForm, OrderGenForm
from users.models import User as Usermodel
from django.template.response import TemplateResponse
from users.models import Member, Merchant, Project
import copy


def index(request):
    print "got in index"
    context = {}
    context['projects'] = []
    try:
        p = Project.objects.get(id=1)
        context['projects'].append(p.getDict())
    except p.DoesNotExist:
        print "Not found project"
        pass
    return TemplateResponse(request, "mobile/mindex.html", context)


def orderinfo(request):
    print "got here"
    context = {}
    context['project'] = {}
    context['form'] = OrderGenForm()
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
