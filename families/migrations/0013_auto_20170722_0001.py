# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 04:01
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0012_auto_20170721_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='region', chained_model_field='region', default=18, on_delete=django.db.models.deletion.CASCADE, to='cities_local.City'),
        ),
    ]