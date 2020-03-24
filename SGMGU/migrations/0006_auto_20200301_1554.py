# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2020-03-01 20:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0005_auto_20200109_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='procesotrabajadorsocialjans',
            name='rectificar_causa_baja',
        ),
        migrations.AlterField(
            model_name='entidad',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 15, 54, 53, 108000)),
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 15, 54, 53, 77000)),
        ),
        migrations.AlterField(
            model_name='organismosautorizadosregistrarinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 15, 54, 53, 218000)),
        ),
    ]