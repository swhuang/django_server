from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
@permission_required('crm.view')
@login_required(login_url="/accounts/login/")
def crmtest(request):
    # return HttpResponse('crm_test')
    print "test"
    return render(request, "project/tables.html")

def test(request):
    return HttpResponse("testok!")
