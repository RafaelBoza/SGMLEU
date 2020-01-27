# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-12-01 00:01
from __future__ import unicode_literals

import SGMGU.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CausalNoRequiereEmpleo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('causa', models.CharField(max_length=255)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ControlJovenAbandonanNS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incorporado', models.CharField(max_length=255)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('causa_no_ubicado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.CausalNoUbicado')),
            ],
        ),
        migrations.CreateModel(
            name='JovenAbandonanNS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_apellidos', models.CharField(max_length=255)),
                ('ci', models.CharField(max_length=11, unique=True, validators=[SGMGU.models.validacion_ci_joven_abandona_ns])),
                ('sexo', models.CharField(max_length=1)),
                ('direccion_particular', models.CharField(max_length=255)),
                ('anno_abandona', models.IntegerField()),
                ('reincorporado_educacion', models.IntegerField()),
                ('anno_baja', models.IntegerField()),
                ('mes_baja', models.IntegerField()),
                ('dia_baja', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificad', models.DateTimeField(auto_now=True)),
                ('carrera_abandona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Carrera')),
                ('causa_baja_ns', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.CausalBaja')),
                ('municipio_residencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipio_residencia_joven_abandona_ns', to='SGMGU.Municipio')),
                ('nivel_escolar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.NivelEscolar')),
            ],
        ),
        migrations.CreateModel(
            name='ProcesoDireccionMEmpleoJANS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicado', models.CharField(choices=[(b'S', b'S\xc3\xad'), (b'N', b'No')], max_length=1)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('causa_no_ubicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.CausalNoUbicado')),
            ],
        ),
        migrations.CreateModel(
            name='ProcesoTrabajadorSocialJANS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requiere_empleo', models.CharField(choices=[(b'S', b'S\xc3\xad'), (b'N', b'No')], max_length=1)),
                ('observaciones_empleo', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('causa_no_requiere_empleo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.CausalNoRequiereEmpleo')),
                ('joven_abandona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.JovenAbandonanNS')),
                ('oficio_conoce', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Carrera')),
                ('rectificar_causa_baja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.CausalBaja')),
            ],
        ),
        migrations.AlterField(
            model_name='entidad',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 30, 19, 1, 57, 785000)),
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 30, 19, 1, 57, 769000)),
        ),
        migrations.AlterField(
            model_name='organismosautorizadosregistrarinterrupto',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 30, 19, 1, 57, 894000)),
        ),
        migrations.AddField(
            model_name='procesodireccionmempleojans',
            name='entidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Entidad'),
        ),
        migrations.AddField(
            model_name='procesodireccionmempleojans',
            name='joven_abandona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.JovenAbandonanNS'),
        ),
        migrations.AddField(
            model_name='procesodireccionmempleojans',
            name='municipio_entidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Municipio'),
        ),
        migrations.AddField(
            model_name='procesodireccionmempleojans',
            name='organismo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Organismo'),
        ),
        migrations.AddField(
            model_name='procesodireccionmempleojans',
            name='ubicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Ubicacion'),
        ),
        migrations.AddField(
            model_name='controljovenabandonanns',
            name='entidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Entidad'),
        ),
        migrations.AddField(
            model_name='controljovenabandonanns',
            name='joven_abandona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.JovenAbandonanNS'),
        ),
        migrations.AddField(
            model_name='controljovenabandonanns',
            name='municipio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Municipio'),
        ),
        migrations.AddField(
            model_name='controljovenabandonanns',
            name='organismo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Organismo'),
        ),
        migrations.AddField(
            model_name='controljovenabandonanns',
            name='ubicacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Ubicacion'),
        ),
    ]