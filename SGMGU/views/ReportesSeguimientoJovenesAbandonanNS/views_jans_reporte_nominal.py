# -*- coding: utf-8 -*-
import time as time1
from datetime import *
from SGMGU.models import *
from xlsxwriter import Workbook
from django.http import HttpResponse
from SGMGU.views.utiles import permission_required
from django.contrib.auth.decorators import login_required


@login_required()
@permission_required(['administrador', 'trabajador_social_joven_abandona', 'organismo', 'dmt', 'dpt_ee'])
def reporte_nominal_jans(request):

    start_time = time1.time()
    anno_actual = datetime.today().year
    perfil_usuario = request.user.perfil_usuario
    categoria_usuario = perfil_usuario.categoria.nombre
    municipio = perfil_usuario.municipio
    provincia = perfil_usuario.provincia
    organismo = perfil_usuario.organismo
    jovenes = None

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    if categoria_usuario == 'administrador':
        response[
            'Content-Disposition'] = "attachment; filename=Reporte_nominal_({}).xlsx".format(anno_actual)

        jovenes = JovenAbandonanNS.objects.filter(fecha_registro__year=anno_actual)

    elif categoria_usuario in ['dmt', 'trabajador_social_joven_abandona']:
        response[
            'Content-Disposition'] = "attachment; filename=Reporte_nominal_({}_{}).xlsx".format(municipio, anno_actual)

        jovenes = JovenAbandonanNS.objects.filter(fecha_registro__year=anno_actual, municipio_residencia=municipio)

    elif categoria_usuario == 'dpt_ee':
        response[
            'Content-Disposition'] = "attachment; filename=Reporte_nominal_({}_{}).xlsx".format(provincia, anno_actual)

        jovenes = JovenAbandonanNS.objects.filter(fecha_registro__year=anno_actual, municipio_residencia__provincia=provincia)

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte Nominal")

    formato_primera_fila = book.add_format({'bold': True, 'border': 1})
    formato1 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Nombre y apellidos", formato_primera_fila)
    worksheet_data.write("B1", "CI", formato_primera_fila)
    worksheet_data.write("C1", "Sexo", formato_primera_fila)
    worksheet_data.write("D1", "Municipio de residencia", formato_primera_fila)
    worksheet_data.write("E1", "Provincia de residencia", formato_primera_fila)
    worksheet_data.write("F1", "Dirección particular".decode('utf-8'), formato_primera_fila)
    worksheet_data.write("G1", "Nivel escolar", formato_primera_fila)
    worksheet_data.write("H1", "Centro de estudio", formato_primera_fila)
    worksheet_data.write("I1", "Carrera que abandona", formato_primera_fila)
    worksheet_data.write("J1", "Año en que abandona".decode('utf-8'), formato_primera_fila)
    worksheet_data.write("K1", "Causa de la baja del NS", formato_primera_fila)
    worksheet_data.write("L1", "Día de la baja".decode('utf-8'), formato_primera_fila)
    worksheet_data.write("M1", "Mes de la baja", formato_primera_fila)
    worksheet_data.write("N1", "Año de la baja".decode('utf-8'), formato_primera_fila)

    worksheet_data.set_column("A:A", 35)
    worksheet_data.set_column("B:B", 13)
    worksheet_data.set_column("C:C", 9.30)
    worksheet_data.set_column("D:D", 21.90)
    worksheet_data.set_column("E:E", 21)
    worksheet_data.set_column("F:F", 24)
    worksheet_data.set_column("G:G", 14)
    worksheet_data.set_column("H:H", 24)
    worksheet_data.set_column("I:I", 24)
    worksheet_data.set_column("J:J", 19.75)
    worksheet_data.set_column("K:K", 25)
    worksheet_data.set_column("L:L", 12)
    worksheet_data.set_column("M:M", 13)
    worksheet_data.set_column("N:N", 12.75)

    if jovenes is not None:
        indice = 0

        for joven in jovenes:

            worksheet_data.write(indice + 1, 0, joven.nombre_apellidos, formato1)
            worksheet_data.write(indice + 1, 1, joven.ci, formato1)
            worksheet_data.write(indice + 1, 2, joven.get_sexo(), formato1)
            worksheet_data.write(indice + 1, 3, joven.municipio_residencia.nombre, formato1)
            worksheet_data.write(indice + 1, 4, joven.municipio_residencia.provincia.nombre, formato1)
            worksheet_data.write(indice + 1, 5, joven.direccion_particular, formato1)
            worksheet_data.write(indice + 1, 6, joven.nivel_escolar.nombre, formato1)
            worksheet_data.write(indice + 1, 7, joven.centro_estudio.nombre, formato1)
            worksheet_data.write(indice + 1, 8, joven.carrera_abandona.nombre, formato1)
            worksheet_data.write(indice + 1, 9, joven.get_anno_abandona(), formato1)
            worksheet_data.write(indice + 1, 10, joven.causa_baja_ns.causa, formato1)
            worksheet_data.write(indice + 1, 11, joven.dia_baja, formato1)
            worksheet_data.write(indice + 1, 12, joven.mes_baja, formato1)
            worksheet_data.write(indice + 1, 13, joven.anno_baja, formato1)

            indice += 1

    book.close()
    print("Tiempo de ejecución: %.2f segundos" % (time1.time() - start_time))
    return response
