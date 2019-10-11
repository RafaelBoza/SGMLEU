# -*- coding: utf-8 -*-
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range
from SGMGU.models import *
from SGMGU.views.utiles import permission_required


@login_required()
@permission_required(['administrador'])
def menores_ubicados_por_sector(request):
    start_time = time.time()

    anno = datetime.today().year

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Menores_ubicados_por_sector._(%s).xlsx" % (
        anno)
    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Provincias", formato)
    worksheet_data.write(0, 1, "Total", formato)

    ubicaciones = Ubicacion.objects.filter(activo=True).order_by('id')
    cantidad_ubicaciones = ubicaciones.count()
    indice = 2

    for ubicacion in ubicaciones:
        worksheet_data.write(0, indice, ubicacion.ubicacion, formato)
        indice = indice + 1

    worksheet_data.set_column("A:A", 17)

    provincias = Provincia.objects.all()
    arr_provincias = []
    for p in provincias:
        arr_provincias.append(p.nombre)

    worksheet_data.write_column(1, 0, arr_provincias, formato2)

    cantidad_provincias = arr_provincias.__len__()
    indice_total = cantidad_provincias + 1

    worksheet_data.write(indice_total, 0, "Total", formato)
    
    edades = [15, 16]

    obreros_calificados = TMedioOCalificadoEOficio.objects.filter(edad__in=edades, ubicado=True, fuente_procedencia_id=7,
                                                                    activo=True)

    escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(edad__in=edades, ubicado=True, fuente_procedencia_id=8,
                                                                activo=True)

    menores_incapacitados = Menores.objects.filter(ubicado=True, fuente_procedencia_id=12, activo=True)

    menores_desvinculados = Menores.objects.filter(ubicado=True, fuente_procedencia_id=13, activo=True)

    menores_dictamen = Menores.objects.filter(ubicado=True, fuente_procedencia_id=14, activo=True)


    total_obreros_calificados_provincias = []
    total_escuela_oficio_provincias = []
    total_menores_incapacitados_provincias = []
    total_menores_desvinculados_provincias = []
    total_menores_dictamen_provincias = []

    for provincia in provincias:

        # UBICADOS: Egresados obreros calificados
        total_obreros_calificados_provincias.append(
            obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Egresados escuelas de oficio
        total_escuela_oficio_provincias.append(
            escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Menores incapacitados para el estudio por dictamen médico
        total_menores_incapacitados_provincias.append(
            menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Menores desvinculados del SNE por bajo rendimiento
        total_menores_desvinculados_provincias.append(
            menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Menores con dictamen del CDO-MININT
        total_menores_dictamen_provincias.append(
            menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia).count())

    worksheet_data.write_column(1, 2, total_obreros_calificados_provincias, formato2)
    worksheet_data.write_column(1, 3, total_escuela_oficio_provincias, formato2)
    worksheet_data.write_column(1, 4, total_menores_incapacitados_provincias, formato2)
    worksheet_data.write_column(1, 5, total_menores_desvinculados_provincias, formato2)
    worksheet_data.write_column(1, 6, total_menores_dictamen_provincias, formato2)

    # ------------ SUMAS ABAJO-------------------

    sumas = []
    for a in range(1, 7):
        total = '=SUM(%s)' % xl_range(1, a, cantidad_provincias, a)
        sumas.append(total)

    indice_sumas = 1
    for suma in sumas:
        worksheet_data.write(17, indice_sumas, suma, formato2)
        indice_sumas = indice_sumas + 1

    # ------------ SUMAS ARRIBA-------------------
    sumas_abajo = []
    inicio = 2
    for i in range(1, cantidad_provincias + 1):
        total2 = '=SUM(%s)' % xl_range(i, inicio, i, cantidad_ubicaciones + inicio - 1)
        sumas_abajo.append(total2)

    indice_sumas = 1
    for suma in sumas_abajo:
        worksheet_data.write(indice_sumas, 1, suma, formato2)
        indice_sumas = indice_sumas + 1

    book.close()
    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
