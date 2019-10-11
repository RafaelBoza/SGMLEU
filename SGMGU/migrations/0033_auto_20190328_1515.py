# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-03-28 19:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0032_auto_20190328_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividadinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='asociacion',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='causalbaja',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='causalinterrupcion',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='causalnoaceptacion',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='causalnoincorporado',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='causalnoreubicacion',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='causalnoubicado',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comprobacionanualempleoestatal',
            name='fecha_comprobacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='controllicenciadossma',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='delito',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='desvinculado',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='discapacidad',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='discapacitados',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='discapacitados',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='egresadosefi',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='egresadosefi',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='egresadosescuelasconducta',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='egresadosescuelasconducta',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='egresadosescuelasespeciales',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='egresadosescuelasespeciales',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='egresadosestablecimientospenitenciarios',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='entidad',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 15, 15, 35, 833000)),
        ),
        migrations.AlterField(
            model_name='estadoincorporado',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 15, 15, 35, 817000)),
        ),
        migrations.AlterField(
            model_name='fuenteprocedencia',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialdesvinculado',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialdiscapacitados',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialegresadosefi',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialegresadosescuelasconducta',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialegresadosescuelasespeciales',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialegresadosysancionados',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historiallicenciadossma',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialmenores',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialpersonasriesgo',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historialtmedioocalificadoeoficio',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='interruptos',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menores',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menores',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='motivoegreso',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='nivelescolar',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='organismosautorizadosregistrarinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 15, 15, 35, 926000)),
        ),
        migrations.AlterField(
            model_name='personasriesgo',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='personasriesgo',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tmedioocalificadoeoficio',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tmedioocalificadoeoficio',
            name='fecha_ubicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
