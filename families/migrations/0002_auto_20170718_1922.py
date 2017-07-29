# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 23:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import families.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('families', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=15)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(max_length=50)),
                ('suffix', models.CharField(blank=True, max_length=15)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('date_joined', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('occupation', models.CharField(blank=True, max_length=255)),
                ('workplace', models.CharField(blank=True, max_length=255)),
                ('work_address', models.CharField(blank=True, max_length=255)),
                ('marital_status', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=15)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(max_length=50)),
                ('suffix', models.CharField(blank=True, max_length=15)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('date_joined', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('school', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Children',
            },
        ),
        migrations.AddField(
            model_name='family',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=families.models.Family.get_image_path),
        ),
        migrations.AddField(
            model_name='family',
            name='image_sm',
            field=models.ImageField(blank=True, null=True, upload_to=families.models.Family.get_image_path),
        ),
        migrations.AddField(
            model_name='family',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='child',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='families.Family'),
        ),
        migrations.AddField(
            model_name='adult',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='families.Family'),
        ),
    ]
