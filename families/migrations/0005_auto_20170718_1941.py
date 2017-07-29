# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0004_auto_20170718_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='adult',
            name='membership_status',
            field=models.CharField(choices=[('FM', 'Member'), ('RA', 'Regular Attender')], default='FM', max_length=2),
        ),
        migrations.AddField(
            model_name='child',
            name='membership_status',
            field=models.CharField(choices=[('FM', 'Member'), ('RA', 'Regular Attender')], default='FM', max_length=2),
        ),
    ]
