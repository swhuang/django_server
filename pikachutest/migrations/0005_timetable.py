# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-26 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pikachutest', '0004_auto_20170419_0323'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_key', models.IntegerField(default=0)),
                ('teacherid', models.IntegerField(default=0)),
                ('courseid', models.IntegerField(default=0)),
                ('classid', models.IntegerField(default=0)),
                ('grade', models.IntegerField(default=0)),
            ],
        ),
    ]