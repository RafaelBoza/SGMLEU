# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-03-28 18:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0026_auto_20190321_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividadinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 196000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='asociacion',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 180000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='causalbaja',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 102000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='causalinterrupcion',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 196000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='causalnoaceptacion',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 102000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='causalnoincorporado',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 102000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='causalnoreubicacion',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 196000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='causalnoubicado',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 102000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='controllicenciadossma',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 118000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='delito',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 118000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='desvinculado',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 133000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='discapacidad',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 180000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='discapacitados',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 180000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='egresadosefi',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 180000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='egresadosescuelasconducta',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 164000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='egresadosescuelasespeciales',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 164000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='egresadosestablecimientospenitenciarios',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 133000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='entidad',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 102000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='estadoincorporado',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 102000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 14, 11, 44, 86000)),
        ),
        migrations.AlterField(
            model_name='fuenteprocedencia',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 118000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='licenciadossma',
            name='fecha_registro',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='menores',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 149000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='motivoegreso',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 118000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='nivelescolar',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 102000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organismosautorizadosregistrarinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 14, 11, 44, 196000)),
        ),
        migrations.AlterField(
            model_name='personasriesgo',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 196000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tmedioocalificadoeoficio',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 149000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 11, 44, 102000, tzinfo=utc)),
        ),
    ]
