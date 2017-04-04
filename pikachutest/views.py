from django.shortcuts import render

# Create your views here.
#coding:utf-8
from django.http import HttpResponse
 
def index(request):
    return HttpResponse(u"I am pikachu!")
def test(request):
    return HttpResponse(u"gogogo")
