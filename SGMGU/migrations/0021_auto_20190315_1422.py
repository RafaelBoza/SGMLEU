# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-03-15 18:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0020_auto_20190306_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organismosautorizadosregistrarinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
