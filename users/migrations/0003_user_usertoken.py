# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-09 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_sessiontoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='usertoken',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
