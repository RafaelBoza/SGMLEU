# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-10 19:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0033_auto_20190328_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidad',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 10, 15, 14, 10, 590000)),
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 10, 15, 14, 10, 574000)),
        ),
        migrations.AlterField(
            model_name='licenciadossma',
            name='incorporado',
            field=models.CharField(default=b'', max_length=1),
        ),
        migrations.AlterField(
            model_name='organismosautorizadosregistrarinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 10, 15, 14, 10, 684000)),
        ),
    ]
