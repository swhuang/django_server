from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/accounts/login/")
def crmtest(request):
    # return HttpResponse('crm_test')
    print "test"
    return render(request, "project/tables.html")
