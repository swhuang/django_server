# -*- coding: utf-8 -*-
from django import forms
from crm.models import Merchant
from users.models import Project
from users.fields import PhoneField, MerchantField
from django.utils.translation import ugettext_lazy as _


class QueryForm(forms.Form):
    r'''
    用户管理搜索表单

    '''
    error_messages = {
    }
    username = forms.CharField(label=_(u'姓名'), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control input-sm'}))
    phone = PhoneField(label=_(u'手机号'), max_length=11, min_length=11,
                       widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))
    id_no = forms.CharField(label=_(u'身份证号'), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control input-sm'}))
    email = forms.EmailField(label=_(u'邮箱'), max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control input-sm'}))

class ProjChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.proj_name

class OrderQueryForm(forms.Form):
    r'''
    订单管理搜索表单
    '''
    error_messages = {}
    mid = MerchantField(label=_(u'商户号'), max_length=15, widget=forms.TextInput(attrs={'class': 'form-control input-sm'}))
    merchant = forms.CharField(label=_(u'商户名称'), max_length=200,
                               widget=forms.TextInput(attrs={'class': 'form-control input-sm'}))
    membername = forms.CharField(label=_(u'用户姓名'), max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control input-sm'}))
    memberid = forms.CharField(label=_(u'用户id'), max_length=15,
                               widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))
    id_type = forms.TypedChoiceField(label=_(u'证件类型'), choices=([('1', '身份证'), ('2', '学生证')]), initial='1',
                                     widget=forms.Select(attrs={'class': 'form-control input-sm'}))
    id_num = forms.CharField(label=_(u'证件号'), widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))

    def __init__(self, _merchant):
        super(OrderQueryForm, self).__init__()
        self.fields['project'] = ProjChoiceField(label=_(u'缴费项目'),
                                                        queryset=Project.objects.filter(mid=_merchant),
                                                        empty_label=_(u"请选择缴费项目"), to_field_name="proj_id",
                                                        widget=forms.Select(attrs={'class': 'form-control input-sm'}))

class OrderGenForm(forms.Form):
    r'''
    订单生成表单
    '''
    orderamount = forms.CharField(label=_(u'订单金额'), widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))


class OrderPaymentForm(forms.Form):
    r'''
    提交支付
    '''
    paymentamount = forms.CharField(label=_(u'支付金额'),
                                    widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))

# 获取授权信息
# input:
#     merchantid
#     timeStamp
#     [securitykey]
#     checksum
class GetSessionForm(forms.Form):
    merchantid = forms.CharField(max_length=200)
    timestamp = forms.DateTimeField(input_formats='%d/%m/%Y %h:%i')
    checksum = forms.CharField(max_length=100)

    def clean(self):
        _merchantid = self.cleaned_data.get('merchantid')
        _merchant = Merchant.objects.filter(merchantid=_merchantid)
        if not _merchant.exists():
            raise forms.ValidationError(u'Merchant does not exist')
