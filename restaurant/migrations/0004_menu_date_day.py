# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20160707_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='date_day',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
