# -*- coding: utf-8 -*-
from rest_framework import serializers
import datetime
import time
import os
from rest_framework.settings import api_settings
from rest_framework import ISO_8601
from django.utils import six, timezone
from crm.server_utils.base import FSM
import logging

class PdImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value or value == 'null' or value == '':
            return None

        use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)

        if use_url:
            if not getattr(value, 'url', None):
                # If the file has not been saved it may not have a URL.
                return None

            request = self.context.get('request', None)
            if request is not None:
                url = '{scheme}://{host}/{path}'.format(scheme=request.scheme,
                                                           host=request.get_host(),
                                                           path=value.url)
                avatar = '{scheme}://{host}/{path}'.format(scheme=request.scheme,
                                                           host=request.get_host(),
                                                           path=value['avatar'].url)
            else:
                url = value.url
                avatar = value['avatar'].url
            name = value.url.split('/')[-1]

            return {'url': url, 'avatar': avatar, 'name': name}
        return value.name


class ModifiedDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        if not value:
            return None

        output_format = getattr(self, 'format', api_settings.DATETIME_FORMAT)

        if output_format is None or isinstance(value, six.string_types):
            return value

        value = self.enforce_timezone(value)

        if output_format.lower() == ISO_8601:
            return value.strftime('%y-%m-%d %H:%M:%S')
        return value.strftime(output_format)


class AmountField(serializers.DecimalField):
    def __init__(self, coerce_to_string=None, max_value=None, min_value=None,
                 localize=False, rounding=None, **kwargs):

        super(AmountField, self).__init__(max_digits=12, decimal_places=2, coerce_to_string=coerce_to_string,
                                          max_value=max_value, min_value=min_value,
                                          localize=localize, rounding=rounding, **kwargs)


    def to_internal_value(self, data):
        return super(AmountField, self).to_internal_value(data)

    def to_representation(self, value):
        return str(super(AmountField, self).to_representation(value))

class StrfloatField(serializers.FloatField):

    def to_internal_value(self, data):
        if isinstance(data, six.text_type) and len(data) > self.MAX_STRING_LENGTH:
            self.fail('max_string_length')

        try:
            return float(data)
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return str(value)


class StatusField(serializers.IntegerField):

    def to_representation(self, value):
        if isinstance(value, FSM.State):
            for i, v in (FSM.statedict.items()):
                if type(value) == v:
                    return str(i)
            logging.getLogger('django').error("status error" + value.__class__.__name__)
            raise ValueError("status error" + value.__class__.__name__)
        else:
            return str(super(StatusField, self).to_representation(value))

class JsonField(serializers.CharField):
    def to_representation(self, value):
        if value == '':
            return value
        if value.has_key('mainimage'):
            request = self.context.get('request', None)
            url = '{scheme}://{host}/{path}'.format(scheme=request.scheme,
                                                    host=request.get_host(),
                                                    path=value['mainimage'])
            value['mainimage'] = url
            return value
        else:
            return value
        #return super(JsonField, self).to_representation(value)

class ArrayField(serializers.CharField):
    def to_internal_value(self, data):
        return super(ArrayField, self).to_internal_value(data)

    def to_representation(self, value):
        return super(ArrayField, self).to_representation(value)