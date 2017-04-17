from django.shortcuts import render

# Create your views here.
#coding:utf-8
import hashlib
from lxml import etree
from django.utils.encoding import smart_str
from django.http import HttpResponse
import sys

WEIXIN_TOKEN="123456"

def index(request):
    pagehtml = u"<h>Go2parking</h><p>luludasabi</p>"
    return HttpResponse(pagehtml)
def test(request):
    pagehtml = str(request.GET)+"get!"
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        #signature = request.REQUEST.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        print "local sign is:" + tmp_str
        #print "**************"
        #print "sign is :"+signature
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin index")
    else:
        xml_str = smart_str(request.body)
        request_xml = etree.fromstring(xml_str)
        #response_xml = auto_reply_main(request_xml)
        return HttpResponse(request_xml)

    #return HttpResponse(pagehtml)

def getmodel(request):


    return HttpResponse("work")

def initatable(request):
    from pikachutest.models import ParkingInfo
    tstInfo = {}
    tstInfo["pid"]=0;
    tstInfo["name"]="test";
    tstInfo["longitude"]="100.000";
    tstInfo["latitude"]="99.999";
    tstInfo["max_parkingCapacity"]=100;
    getrt = ParkingInfo.objects.create(**tstInfo);
    if request.method == "GET":
        tstInfo["longitude"] = request.GET.get("longitude",None)
        tstInfo["latitude"] = request.GET.get("latitude",None)
        #title = title.encode('utf-8')
        tstInfo["name"] = request.GET.get("name",None)
        tstInfo["name"] = tstInfo["name"].encode('utf-8')
        tstInfo["max_parkingCapacity"] = request.GET.get("MaxCount",0)
        ParkingInfo.objects.create(**tstInfo)
        return HttpResponse("Init is OK"+tstInfo["name"]);
    else:
        pass

    return HttpResponse("Init OK");

def UpdateParkingData(request):
    from pikachutest.models import ParkingInfo
    ret = []
    if request.method == "GET":
        ParkingList = ParkingInfo.objects.all()

        for key in ParkingList:
            ele = {}
            ele['name'] = key.name
            ele['longitude'] = key.longitude
            ele['latitude'] = key.latitude
            ele['max_parkingCapacity'] = key.max_parkingCapacity
            ele['parkingCount'] = key.parkingCount
            ret.append(ele)
        print  ret
        return HttpResponse(ret)
    else:
        pass
    return