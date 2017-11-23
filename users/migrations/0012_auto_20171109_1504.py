# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-09 07:04
from __future__ import unicode_literals

from django.db import migrations, models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20171109_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderid',
            field=models.CharField(db_index=True, default=users.utils.gettimestamp, max_length=20, unique=True),
        ),
    ]