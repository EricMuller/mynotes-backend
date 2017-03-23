# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-22 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mynotes', '0009_auto_20161022_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='type',
            field=models.CharField(choices=[('NOTE', 'Note')], default='NOTE', max_length=10),
        ),
        migrations.AlterField(
            model_name='typenote',
            name='code',
            field=models.CharField(choices=[('NOTE', 'Note')], db_index=True, default='D', max_length=64, verbose_name='code'),
        ),
    ]
