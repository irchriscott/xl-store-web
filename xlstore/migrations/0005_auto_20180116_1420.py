# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-16 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xlstore', '0004_auto_20171109_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='xlstore.CompanyCategories'),
        ),
    ]
