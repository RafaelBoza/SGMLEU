# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from SGMGU.models import *
from SGMGU.views.utiles import obtener_mes
from SGMGU.views.ReportesInterruptos.metodos_auxiliares import *
from SGMGU.views.utiles import permission_required
from datetime import *


@login_required()
@permission_required(['administrador', 'interrupto'])
def interruptos_por_causas_interrupcion(request):
    anno_actual = datetime.today().year
    mes_actual = datetime.today().month
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    organismo = request.user.perfil_usuario.organismo
    nombre_organismo = organismo.nombre.encode('utf-8').strip()
    num_anno = anno_actual

    if mes_actual == 12:
        num_anno = anno_actual - 1

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if categoria_usuario == 'interrupto':
        response[
            'Content-Disposition'] = "attachment; filename=Interruptos_por_causas_de_interrupcion(%s)_(%s_%s).xlsx" % (
            str(nombre_organismo).replace(" ", "_"), obtener_mes(mes_actual - 1), num_anno)
    else:
        response['Content-Disposition'] = "attachment; filename=Interruptos_por_causas_de_interrupcion(%s_%s).xlsx" % (
            obtener_mes(mes_actual - 1), num_anno)

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Interruptos por Provincias")

    formato = book.add_format({'bold': True,
                               'border': 1})
    formato1 = book.add_format({'align': 'center',
                                'valign': 'vcenter',
                                'bold': True,
                                'border': 1})
    formato5 = book.add_format({'border': 1,
                                'text_wrap': True})
    formato_organismos = book.add_format({'bold': True,
                                          'border': 1})

    worksheet_data.write("A1", "OACE-OSDE / Causas", formato1)
    worksheet_data.set_column("A:A", 25)

    causas_interrupcion = CausalInterrupcion.objects.filter(activo=True)
    posicion_total_derecho = causas_interrupcion.count() + 1
    totales = 0
    lista_totales = []

    for indice, causa in enumerate(causas_interrupcion):
        lista_totales.insert(indice, totales)
        worksheet_data.write(0, indice + 1, causa.causa, formato)

    worksheet_data.write(0, posicion_total_derecho, "Totales", formato)

    if categoria_usuario == 'interrupto':
        if es_oace(organismo):
            osdes = obtener_osdes_de_un_oace(organismo)
            if osdes.__len__() > 0:
                interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                         organismo__id__in=[osde.id for osde in osdes]
                                                         ) | \
                    Interruptos.objects.filter(organismo=organismo)
            else:
                interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                         organismo=organismo
                                                         )
            organismos = Organismo.objects.filter(id=organismo.id)
        else:
            interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                     organismo=organismo
                                                     )
        query = """SELECT id
                        FROM public."SGMGU_interruptos" t where
                            date_part('month',t.fecha_registro)=""" + unicode(mes_actual) + """ AND
                            date_part('year',t.fecha_registro)=""" + unicode(anno_actual) + """;"""

        resultado_query_interruptos = Interruptos.objects.raw(query)
        ids_interruptos = [interr.id for interr in resultado_query_interruptos]
        interruptos = Interruptos.objects.filter(id__in=ids_interruptos)

    elif categoria_usuario == 'administrador':
        query = """SELECT id
                FROM public."SGMGU_interruptos" t where
                    date_part('month',t.fecha_registro)=""" + unicode(mes_actual) + """ AND
                    date_part('year',t.fecha_registro)=""" + unicode(anno_actual) + """;"""

        resultado_query_interruptos = Interruptos.objects.raw(query)
        ids_interruptos = [interr.id for interr in resultado_query_interruptos]
        interruptos = Interruptos.objects.filter(id__in=ids_interruptos)
        organismos = obtener_oaces()

    inicio_fila = 1
    i = 0

    if es_oace(organismo) or categoria_usuario == 'administrador':

        for oace in organismos:

            worksheet_data.write(inicio_fila + i, 0, oace.siglas, formato_organismos)  # organismo

            totales_a = 0

            for indice, causa in enumerate(causas_interrupcion):

                worksheet_data.write(inicio_fila + i, indice + 1, totales_interruptos_organismo_causas_interrupcion(interruptos, oace, causa.id), formato_organismos)
                lista_totales[indice] = lista_totales[indice] + totales_interruptos_organismo_causas_interrupcion(interruptos, oace, causa.id)
                totales_a = totales_a + totales_interruptos_organismo_causas_interrupcion(interruptos, oace, causa.id)

                worksheet_data.write(inicio_fila + i, posicion_total_derecho, totales_a, formato)

            i = i + 1

            l_interruptos = interruptos.filter(organismo__id=oace.id)
            for interrupto in l_interruptos:

                worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad

                totales_a = 0

                for indice, causa in enumerate(causas_interrupcion):
                    worksheet_data.write(inicio_fila + i, indice + 1, totales_interruptos_causas_interrupcion(interrupto, causa.id), formato5)
                    totales_a = totales_a + totales_interruptos_causas_interrupcion(interrupto, causa.id)

                    worksheet_data.write(inicio_fila + i, posicion_total_derecho, totales_a, formato)

                i = i + 1

            osdes = obtener_osdes_de_un_oace(oace)

            if obtener_osdes_de_un_oace(oace).__len__() > 0:
                for osde in osdes:

                    worksheet_data.write(inicio_fila + i, 0, osde.siglas, formato_organismos)  # osde

                    totales_a = 0

                    for indice, causa in enumerate(causas_interrupcion):

                        worksheet_data.write(inicio_fila + i, indice + 1, totales_interruptos_organismo_causas_interrupcion(interruptos, osde, causa.id), formato_organismos)
                        lista_totales[indice] = lista_totales[indice] + totales_interruptos_organismo_causas_interrupcion(interruptos, osde, causa.id)
                        totales_a = totales_a + totales_interruptos_organismo_causas_interrupcion(interruptos, osde, causa.id)

                        worksheet_data.write(inicio_fila + i, posicion_total_derecho, totales_a, formato)

                    i = i + 1

                    l_interruptos = interruptos.filter(organismo_id=osde.id)

                    for interrupto in l_interruptos:

                        worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad

                        totales_a = 0

                        for indice, causa in enumerate(causas_interrupcion):

                            worksheet_data.write(inicio_fila + i, indice + 1, totales_interruptos_causas_interrupcion(interrupto, causa.id), formato5)
                            totales_a = totales_a + totales_interruptos_causas_interrupcion(interrupto, causa.id)

                            worksheet_data.write(inicio_fila + i, posicion_total_derecho, totales_a, formato)

                        i = i + 1

    if not es_oace(organismo):

        worksheet_data.write(inicio_fila + i, 0, organismo.siglas, formato_organismos)  # organismo

        totales_a = 0

        for indice, causa in enumerate(causas_interrupcion):
            worksheet_data.write(inicio_fila + i, indice + 1, totales_interruptos_organismo_causas_interrupcion(interruptos, organismo, causa.id), formato_organismos)
            lista_totales[indice] = lista_totales[indice] + totales_interruptos_organismo_causas_interrupcion(interruptos, organismo, causa.id)
            totales_a = totales_a + totales_interruptos_organismo_causas_interrupcion(interruptos, organismo, causa.id)

            worksheet_data.write(inicio_fila + i, posicion_total_derecho, totales_a, formato)

        i = i + 1

        l_interruptos = interruptos.filter(organismo__nombre=organismo)

        for interrupto in l_interruptos:

            worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad

            totales_a = 0

            for indice, causa in enumerate(causas_interrupcion):
                worksheet_data.write(inicio_fila + i, indice + 1, totales_interruptos_causas_interrupcion(interrupto, causa.id), formato5)
                totales_a = totales_a + totales_interruptos_causas_interrupcion(interrupto, causa.id)

                worksheet_data.write(inicio_fila + i, posicion_total_derecho, totales_a, formato)

            i = i + 1

    total = 0

    worksheet_data.write(inicio_fila + i, 0, "TOTALES", formato_organismos)
    for indice, causas in enumerate(causas_interrupcion):
        worksheet_data.write(inicio_fila + i, indice + 1, lista_totales[indice], formato_organismos)
        total = total + lista_totales[indice]

        worksheet_data.write(inicio_fila + i, posicion_total_derecho, total, formato)

    book.close()
    return response
