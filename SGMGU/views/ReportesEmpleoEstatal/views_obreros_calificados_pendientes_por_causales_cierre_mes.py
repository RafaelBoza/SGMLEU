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
def obreros_calificados_pendientes_por_causales_cierre_mes(request):
    start_time = time.time()

    anno = datetime.today().year
    mes = datetime.today().month

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Obreros_calificados_pendientes_por_causales._(%s).xlsx" % (
        anno)
    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Provincias", formato)
    worksheet_data.set_column("A:A", 17)

    worksheet_data.write(0, 1, "Total", formato)

    provincias = Provincia.objects.all()
    arr_provincias = []
    for p in provincias:
        arr_provincias.append(p.nombre)

    worksheet_data.write_column(1, 0, arr_provincias, formato2)

    cantidad_provincias = arr_provincias.__len__()
    indice_total = cantidad_provincias + 1

    worksheet_data.write(indice_total, 0, "Total", formato)

    obreros_calificados = TMedioOCalificadoEOficio.objects.filter(ubicado=False,
                                                                  fuente_procedencia_id=7,
                                                                  activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 7;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    obreros_calificados = obreros_calificados.exclude(id__in=ids_listado)

    ids_causas = []

    if obreros_calificados.count() > 0:
        for persona in obreros_calificados:
            if persona.causa_no_ubicado is None:
                pass
            elif persona.causa_no_ubicado.id not in ids_causas:
                ids_causas.append(persona.causa_no_ubicado.id)

    causales_no_ubicado = CausalNoUbicado.objects.filter(id__in=ids_causas, activo=True)
    cantidad_causales_no_ubicado = causales_no_ubicado.count()
    indice = 2

    for causa in causales_no_ubicado:
        worksheet_data.write(0, indice, causa.causa, formato)
        indice = indice + 1

    for indice_provincia, provincia in enumerate(provincias):

        for indice_causa, causa in enumerate(causales_no_ubicado):

            worksheet_data.write(indice_provincia + 1, indice_causa + 2,
                                 obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia,
                                                            causa_no_ubicado=causa).count(),
                                 formato2)

    # ------------ SUMAS ABAJO-------------------
    sumas_lateral = []
    for a in range(1, cantidad_causales_no_ubicado + 2):
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
        total2 = '=SUM(%s)' % xl_range(i, inicio + 1, i, cantidad_causales_no_ubicado + inicio)
        sumas_abajo.append(total2)

    indice_sumas = 1
    for suma in sumas_abajo:
        worksheet_data.write(indice_sumas, inicio, suma, formato2)
        indice_sumas = indice_sumas + 1

    book.close()
    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
