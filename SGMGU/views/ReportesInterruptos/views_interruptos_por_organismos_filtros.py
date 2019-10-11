# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from xlsxwriter import Workbook
from SGMGU.models import *
from SGMGU.views.utiles import obtener_mes
from SGMGU.views.ReportesInterruptos.metodos_auxiliares import *
from SGMGU.views.utiles import permission_required
from datetime import *


@login_required()
@permission_required(['administrador', 'interrupto', 'dpt_ee'])
def interruptos_por_organismos_filtros(request):

    if request.method == 'POST':

        anno_actual = datetime.today().year
        nombre_anno = anno_actual
        mes = datetime.today().month
        categoria_usuario = request.user.perfil_usuario.categoria.nombre
        organismo = request.user.perfil_usuario.organismo
        nombre_organismo = organismo.nombre.encode('utf-8').strip()

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        if request.POST['mes']:
            mes = int(request.POST['mes'])
            nombre_mes = obtener_mes(mes - 1)
            if mes == 12:
                mes = 1
                nombre_mes = obtener_mes(mes - 1)
                anno_actual = anno_actual + 1
            else:
                mes = mes + 1

        if request.POST['anno']:
            nombre_anno = int(request.POST['anno'])
            if request.POST['mes']:
                if int(request.POST['mes']) == 12:
                    anno_actual = int(request.POST['anno']) + 1
                else:
                    anno_actual = int(request.POST['anno'])

        if request.POST['provincia']:
            provincia = request.POST['provincia']
            p = Provincia.objects.get(id=provincia)
            nombre_provincia = p.nombre.encode('utf-8').strip()

            if categoria_usuario == 'interrupto':
                response[
                    'Content-Disposition'] = "attachment; filename=Interruptos_por_organismos_(%s)_(%s_%s)_(%s).xlsx" % (
                    str(nombre_organismo).replace(" ", "_"), nombre_mes, nombre_anno, str(nombre_provincia).replace(" ", "_"))
            else:
                response['Content-Disposition'] = "attachment; filename=Interruptos_por_organismos_(%s_%s)_(%s).xlsx" % (
                    nombre_mes, nombre_anno,  str(nombre_provincia).replace(" ", "_"))
        else:

            if categoria_usuario == 'interrupto':
                response[
                    'Content-Disposition'] = "attachment; filename=Interruptos_por_organismos_(%s)_(%s_%s).xlsx" % (
                    str(nombre_organismo).replace(" ", "_"), nombre_mes, nombre_anno)
            else:
                response['Content-Disposition'] = "attachment; filename=Interruptos_por_organismos_(%s_%s).xlsx" % (
                    nombre_mes, nombre_anno)

        book = Workbook(response, {'in_memory': True})
        worksheet_data = book.add_worksheet("Interruptos por Organismos")

        formato1 = book.add_format({'align': 'center',
                                    'valign': 'vcenter',
                                    'bold': True,
                                    'border': 1})
        formato2 = book.add_format({'rotation': 45,
                                    'align': 'center',
                                    'valign': 'vcenter',
                                    'bold': True,
                                    'border': 1,
                                    'text_wrap': True})
        formato3 = book.add_format({'align': 'center',
                                    'bold': True,
                                    'border': 1})
        formato4 = book.add_format({'rotation': 90,
                                    'align': 'center',
                                    'valign': 'vcenter',
                                    'bold': True,
                                    'border': 1,
                                    'text_wrap': True})
        formato5 = book.add_format({'border': 1,
                                    'text_wrap': True})
        formato_organismos = book.add_format({'bold': True,
                                              'border': 1})

        worksheet_data.merge_range('A1:A4', "OACE-OSDE", formato1)
        worksheet_data.merge_range("B1:O1", "Interruptos: %s-%s" % (nombre_mes, nombre_anno), formato3)
        worksheet_data.merge_range("B2:B4", "Total", formato2)
        worksheet_data.merge_range("C2:C4", "Femeninos", formato2)
        worksheet_data.merge_range("D2:D4", "Jovenes", formato2)
        worksheet_data.merge_range("E2:H2", "Tiempo de Interrupcion", formato3)
        worksheet_data.merge_range("I2:O2", "Situacion Actual", formato3)
        worksheet_data.merge_range("E3:E4", "Hasta 30 dias", formato4)
        worksheet_data.merge_range("F3:F4", "Mas de 30 y hasta 60 dias", formato4)
        worksheet_data.merge_range("G3:G4", "Mas de 60 dias y hasta 1 anno", formato4)
        worksheet_data.merge_range("H3:H4", "Mas de 1 anno", formato4)
        worksheet_data.merge_range("I3:K3", "Reubicados Temporales", formato3)
        worksheet_data.write("I4", "En la misma entidad", formato4)
        worksheet_data.write("J4", "En otra entidad del mismo organismo", formato4)
        worksheet_data.write("K4", "En una entidad de otro organismo", formato4)
        worksheet_data.merge_range("L3:L4", "Cobrando Garantia Salarial", formato4)
        worksheet_data.merge_range("M3:M4", "Sin Garantia Salarial", formato4)
        worksheet_data.merge_range("N3:N4", "Bajas", formato4)
        worksheet_data.merge_range("O3:O4", "Propuesto a Disponibles", formato4)

        worksheet_data.set_column("A:A", 20.58)
        worksheet_data.set_row(3, 80)
        if categoria_usuario == 'interrupto':
            if es_oace(organismo):
                osdes = obtener_osdes_de_un_oace(organismo)
                if osdes.__len__() > 0:
                    if request.POST['provincia']:
                        interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                                 organismo__id__in=[osde.id for osde in osdes],
                                                                 municipio__provincia=p
                                                                 ) | \
                                      Interruptos.objects.filter(organismo=organismo)
                    else:
                        interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                                 organismo__id__in=[osde.id for osde in osdes],
                                                                 ) | \
                                      Interruptos.objects.filter(organismo=organismo)
                else:
                    if request.POST['provincia']:
                        interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                                 organismo=organismo,
                                                                 municipio__provincia=p
                                                                 )
                    else:
                        interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                                 organismo=organismo,
                                                                 )
                organismos = Organismo.objects.filter(id=organismo.id)
            else:
                if request.POST['provincia']:
                    interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                             organismo=organismo,
                                                             municipio__provincia=p
                                                             )
                else:
                    interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                             organismo=organismo,
                                                             )
            query = """SELECT id
                            FROM public."SGMGU_interruptos" t where
                                date_part('month',t.fecha_registro)=""" + unicode(mes) + """;"""

            resultado_query_interruptos = Interruptos.objects.raw(query)
            ids_interruptos = [interr.id for interr in resultado_query_interruptos]
            interruptos = interruptos.filter(id__in=ids_interruptos)

        elif categoria_usuario == 'administrador':

            query = """SELECT id
                    FROM public."SGMGU_interruptos" t where
                        date_part('month',t.fecha_registro)=""" + unicode(mes) + """;"""

            resultado_query_interruptos = Interruptos.objects.raw(query)
            ids_interruptos = [interr.id for interr in resultado_query_interruptos]
            if request.POST['provincia']:
                interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                         id__in=ids_interruptos, municipio__provincia=p)
            else:
                interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual, id__in=ids_interruptos)

            organismos = obtener_oaces()

        inicio_fila = 4
        i = 0

        totales = 0
        totales_femeninos = 0
        totales_jovenes = 0
        totales_hasta_treinta_dias = 0
        totales_mas_treinta_menos_sesenta_dias = 0
        totales_mas_sesenta_dias_menos_un_anno = 0
        totales_mas_un_anno = 0
        totales_reubicados_temporal_misma_entidad = 0
        totales_reubicados_temporal_mismo_organismo = 0
        totales_reubicados_temporal_otro_organismo = 0
        totales_cobrando_garantia_salarial = 0
        totales_sin_garantia_salarial = 0
        totales_baja = 0
        totales_propuesto_disponible = 0

        if es_oace(organismo) or categoria_usuario == 'administrador':
            for oace in organismos:

                org = interruptos.filter(organismo=oace)
                dict_totales = totales_por_organismo(org)
                t = dict_totales['t']
                t_femeninos = dict_totales['t_femeninos']
                t_jovenes = dict_totales['t_jovenes']
                t_hasta_treinta_dias = dict_totales['t_hasta_treinta_dias']
                t_mas_treinta_menos_sesenta_dias = dict_totales['t_mas_treinta_menos_sesenta_dias']
                t_mas_sesenta_dias_menos_un_anno = dict_totales['t_mas_sesenta_dias_menos_un_anno']
                t_mas_un_anno = dict_totales['t_mas_un_anno']
                t_reubicados_temporal_misma_entidad = dict_totales['t_reubicados_temporal_misma_entidad']
                t_reubicados_temporal_mismo_organismo = dict_totales['t_reubicados_temporal_mismo_organismo']
                t_reubicados_temporal_otro_organismo = dict_totales['t_reubicados_temporal_otro_organismo']
                t_cobrando_garantia_salarial = dict_totales['t_cobrando_garantia_salarial']
                t_sin_garantia_salarial = dict_totales['t_sin_garantia_salarial']
                t_baja = dict_totales['t_baja']
                t_propuesto_disponible = dict_totales['t_propuesto_disponible']

                worksheet_data.write(inicio_fila + i, 0, oace.siglas, formato_organismos)  # organismo
                worksheet_data.write(inicio_fila + i, 1, t, formato5)  # total
                worksheet_data.write(inicio_fila + i, 2, t_femeninos, formato5)  # totales femeninos
                worksheet_data.write(inicio_fila + i, 3, t_jovenes, formato5)  # totales jóvenes
                worksheet_data.write(inicio_fila + i, 4, t_hasta_treinta_dias, formato5)  # menos de 30 dias
                worksheet_data.write(inicio_fila + i, 5, t_mas_treinta_menos_sesenta_dias, formato5)  # entre 30 y 60 dias
                worksheet_data.write(inicio_fila + i, 6, t_mas_sesenta_dias_menos_un_anno,
                                     formato5)  # entre 60 dias y un año
                worksheet_data.write(inicio_fila + i, 7, t_mas_un_anno, formato5)  # mas de un año
                worksheet_data.write(inicio_fila + i, 8, t_reubicados_temporal_misma_entidad,
                                     formato5)  # reubicado temporal dentro de la misma entidad
                worksheet_data.write(inicio_fila + i, 9, t_reubicados_temporal_mismo_organismo,
                                     formato5)  # reubicado temporal dentro del mismo organismo
                worksheet_data.write(inicio_fila + i, 10, t_reubicados_temporal_otro_organismo,
                                     formato5)  # reubicado temporal dentro de otro organismo
                worksheet_data.write(inicio_fila + i, 11, t_cobrando_garantia_salarial,
                                     formato5)  # cobrando garantia salarial
                worksheet_data.write(inicio_fila + i, 12, t_sin_garantia_salarial, formato5)  # sin garantia salarial
                worksheet_data.write(inicio_fila + i, 13, t_baja, formato5)  # baja
                worksheet_data.write(inicio_fila + i, 14, t_propuesto_disponible, formato5)  # propuesto a disponible

                totales += t
                totales_femeninos += t_femeninos
                totales_jovenes += t_jovenes
                totales_hasta_treinta_dias += t_hasta_treinta_dias
                totales_mas_treinta_menos_sesenta_dias += t_mas_treinta_menos_sesenta_dias
                totales_mas_sesenta_dias_menos_un_anno += t_mas_sesenta_dias_menos_un_anno
                totales_mas_un_anno += t_mas_un_anno
                totales_reubicados_temporal_misma_entidad += t_reubicados_temporal_misma_entidad
                totales_reubicados_temporal_mismo_organismo += t_reubicados_temporal_mismo_organismo
                totales_reubicados_temporal_otro_organismo += t_reubicados_temporal_otro_organismo
                totales_cobrando_garantia_salarial += t_cobrando_garantia_salarial
                totales_sin_garantia_salarial += t_sin_garantia_salarial
                totales_baja += t_baja
                totales_propuesto_disponible += t_propuesto_disponible

                i = i + 1

                for interrupto in interruptos:
                    if interrupto.organismo_id == oace.id:
                        worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad
                        worksheet_data.write(inicio_fila + i, 1, total_interruptos_por_entidad(interrupto),
                                             formato5)  # total
                        worksheet_data.write(inicio_fila + i, 2, total_femeninos_interruptos_por_entidad(interrupto),
                                             formato5)  # totales femeninos
                        worksheet_data.write(inicio_fila + i, 3, total_jovenes_interruptos_por_entidad(interrupto),
                                             formato5)  # totales jóvenes
                        worksheet_data.write(inicio_fila + i, 4, interruptos_hasta_treinta_dias_por_entidad(interrupto),
                                             formato5)  # menos de 30 dias
                        worksheet_data.write(inicio_fila + i, 5,
                                             interruptos_mas_treinta_hasta_sesenta_por_entidad(interrupto),
                                             formato5)  # entre 30 y 60 dias
                        worksheet_data.write(inicio_fila + i, 6,
                                             interruptos_mas_sesenta_menos_un_anno_por_entidad(interrupto),
                                             formato5)  # entre 60 dias y un año
                        worksheet_data.write(inicio_fila + i, 7, interruptos_mas_un_anno_por_entidad(interrupto),
                                             formato5)  # mas de un año
                        worksheet_data.write(inicio_fila + i, 8,
                                             interruptos_reubicado_misma_entidad_por_entidad(interrupto),
                                             formato5)  # reubicado temporal dentro de la misma entidad
                        worksheet_data.write(inicio_fila + i, 9,
                                             interruptos_reubicado_mismo_organismo_por_entidad(interrupto),
                                             formato5)  # reubicado temporal dentro del mismo organismo
                        worksheet_data.write(inicio_fila + i, 10,
                                             interruptos_reubicado_otro_organismo_por_entidad(interrupto),
                                             formato5)  # reubicado temporal dentro de otro organismo
                        worksheet_data.write(inicio_fila + i, 11,
                                             interruptos_cobrando_garantia_salarial_por_entidad(interrupto),
                                             formato5)  # cobrando garantia salarial
                        worksheet_data.write(inicio_fila + i, 12, interruptos_sin_garantia_salarial_por_entidad(interrupto),
                                             formato5)  # sin garantia salarial
                        worksheet_data.write(inicio_fila + i, 13, interruptos_baja_por_entidad(interrupto),
                                             formato5)  # baja
                        worksheet_data.write(inicio_fila + i, 14, interruptos_propuesto_disponible_por_entidad(interrupto),
                                             formato5)  # propuesto a disponible
                        i = i + 1

                osdes = obtener_osdes_de_un_oace(oace)
                if osdes.__len__() > 0:
                    for osde in osdes:

                        org = interruptos.filter(organismo=osde)
                        dict_totales = totales_por_organismo(org)
                        t = dict_totales['t']
                        t_femeninos = dict_totales['t_femeninos']
                        t_jovenes = dict_totales['t_jovenes']
                        t_hasta_treinta_dias = dict_totales['t_hasta_treinta_dias']
                        t_mas_treinta_menos_sesenta_dias = dict_totales['t_mas_treinta_menos_sesenta_dias']
                        t_mas_sesenta_dias_menos_un_anno = dict_totales['t_mas_sesenta_dias_menos_un_anno']
                        t_mas_un_anno = dict_totales['t_mas_un_anno']
                        t_reubicados_temporal_misma_entidad = dict_totales['t_reubicados_temporal_misma_entidad']
                        t_reubicados_temporal_mismo_organismo = dict_totales['t_reubicados_temporal_mismo_organismo']
                        t_reubicados_temporal_otro_organismo = dict_totales['t_reubicados_temporal_otro_organismo']
                        t_cobrando_garantia_salarial = dict_totales['t_cobrando_garantia_salarial']
                        t_sin_garantia_salarial = dict_totales['t_sin_garantia_salarial']
                        t_baja = dict_totales['t_baja']
                        t_propuesto_disponible = dict_totales['t_propuesto_disponible']

                        worksheet_data.write(inicio_fila + i, 0, osde.siglas, formato_organismos)  # osde
                        worksheet_data.write(inicio_fila + i, 1, t, formato5)  # total
                        worksheet_data.write(inicio_fila + i, 2, t_femeninos, formato5)  # totales femeninos
                        worksheet_data.write(inicio_fila + i, 3, t_jovenes, formato5)  # totales jóvenes
                        worksheet_data.write(inicio_fila + i, 4, t_hasta_treinta_dias, formato5)  # menos de 30 dias
                        worksheet_data.write(inicio_fila + i, 5, t_mas_treinta_menos_sesenta_dias,
                                             formato5)  # entre 30 y 60 dias
                        worksheet_data.write(inicio_fila + i, 6, t_mas_sesenta_dias_menos_un_anno,
                                             formato5)  # entre 60 dias y un año
                        worksheet_data.write(inicio_fila + i, 7, t_mas_un_anno, formato5)  # mas de un año
                        worksheet_data.write(inicio_fila + i, 8, t_reubicados_temporal_misma_entidad,
                                             formato5)  # reubicado temporal dentro de la misma entidad
                        worksheet_data.write(inicio_fila + i, 9, t_reubicados_temporal_mismo_organismo,
                                             formato5)  # reubicado temporal dentro del mismo organismo
                        worksheet_data.write(inicio_fila + i, 10, t_reubicados_temporal_otro_organismo,
                                             formato5)  # reubicado temporal dentro de otro organismo
                        worksheet_data.write(inicio_fila + i, 11, t_cobrando_garantia_salarial,
                                             formato5)  # cobrando garantia salarial
                        worksheet_data.write(inicio_fila + i, 12, t_sin_garantia_salarial,
                                             formato5)  # sin garantia salarial
                        worksheet_data.write(inicio_fila + i, 13, t_baja, formato5)  # baja
                        worksheet_data.write(inicio_fila + i, 14, t_propuesto_disponible,
                                             formato5)  # propuesto a disponible

                        totales += t
                        totales_femeninos += t_femeninos
                        totales_jovenes += t_jovenes
                        totales_hasta_treinta_dias += t_hasta_treinta_dias
                        totales_mas_treinta_menos_sesenta_dias += t_mas_treinta_menos_sesenta_dias
                        totales_mas_sesenta_dias_menos_un_anno += t_mas_sesenta_dias_menos_un_anno
                        totales_mas_un_anno += t_mas_un_anno
                        totales_reubicados_temporal_misma_entidad += t_reubicados_temporal_misma_entidad
                        totales_reubicados_temporal_mismo_organismo += t_reubicados_temporal_mismo_organismo
                        totales_reubicados_temporal_otro_organismo += t_reubicados_temporal_otro_organismo
                        totales_cobrando_garantia_salarial += t_cobrando_garantia_salarial
                        totales_sin_garantia_salarial += t_sin_garantia_salarial
                        totales_baja += t_baja
                        totales_propuesto_disponible += t_propuesto_disponible

                        i = i + 1

                        l_interruptos = interruptos.filter(organismo_id=osde)

                        for interrupto in l_interruptos:
                            worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad
                            worksheet_data.write(inicio_fila + i, 1, total_interruptos_por_entidad(interrupto),
                                                 formato5)  # total
                            worksheet_data.write(inicio_fila + i, 2, total_femeninos_interruptos_por_entidad(interrupto),
                                                 formato5)  # totales femeninos
                            worksheet_data.write(inicio_fila + i, 3, total_jovenes_interruptos_por_entidad(interrupto),
                                                 formato5)  # totales jóvenes
                            worksheet_data.write(inicio_fila + i, 4, interruptos_hasta_treinta_dias_por_entidad(interrupto),
                                                 formato5)  # menos de 30 dias
                            worksheet_data.write(inicio_fila + i, 5,
                                                 interruptos_mas_treinta_hasta_sesenta_por_entidad(interrupto),
                                                 formato5)  # entre 30 y 60 dias
                            worksheet_data.write(inicio_fila + i, 6,
                                                 interruptos_mas_sesenta_menos_un_anno_por_entidad(interrupto),
                                                 formato5)  # entre 60 dias y un año
                            worksheet_data.write(inicio_fila + i, 7, interruptos_mas_un_anno_por_entidad(interrupto),
                                                 formato5)  # mas de un año
                            worksheet_data.write(inicio_fila + i, 8,
                                                 interruptos_reubicado_misma_entidad_por_entidad(interrupto),
                                                 formato5)  # reubicado temporal dentro de la misma entidad
                            worksheet_data.write(inicio_fila + i, 9,
                                                 interruptos_reubicado_mismo_organismo_por_entidad(interrupto),
                                                 formato5)  # reubicado temporal dentro del mismo organismo
                            worksheet_data.write(inicio_fila + i, 10,
                                                 interruptos_reubicado_otro_organismo_por_entidad(interrupto),
                                                 formato5)  # reubicado temporal dentro de otro organismo
                            worksheet_data.write(inicio_fila + i, 11,
                                                 interruptos_cobrando_garantia_salarial_por_entidad(interrupto),
                                                 formato5)  # cobrando garantia salarial
                            worksheet_data.write(inicio_fila + i, 12,
                                                 interruptos_sin_garantia_salarial_por_entidad(interrupto),
                                                 formato5)  # sin garantia salarial
                            worksheet_data.write(inicio_fila + i, 13, interruptos_baja_por_entidad(interrupto),
                                                 formato5)  # baja
                            worksheet_data.write(inicio_fila + i, 14,
                                                 interruptos_propuesto_disponible_por_entidad(interrupto),
                                                 formato5)  # propuesto a disponible
                            i = i + 1

        if not es_oace(organismo):

            org = interruptos.filter(organismo=organismo)
            dict_totales = totales_por_organismo(org)
            t = dict_totales['t']
            t_femeninos = dict_totales['t_femeninos']
            t_jovenes = dict_totales['t_jovenes']
            t_hasta_treinta_dias = dict_totales['t_hasta_treinta_dias']
            t_mas_treinta_menos_sesenta_dias = dict_totales['t_mas_treinta_menos_sesenta_dias']
            t_mas_sesenta_dias_menos_un_anno = dict_totales['t_mas_sesenta_dias_menos_un_anno']
            t_mas_un_anno = dict_totales['t_mas_un_anno']
            t_reubicados_temporal_misma_entidad = dict_totales['t_reubicados_temporal_misma_entidad']
            t_reubicados_temporal_mismo_organismo = dict_totales['t_reubicados_temporal_mismo_organismo']
            t_reubicados_temporal_otro_organismo = dict_totales['t_reubicados_temporal_otro_organismo']
            t_cobrando_garantia_salarial = dict_totales['t_cobrando_garantia_salarial']
            t_sin_garantia_salarial = dict_totales['t_sin_garantia_salarial']
            t_baja = dict_totales['t_baja']
            t_propuesto_disponible = dict_totales['t_propuesto_disponible']

            worksheet_data.write(inicio_fila + i, 0, organismo.siglas, formato_organismos)  # organismo
            worksheet_data.write(inicio_fila + i, 1, t, formato5)  # total
            worksheet_data.write(inicio_fila + i, 2, t_femeninos, formato5)  # totales femeninos
            worksheet_data.write(inicio_fila + i, 3, t_jovenes, formato5)  # totales jóvenes
            worksheet_data.write(inicio_fila + i, 4, t_hasta_treinta_dias, formato5)  # menos de 30 dias
            worksheet_data.write(inicio_fila + i, 5, t_mas_treinta_menos_sesenta_dias, formato5)  # entre 30 y 60 dias
            worksheet_data.write(inicio_fila + i, 6, t_mas_sesenta_dias_menos_un_anno, formato5)  # entre 60 dias y un año
            worksheet_data.write(inicio_fila + i, 7, t_mas_un_anno, formato5)  # mas de un año
            worksheet_data.write(inicio_fila + i, 8, t_reubicados_temporal_misma_entidad,
                                 formato5)  # reubicado temporal dentro de la misma entidad
            worksheet_data.write(inicio_fila + i, 9, t_reubicados_temporal_mismo_organismo,
                                 formato5)  # reubicado temporal dentro del mismo organismo
            worksheet_data.write(inicio_fila + i, 10, t_reubicados_temporal_otro_organismo,
                                 formato5)  # reubicado temporal dentro de otro organismo
            worksheet_data.write(inicio_fila + i, 11, t_cobrando_garantia_salarial, formato5)  # cobrando garantia salarial
            worksheet_data.write(inicio_fila + i, 12, t_sin_garantia_salarial, formato5)  # sin garantia salarial
            worksheet_data.write(inicio_fila + i, 13, t_baja, formato5)  # baja
            worksheet_data.write(inicio_fila + i, 14, t_propuesto_disponible, formato5)  # propuesto a disponible

            totales += t
            totales_femeninos += t_femeninos
            totales_jovenes += t_jovenes
            totales_hasta_treinta_dias += t_hasta_treinta_dias
            totales_mas_treinta_menos_sesenta_dias += t_mas_treinta_menos_sesenta_dias
            totales_mas_sesenta_dias_menos_un_anno += t_mas_sesenta_dias_menos_un_anno
            totales_mas_un_anno += t_mas_un_anno
            totales_reubicados_temporal_misma_entidad += t_reubicados_temporal_misma_entidad
            totales_reubicados_temporal_mismo_organismo += t_reubicados_temporal_mismo_organismo
            totales_reubicados_temporal_otro_organismo += t_reubicados_temporal_otro_organismo
            totales_cobrando_garantia_salarial += t_cobrando_garantia_salarial
            totales_sin_garantia_salarial += t_sin_garantia_salarial
            totales_baja += t_baja
            totales_propuesto_disponible += t_propuesto_disponible

            i = i + 1

            for interrupto in interruptos:

                if interrupto.organismo_id == organismo.id:
                    worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad
                    worksheet_data.write(inicio_fila + i, 1, total_interruptos_por_entidad(interrupto), formato5)  # total
                    worksheet_data.write(inicio_fila + i, 2, total_femeninos_interruptos_por_entidad(interrupto),
                                         formato5)  # totales femeninos
                    worksheet_data.write(inicio_fila + i, 3, total_jovenes_interruptos_por_entidad(interrupto),
                                         formato5)  # totales jóvenes
                    worksheet_data.write(inicio_fila + i, 4, interruptos_hasta_treinta_dias_por_entidad(interrupto),
                                         formato5)  # menos de 30 dias
                    worksheet_data.write(inicio_fila + i, 5, interruptos_mas_treinta_hasta_sesenta_por_entidad(interrupto),
                                         formato5)  # entre 30 y 60 dias
                    worksheet_data.write(inicio_fila + i, 6, interruptos_mas_sesenta_menos_un_anno_por_entidad(interrupto),
                                         formato5)  # entre 60 dias y un año
                    worksheet_data.write(inicio_fila + i, 7, interruptos_mas_un_anno_por_entidad(interrupto),
                                         formato5)  # mas de un año
                    worksheet_data.write(inicio_fila + i, 8, interruptos_reubicado_misma_entidad_por_entidad(interrupto),
                                         formato5)  # reubicado temporal dentro de la misma entidad
                    worksheet_data.write(inicio_fila + i, 9, interruptos_reubicado_mismo_organismo_por_entidad(interrupto),
                                         formato5)  # reubicado temporal dentro del mismo organismo
                    worksheet_data.write(inicio_fila + i, 10, interruptos_reubicado_otro_organismo_por_entidad(interrupto),
                                         formato5)  # reubicado temporal dentro de otro organismo
                    worksheet_data.write(inicio_fila + i, 11,
                                         interruptos_cobrando_garantia_salarial_por_entidad(interrupto),
                                         formato5)  # cobrando garantia salarial
                    worksheet_data.write(inicio_fila + i, 12, interruptos_sin_garantia_salarial_por_entidad(interrupto),
                                         formato5)  # sin garantia salarial
                    worksheet_data.write(inicio_fila + i, 13, interruptos_baja_por_entidad(interrupto), formato5)  # baja
                    worksheet_data.write(inicio_fila + i, 14, interruptos_propuesto_disponible_por_entidad(interrupto),
                                         formato5)  # propuesto a disponible
                    i = i + 1

        # TOTALES
        worksheet_data.write(inicio_fila + i, 0, "TOTALES", formato_organismos)
        worksheet_data.write(inicio_fila + i, 1, totales, formato_organismos)
        worksheet_data.write(inicio_fila + i, 2, totales_femeninos, formato_organismos)
        worksheet_data.write(inicio_fila + i, 3, totales_jovenes, formato_organismos)
        worksheet_data.write(inicio_fila + i, 4, totales_hasta_treinta_dias, formato_organismos)
        worksheet_data.write(inicio_fila + i, 5, totales_mas_treinta_menos_sesenta_dias, formato_organismos)
        worksheet_data.write(inicio_fila + i, 6, totales_mas_sesenta_dias_menos_un_anno, formato_organismos)
        worksheet_data.write(inicio_fila + i, 7, totales_mas_un_anno, formato_organismos)
        worksheet_data.write(inicio_fila + i, 8, totales_reubicados_temporal_misma_entidad, formato_organismos)
        worksheet_data.write(inicio_fila + i, 9, totales_reubicados_temporal_mismo_organismo, formato_organismos)
        worksheet_data.write(inicio_fila + i, 10, totales_reubicados_temporal_otro_organismo, formato_organismos)
        worksheet_data.write(inicio_fila + i, 11, totales_cobrando_garantia_salarial, formato_organismos)
        worksheet_data.write(inicio_fila + i, 12, totales_sin_garantia_salarial, formato_organismos)
        worksheet_data.write(inicio_fila + i, 13, totales_baja, formato_organismos)
        worksheet_data.write(inicio_fila + i, 14, totales_propuesto_disponible, formato_organismos)

        book.close()
        return response

    anno_inicio = 2018
    anno_actual = datetime.today().year

    annos = range(anno_inicio, anno_actual + 1)
    provincias = Provincia.objects.all()
    context = {'provincias': provincias, 'titulo': 'Interruptos por organismos.', 'annos': annos}
    return render(request, "Reportes/ReportesInterrupto/filtrar_interruptos.html", context)
