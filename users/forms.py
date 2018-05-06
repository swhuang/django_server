# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .fields import HoneyPotField, PasswordField, UsersEmailField, UsercharField, MerchantField, PhoneField
from django.contrib.auth.models import Group
from users.models import Member


class UserCreationForm(forms.ModelForm):

    error_messages = {
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    email = UsersEmailField(label=_('Email Address'), max_length=255)
    identification = forms.CharField(label=_(u'性别'), max_length=1)
    username = UsercharField(label=_(u'用户姓名'), max_length=100)
    userid = UsercharField(label=_(u'用户名'), max_length=255)
    password1 = PasswordField(label=_(u'密码'))
    password2 = PasswordField(
        label=_(u'确认密码'),
        help_text=_('Enter the same password as above, for verification.'))

    mid = MerchantField(label=_(u'商户号'))

    class Meta:
        model = get_user_model()
        fields = ('userid',)

    def clean_email(self):

        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = not settings.USERS_VERIFY_EMAIL
        user.email = self.cleaned_data['email']
        user.identification = int(self.cleaned_data['identification'])
        user.username = self.cleaned_data['username']
        _merchant = None

        try:
            from crm.models import Merchant
            _merchant = Merchant.objects.get(merchantid=self.cleaned_data['mid'])
        except:
            print "error!!!!"+str(self.cleaned_data['mid'])


        user.mid = _merchant
        if commit:
            user.save()
        print(user.groups.add(Group.objects.get(name='OrderUser')))
        return user


class MemberCreationForm(forms.ModelForm):

    """docstring for MemberCreationForm"""
    error_messages = {
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    phone = PhoneField(label=_(u'手机号'), max_length=11, min_length=11)
    password1 = PasswordField(label=_(u'密码'))
    '''
    password2 = PasswordField(
        label=_(u'确认密码'),
        help_text=_('Enter the same password as above, for verification.'))
    '''
    mid = MerchantField(label=_(u'商户号'))

    class Meta:

        model = Member
        #fields = ('email',)
        fields = ('phone',)

    def save(self, commit=True):
        member = super(MemberCreationForm, self).save(commit=False)
        member.set_password(self.cleaned_data['password1'])
        member.phone = self.cleaned_data['phone']
        member.default_init()
        _merchant = None
        try:
            from crm.models import Merchant
            _merchant = Merchant.objects.get(merchantid=self.cleaned_data['mid'])
        except:
            print "error!!!!"+"error!!!!"+str(self.cleaned_data['mid'])
        member.mid = _merchant
        if commit:
            member.save()
        return member


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(label=_('Password'), help_text=_(
        'Raw passwords are not stored, so there is no way to see '
        'this user\'s password, but you can change the password '
        'using <a href=\"password/\">this form</a>.'))

    class Meta:
        model = get_user_model()
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial['password']


class RegistrationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.

    """
    tos = forms.BooleanField(
        label=_('I have read and agree to the Terms of Service'),
        widget=forms.CheckboxInput,
        error_messages={
            'required': _('You must agree to the terms to register')
        })


class RegistrationFormHoneypot(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a honeypot field
    for Spam Prevention

    """
    accept_terms = HoneyPotField()
