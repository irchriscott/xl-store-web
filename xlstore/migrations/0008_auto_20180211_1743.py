# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-11 17:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xlstore', '0007_auto_20180120_0442'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_created=True)),
                ('address', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='company',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='xlstore.Company'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='xlstore.User'),
        ),
    ]
