# -*- coding: utf-8 -*-
import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range

from SGMGU.models import *
from SGMGU.views.utiles import permission_required


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def desvinculados_no_ubicados_por_causales(request):
    start_time = time.time()

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    anno_actual = datetime.today().year

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Desvinculados_no_ubicados_por_causales._(%s).xlsx" % (
        anno_actual)
    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    if categoria_usuario == 'dpt_ee':
        worksheet_data.write("A1", "Provincia", formato)

        provincias = Provincia.objects.filter(id=provincia_usuario.id)
        desvinculados = Desvinculado.objects.filter(activo=True, municipio_solicita_empleo__provincia=provincia_usuario)
    elif categoria_usuario == 'dmt':
        worksheet_data.write("A1", "Municipio", formato)

        desvinculados = Desvinculado.objects.filter(activo=True, municipio_solicita_empleo=municipio_usuario)
    else:
        worksheet_data.write("A1", "Provincias", formato)

        provincias = Provincia.objects.all()
        desvinculados = Desvinculado.objects.filter(activo=True)

    worksheet_data.set_column("A:A", 17)

    causas_no_ubicacion = CausalNoUbicado.objects.filter(activo=True).order_by('id')
    cantidad_causas = causas_no_ubicacion.count()
    indice = 1

    for causa in causas_no_ubicacion:
        worksheet_data.write(0, indice, causa.causa, formato)
        indice = indice + 1

    total_arriba = indice
    worksheet_data.write(0, total_arriba, "Total", formato)

    if categoria_usuario == 'administrador' or categoria_usuario == 'dpt_ee':

        arr_provincias = []
        for p in provincias:
            arr_provincias.append(p.nombre)

        worksheet_data.write_column(1, 0, arr_provincias, formato2)

        cantidad_provincias = arr_provincias.__len__()
        indice_total = cantidad_provincias + 1

        for indice_provincia, provincia in enumerate(provincias):

            for indice_causa, causa in enumerate(causas_no_ubicacion):

                worksheet_data.write(indice_provincia + 1, indice_causa + 1,
                                     desvinculados.filter(causa_no_ubicado=causa, municipio_solicita_empleo__provincia=provincia).count(),
                                     formato2)

        # ------------ SUMAS ARRIBA-------------------
        sumas_abajo = []
        inicio = 1
        for i in range(1, cantidad_provincias + 1):
            total2 = '=SUM(%s)' % xl_range(i, inicio, i, cantidad_causas + inicio - 1)
            sumas_abajo.append(total2)

        indice_sumas = 1
        for suma in sumas_abajo:
            worksheet_data.write(indice_sumas, inicio + cantidad_causas, suma, formato2)
            indice_sumas = indice_sumas + 1

        if categoria_usuario == 'administrador':
            # ------------ SUMAS ABAJO-------------------
            worksheet_data.write(indice_total, 0, "Total", formato)

            sumas_lateral = []
            for a in range(1, cantidad_causas + 2):
                total = '=SUM(%s)' % xl_range(1, a, cantidad_provincias, a)
                sumas_lateral.append(total)

            indice_sumas = 1
            for suma in sumas_lateral:
                worksheet_data.write(cantidad_provincias + 1, indice_sumas, suma, formato2)
                indice_sumas = indice_sumas + 1

    if categoria_usuario == 'dmt':

        worksheet_data.write(1, 0, municipio_usuario.nombre, formato2)

        for indice_causa, causa in enumerate(causas_no_ubicacion):
            worksheet_data.write(1, indice_causa + 1,
                                 desvinculados.filter(causa_no_ubicado=causa).count(),
                                 formato2)

        # ------------ SUMAS ARRIBA-------------------
        total = '=SUM(%s)' % xl_range(1, 1, 1, cantidad_causas)

        worksheet_data.write(1, cantidad_causas + 1, total, formato2)

    book.close()

    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    # print("Tiempo transcurrido: % segundos." % elapsed_time)

    return response
