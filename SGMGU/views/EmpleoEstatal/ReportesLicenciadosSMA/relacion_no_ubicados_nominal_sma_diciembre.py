# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range

from SGMGU.models import *
from SGMGU.views.utiles import permission_required
from datetime import *
from metodos_auxiliares_sma import *
import time


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def relacion_no_ubicados_nominal_sma_diciembre(request):
    # start_time = time.time()
    anno_actual = datetime.today().year

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if categoria_usuario == 'dmt':
        response[
            'Content-Disposition'] = "attachment; filename=Relacion_nominal_no_incorporados_sma_Diciembre(%s)_(%s).xlsx" % (municipio_usuario,
                                                                                                anno_actual)

        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario, mes_entrevista='Diciembre',
                                                        fecha_registro__year=anno_actual, incorporado_id=2).values("municipio_residencia__provincia__nombre", "nombre_apellidos", "ci", "municipio_residencia__nombre", "mes_entrevista", "causa_no_ubicado__causa") | \
                          LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario, mes_entrevista='Diciembre',
                                                        activo=True, incorporado_id=2).values("municipio_residencia__provincia__nombre", "nombre_apellidos", "ci", "municipio_residencia__nombre", "mes_entrevista", "causa_no_ubicado__causa")
    elif categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Relacion_nominal_no_incorporados_sma_Diciembre(%s)_(%s).xlsx" % (provincia_usuario,
                                                                                                     anno_actual)

        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario, mes_entrevista='Diciembre',
                                                        fecha_registro__year=anno_actual, incorporado_id=2).values("municipio_residencia__provincia__nombre", "nombre_apellidos", "ci", "municipio_residencia__nombre", "mes_entrevista", "causa_no_ubicado__causa") | \
                          LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario, mes_entrevista='Diciembre',
                                                        activo=True, incorporado_id=2).values("municipio_residencia__provincia__nombre", "nombre_apellidos", "ci", "municipio_residencia__nombre", "mes_entrevista", "causa_no_ubicado__causa")
    else:
        response['Content-Disposition'] = "attachment; filename=Relacion_nominal_no_incorporados_sma_Diciembre(%s).xlsx" % anno_actual

        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(fecha_registro__year=anno_actual, mes_entrevista='Diciembre', incorporado_id=2).values("municipio_residencia__provincia__nombre", "nombre_apellidos", "ci", "municipio_residencia__nombre", "mes_entrevista", "causa_no_ubicado__causa") | \
                          LicenciadosSMA.objects.filter(activo=True, mes_entrevista='Diciembre', incorporado_id=2).values("municipio_residencia__provincia__nombre", "nombre_apellidos", "ci", "municipio_residencia__nombre", "mes_entrevista", "causa_no_ubicado__causa")

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet('No_incorporados')

    formato = book.add_format({'bold': True,
                               'border': 1})
    formato2 = book.add_format({'border': 1})

    if categoria_usuario == 'dmt':
        worksheet_data.write("A1", "Municipio", formato)
    else:
        worksheet_data.write("A1", "Nombre", formato)

    worksheet_data.write("B1", "CI", formato)
    worksheet_data.write("C1", "Municipio", formato)
    worksheet_data.write("D1", "Provincia", formato)
    worksheet_data.write("E1", "Fecha de la entrevista", formato)
    worksheet_data.write("F1", "Causa de no Incorporacion", formato)

    worksheet_data.set_column("A:A", 31)
    worksheet_data.set_column("B:B", 14)
    worksheet_data.set_column("C:C", 20.60)
    worksheet_data.set_column("D:D", 17)
    worksheet_data.set_column("E:E", 20)
    worksheet_data.set_column("F:F", 28.30)

    INICIO = 1

    for persona in LICENCIADOS_SMA:
        worksheet_data.write(INICIO, 0, persona['nombre_apellidos'], formato2)
        worksheet_data.write(INICIO, 1, persona['ci'], formato2)
        worksheet_data.write(INICIO, 2, persona['municipio_residencia__nombre'], formato2)
        worksheet_data.write(INICIO, 3, persona['municipio_residencia__provincia__nombre'], formato2)
        worksheet_data.write(INICIO, 4, persona["mes_entrevista"], formato2)
        worksheet_data.write(INICIO, 5, persona["causa_no_ubicado__causa"], formato2)

        INICIO += 1

    book.close()
    # elapsed_time = time.time() - start_time
    # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
