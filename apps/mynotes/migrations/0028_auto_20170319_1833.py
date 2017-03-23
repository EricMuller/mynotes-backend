# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-03-19 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mynotes', '0027_auto_20170314_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnote',
            name='schedule_dt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='schedule_dt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='historicalnote',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('V', 'Valid'), ('T', 'Trash')], default='D', max_length=1),
        ),
        migrations.AlterField(
            model_name='historicalnote',
            name='type',
            field=models.CharField(choices=[('NOTE', 'Note'), ('TODO', 'Todo'), ('MAIL', 'Mail'), ('LINK', 'Link')], default='NOTE', max_length=10),
        ),
        migrations.AlterField(
            model_name='note',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('V', 'Valid'), ('T', 'Trash')], default='D', max_length=1),
        ),
        migrations.AlterField(
            model_name='note',
            name='type',
            field=models.CharField(choices=[('NOTE', 'Note'), ('TODO', 'Todo'), ('MAIL', 'Mail'), ('LINK', 'Link')], default='NOTE', max_length=10),
        ),
    ]
