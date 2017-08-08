# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-30 12:01
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('webmarks_bookmarks', '0009_auto_20170730_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalbookmark',
            name='uuid',
            field=models.UUIDField(
                db_index=False, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, null=True),
        ),
    ]