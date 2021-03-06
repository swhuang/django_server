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
from crm.forms import QueryForm, OrderQueryForm, ProjQueryForm, ProjNewFrom, OrderGenForm
from users.models import User as Usermodel
from django.template.response import TemplateResponse
from users.models import Member, Merchant, Project, ExtendMember
import copy
from djpjax import pjax


@pjax("project/tables-pjax.html")
def pjaxtest(request):
    return TemplateResponse(request, "project/tables.html")


# Create your views here.
@permission_required('crm.view')
@login_required(login_url="/accounts/login/")
#@pjax("project/tables-pjax.html")
def crm_main(request, template_name="project/tables.html"):
    r'''
    用户管理页面
    :param request:
    :param template_name:
    :return:
    '''
    if request.method == 'POST':
        pass
    else:
        _merchant = 'None'
        if request.user.mid:
            _merchant = request.user.mid
        else:
            return HttpResponse('ok')
            # _merchant = request.user.mid.merchantid
        keylst = [u'用户名', u'学生id', u'身份证姓名', u'身份证号', u'性别', u'电话']
        membs = list(
            Member.objects.filter(mid=_merchant).values('username', 'memberid', 'id_name', 'id_no', 'gender', 'phone'))
        print membs
        mem_data = []

        for m in membs:
            l = []
            l.append(m['username'])
            l.append(m['memberid'])
            l.append(m['id_name'])
            l.append(m['id_no'])
            l.append(m['gender'])
            l.append(m['phone'])
            mem_data.append(copy.copy(l))
        print mem_data

        form = QueryForm()

    if request.META.get('HTTP_X_PJAX', False):
        ispjax = 1
    else:
        ispjax = 0

    context = {
        'ispjax': ispjax,
        'form': form,
        'merchant': _merchant.merchantid,
        'tablename': u'用户管理',
        'col_name': keylst,
        'mem_data': mem_data
    }
    return TemplateResponse(request, template_name, context)


@permission_required('crm.view')
@login_required(login_url="/accounts/login/")
def panel_projectform(request):
    form = ProjQueryForm()
    form_new = ProjNewFrom()
    context = {
        'tablename': u'项目管理',
        'merchant': request.user.mid.merchantid,
        'form': form,
        'form_new': form_new
    }
    return render(request, "project/ProjManager.html", context)


@permission_required('crm.view')
@login_required(login_url="/accounts/login/")
def panel_preferences(request):
    return render(request, "project/preferences.html")


@permission_required('crm.view')
@login_required(login_url="/accounts/login/")
def panel_ordermanager(request):
    form = OrderQueryForm(request.user.mid)
    form_new = OrderGenForm(request.user.mid)
    context = {
        'tablename': u'订单管理',
        'merchant': request.user.mid.merchantid,
        'form': form,
        'form_new': form_new
    }
    return render(request, "project/OrderManager.html", context)


def test(request):
    current_path = os.path.dirname(os.path.realpath(__file__))
    with open(current_path + '/data/lmn&p.csv', 'rb') as f:
        reader = csv.reader(f)
        firstin = True
        for row in reader:
            if firstin == True:
                firstin = False
            else:
                p = Userdata(username=row[0].encode('utf-8'), phone=row[1], vertime=row[2].encode('utf-8'))
                p.save()

    return HttpResponse("testok!")


def generatetestmerchant(request):
    '''
    _mcht = Merchant.objects.get(merchantid='100000000000001')
    p = Project(proj_name=u'测试项目1', mid=_mcht)
    p.save()
    return HttpResponse('I am ok')
    '''
    _key = mUtil.generate_key()
    print _key
    try:
        p = Merchant.objects.get(merchantid='100000000000001')
    except Merchant.DoesNotExist:
        p = Merchant(merchantid='100000000000001', name=u'测试商户1', key=_key)
        p.save()
        _mcht = Merchant.objects.get(merchantid='100000000000001')
        p = Project(proj_name=u'测试项目1', mid=_mcht)
        p.save()
    return HttpResponse('ook')
    l = []
    from django.db.models import Count
    count = Userdata.objects.aggregate(Count('id'))
    for i in xrange(count['id__count']):
        l.append(str(i + 1))
        if ((i + 1) % 100) == 0:
            dp = Datapool(mid=p, datapool=','.join(l), merchantid=p.merchantid)
            dp.save()
            l = []

    return HttpResponse('ok')


def djtest(request):
    dp = Datapool.objects.filter(merchantid='100000000000001').values()
    import random
    t1 = random.randint(0, dp.count())
    print random.randint(0, 1)

    _l = str(dp[t1]['datapool']).split(',')

    t2 = random.randint(0, len(_l))
    key = int(_l[t2])
    del _l[t2]

    if len(_l) != 0:
        print dp[t1]['datapool']
        print dp[t1]['id']
        print dp[t1]['merchantid']
        dp[t1].datapool = ','.join(_l)
        dp[t1].save()
    else:
        dp[t1].delete()

    return HttpResponse('test ok')


# 获取授权信息
# input:
#     merchantid
#     timeStamp
#     [securitykey]
#     checksum
#     username
#     password
# 签名原窜：merchantid=123456789&timestamp=123456789&key=123456789
# output:
#     sessionToken
#     merchantid
#     status
#     errorcode
#     reason
#     version
@csrf_exempt
def getSessionToken(request):
    if request.method == 'POST':
        merchantid = request.POST.getlist('merchantid', '')[0]
        timestamp = request.POST.getlist('timestamp', '')[0]
        username = request.POST.getlist('username', '')[0]
        checksum = request.POST.getlist('checksum', '')[0]
        password = request.POST.getlist('password', '')[0]
        if not merchantid or not timestamp or not checksum or not username or not password:
            retmsg = mUtil.SessionTokenRsp(status='Fail', errorcode='01', reason='Invalid Input')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        try:
            _merchant = Merchant.objects.get(merchantid=merchantid)

        except _merchant.DoesNotExist:
            retmsg = mUtil.SessionTokenRsp(status='Fail', errorcode='02', reason='Invalid Merchant')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        # rsa encoding
        if not _merchant.key:
            retmsg = mUtil.SessionTokenRsp(status='Fail', errorcode='03', reason='Invalid Merchant key')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        try:
            # _user = Usermodel._default_manager.get_by_natural_key(username)
            _user = Usermodel.objects.get(userid=username)
        except Usermodel.DoesNotExist:
            return HttpResponse("error4")
        else:
            if not _user.check_password(password):
                retmsg = mUtil.SessionTokenRsp(status='Fail', errorcode='04', reason='Invalid Password')
                return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
                # return HttpResponse("error5")#密码错误
        checksrc = 'merchantid=' + merchantid + '&' + 'timestamp=' + timestamp + '&' + 'key=' + _merchant.key
        m = hashlib.md5()
        m.update(checksrc)
        _checksum = m.hexdigest()
        if _checksum != checksum:
            retmsg = mUtil.SessionTokenRsp(status='Fail', errorcode='05', reason='Invalid Sign')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
            # return HttpResponse("error4") #返回验签错误
        userkey = _merchant.key + username  # 用户秘钥=商户秘钥+用户名
        if _user.usertoken != '' and mUtil.certify_token(userkey, _user.usertoken):
            retmsg = mUtil.SessionTokenRsp(status='Fail', errorcode='06', reason='Token already active')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        rettoken = mUtil.generate_token(userkey, _merchant.expiretime)
        retmsg = mUtil.SessionTokenRsp(sessiontoken=rettoken, merchantid=_merchant.merchantid)
        _user.usertoken = rettoken
        _user.save()
        _token = TokenManager(token=rettoken, max_count=_merchant.daily_maxcount)
        _token.save()
        return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")

    else:
        return HttpResponse("")


@csrf_exempt
def getUserData(request):
    r"""
    input:
        sessiontoken;
        merchantid;
        username;
        condition;
    output:
        merchantid
        userinfo;
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            sessiontoken = request.POST.getlist('sessiontoken', '')[0]
            merchantid = request.POST.getlist('merchantid', '')[0]
            username = request.POST.getlist('username', '')[0]
        except IndexError:
            retmsg = mUtil.UserDataRsp(status='Fail', errorcode='01', reason='Invalid Parameter')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")

        condition = request.POST.getlist('condition', '')

        if not sessiontoken or not merchantid or not username:
            retmsg = mUtil.UserDataRsp(status='Fail', errorcode='01', reason='Invalid Parameter')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        try:
            _merchant = Merchant.objects.get(merchantid=merchantid)
        except Merchant.DoesNotExist:
            retmsg = mUtil.UserDataRsp(status='Fail', errorcode='02', reason='Invalid Merchant')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        if not mUtil.certify_token(_merchant.key + username, sessiontoken):
            retmsg = mUtil.UserDataRsp(status='Fail', errorcode='03', reason='Invalid Token')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        try:
            _id = Datapool.get_single_data(_merchant.merchantid)
        except:
            retmsg = mUtil.UserDataRsp(status='Fail', errorcode='04', reason='No Available Data ')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        try:
            _data = Userdata.objects.get(id=_id)
        except Userdata.DoesNotExist:
            retmsg = mUtil.UserDataRsp(status='Fail', errorcode='05', reason='No Available Data [full]')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        try:
            _token = TokenManager.objects.get(token=sessiontoken)
        except TokenManager.DoesNotExist:
            retmsg = mUtil.UserDataRsp(status='Fail', errorcode='06',
                                       reason='Token error, please request the token again')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        if _token.max_count == _token.count:
            retmsg = mUtil.UserDataRsp(status='Fail', errorcode='07',
                                       reason='Over limit')
            return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
        _token.count = _token.count + 1
        _token.save()
        retmsg = mUtil.UserDataRsp(merchantid=merchantid, datainfo=_data.getinfo())
        return HttpResponse(json.dumps(retmsg.dict), content_type="application/json")
    else:
        return HttpResponse('')
    pass


if __name__ == '__main__':
    import httplib

    conn = httplib.HTTPConnection("127.0.0.1:8000")
    conn.request("GET", "/userform/getSessionToken/")
    ri = conn.getresponse()
    print ri.status, ri.reason
    data = ri.read()
    print data
