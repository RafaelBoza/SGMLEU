# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2020-03-14 16:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0009_auto_20200314_1246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jovenabandonanns',
            old_name='fecha_modificad',
            new_name='fecha_modificado',
        ),
        migrations.RemoveField(
            model_name='jovenabandonanns',
            name='reincorporado_educacion',
        ),
        migrations.AddField(
            model_name='procesotrabajadorsocialjans',
            name='reincorporado_educacion',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entidad',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 14, 12, 51, 33, 927000)),
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 14, 12, 51, 33, 911000)),
        ),
        migrations.AlterField(
            model_name='organismosautorizadosregistrarinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 14, 12, 51, 34, 52000)),
        ),
    ]
