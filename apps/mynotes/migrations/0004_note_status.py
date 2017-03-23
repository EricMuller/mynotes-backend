# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-20 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mynotes', '0003_auto_20161017_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('V', 'Valid')], default='D', max_length=1),
        ),
    ]
