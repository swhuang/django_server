# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pikachutest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinginfo',
            name='parkingCount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]