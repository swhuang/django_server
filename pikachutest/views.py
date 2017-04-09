from django.shortcuts import render

# Create your views here.
#coding:utf-8
import hashlib
from lxml import etree
from django.utils.encoding import smart_str
from django.http import HttpResponse

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
    print getrt
    result = str(getrt);
    ParkingInfo.objects.filter(pid=0).delete();
    return HttpResponse("Init OK"+result);