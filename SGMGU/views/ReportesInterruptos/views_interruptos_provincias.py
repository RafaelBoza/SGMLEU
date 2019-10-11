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
def interruptos_por_provincias(request):
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
            'Content-Disposition'] = "attachment; filename=Interruptos_por_organismos_(%s)_(%s_%s).xlsx" % (
            str(nombre_organismo).replace(" ", "_"), obtener_mes(mes_actual - 1), num_anno)
    else:
        response['Content-Disposition'] = "attachment; filename=Interruptos_por_provincias_(%s_%s).xlsx" % (
            obtener_mes(mes_actual - 1), num_anno)

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Interruptos por Provincias")

    formato1 = book.add_format({'align': 'center',
                                'valign': 'vcenter',
                                'bold': True,
                                'border': 1})
    formato5 = book.add_format({'border': 1,
                                'text_wrap': True})
    formato_organismos = book.add_format({'bold': True,
                                          'border': 1})

    worksheet_data.write("A1", "OACE-OSDE / Provincias", formato1)

    totales_provincias = dict()
    provincias = Provincia.objects.all()

    for indice, p in enumerate(provincias):
        worksheet_data.write(0, indice + 1, p.siglas, formato1)
        totales_provincias[p] = 0

    worksheet_data.set_column("A:A", 24)

    if categoria_usuario == 'interrupto':
        if es_oace(organismo):
            osdes = obtener_osdes_de_un_oace(organismo)
            if osdes.__len__() > 0:
                interruptos = Interruptos.objects.filter(fecha_registro__year=anno_actual,
                                                         organismo__id__in=[osde.id for osde in osdes]
                                                         )
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

            for indice, p in enumerate(provincias):
                t = totales_interruptos_organismo_provincia(interruptos, oace, p)
                worksheet_data.write(inicio_fila + i, indice + 1, t, formato5)
                totales_provincias[p] = totales_provincias[p] + t

            i = i + 1

            for interrupto in interruptos:
                if interrupto.organismo_id == oace.id:

                    worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad

                    for indice, p in enumerate(provincias):
                        if interrupto.municipio.provincia == p:
                            worksheet_data.write(inicio_fila + i, indice + 1, total_interruptos(interrupto), formato5)
                        else:
                            worksheet_data.write(inicio_fila + i, indice + 1, 0, formato5)

                    i = i + 1

            osdes = obtener_osdes_de_un_oace(oace)

            if obtener_osdes_de_un_oace(oace).__len__() > 0:
                for osde in osdes:

                    worksheet_data.write(inicio_fila + i, 0, osde.siglas, formato_organismos)  # osde

                    for indice, p in enumerate(provincias):
                        t = totales_interruptos_organismo_provincia(interruptos, osde, p)
                        worksheet_data.write(inicio_fila + i, indice + 1, t, formato5)
                        totales_provincias[p] = totales_provincias[p] + t

                    i = i + 1

                    l_interruptos = interruptos.filter(organismo_id=osde)

                    for interrupto in l_interruptos:

                        worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad

                        for indice, p in enumerate(provincias):
                            if interrupto.municipio.provincia == p:
                                worksheet_data.write(inicio_fila + i, indice + 1, total_interruptos(interrupto), formato5)
                            else:
                                worksheet_data.write(inicio_fila + i, indice + 1, 0, formato5)

                        i = i + 1

    if not es_oace(organismo):

        worksheet_data.write(inicio_fila + i, 0, organismo.siglas, formato_organismos)  # organismo

        for indice, p in enumerate(provincias):
            t = totales_interruptos_organismo_provincia(interruptos, organismo, p)
            worksheet_data.write(inicio_fila + i, indice + 1, t, formato5)
            totales_provincias[p] = totales_provincias[p] + t

        i = i + 1

        interruptos = interruptos.filter(organismo__nombre=organismo)

        for interrupto in interruptos:

            worksheet_data.write(inicio_fila + i, 0, interrupto.entidad.e_nombre, formato5)  # entidad

            for indice, p in enumerate(provincias):
                if interrupto.municipio.provincia == p:
                    worksheet_data.write(inicio_fila + i, indice + 1, total_interruptos(interrupto), formato5)
                else:
                    worksheet_data.write(inicio_fila + i, indice + 1, 0, formato5)

            i = i + 1

    worksheet_data.write(inicio_fila + i, 0, "TOTALES", formato_organismos)

    for indice, x in enumerate(totales_provincias.values()):
        worksheet_data.write(inicio_fila + i, indice + 1, x, formato_organismos)

    book.close()
    return response
