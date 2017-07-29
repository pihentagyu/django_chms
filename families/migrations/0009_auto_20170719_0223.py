# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-19 06:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0008_auto_20170719_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='families_family_related', related_query_name='families_familys', to='families.Country'),
        ),
    ]
