# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-04-07 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20180331_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='mid',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Merchant'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mid',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Merchant'),
        ),
    ]
