# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range

from SGMGU.models import *
from SGMGU.views.utiles import permission_required
from datetime import *
from metodos_auxiliares_sma import *
import time


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def causas_no_incorporado_sma(request):
    # start_time = time.time()
    anno_actual = datetime.today().year

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if categoria_usuario == 'dmt':
        response[
            'Content-Disposition'] = "attachment; filename=Causas_no_incorporados_sma_(%s)_(%s).xlsx" % (municipio_usuario,
                                                                                                anno_actual)

        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario,
                                                        fecha_registro__year=anno_actual).values("causa_no_ubicado", "municipio_residencia__provincia_id", "ubicacion", "municipio_residencia") | \
                          LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario,
                                                        activo=True).values("causa_no_ubicado", "municipio_residencia__provincia_id", "ubicacion", "municipio_residencia")
    elif categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Causas_no_incorporados_sma_(%s)_(%s).xlsx" % (provincia_usuario,
                                                                                                     anno_actual)
        PROVINCIAS = Provincia.objects.filter(id=provincia_usuario.id)
        MUNICIPIOS = Municipio.objects.all()
        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario,
                                                        fecha_registro__year=anno_actual).values("causa_no_ubicado", "municipio_residencia__provincia_id", "ubicacion", "municipio_residencia") | \
                          LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario,
                                                        activo=True).values("causa_no_ubicado", "municipio_residencia__provincia_id", "ubicacion", "municipio_residencia")
    else:
        response['Content-Disposition'] = "attachment; filename=Causas_no_incorporados_sma_(%s).xlsx" % anno_actual

        PROVINCIAS = Provincia.objects.all()
        MUNICIPIOS = Municipio.objects.all()
        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(fecha_registro__year=anno_actual).values("causa_no_ubicado_id", "municipio_residencia__provincia_id", "ubicacion", "municipio_residencia") | \
                          LicenciadosSMA.objects.filter(activo=True).values("causa_no_ubicado_id", "municipio_residencia__provincia_id", "ubicacion", "municipio_residencia")

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet('Causas_no_incorporados')

    worksheet_data.set_column("A:A", 19.20)
    worksheet_data.set_column("C:C", 14.43)
    worksheet_data.set_column("D:D", 19.43)
    worksheet_data.set_column("E:E", 11.15)
    worksheet_data.set_column("F:F", 11.15)
    worksheet_data.set_column("G:G", 27)

    formato = book.add_format({'bold': True,
                               'border': 1})
    formato2 = book.add_format({'border': 1})

    if categoria_usuario == 'dmt':
        worksheet_data.write("A1", "Municipio", formato)
    else:
        worksheet_data.write("A1", "Provincia / Municipio", formato)

    worksheet_data.write(0, 1, 'Total', formato)
    CAUSAS = CausalNoUbicado.objects.filter(id__in=[1, 2, 3, 4, 5])
    causas_no_ubicados = [causa.causa for causa in CAUSAS]
    worksheet_data.write_row(0, 2, causas_no_ubicados, formato)

    TOTALES = [0, 0, 0, 0, 0]

    INICIO = 1

    if categoria_usuario == 'dpt_ee' or categoria_usuario == 'administrador':

        for provincia in PROVINCIAS:
            worksheet_data.write(INICIO, 0, provincia.nombre, formato)
            total_causas_provincia = '=SUM(%s)' % xl_range(INICIO, 2, INICIO, CAUSAS.count() + 1)
            worksheet_data.write(INICIO, 1, total_causas_provincia, formato)

            for index, causa in enumerate(CAUSAS):

                cantidad = LICENCIADOS_SMA.filter(
                    causa_no_ubicado_id=causa.id, municipio_residencia__provincia_id=provincia.id).count()
                TOTALES[index] += cantidad

                worksheet_data.write(INICIO, index + 2, cantidad, formato2)

            INICIO += 1

            L_MUNICIPIOS = MUNICIPIOS.filter(provincia=provincia)
            for municipio in L_MUNICIPIOS:
                worksheet_data.write(INICIO, 0, municipio.nombre, formato2)
                total_causas_municipio = '=SUM(%s)' % xl_range(INICIO, 2, INICIO, CAUSAS.count() + 1)
                worksheet_data.write(INICIO, 1, total_causas_municipio, formato)

                for index, causa in enumerate(CAUSAS):

                    cantidad = LICENCIADOS_SMA.filter(
                        causa_no_ubicado_id=causa.id, municipio_residencia=municipio.id).count()
                    worksheet_data.write(INICIO, index + 2, cantidad, formato2)

                INICIO += 1

        worksheet_data.write(INICIO, 0, 'TOTALES', formato)

        total = '=SUM(%s)' % xl_range(INICIO, 2, INICIO, CAUSAS.count() + 1)
        worksheet_data.write(INICIO, 1, total, formato)

        worksheet_data.write_row(INICIO, 2, TOTALES, formato)


    book.close()
    # elapsed_time = time.time() - start_time
    # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
