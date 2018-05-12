# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductRental
from crm.server_utils.base import FSM


class StatusField(serializers.IntegerField):

    def to_representation(self, value):
        if isinstance(value, FSM.State):
            return int(value.statevalue)
        else:
            return super(StatusField, self).to_representation(value)

class RentalServiceSerializer(serializers.ModelSerializer):

    serviceStatus = StatusField()
    createTime = serializers.DateTimeField(source='gmt_create')

    class Meta:
        model = ProductRental
        exclude = ('gmt_create', 'gmt_modified', 'product')