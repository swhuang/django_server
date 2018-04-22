# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-04-19 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalorder',
            name='userinfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Member'),
        ),
        migrations.AddField(
            model_name='productrental',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ProductDetail'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='pdetail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proditem', to='crm.ProductDetail'),
        ),
        migrations.AddField(
            model_name='datapool',
            name='mid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Merchant'),
        ),
        migrations.AddField(
            model_name='comborental',
            name='current_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ProductDetail'),
        ),
        migrations.AddField(
            model_name='comborental',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Package'),
        ),
    ]