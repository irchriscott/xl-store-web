# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-01 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xlstore_ecommerce', '0006_auto_20180301_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='ec_shoppingcart',
            name='others_chargers',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=18),
        ),
        migrations.AddField(
            model_name='ec_shoppingcart',
            name='total_net',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=18),
        ),
    ]
