# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-02-06 19:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0016_auto_20190205_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComprobacionAnualEmpleoEstatal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_comprobacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
