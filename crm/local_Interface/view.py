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
from crm.forms import QueryForm
from users.models import User as Usermodel
from django.template.response import TemplateResponse
from users.models import Member, Merchant, Order, Project
import copy

@csrf_exempt
def GetMemberData(request):
    if request.method == 'POST':
        _merchant = 'None'
        if request.user.mid:
            _merchant = request.user.mid
        membs = list(
            Member.objects.filter(mid=_merchant).values('username', 'memberid', 'id_name', 'id_no', 'gender', 'phone'))
        req = {}
        req['total'] = 5
        req['rows'] = membs
        return HttpResponse(json.dumps(req), content_type="application/json")
    else:
        pass
    return HttpResponse('ok')

@csrf_exempt
def GetOrderData(request):
    r'''
    todo
    :param request:
    :return:
    '''
    if request.method == 'POST':
        _merchant = 'None'
        if request.user.mid:
            _merchant = request.user.mid
        orderinfo = list(Order.objects.filter(mid=_merchant))
        rsporderinfo = []
        for obj in orderinfo:
            rsporderinfo.append(obj.getDict())

        req = {}
        req['total'] = len(orderinfo)
        req['rows'] = rsporderinfo
        return HttpResponse(json.dumps(req), content_type="application/json")
    else:
        pass
    return HttpResponse('ok')
