# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-30 16:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20180331_0022'),
        ('crm', '0009_auto_20180330_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paytime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u652f\u4ed8\u65f6\u95f4')),
                ('orderamount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='\u8ba2\u5355\u91d1\u989d')),
                ('payedamount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='\u652f\u4ed8\u91d1\u989d')),
                ('payment_status', models.SmallIntegerField(verbose_name='\u652f\u4ed8\u72b6\u6001')),
                ('orderid', models.CharField(db_index=True, default=users.utils.gettimestamp, max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('gmt_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('proj_id', models.CharField(db_index=True, default='', max_length=10)),
                ('proj_name', models.CharField(default='', max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='merchant',
            name='gmt_create',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='gmt_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='gmt_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='project',
            name='mid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Merchant'),
        ),
        migrations.AddField(
            model_name='order',
            name='mid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Merchant'),
        ),
        migrations.AddField(
            model_name='order',
            name='proj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Project'),
        ),
        migrations.AddField(
            model_name='order',
            name='userinfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Member'),
        ),
    ]
