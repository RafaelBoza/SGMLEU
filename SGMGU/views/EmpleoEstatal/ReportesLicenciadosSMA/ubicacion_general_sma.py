# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from SGMGU.models import *
from SGMGU.views.utiles import permission_required
from datetime import *
from metodos_auxiliares_sma import *
import time


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def ubicacion_general_sma(request):
    # start_time = time.time()
    anno_actual = datetime.today().year

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if categoria_usuario == 'dmt':
        response[
            'Content-Disposition'] = "attachment; filename=Control_incorporacion_sma_(%s)_(%s).xlsx" % (municipio_usuario,
                                                                                                anno_actual)

        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario,
                                                        fecha_registro__year=anno_actual).values("incorporado", "sexo", "ubicacion") | \
                          LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario,
                                                        activo=True).values("incorporado", "sexo", "ubicacion")
    elif categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Control_incorporacion_sma_(%s)_(%s).xlsx" % (provincia_usuario,
                                                                                                     anno_actual)
        PROVINCIAS = Provincia.objects.filter(id=provincia_usuario.id)
        MUNICIPIOS = Municipio.objects.all()
        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario,
                                                        fecha_registro__year=anno_actual).values("incorporado", "sexo", "ubicacion") | \
                          LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario,
                                                        activo=True).values("incorporado", "sexo", "ubicacion")
    else:
        response['Content-Disposition'] = "attachment; filename=Control_incorporacion_sma_(%s).xlsx" % anno_actual

        PROVINCIAS = Provincia.objects.all()
        MUNICIPIOS = Municipio.objects.all()
        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(fecha_registro__year=anno_actual).values("incorporado", "sexo", "ubicacion") | \
                          LicenciadosSMA.objects.filter(activo=True).values("incorporado", "sexo", "ubicacion")

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet('Ubicacion')

    formato = book.add_format({'bold': True,
                               'border': 1})
    formato2 = book.add_format({'border': 1})

    if categoria_usuario == 'dmt':
        worksheet_data.write("A1", "Municipio", formato)
    else:
        worksheet_data.write("A1", "Provincia / Municipio", formato)

    worksheet_data.write("B1", "Controlados", formato)
    worksheet_data.write("C1", "Femenino", formato)
    worksheet_data.write("D1", "Incorporados", formato)
    worksheet_data.write("E1", "Femenino", formato)
    worksheet_data.write("F1", "Empleo Estatal", formato)
    worksheet_data.write("G1", "TPCP", formato)
    worksheet_data.write("H1", "DL 358", formato)
    worksheet_data.write("I1", "Otra no Estatal", formato)
    worksheet_data.write("J1", "No Incorporados", formato)
    worksheet_data.write("K1", "Femenino", formato)
    worksheet_data.set_column("A:A", 24)
    worksheet_data.set_column("B:B", 11)
    worksheet_data.set_column("C:C", 11)
    worksheet_data.set_column("D:D", 12)
    worksheet_data.set_column("E:E", 11)
    worksheet_data.set_column("F:F", 13.50)
    worksheet_data.set_column("G:G", 8)
    worksheet_data.set_column("H:H", 11)
    worksheet_data.set_column("I:I", 13.50)
    worksheet_data.set_column("J:J", 15)
    worksheet_data.set_column("K:K", 11)

    INICIO = 1
    TOTALES = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if categoria_usuario == 'dpt_ee' or categoria_usuario == 'administrador':

        for provincia in PROVINCIAS:
            worksheet_data.write(INICIO, 0, provincia.nombre, formato)

            L_LICENCIADOS_SMA = LICENCIADOS_SMA.filter(municipio_residencia__provincia=provincia)
            dic_totales = controlados_provincia(L_LICENCIADOS_SMA)
            controlados = dic_totales['controlados']
            controlados_femeninos = dic_totales['controlados_femeninos']
            incorporados = dic_totales['incorporados']
            incorporados_femeninos = dic_totales['incorporados_femeninos']
            empleo_estatal = dic_totales['empleo_estatal']
            tpcp = dic_totales['tpcp']
            dl_358 = dic_totales['dl_358']
            otra_no_estatal = dic_totales['otra_no_estatal']
            no_incorporados = dic_totales['no_incorporados']
            no_incorporados_femeninos = dic_totales['no_incorporados_femeninos']

            worksheet_data.write(INICIO, 1, controlados, formato)
            worksheet_data.write(INICIO, 2, controlados_femeninos, formato2)
            worksheet_data.write(INICIO, 3, incorporados, formato2)
            worksheet_data.write(INICIO, 4, incorporados_femeninos, formato2)
            worksheet_data.write(INICIO, 5, empleo_estatal, formato2)
            worksheet_data.write(INICIO, 6, tpcp, formato2)
            worksheet_data.write(INICIO, 7, dl_358, formato2)
            worksheet_data.write(INICIO, 8, otra_no_estatal, formato2)
            worksheet_data.write(INICIO, 9, no_incorporados, formato2)
            worksheet_data.write(INICIO, 10, no_incorporados_femeninos, formato2)

            INICIO += 1

            L_MUNICIPIOS = MUNICIPIOS.filter(provincia=provincia)
            for municipio in L_MUNICIPIOS:
                worksheet_data.write(INICIO, 0, municipio.nombre, formato2)

                L_LICENCIADOS_SMA = LICENCIADOS_SMA.filter(municipio_residencia=municipio)
                dic_totales = controlados_provincia(L_LICENCIADOS_SMA)
                controlados = dic_totales['controlados']
                controlados_femeninos = dic_totales['controlados_femeninos']
                incorporados = dic_totales['incorporados']
                incorporados_femeninos = dic_totales['incorporados_femeninos']
                empleo_estatal = dic_totales['empleo_estatal']
                tpcp = dic_totales['tpcp']
                dl_358 = dic_totales['dl_358']
                otra_no_estatal = dic_totales['otra_no_estatal']
                no_incorporados = dic_totales['no_incorporados']
                no_incorporados_femeninos = dic_totales['no_incorporados_femeninos']

                TOTALES[0] += controlados
                TOTALES[1] += controlados_femeninos
                TOTALES[2] += incorporados
                TOTALES[3] += incorporados_femeninos
                TOTALES[4] += empleo_estatal
                TOTALES[5] += tpcp
                TOTALES[6] += dl_358
                TOTALES[7] += otra_no_estatal
                TOTALES[8] += no_incorporados
                TOTALES[9] += no_incorporados_femeninos

                worksheet_data.write(INICIO, 1, controlados, formato2)
                worksheet_data.write(INICIO, 2, controlados_femeninos, formato2)
                worksheet_data.write(INICIO, 3, incorporados, formato2)
                worksheet_data.write(INICIO, 4, incorporados_femeninos, formato2)
                worksheet_data.write(INICIO, 5, empleo_estatal, formato2)
                worksheet_data.write(INICIO, 6, tpcp, formato2)
                worksheet_data.write(INICIO, 7, dl_358, formato2)
                worksheet_data.write(INICIO, 8, otra_no_estatal, formato2)
                worksheet_data.write(INICIO, 9, no_incorporados, formato2)
                worksheet_data.write(INICIO, 10, no_incorporados_femeninos, formato2)

                INICIO += 1

        worksheet_data.write(INICIO, 0, 'Total', formato)
        worksheet_data.write_row(INICIO, 1, TOTALES, formato)

    if categoria_usuario == 'dmt':
        worksheet_data.write(INICIO, 0, municipio_usuario.nombre, formato)

        L_LICENCIADOS_SMA = LICENCIADOS_SMA.filter(municipio_residencia=municipio_usuario)
        dic_totales = controlados_provincia(L_LICENCIADOS_SMA)
        controlados = dic_totales['controlados']
        controlados_femeninos = dic_totales['controlados_femeninos']
        incorporados = dic_totales['incorporados']
        incorporados_femeninos = dic_totales['incorporados_femeninos']
        empleo_estatal = dic_totales['empleo_estatal']
        tpcp = dic_totales['tpcp']
        dl_358 = dic_totales['dl_358']
        otra_no_estatal = dic_totales['otra_no_estatal']
        no_incorporados = dic_totales['no_incorporados']
        no_incorporados_femeninos = dic_totales['no_incorporados_femeninos']

        TOTALES[0] += controlados
        TOTALES[1] += controlados_femeninos
        TOTALES[2] += incorporados
        TOTALES[3] += incorporados_femeninos
        TOTALES[4] += empleo_estatal
        TOTALES[5] += tpcp
        TOTALES[6] += dl_358
        TOTALES[7] += otra_no_estatal
        TOTALES[8] += no_incorporados
        TOTALES[9] += no_incorporados_femeninos

        worksheet_data.write(INICIO, 1, controlados, formato2)
        worksheet_data.write(INICIO, 2, controlados_femeninos, formato2)
        worksheet_data.write(INICIO, 3, incorporados, formato2)
        worksheet_data.write(INICIO, 4, incorporados_femeninos, formato2)
        worksheet_data.write(INICIO, 5, empleo_estatal, formato2)
        worksheet_data.write(INICIO, 6, tpcp, formato2)
        worksheet_data.write(INICIO, 7, dl_358, formato2)
        worksheet_data.write(INICIO, 8, otra_no_estatal, formato2)
        worksheet_data.write(INICIO, 9, no_incorporados, formato2)
        worksheet_data.write(INICIO, 10, no_incorporados_femeninos, formato2)

        INICIO += 1

    book.close()
    # elapsed_time = time.time() - start_time
    # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
