# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-10 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_datapool'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapool',
            name='merchantid',
            field=models.CharField(db_index=True, default='', max_length=15, verbose_name='\u5546\u6237\u7f16\u53f7'),
        ),
    ]
