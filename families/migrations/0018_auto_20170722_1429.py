# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0017_auto_20170722_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='family',
            name='country',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='family',
            name='region',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]