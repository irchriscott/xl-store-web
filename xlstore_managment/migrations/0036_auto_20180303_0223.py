# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-03 02:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xlstore', '0008_auto_20180211_1743'),
        ('xlstore_managment', '0035_auto_20180302_0506'),
    ]

    operations = [
        migrations.CreateModel(
            name='MS_CompanyMobile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xlstore_managment.MS_CompanyAdministrator')),
            ],
        ),
    ]
