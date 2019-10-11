# -*- coding: utf-8 -*-
import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range

from SGMGU.models import *
from SGMGU.views.utiles import permission_required


@login_required()
@permission_required(['administrador'])
def obreros_calificados_pendientes_por_no_existir_oferta(request):
    start_time = time.time()

    anno = datetime.today().year

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Obreros_calificados_pendientes_por_no_existir_oferta._(%s).xlsx" % (
        anno)
    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Provincias", formato)
    worksheet_data.set_column("A:A", 17)

    obreros_calificados = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=7, causa_no_ubicado_id=1,
                                                            activo=True)
    ids_especialidades = []
    for persona in obreros_calificados:
        if persona.carrera is None:
            pass
        elif persona.carrera.id not in ids_especialidades:
            ids_especialidades.append(persona.carrera.id)

    especialidades = Carrera.objects.filter(id__in=ids_especialidades)
    cantidad_especialidades = especialidades.count()
    indice = 1

    for especialidad in especialidades:
        worksheet_data.write(0, indice, especialidad.nombre, formato)
        indice = indice + 1

    total_arriba = indice
    worksheet_data.write(0, total_arriba, "Total", formato)

    provincias = Provincia.objects.all()
    arr_provincias = []
    for p in provincias:
        arr_provincias.append(p.nombre)

    worksheet_data.write_column(1, 0, arr_provincias, formato2)

    cantidad_provincias = arr_provincias.__len__()
    indice_total = cantidad_provincias + 1

    worksheet_data.write(indice_total, 0, "Total", formato)

    for indice_provincia, provincia in enumerate(provincias):

        for indice_causa, especialidad in enumerate(especialidades):

            worksheet_data.write(indice_provincia + 1, indice_causa + 1,
                                 obreros_calificados.filter(carrera_id=especialidad.id, municipio_solicita_empleo__provincia=provincia).count(),
                                 formato2)

    # ------------ SUMAS ABAJO-------------------
    sumas_lateral = []
    for a in range(1, cantidad_especialidades + 2):
        total = '=SUM(%s)' % xl_range(1, a, cantidad_provincias, a)
        sumas_lateral.append(total)

    indice_sumas = 1
    for suma in sumas_lateral:
        worksheet_data.write(cantidad_provincias + 1, indice_sumas, suma, formato2)
        indice_sumas = indice_sumas + 1

    # ------------ SUMAS ARRIBA-------------------
    sumas_abajo = []
    inicio = 1
    for i in range(1, cantidad_provincias + 1):
        total2 = '=SUM(%s)' % xl_range(i, inicio, i, cantidad_especialidades + inicio - 1)
        sumas_abajo.append(total2)

    indice_sumas = 1
    for suma in sumas_abajo:
        worksheet_data.write(indice_sumas, inicio + cantidad_especialidades, suma, formato2)
        indice_sumas = indice_sumas + 1

    book.close()

    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    # print("Tiempo transcurrido: % segundos." % elapsed_time)

    return response
