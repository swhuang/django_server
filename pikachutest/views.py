from django.shortcuts import render

# Create your views here.
#coding:utf-8
from django.http import HttpResponse
 
def index(request):
    pagehtml = u"<h>Go2parking</h><p>luludasabi</p>"
    return HttpResponse(pagehtml)
def test(request):
    return HttpResponse(u"gogogo")
