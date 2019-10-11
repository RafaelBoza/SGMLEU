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
def resultados_entrevistas_sma_diciembre(request):
    start_time = time.time()
    anno_actual = datetime.today().year

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if categoria_usuario == 'dmt':
        response[
            'Content-Disposition'] = "attachment; filename=Resultados_entrevistas_sma_(Diciembre)(%s)_(%s).xlsx" % (municipio_usuario,
                                                                                                anno_actual)

        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario,  mes_entrevista='Diciembre',
                                                        activo=True).values("recibio_oferta", "acepto_oferta", "ubicacion", "causa_no_aceptacion")
    elif categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Resultados_entrevistas_sma_(Diciembre)(%s)_(%s).xlsx" % (provincia_usuario,
                                                                                                     anno_actual)
        PROVINCIAS = Provincia.objects.filter(id=provincia_usuario.id)
        MUNICIPIOS = Municipio.objects.all()
        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario,  mes_entrevista='Diciembre',
                                                        activo=True).values("recibio_oferta", "acepto_oferta", "ubicacion", "causa_no_aceptacion")
    else:
        response['Content-Disposition'] = "attachment; filename=Resultados_entrevistas_sma_(Diciembre)(%s).xlsx" % anno_actual

        PROVINCIAS = Provincia.objects.all()
        MUNICIPIOS = Municipio.objects.all()
        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(activo=True, mes_entrevista='Diciembre').values("recibio_oferta", "acepto_oferta", "ubicacion", "causa_no_aceptacion")

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet('Resultados_entrevistas')

    formato = book.add_format({'bold': True,
                               'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("B1", "Controlados", formato)
    worksheet_data.write("C1", "Recibio oferta", formato)
    worksheet_data.write("D1", "Acepto oferta", formato)
    worksheet_data.write("E1", "Empleo Estatal", formato)
    worksheet_data.write("F1", "TPCP", formato)
    worksheet_data.write("G1", "DL 358", formato)
    worksheet_data.write("H1", "Otra no Estatal", formato)
    worksheet_data.write("I1", "No acepto oferta", formato)
    worksheet_data.write("J1", "No le gustan las ofertas", formato)
    worksheet_data.write("K1", "No desea trabajar", formato)

    worksheet_data.set_column("A:A", 23)
    worksheet_data.set_column("B:B", 11)
    worksheet_data.set_column("C:C", 13)
    worksheet_data.set_column("D:D", 13)
    worksheet_data.set_column("E:E", 14)
    worksheet_data.set_column("F:F", 7)
    worksheet_data.set_column("G:G", 7)
    worksheet_data.set_column("H:H", 14)
    worksheet_data.set_column("I:I", 16)
    worksheet_data.set_column("J:J", 22)
    worksheet_data.set_column("K:K", 16)

    if categoria_usuario == 'dmt':
        worksheet_data.write("A1", "Municipio", formato)
    else:
        worksheet_data.write("A1", "Provincia / Municipio", formato)

    INICIO = 1
    TOTALES = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if categoria_usuario == 'dpt_ee' or categoria_usuario == 'administrador':

        for provincia in PROVINCIAS:

            worksheet_data.write(INICIO, 0, provincia.nombre, formato)

            DIC_LICENCIADOS_SMA_PROVINCIA = resultados_entrevistas_provincia(LICENCIADOS_SMA.filter(municipio_residencia__provincia=provincia))

            controlados = DIC_LICENCIADOS_SMA_PROVINCIA['controlados']
            recibio_oferta = DIC_LICENCIADOS_SMA_PROVINCIA['recibio_oferta']
            acepto_oferta = DIC_LICENCIADOS_SMA_PROVINCIA['acepto_oferta']
            empleo_estatal = DIC_LICENCIADOS_SMA_PROVINCIA['empleo_estatal']
            tpcp = DIC_LICENCIADOS_SMA_PROVINCIA['tpcp']
            dl_358 = DIC_LICENCIADOS_SMA_PROVINCIA['dl_358']
            otra_no_estatal = DIC_LICENCIADOS_SMA_PROVINCIA['otra_no_estatal']
            no_acepto_oferta = DIC_LICENCIADOS_SMA_PROVINCIA['no_acepto_oferta']
            no_le_gustan_las_ofertas = DIC_LICENCIADOS_SMA_PROVINCIA['no_le_gustan_las_ofertas']
            no_desea_trabajar = DIC_LICENCIADOS_SMA_PROVINCIA['no_desea_trabajar']

            worksheet_data.write(INICIO, 1, DIC_LICENCIADOS_SMA_PROVINCIA['controlados'], formato)
            worksheet_data.write(INICIO, 2, DIC_LICENCIADOS_SMA_PROVINCIA['recibio_oferta'], formato)
            worksheet_data.write(INICIO, 3, DIC_LICENCIADOS_SMA_PROVINCIA['acepto_oferta'], formato)
            worksheet_data.write(INICIO, 4, DIC_LICENCIADOS_SMA_PROVINCIA['empleo_estatal'], formato)
            worksheet_data.write(INICIO, 5, DIC_LICENCIADOS_SMA_PROVINCIA['tpcp'], formato)
            worksheet_data.write(INICIO, 6, DIC_LICENCIADOS_SMA_PROVINCIA['dl_358'], formato)
            worksheet_data.write(INICIO, 7, DIC_LICENCIADOS_SMA_PROVINCIA['otra_no_estatal'], formato)
            worksheet_data.write(INICIO, 8, DIC_LICENCIADOS_SMA_PROVINCIA['no_acepto_oferta'], formato)
            worksheet_data.write(INICIO, 9, DIC_LICENCIADOS_SMA_PROVINCIA['no_le_gustan_las_ofertas'], formato)
            worksheet_data.write(INICIO, 10, DIC_LICENCIADOS_SMA_PROVINCIA['no_desea_trabajar'], formato)

            TOTALES[0] += controlados
            TOTALES[1] += recibio_oferta
            TOTALES[2] += acepto_oferta
            TOTALES[3] += empleo_estatal
            TOTALES[4] += tpcp
            TOTALES[5] += dl_358
            TOTALES[6] += otra_no_estatal
            TOTALES[7] += no_acepto_oferta
            TOTALES[8] += no_le_gustan_las_ofertas
            TOTALES[9] += no_desea_trabajar

            INICIO += 1

            L_MUNICIPIOS = MUNICIPIOS.filter(provincia=provincia)
            for municipio in L_MUNICIPIOS:

                worksheet_data.write(INICIO, 0, municipio.nombre, formato2)

                DIC_LICENCIADOS_SMA_MUNICIPIO = resultados_entrevistas_provincia(LICENCIADOS_SMA.filter(municipio_residencia=municipio))

                worksheet_data.write(INICIO, 1, DIC_LICENCIADOS_SMA_MUNICIPIO['controlados'], formato)
                worksheet_data.write(INICIO, 2, DIC_LICENCIADOS_SMA_MUNICIPIO['recibio_oferta'], formato)
                worksheet_data.write(INICIO, 3, DIC_LICENCIADOS_SMA_MUNICIPIO['acepto_oferta'], formato)
                worksheet_data.write(INICIO, 4, DIC_LICENCIADOS_SMA_MUNICIPIO['empleo_estatal'], formato)
                worksheet_data.write(INICIO, 5, DIC_LICENCIADOS_SMA_MUNICIPIO['tpcp'], formato)
                worksheet_data.write(INICIO, 6, DIC_LICENCIADOS_SMA_MUNICIPIO['dl_358'], formato)
                worksheet_data.write(INICIO, 7, DIC_LICENCIADOS_SMA_MUNICIPIO['otra_no_estatal'], formato)
                worksheet_data.write(INICIO, 8, DIC_LICENCIADOS_SMA_MUNICIPIO['no_acepto_oferta'], formato)
                worksheet_data.write(INICIO, 9, DIC_LICENCIADOS_SMA_MUNICIPIO['no_le_gustan_las_ofertas'], formato)
                worksheet_data.write(INICIO, 10, DIC_LICENCIADOS_SMA_MUNICIPIO['no_desea_trabajar'], formato)

                INICIO += 1

        worksheet_data.write(INICIO, 0, 'Total', formato)
        worksheet_data.write_row(INICIO, 1, TOTALES, formato)

    book.close()
    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
