# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_auto_20160712_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_order',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]