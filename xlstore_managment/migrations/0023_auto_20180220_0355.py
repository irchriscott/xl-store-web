# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-20 03:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xlstore', '0008_auto_20180211_1743'),
        ('xlstore_managment', '0022_auto_20180211_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ms_marketaccess',
            name='access_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
