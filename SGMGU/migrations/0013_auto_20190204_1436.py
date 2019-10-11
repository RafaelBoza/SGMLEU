# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-02-04 19:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0012_auto_20190204_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 4, 14, 36, 57, 442000)),
        ),
        migrations.AlterField(
            model_name='interruptos',
            name='informe_valorativo',
            field=models.FileField(blank=True, null=True, upload_to=b'uploads/informe_valorativo_interruptos/'),
        ),
    ]
