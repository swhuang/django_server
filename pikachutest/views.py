# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
#encoding=utf-8
import hashlib
from lxml import etree
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json

import sys
import os
import timetable.DataInit as datainit
import timetable.Util as Util


WEIXIN_TOKEN = "123456"

UNCOUNTABLE = 0
TIGHTEN = 5
BUSY = 15

import MySQLdb
conn = MySQLdb.connect(host='localhost',
                           port=3306,
                           user='root',
                           passwd='vq8612VQE',
                           db='mysql',
                           charset="utf8")
cur = conn.cursor()
# VACANT =
if sys.getdefaultencoding() != 'gbk':
    reload(sys)
    sys.setdefaultencoding('gbk')
default_encoding = sys.getdefaultencoding()

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=100)
    file = forms.FileField()

def index(request):
    pagehtml = u"<h>Go2parking</h><p>luludasabi</p>"
    return render(request, 'home.html')


def test(request):
    pagehtml = str(request.GET) + "get!"
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        # signature = request.REQUEST.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        print "local sign is:" + tmp_str
        # print "**************"
        # print "sign is :"+signature
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin index")
    else:
        xml_str = smart_str(request.body)
        request_xml = etree.fromstring(xml_str)
        # response_xml = auto_reply_main(request_xml)
        return HttpResponse(request_xml)

        # return HttpResponse(pagehtml)


def getmodel(request):
    return HttpResponse("work")


def initatable(request):
    from pikachutest.models import ParkingInfo
    tstInfo = {}
    tstInfo["pid"] = 0;
    tstInfo["name"] = "test";
    tstInfo["longitude"] = "100.000";
    tstInfo["latitude"] = "99.999";
    tstInfo["max_parkingCapacity"] = 100;
    getrt = ParkingInfo.objects.create(**tstInfo);
    if request.method == "GET":
        tstInfo["longitude"] = request.GET.get("longitude", None)
        tstInfo["latitude"] = request.GET.get("latitude", None)
        # title = title.encode('utf-8')
        tstInfo["name"] = request.GET.get("name", None)
        tstInfo["name"] = tstInfo["name"].encode('utf-8')
        tstInfo["max_parkingCapacity"] = request.GET.get("MaxCount", 0)
        ParkingInfo.objects.create(**tstInfo)
        return HttpResponse("Init is OK" + tstInfo["name"]);
    else:
        pass

    return HttpResponse("Init OK");


def UpdateParkingData(request):
    from pikachutest.models import ParkingInfo
    ret = []
    if request.method == "GET":
        Posx_l = request.GET.get("longitude_l", None)
        Posy_l = request.GET.get("latitude_l", None)
        Posx_r = request.GET.get("longitude_r", None)
        Posy_r = request.GET.get("latitude_r", None)
        ParkingList = []
        try:
            # ParkingList = ParkingInfo.objects.all()
            ParkingList = ParkingInfo.objects.filter(longitude__range=[Posx_l, Posx_r]).filter(
                latitude__range=[Posy_r, Posy_l])
        except:
            return HttpResponse("sql error")
        for key in ParkingList:
            ele = {}
            # ele['name'] = key.name
            ele['longitude'] = key.longitude
            ele['latitude'] = key.latitude
            ele['id'] = key.id
            # ele['max_parkingCapacity'] = key.max_parkingCapacity
            # ele['parkingCount'] = key.parkingCount
            if key.parkingCount == UNCOUNTABLE:
                ele['status'] = 0  # Grey:Cannot be counted
            elif key.parkingCount <= TIGHTEN:
                ele['status'] = 1  # Red: Insufficent Parking
            elif key.parkingCount <= BUSY:
                ele['status'] = 2  # Yellow: Busy Parking
            else:
                ele['status'] = 3  # Green: Empty
            ret.append(ele)
        print ret
        vjs = json.dumps(ret).decode("unicode-escape")
        return HttpResponse(vjs)
    else:
        pass
    return


def GetParkingInfo(request):
    from pikachutest.models import ParkingInfo
    if request.method == 'GET':
        mID = request.GET.get("id", None)
        try:
            mParkInfo = ParkingInfo.objects.get(id=mID)

            rtinfo = {}
            for k in mParkInfo._meta.get_fields():
                rtinfo[k.name] = getattr(mParkInfo, k.name)
            vjs = json.dumps(rtinfo).decode("unicode-escape")
            vjs.replace('\r\n', ' ')
            vjs.replace('\r', ' ')
            vjs.replace('\n', ' ')
            return HttpResponse(vjs)
        except:
            return HttpResponse("sql error:" + str(mID))
        pass

    else:
        return HttpResponse("cannot be accessed")
    return


def process_teacher(name_tag,_file,conn,qt=''):
    a = '\xd0\xdc\xb0\xae\xb6\xf0'
    print a.encode('utf-8')
    cur = conn.cursor()
    datainit.checktable("pikachutest_teacher" + name_tag, conn, cur)
    import csv
    with open(_file, 'rb') as f2:
        reader = csv.reader(f2)
        sqli = "create table pikachutest_teacher" + name_tag + "(id int not null primary key auto_increment,tname varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci,tid int)CHARACTER SET utf8 COLLATE utf8_general_ci;"
        try:
            cur.execute(sqli)
        except Exception, e:
            print "create table fail"
            print e.message
            # exit()
        sqli = "insert into pikachutest_teacher" + name_tag + " (tname,tid) values(\'%s\',%s)"

        for row in reader:
            print "==================.....==================="
            print row[0].encode('gbk')
            cur.execute(sqli % (row[0].encode('gbk'), row[1]))
    cur.close()
    conn.commit()

def process_timetable(name_tag, _file, conn):
    a = '\xd0\xdc\xb0\xae\xb6\xf0'
    print a.encode('utf-8')


@csrf_exempt
def TimeTable(request):
    result_list = ""
    FA = ''
    if request.method == 'POST':
        result_list = request.POST.getlist('name','')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if not os.path.isdir('data/'+result_list[0]):
                os.makedirs('data/'+result_list[0])

            mfile = request.FILES.get('file')
            dest = open('data/'+result_list[0]+"/std_"+result_list[0]+".csv",'wb+')
            dest.write(mfile.read())
            dest.close()
            FA = 'data/'+result_list[0]+"/std_"+result_list[0]+".csv"
            #path = default_storage.save('data/'+result_list[0]+"/std_"+result_list[0]+".csv", ContentFile(mfile.read()))

            mfile_te = request.FILES.get('file2')
            dest = open('data/'+result_list[0]+"/teacher_"+result_list[0]+".csv",'wb+')
            dest.write(mfile_te.read())
            dest.close()
            FB = 'data/'+result_list[0]+"/teacher_"+result_list[0]+".csv"

            mfile_te = request.FILES.get('file3')
            dest = open('data/' + result_list[0] + "/timetable_" + result_list[0] + ".csv", 'wb+')
            dest.write(mfile_te.read())
            dest.close()
            FC = 'data/' + result_list[0] + "/timetable_" + result_list[0] + ".csv"

            aaa = "黄圣伟"
            ss = '\xd0\xdc\xb0\xae\xb6\xf0'
            print ss.encode('utf-8')
            datainit.process_timetable(result_list[0], FC, conn)
            datainit.process_teacher(result_list[0],FB,conn)
            #return HttpResponse("黄圣伟".encode('utf-8'))
            datainit.process_std(result_list[0],FA,conn)
            #datainit.process_teacher(result_list[0],FB,conn,ss)


    return HttpResponse(u"黄圣伟")

@csrf_exempt
def SortTable(request):
    if request.method == 'GET':
        #return HttpResponse(request.GET.get("name", None))
        import timetable.tablesort as tbsort
        #tbsort.moduleInit(request.GET.get("name", None))
        macrotag = request.GET.get("name", None)
        #init
        tbsort.WEEKDAY = 1
        tbsort.LESSON = 3
        tbsort.CLASSN = 5
        tbsort.resourcedata, tbsort.teacherclsdict = datainit.getResourcedata(conn, tbsort.WEEKDAY * tbsort.LESSON * tbsort.CLASSN, macrotag)
        tbsort.teacherdict = datainit.getTeacherInfo(conn, macrotag)
        tbsort.MACROTAG=request.GET.get("name", None)
        ga = tbsort.GA(300,[tbsort.ContinousClass],2000)
        return HttpResponse("sadas")
