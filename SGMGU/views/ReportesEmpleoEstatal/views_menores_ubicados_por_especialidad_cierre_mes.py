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
def menores_ubicados_por_especialidad_cierre_mes(request):
    start_time = time.time()

    anno = datetime.today().year
    mes = datetime.today().month

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Menores_ubicados_por_especialidad._(%s).xlsx" % (
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

    edades = [15, 16]

    obreros_calificados = TMedioOCalificadoEOficio.objects.filter(edad__in=edades, ubicado=True,
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

    escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(edad__in=edades, ubicado=True, fuente_procedencia_id=8,
                                                              activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 8;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    escuelas_oficio = escuelas_oficio.exclude(id__in=ids_listado)

    menores_incapacitados = Menores.objects.filter(ubicado=True, fuente_procedencia_id=12, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 12;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_incapacitados = menores_incapacitados.exclude(id__in=ids_listado)

    menores_desvinculados = Menores.objects.filter(ubicado=True, fuente_procedencia_id=13, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 13;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_desvinculados = menores_desvinculados.exclude(id__in=ids_listado)

    menores_dictamen = Menores.objects.filter(ubicado=True, fuente_procedencia_id=14, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 14;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_dictamen = menores_dictamen.exclude(id__in=ids_listado)

    ids_especialidades = []

    if obreros_calificados.count() > 0:
        for persona in obreros_calificados:
            if persona.carrera is None:
                pass
            elif persona.carrera.id not in ids_especialidades:
                ids_especialidades.append(persona.carrera.id)

    if escuelas_oficio.count() > 0:
        for persona in escuelas_oficio:
            if persona.carrera is None:
                pass
            elif persona.carrera.id not in ids_especialidades:
                ids_especialidades.append(persona.carrera.id)

    if menores_incapacitados.count() > 0:
        for persona in menores_incapacitados:
            if persona.carrera is None:
                pass
            elif persona.carrera.id not in ids_especialidades:
                ids_especialidades.append(persona.carrera.id)

    if menores_desvinculados.count() > 0:
        for persona in menores_desvinculados:
            if persona.carrera is None:
                pass
            elif persona.carrera.id not in ids_especialidades:
                ids_especialidades.append(persona.carrera.id)

    if menores_dictamen.count() > 0:
        for persona in menores_dictamen:
            if persona.carrera is None:
                pass
            elif persona.carrera.id not in ids_especialidades:
                ids_especialidades.append(persona.carrera.id)

    especialidades = Carrera.objects.filter(id__in=ids_especialidades)
    cantidad_especialidades = especialidades.count()
    indice = 2

    for especialidad in especialidades:
        worksheet_data.write(0, indice, especialidad.nombre, formato)
        indice = indice + 1

    for indice_provincia, provincia in enumerate(provincias):

        for indice_especialidad, especialidad in enumerate(especialidades):


            # UBICADOS: Egresados obreros calificados
            total_obreros_calificados_provincias = obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia, carrera=especialidad).count()

            # UBICADOS: Egresados escuelas de oficio
            total_escuela_oficio_provincias = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia, carrera=especialidad).count()

            # UBICADOS: Menores incapacitados para el estudio por dictamen médico
            total_menores_incapacitados_provincias = menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia, carrera=especialidad).count()

            # UBICADOS: Menores desvinculados del SNE por bajo rendimiento
            total_menores_desvinculados_provincias = menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia, carrera=especialidad).count()

            # UBICADOS: Menores con dictamen del CDO-MININT
            total_menores_dictamen_provincias = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia, carrera=especialidad).count()

            total = total_obreros_calificados_provincias + total_escuela_oficio_provincias + total_menores_incapacitados_provincias + total_menores_desvinculados_provincias + total_menores_dictamen_provincias

            worksheet_data.write(indice_provincia + 1, indice_especialidad + 2, total, formato2)

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
        total2 = '=SUM(%s)' % xl_range(i, inicio + 1, i, cantidad_especialidades + inicio)
        sumas_abajo.append(total2)

    indice_sumas = 1
    for suma in sumas_abajo:
        worksheet_data.write(indice_sumas, inicio, suma, formato2)
        indice_sumas = indice_sumas + 1

    book.close()
    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
