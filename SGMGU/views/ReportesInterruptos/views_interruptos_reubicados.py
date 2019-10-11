# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range

from SGMGU.models import *
from SGMGU.views.utiles import obtener_mes
from SGMGU.views.ReportesInterruptos.metodos_auxiliares import *
from SGMGU.views.utiles import permission_required
from datetime import *


@login_required()
@permission_required(['administrador'])
def interruptos_situacion_duracion(request):
    anno_actual = datetime.today().year
    mes_actual = datetime.today().month
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    organismo = request.user.perfil_usuario.organismo
    nombre_organismo = organismo.nombre.encode('utf-8').strip()
    num_anno = anno_actual

    if mes_actual == 12:
        num_anno = anno_actual - 1

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    if categoria_usuario == 'interrupto' or categoria_usuario == 'interrupto':
        response[
            'Content-Disposition'] = "attachment; filename=Interruptos_reubicados_por_organismos_(%s)_(%s_%s).xlsx" % (
            str(nombre_organismo).replace(" ", "_"), obtener_mes(mes_actual - 1), num_anno)
    else:
        response['Content-Disposition'] = "attachment; filename=Interruptos_reubicados_por_organismos_(%s_%s).xlsx" % (
            obtener_mes(mes_actual - 1), num_anno)

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

    worksheet_data.merge_range('A1:A3', "OACE-OSDE", formato1)
    worksheet_data.merge_range("B1:N1", "Interruptos - Reubicados Temporales: %s-%s" % (obtener_mes(mes_actual - 1), num_anno), formato3)
    worksheet_data.merge_range("B2:B3", "Total", formato2)
    worksheet_data.merge_range("C2:E2", "Hasta 30 dias", formato1)
    worksheet_data.merge_range("F2:H2", "Mas de 30 y hasta 60 dias", formato1)
    worksheet_data.merge_range("I2:K2", "Mas de 60 dias y hasta 1", formato1)
    worksheet_data.merge_range("L2:N2", "Mas de 1", formato1)
    # Hasta 30 dias
    worksheet_data.write("C3", "En la misma entidad", formato4)
    worksheet_data.write("D3", "En otra entidad del mismo organismo", formato4)
    worksheet_data.write("E3", "En una entidad de otro organismo", formato4)
    # Mas de 30 y hasta 60 dias
    worksheet_data.write("F3", "En la misma entidad", formato4)
    worksheet_data.write("G3", "En otra entidad del mismo organismo", formato4)
    worksheet_data.write("H3", "En una entidad de otro organismo", formato4)
    # Mas de 60 dias y hasta 1 anno
    worksheet_data.write("I3", "En la misma entidad", formato4)
    worksheet_data.write("J3", "En otra entidad del mismo organismo", formato4)
    worksheet_data.write("K3", "En una entidad de otro organismo", formato4)
    # Mas de 1 anno
    worksheet_data.write("L3", "En la misma entidad", formato4)
    worksheet_data.write("M3", "En otra entidad del mismo organismo", formato4)
    worksheet_data.write("N3", "En una entidad de otro organismo", formato4)

    worksheet_data.set_column("A:A", 20.58)

    if categoria_usuario == 'interrupto':
        if es_oace(organismo):
            osdes = obtener_osdes_de_un_oace(organismo)
            if osdes.__len__() > 0:
                interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                         organismo__id__in=[osde.id for osde in osdes]
                                                         ).values("hastatreintadias_reubicadostemporal_misma_entidad", "hastatreintadias_reubicadostemporal_mismo_organismo", "hastatreintadias_reubicadostemporal_otro_organismo",
                                                              "entretreintaysesentadias_reubicadostemporal_misma_entidad", "entretreintaysesentadias_reubicadostemporal_mismo_organismo", "entretreintaysesentadias_reubicadostemporal_otro_organismo",
                                                              "masdesesentayunanno_reubicadostemporal_misma_entidad", "masdesesentayunanno_reubicadostemporal_mismo_organismo", "masdesesentayunanno_reubicadostemporal_otro_organismo",
                                                              "masdeunanno_reubicadostemporal_misma_entidad", "masdeunanno_reubicadostemporal_mismo_organismo", "masdeunanno_reubicadostemporal_otro_organismo",
                                                              "total_interruptos_entidad") | \
                              Interruptos.objects.filter(organismo=organismo).values("hastatreintadias_reubicadostemporal_misma_entidad", "hastatreintadias_reubicadostemporal_mismo_organismo", "hastatreintadias_reubicadostemporal_otro_organismo",
                                                              "entretreintaysesentadias_reubicadostemporal_misma_entidad", "entretreintaysesentadias_reubicadostemporal_mismo_organismo", "entretreintaysesentadias_reubicadostemporal_otro_organismo",
                                                              "masdesesentayunanno_reubicadostemporal_misma_entidad", "masdesesentayunanno_reubicadostemporal_mismo_organismo", "masdesesentayunanno_reubicadostemporal_otro_organismo",
                                                              "masdeunanno_reubicadostemporal_misma_entidad", "masdeunanno_reubicadostemporal_mismo_organismo", "masdeunanno_reubicadostemporal_otro_organismo",
                                                              "total_interruptos_entidad")
            else:
                interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                         organismo=organismo
                                                         ).values("hastatreintadias_reubicadostemporal_misma_entidad", "hastatreintadias_reubicadostemporal_mismo_organismo", "hastatreintadias_reubicadostemporal_otro_organismo",
                                                              "entretreintaysesentadias_reubicadostemporal_misma_entidad", "entretreintaysesentadias_reubicadostemporal_mismo_organismo", "entretreintaysesentadias_reubicadostemporal_otro_organismo",
                                                              "masdesesentayunanno_reubicadostemporal_misma_entidad", "masdesesentayunanno_reubicadostemporal_mismo_organismo", "masdesesentayunanno_reubicadostemporal_otro_organismo",
                                                              "masdeunanno_reubicadostemporal_misma_entidad", "masdeunanno_reubicadostemporal_mismo_organismo", "masdeunanno_reubicadostemporal_otro_organismo",
                                                              "total_interruptos_entidad")
            organismos = Organismo.objects.filter(id=organismo.id)
        else:
            interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                     organismo=organismo
                                                     ).values("hastatreintadias_reubicadostemporal_misma_entidad", "hastatreintadias_reubicadostemporal_mismo_organismo", "hastatreintadias_reubicadostemporal_otro_organismo",
                                                              "entretreintaysesentadias_reubicadostemporal_misma_entidad", "entretreintaysesentadias_reubicadostemporal_mismo_organismo", "entretreintaysesentadias_reubicadostemporal_otro_organismo",
                                                              "masdesesentayunanno_reubicadostemporal_misma_entidad", "masdesesentayunanno_reubicadostemporal_mismo_organismo", "masdesesentayunanno_reubicadostemporal_otro_organismo",
                                                              "masdeunanno_reubicadostemporal_misma_entidad", "masdeunanno_reubicadostemporal_mismo_organismo", "masdeunanno_reubicadostemporal_otro_organismo",
                                                              "total_interruptos_entidad")

        query = """SELECT id
                        FROM public."SGMGU_interruptos" t where
                            date_part('month',t.fecha_registro)=""" + unicode(mes_actual) + """;"""

        resultado_query_interruptos = Interruptos.objects.raw(query)
        ids_interruptos = [interr.id for interr in resultado_query_interruptos]
        interruptos = interruptos.filter(id__in=ids_interruptos)

    elif categoria_usuario == 'administrador':


        query = """SELECT id
                FROM public."SGMGU_interruptos" t where
                    date_part('month',t.fecha_registro)=""" + unicode(mes_actual) + """;"""

        resultado_query_interruptos = Interruptos.objects.raw(query)
        ids_interruptos = [interr.id for interr in resultado_query_interruptos]
        interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual, id__in=ids_interruptos).values("hastatreintadias_reubicadostemporal_misma_entidad", "hastatreintadias_reubicadostemporal_mismo_organismo", "hastatreintadias_reubicadostemporal_otro_organismo",
                                                              "entretreintaysesentadias_reubicadostemporal_misma_entidad", "entretreintaysesentadias_reubicadostemporal_mismo_organismo", "entretreintaysesentadias_reubicadostemporal_otro_organismo",
                                                              "masdesesentayunanno_reubicadostemporal_misma_entidad", "masdesesentayunanno_reubicadostemporal_mismo_organismo", "masdesesentayunanno_reubicadostemporal_otro_organismo",
                                                              "masdeunanno_reubicadostemporal_misma_entidad", "masdeunanno_reubicadostemporal_mismo_organismo", "masdeunanno_reubicadostemporal_otro_organismo",
                                                              "total_interruptos_entidad", "organismo_id", "entidad__e_nombre")

        organismos = obtener_oaces()

    inicio_fila = 3
    i = 0

    totales = 0
    totales_hasta_treinta_dias_misma_entidad = 0
    totales_hasta_treinta_dias_mismo_organismo = 0
    totales_hasta_treinta_dias_otro_organismo = 0
    totales_mas_treinta_misma_entidad = 0
    totales_mas_treinta_mismo_organismo = 0
    totales_mas_treinta_otro_organismo = 0
    totales_mas_sesenta_misma_entidad = 0
    totales_mas_sesenta_mismo_organismo = 0
    totales_mas_sesenta_otro_organismo = 0
    totales_mas_un_anno_misma_entidad = 0
    totales_mas_un_anno_mismo_organismo = 0
    totales_mas_un_anno_otro_organismo = 0

    if es_oace(organismo) or categoria_usuario == 'administrador':

        for oace in organismos:

            INTERRUPTOS_ORGANISMOS = interruptos.filter(organismo=oace)
            dict_totales = totales_situacion_tiempo(INTERRUPTOS_ORGANISMOS)
            t_total = dict_totales['total']
            t_hasta_treinta_dias_misma_entidad = dict_totales['hasta_treinta_dias_misma_entidad']
            t_hasta_treinta_dias_mismo_organismo = dict_totales['hasta_treinta_dias_mismo_organismo']
            t_hasta_treinta_dias_otro_organismo = dict_totales['hasta_treinta_dias_otro_organismo']
            t_mas_treinta_misma_entidad = dict_totales['mas_treinta_misma_entidad']
            t_mas_treinta_mismo_organismo = dict_totales['mas_treinta_mismo_organismo']
            t_mas_treinta_otro_organismo = dict_totales['mas_treinta_otro_organismo']
            t_mas_sesenta_misma_entidad = dict_totales['mas_sesenta_misma_entidad']
            t_mas_sesenta_mismo_organismo = dict_totales['mas_sesenta_mismo_organismo']
            t_mas_sesenta_otro_organismo = dict_totales['mas_sesenta_otro_organismo']
            t_mas_un_anno_misma_entidad = dict_totales['mas_un_anno_misma_entidad']
            t_mas_un_anno_mismo_organismo = dict_totales['mas_un_anno_mismo_organismo']
            t_mas_un_anno_otro_organismo = dict_totales['mas_un_anno_otro_organismo']

            worksheet_data.write(inicio_fila + i, 0, oace.siglas, formato_organismos)  # organismo

            total = '=SUM(%s)' % xl_range(inicio_fila + i, 2, inicio_fila + i, 13)
            # worksheet_data.write(INICIO, cantidad_provincias + 1, total_tpcp, formato)
            worksheet_data.write(inicio_fila + i, 1, total, formato5)  # total
            worksheet_data.write(inicio_fila + i, 2, t_hasta_treinta_dias_misma_entidad, formato5)  # hasta_treinta_dias_misma_entidad
            worksheet_data.write(inicio_fila + i, 3, t_hasta_treinta_dias_mismo_organismo, formato5)  # hasta_treinta_dias_mismo_organismo
            worksheet_data.write(inicio_fila + i, 4, t_hasta_treinta_dias_otro_organismo, formato5)  # hasta_treinta_dias_otro_organismo
            worksheet_data.write(inicio_fila + i, 5, t_mas_treinta_misma_entidad, formato5)  # mas_treinta_misma_entidad
            worksheet_data.write(inicio_fila + i, 6, t_mas_treinta_mismo_organismo, formato5)  # mas_treinta_mismo_organismo
            worksheet_data.write(inicio_fila + i, 7, t_mas_treinta_otro_organismo, formato5)  # mas_treinta_otro_organismo
            worksheet_data.write(inicio_fila + i, 8, t_mas_sesenta_misma_entidad, formato5)  # mas_sesenta_misma_entidad
            worksheet_data.write(inicio_fila + i, 9, t_mas_sesenta_mismo_organismo, formato5)  # mas_sesenta_mismo_organismo
            worksheet_data.write(inicio_fila + i, 10, t_mas_sesenta_otro_organismo, formato5)  # mas_sesenta_otro_organismo
            worksheet_data.write(inicio_fila + i, 11, t_mas_un_anno_misma_entidad, formato5)  # mas_un_anno_misma_entidad
            worksheet_data.write(inicio_fila + i, 12, t_mas_un_anno_mismo_organismo, formato5)  # mas_un_anno_mismo_organismo
            worksheet_data.write(inicio_fila + i, 13, t_mas_un_anno_otro_organismo, formato5)  # mas_un_anno_otro_organismo

            totales += t_total
            totales_hasta_treinta_dias_misma_entidad += t_hasta_treinta_dias_misma_entidad
            totales_hasta_treinta_dias_mismo_organismo += t_hasta_treinta_dias_mismo_organismo
            totales_hasta_treinta_dias_otro_organismo += t_hasta_treinta_dias_otro_organismo
            totales_mas_treinta_misma_entidad += t_mas_treinta_misma_entidad
            totales_mas_treinta_mismo_organismo += t_mas_treinta_mismo_organismo
            totales_mas_treinta_otro_organismo += t_mas_treinta_otro_organismo
            totales_mas_sesenta_misma_entidad += t_mas_sesenta_misma_entidad
            totales_mas_sesenta_mismo_organismo += t_mas_sesenta_mismo_organismo
            totales_mas_sesenta_otro_organismo += t_mas_sesenta_otro_organismo
            totales_mas_un_anno_misma_entidad += t_mas_un_anno_misma_entidad
            totales_mas_un_anno_mismo_organismo += t_mas_un_anno_mismo_organismo
            totales_mas_un_anno_otro_organismo += t_mas_un_anno_otro_organismo

            i = i + 1

            L_INTERRUPTOS = interruptos.filter(organismo=oace)
            for interrupto in L_INTERRUPTOS:
                # if interrupto['organismo_id'] == oace.id:
                worksheet_data.write(inicio_fila + i, 0, interrupto['entidad__e_nombre'], formato5)  # entidad
                total = '=SUM(%s)' % xl_range(inicio_fila + i, 2, inicio_fila + i, 13)
                worksheet_data.write(inicio_fila + i, 1, total, formato5)  # total
                worksheet_data.write(inicio_fila + i, 2, interrupto['hastatreintadias_reubicadostemporal_misma_entidad'], formato5)  # hasta_treinta_dias_misma_entidad
                worksheet_data.write(inicio_fila + i, 3, interrupto['hastatreintadias_reubicadostemporal_mismo_organismo'], formato5)  # hasta_treinta_dias_mismo_organismo
                worksheet_data.write(inicio_fila + i, 4, interrupto['hastatreintadias_reubicadostemporal_otro_organismo'], formato5)  # hasta_treinta_dias_otro_organismo
                worksheet_data.write(inicio_fila + i, 5, interrupto['entretreintaysesentadias_reubicadostemporal_misma_entidad'], formato5)  # mas_treinta_misma_entidad
                worksheet_data.write(inicio_fila + i, 6, interrupto['entretreintaysesentadias_reubicadostemporal_mismo_organismo'], formato5)  # mas_treinta_mismo_organismo
                worksheet_data.write(inicio_fila + i, 7, interrupto['entretreintaysesentadias_reubicadostemporal_otro_organismo'], formato5)  # mas_treinta_otro_organismo
                worksheet_data.write(inicio_fila + i, 8, interrupto['masdesesentayunanno_reubicadostemporal_misma_entidad'], formato5)  # mas_sesenta_misma_entidad
                worksheet_data.write(inicio_fila + i, 9, interrupto['masdesesentayunanno_reubicadostemporal_mismo_organismo'], formato5)  # mas_sesenta_mismo_organismo
                worksheet_data.write(inicio_fila + i, 10, interrupto['masdesesentayunanno_reubicadostemporal_otro_organismo'], formato5)  # mas_sesenta_otro_organismo
                worksheet_data.write(inicio_fila + i, 11, interrupto['masdeunanno_reubicadostemporal_misma_entidad'], formato5)  # mas_un_anno_misma_entidad
                worksheet_data.write(inicio_fila + i, 12, interrupto['masdeunanno_reubicadostemporal_mismo_organismo'], formato5)  # mas_un_anno_mismo_organismo
                worksheet_data.write(inicio_fila + i, 13, interrupto['masdeunanno_reubicadostemporal_otro_organismo'], formato5)  # mas_un_anno_otro_organismo

                i = i + 1

            osdes = obtener_osdes_de_un_oace(oace)
            if osdes.__len__() > 0:
                for osde in osdes:

                    INTERRUPTOS_ORGANISMOS = interruptos.filter(organismo=osde)
                    dict_totales = totales_situacion_tiempo(INTERRUPTOS_ORGANISMOS)
                    t_total = dict_totales['total']
                    t_hasta_treinta_dias_misma_entidad = dict_totales['hasta_treinta_dias_misma_entidad']
                    t_hasta_treinta_dias_mismo_organismo = dict_totales['hasta_treinta_dias_mismo_organismo']
                    t_hasta_treinta_dias_otro_organismo = dict_totales['hasta_treinta_dias_otro_organismo']
                    t_mas_treinta_misma_entidad = dict_totales['mas_treinta_misma_entidad']
                    t_mas_treinta_mismo_organismo = dict_totales['mas_treinta_mismo_organismo']
                    t_mas_treinta_otro_organismo = dict_totales['mas_treinta_otro_organismo']
                    t_mas_sesenta_misma_entidad = dict_totales['mas_sesenta_misma_entidad']
                    t_mas_sesenta_mismo_organismo = dict_totales['mas_sesenta_mismo_organismo']
                    t_mas_sesenta_otro_organismo = dict_totales['mas_sesenta_otro_organismo']
                    t_mas_un_anno_misma_entidad = dict_totales['mas_un_anno_misma_entidad']
                    t_mas_un_anno_mismo_organismo = dict_totales['mas_un_anno_mismo_organismo']
                    t_mas_un_anno_otro_organismo = dict_totales['mas_un_anno_otro_organismo']

                    worksheet_data.write(inicio_fila + i, 0, osde.siglas, formato_organismos)  # osde
                    total = '=SUM(%s)' % xl_range(inicio_fila + i, 2, inicio_fila + i, 13)
                    worksheet_data.write(inicio_fila + i, 1, total, formato5)  # total
                    worksheet_data.write(inicio_fila + i, 2, t_hasta_treinta_dias_misma_entidad, formato5)  # hasta_treinta_dias_misma_entidad
                    worksheet_data.write(inicio_fila + i, 3, t_hasta_treinta_dias_mismo_organismo, formato5)  # hasta_treinta_dias_mismo_organismo
                    worksheet_data.write(inicio_fila + i, 4, t_hasta_treinta_dias_otro_organismo, formato5)  # hasta_treinta_dias_otro_organismo
                    worksheet_data.write(inicio_fila + i, 5, t_mas_treinta_misma_entidad, formato5)  # mas_treinta_misma_entidad
                    worksheet_data.write(inicio_fila + i, 6, t_mas_treinta_mismo_organismo, formato5)  # mas_treinta_mismo_organismo
                    worksheet_data.write(inicio_fila + i, 7, t_mas_treinta_otro_organismo, formato5)  # mas_treinta_otro_organismo
                    worksheet_data.write(inicio_fila + i, 8, t_mas_sesenta_misma_entidad, formato5)  # mas_sesenta_misma_entidad
                    worksheet_data.write(inicio_fila + i, 9, t_mas_sesenta_mismo_organismo, formato5)  # mas_sesenta_mismo_organismo
                    worksheet_data.write(inicio_fila + i, 10, t_mas_sesenta_otro_organismo, formato5)  # mas_sesenta_otro_organismo
                    worksheet_data.write(inicio_fila + i, 11, t_mas_un_anno_misma_entidad, formato5)  # mas_un_anno_misma_entidad
                    worksheet_data.write(inicio_fila + i, 12, t_mas_un_anno_mismo_organismo, formato5)  # mas_un_anno_mismo_organismo
                    worksheet_data.write(inicio_fila + i, 13, t_mas_un_anno_otro_organismo, formato5)  # mas_un_anno_otro_organismo

                    totales += t_total
                    totales_hasta_treinta_dias_misma_entidad += t_hasta_treinta_dias_misma_entidad
                    totales_hasta_treinta_dias_mismo_organismo += t_hasta_treinta_dias_mismo_organismo
                    totales_hasta_treinta_dias_otro_organismo += t_hasta_treinta_dias_otro_organismo
                    totales_mas_treinta_misma_entidad += t_mas_treinta_misma_entidad
                    totales_mas_treinta_mismo_organismo += t_mas_treinta_mismo_organismo
                    totales_mas_treinta_otro_organismo += t_mas_treinta_otro_organismo
                    totales_mas_sesenta_misma_entidad += t_mas_sesenta_misma_entidad
                    totales_mas_sesenta_mismo_organismo += t_mas_sesenta_mismo_organismo
                    totales_mas_sesenta_otro_organismo += t_mas_sesenta_otro_organismo
                    totales_mas_un_anno_misma_entidad += t_mas_un_anno_misma_entidad
                    totales_mas_un_anno_mismo_organismo += t_mas_un_anno_mismo_organismo
                    totales_mas_un_anno_otro_organismo += t_mas_un_anno_otro_organismo

                    i = i + 1

                    L_INTERRUPTOS = interruptos.filter(organismo_id=osde)

                    for interrupto in L_INTERRUPTOS:
                        worksheet_data.write(inicio_fila + i, 0, interrupto['entidad__e_nombre'], formato5)  # entidad
                        total = '=SUM(%s)' % xl_range(inicio_fila + i, 2, inicio_fila + i, 13)
                        worksheet_data.write(inicio_fila + i, 1, total, formato5)  # total
                        worksheet_data.write(inicio_fila + i, 2, interrupto['hastatreintadias_reubicadostemporal_misma_entidad'], formato5)  # hasta_treinta_dias_misma_entidad
                        worksheet_data.write(inicio_fila + i, 3, interrupto['hastatreintadias_reubicadostemporal_mismo_organismo'], formato5)  # hasta_treinta_dias_mismo_organismo
                        worksheet_data.write(inicio_fila + i, 4, interrupto['hastatreintadias_reubicadostemporal_otro_organismo'], formato5)  # hasta_treinta_dias_otro_organismo
                        worksheet_data.write(inicio_fila + i, 5, interrupto['entretreintaysesentadias_reubicadostemporal_misma_entidad'], formato5)  # mas_treinta_misma_entidad
                        worksheet_data.write(inicio_fila + i, 6, interrupto['entretreintaysesentadias_reubicadostemporal_mismo_organismo'], formato5)  # mas_treinta_mismo_organismo
                        worksheet_data.write(inicio_fila + i, 7, interrupto['entretreintaysesentadias_reubicadostemporal_otro_organismo'], formato5)  # mas_treinta_otro_organismo
                        worksheet_data.write(inicio_fila + i, 8, interrupto['masdesesentayunanno_reubicadostemporal_misma_entidad'], formato5)  # mas_sesenta_misma_entidad
                        worksheet_data.write(inicio_fila + i, 9, interrupto['masdesesentayunanno_reubicadostemporal_mismo_organismo'], formato5)  # mas_sesenta_mismo_organismo
                        worksheet_data.write(inicio_fila + i, 10, interrupto['masdesesentayunanno_reubicadostemporal_otro_organismo'], formato5)  # mas_sesenta_otro_organismo
                        worksheet_data.write(inicio_fila + i, 11, interrupto['masdeunanno_reubicadostemporal_misma_entidad'], formato5)  # mas_un_anno_misma_entidad
                        worksheet_data.write(inicio_fila + i, 12, interrupto['masdeunanno_reubicadostemporal_mismo_organismo'], formato5)  # mas_un_anno_mismo_organismo
                        worksheet_data.write(inicio_fila + i, 13, interrupto['masdeunanno_reubicadostemporal_otro_organismo'], formato5)  # mas_un_anno_otro_organismo

                        i = i + 1

    # if not es_oace(organismo):
    #
    #     org = interruptos.filter(organismo=organismo)
    #     dict_totales = totales_por_organismo(org)
    #     t = dict_totales['t']
    #     t_femeninos = dict_totales['t_femeninos']
    #     t_jovenes = dict_totales['t_jovenes']
    #     t_hasta_treinta_dias = dict_totales['t_hasta_treinta_dias']
    #     t_mas_treinta_menos_sesenta_dias = dict_totales['t_mas_treinta_menos_sesenta_dias']
    #     t_mas_sesenta_dias_menos_un_anno = dict_totales['t_mas_sesenta_dias_menos_un_anno']
    #     t_mas_un_anno = dict_totales['t_mas_un_anno']
    #     t_reubicados_temporal_misma_entidad = dict_totales['t_reubicados_temporal_misma_entidad']
    #     t_reubicados_temporal_mismo_organismo = dict_totales['t_reubicados_temporal_mismo_organismo']
    #     t_reubicados_temporal_otro_organismo = dict_totales['t_reubicados_temporal_otro_organismo']
    #     t_cobrando_garantia_salarial = dict_totales['t_cobrando_garantia_salarial']
    #     t_sin_garantia_salarial = dict_totales['t_sin_garantia_salarial']
    #     t_baja = dict_totales['t_baja']
    #     t_propuesto_disponible = dict_totales['t_propuesto_disponible']
    #
    #     worksheet_data.write(inicio_fila + i, 0, organismo.siglas, formato_organismos)  # organismo
    #     worksheet_data.write(inicio_fila + i, 1, t, formato5)  # total
    #     worksheet_data.write(inicio_fila + i, 2, t_femeninos, formato5)  # totales femeninos
    #     worksheet_data.write(inicio_fila + i, 3, t_jovenes, formato5)  # totales jóvenes
    #     worksheet_data.write(inicio_fila + i, 4, t_hasta_treinta_dias, formato5)  # menos de 30 dias
    #     worksheet_data.write(inicio_fila + i, 5, t_mas_treinta_menos_sesenta_dias, formato5)  # entre 30 y 60 dias
    #     worksheet_data.write(inicio_fila + i, 6, t_mas_sesenta_dias_menos_un_anno, formato5)  # entre 60 dias y un año
    #     worksheet_data.write(inicio_fila + i, 7, t_mas_un_anno, formato5)  # mas de un año
    #     worksheet_data.write(inicio_fila + i, 8, t_reubicados_temporal_misma_entidad,
    #                          formato5)  # reubicado temporal dentro de la misma entidad
    #     worksheet_data.write(inicio_fila + i, 9, t_reubicados_temporal_mismo_organismo,
    #                          formato5)  # reubicado temporal dentro del mismo organismo
    #     worksheet_data.write(inicio_fila + i, 10, t_reubicados_temporal_otro_organismo,
    #                          formato5)  # reubicado temporal dentro de otro organismo
    #     worksheet_data.write(inicio_fila + i, 11, t_cobrando_garantia_salarial, formato5)  # cobrando garantia salarial
    #     worksheet_data.write(inicio_fila + i, 12, t_sin_garantia_salarial, formato5)  # sin garantia salarial
    #     worksheet_data.write(inicio_fila + i, 13, t_baja, formato5)  # baja
    #     worksheet_data.write(inicio_fila + i, 14, t_propuesto_disponible, formato5)  # propuesto a disponible
    #
    #     totales += t
    #     totales_hasta_treinta_dias += t_hasta_treinta_dias
    #     totales_mas_treinta_menos_sesenta_dias += t_mas_treinta_menos_sesenta_dias
    #     totales_mas_sesenta_dias_menos_un_anno += t_mas_sesenta_dias_menos_un_anno
    #     totales_mas_un_anno += t_mas_un_anno
    #     totales_reubicados_temporal_misma_entidad += t_reubicados_temporal_misma_entidad
    #     totales_reubicados_temporal_mismo_organismo += t_reubicados_temporal_mismo_organismo
    #     totales_reubicados_temporal_otro_organismo += t_reubicados_temporal_otro_organismo
    #     totales_cobrando_garantia_salarial += t_cobrando_garantia_salarial
    #     totales_sin_garantia_salarial += t_sin_garantia_salarial
    #     totales_baja += t_baja
    #     totales_propuesto_disponible += t_propuesto_disponible
    #
    #     i = i + 1
    #
    #     for interrupto in interruptos:
    #         if interrupto.organismo_id == organismo.id:
    #             worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad
    #             worksheet_data.write(inicio_fila + i, 1, total_interruptos_por_entidad(interrupto), formato5)  # total
    #             worksheet_data.write(inicio_fila + i, 2, total_femeninos_interruptos_por_entidad(interrupto),
    #                                  formato5)  # totales femeninos
    #             worksheet_data.write(inicio_fila + i, 3, total_jovenes_interruptos_por_entidad(interrupto),
    #                                  formato5)  # totales jóvenes
    #             worksheet_data.write(inicio_fila + i, 4, interruptos_hasta_treinta_dias_por_entidad(interrupto),
    #                                  formato5)  # menos de 30 dias
    #             worksheet_data.write(inicio_fila + i, 5, interruptos_mas_treinta_hasta_sesenta_por_entidad(interrupto),
    #                                  formato5)  # entre 30 y 60 dias
    #             worksheet_data.write(inicio_fila + i, 6, interruptos_mas_sesenta_menos_un_anno_por_entidad(interrupto),
    #                                  formato5)  # entre 60 dias y un año
    #             worksheet_data.write(inicio_fila + i, 7, interruptos_mas_un_anno_por_entidad(interrupto),
    #                                  formato5)  # mas de un año
    #             worksheet_data.write(inicio_fila + i, 8, interruptos_reubicado_misma_entidad_por_entidad(interrupto),
    #                                  formato5)  # reubicado temporal dentro de la misma entidad
    #             worksheet_data.write(inicio_fila + i, 9, interruptos_reubicado_mismo_organismo_por_entidad(interrupto),
    #                                  formato5)  # reubicado temporal dentro del mismo organismo
    #             worksheet_data.write(inicio_fila + i, 10, interruptos_reubicado_otro_organismo_por_entidad(interrupto),
    #                                  formato5)  # reubicado temporal dentro de otro organismo
    #             worksheet_data.write(inicio_fila + i, 11,
    #                                  interruptos_cobrando_garantia_salarial_por_entidad(interrupto),
    #                                  formato5)  # cobrando garantia salarial
    #             worksheet_data.write(inicio_fila + i, 12, interruptos_sin_garantia_salarial_por_entidad(interrupto),
    #                                  formato5)  # sin garantia salarial
    #             worksheet_data.write(inicio_fila + i, 13, interruptos_baja_por_entidad(interrupto), formato5)  # baja
    #             worksheet_data.write(inicio_fila + i, 14, interruptos_propuesto_disponible_por_entidad(interrupto),
    #                                  formato5)  # propuesto a disponible
    #             i = i + 1

    # SUMAS
    # totales           = '=SUM(%s)' % xl_range(inicio_fila, 1, inicio_fila + i - 1, 1)
    # totales_femeninos = '=SUM(%s)' % xl_range(inicio_fila, 2, inicio_fila + i - 1, 2)
    # totales_jovenes = '=SUM(%s)' % xl_range(inicio_fila, 3, inicio_fila + i - 1, 3)
    # totales_hasta_treinta_dias = '=SUM(%s)' % xl_range(inicio_fila, 4, inicio_fila + i - 1, 4)
    # totales_mas_treinta_menos_sesenta_dias = '=SUM(%s)' % xl_range(inicio_fila, 5, inicio_fila + i - 1, 5)
    # totales_mas_sesenta_dias_menos_un_anno = '=SUM(%s)' % xl_range(inicio_fila, 6, inicio_fila + i - 1, 6)
    # totales_mas_un_anno = '=SUM(%s)' % xl_range(inicio_fila, 7, inicio_fila + i - 1, 7)
    # totales_reubicados_temporal_misma_entidad = '=SUM(%s)' % xl_range(inicio_fila, 8, inicio_fila + i - 1, 8)
    # totales_reubicados_temporal_mismo_organismo = '=SUM(%s)' % xl_range(inicio_fila, 9, inicio_fila + i - 1, 9)
    # totales_reubicados_temporal_otro_organismo = '=SUM(%s)' % xl_range(inicio_fila, 10, inicio_fila + i - 1, 10)
    # totales_cobrando_garantia_salarial = '=SUM(%s)' % xl_range(inicio_fila, 11, inicio_fila + i - 1, 11)
    # totales_sin_garantia_salarial = '=SUM(%s)' % xl_range(inicio_fila, 12, inicio_fila + i - 1, 12)
    # totales_baja = '=SUM(%s)' % xl_range(inicio_fila, 13, inicio_fila + i - 1, 13)
    # totales_propuesto_disponible = '=SUM(%s)' % xl_range(inicio_fila, 14, inicio_fila + i - 1, 14)

    # TOTALES
    worksheet_data.write(inicio_fila + i, 0, "TOTALES", formato_organismos)
    worksheet_data.write(inicio_fila + i, 1, totales, formato_organismos)
    worksheet_data.write(inicio_fila + i, 2, totales_hasta_treinta_dias_misma_entidad, formato_organismos)
    worksheet_data.write(inicio_fila + i, 3, totales_hasta_treinta_dias_mismo_organismo, formato_organismos)
    worksheet_data.write(inicio_fila + i, 4, totales_hasta_treinta_dias_otro_organismo, formato_organismos)
    worksheet_data.write(inicio_fila + i, 5, totales_mas_treinta_misma_entidad, formato_organismos)
    worksheet_data.write(inicio_fila + i, 6, totales_mas_treinta_mismo_organismo, formato_organismos)
    worksheet_data.write(inicio_fila + i, 7, totales_mas_treinta_otro_organismo, formato_organismos)
    worksheet_data.write(inicio_fila + i, 8, totales_mas_sesenta_misma_entidad, formato_organismos)
    worksheet_data.write(inicio_fila + i, 9, totales_mas_sesenta_mismo_organismo, formato_organismos)
    worksheet_data.write(inicio_fila + i, 10, totales_mas_sesenta_otro_organismo, formato_organismos)
    worksheet_data.write(inicio_fila + i, 11, totales_mas_un_anno_misma_entidad, formato_organismos)
    worksheet_data.write(inicio_fila + i, 12, totales_mas_un_anno_mismo_organismo, formato_organismos)
    worksheet_data.write(inicio_fila + i, 13, totales_mas_un_anno_otro_organismo, formato_organismos)

    book.close()
    return response
