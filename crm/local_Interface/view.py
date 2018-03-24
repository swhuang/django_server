# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
import csv
from crm.models import *
import os
import hashlib
import crm.util as mUtil
from django.views.decorators.csrf import csrf_exempt
import json
from crm.forms import QueryForm, OrderGenForm
from users.models import User as Usermodel
from django.template.response import TemplateResponse
from users.models import Member, Merchant, Order, Project
import copy


@csrf_exempt
def GetTableData(request):
    if request.method == 'POST':
        _merchant = 'None'
        if request.user.mid:
            _merchant = request.user.mid
        offset = request.POST.get('offset', None)
        limit = request.POST.get('limit', None)
        sortway = request.POST.get('sortway', 'asc')
        table_name = request.POST.get('table_name', None)
        _search = request.POST.get('search', None)
        rspdata = []
        marg = {
            'mid': _merchant
        }
        max_count = 0
        if table_name == 'member':
            if _search != None:
                _search = json.loads(_search)
                for k in _search:
                    if _search[k] != u'' and _search[k] != '':
                        marg.update({k: _search[k]})
            rspdata = list(
                Member.objects.filter(**marg)[offset: offset + limit].values('username', 'memberid', 'id_name', 'id_no',
                                                                             'gender', 'phone'))
            max_count = Member.objects.filter(**marg).count()
        elif table_name == 'order':
            if _search != None:
                _search = json.loads(_search)
                for k in _search:
                    if _search[k] != u'' and _search[k] != '':
                        if k == 'username':
                            marg.update({'userinfo__username': _search[k]})
                        elif k == 'memberid':
                            marg.update({'userinfo__memberid': _search[k]})
                        elif k == 'id_type':
                            marg.update({'userinfo__id_type': _search[k]})
                        elif k == 'id_no':
                            marg.update({'userinfo__id_no': _search[k]})
                        elif k == 'proj_name':
                            marg.update({'proj__proj_name': _search[k]})
                        else:
                            marg.update({k: _search[k]})

            orderinfo = list(Order.objects.filter(**marg)[offset: offset + limit])
            for obj in orderinfo:
                rspdata.append(obj.getDict())
            max_count = Order.objects.filter(**marg).count()
        elif table_name == 'project':
            if _search != None:
                _search = json.loads(_search)
                for k in _search:
                    if _search[k] != u'' and _search[k] != '':
                        marg.update({k: _search[k]})

            projinfo = list(Project.objects.filter(**marg)[offset: offset + limit])
            for obj in projinfo:
                rspdata.append(obj.getDict())
            max_count = Project.objects.filter(**marg).count()

        req = {}
        req['total'] = max_count
        req['rows'] = rspdata
        return HttpResponse(json.dumps(req), content_type="application/json")
    else:
        pass
    return HttpResponse('ok')


@csrf_exempt
def CreateProject(request):
    if request.method == 'POST':
        dump = lambda d: HttpResponse(json.dumps(d), content_type='application/json')
        projectname = request.POST.get('projname', None)
        if projectname == '' or projectname == None:
            return dump({'ok': False, 'msg': '项目名称为空'})
        try:
            if request.user.mid:
                _merchant = request.user.mid
            else:
                return dump({'ok': False, 'msg': '创建失败:商户错误'})
            p = Project(proj_name=projectname, mid=_merchant)
            p.save()
        except Exception as e:
            return dump({'ok': False, 'msg': '创建失败:'+e.message.encode('utf-8')})
        return dump({'ok':True})

@csrf_exempt
@mUtil.crmlogin_check
def userVerification(request):
    if request.method == 'POST':
        userid = request.POST.get('userid', None)
        if userid == None or userid == '':
            return JsonResponse({'ok': False, 'msg': '用户编号为空'})
        try:
            puser = Member.objects.get(memberid=userid)
        except Member.DoesNotExist:
            return JsonResponse({'ok': False, 'msg': '用户不存在'})
        retcontext = {'ok': True}
        retcontext.update({
            'username': puser.username
        })
        return JsonResponse(retcontext)

def GetOrderCreateForm(request):
    pass


def OrderNewForm(request):
    form = OrderGenForm()
    context = {
        'form': form
    }
    return TemplateResponse(request, 'partials/order_new.html', context)
