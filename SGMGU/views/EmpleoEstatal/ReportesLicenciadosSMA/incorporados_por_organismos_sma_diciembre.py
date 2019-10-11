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
def incorporados_por_organismos_sma_diciembre(request):
    # start_time = time.time()
    anno_actual = datetime.today().year

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if categoria_usuario == 'dmt':
        response[
            'Content-Disposition'] = "attachment; filename=Incorporados_por_organismos_sma_Diciemre_(%s)_(%s).xlsx" % (municipio_usuario,
                                                                                                anno_actual)

        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario, mes_entrevista='Diciembre',
                                                        fecha_registro__year=anno_actual).values("incorporado", "organismo_id", "ubicacion_id",
                                                                                                 "municipio_residencia__provincia_id") | \
                          LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario, mes_entrevista='Diciembre',
                                                        activo=True).values("incorporado", "organismo_id", "ubicacion_id",
                                                                            "municipio_residencia__provincia_id")
        MUNICIPIO = Municipio.objects.filter(id=municipio_usuario.id)
    elif categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Incorporados_por_organismos_sma_Diciemre_(%s)_(%s).xlsx" % (provincia_usuario,
                                                                                                     anno_actual)
        PROVINCIAS = Provincia.objects.filter(id=provincia_usuario.id)
        # MUNICIPIOS = Municipio.objects.all()
        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario, mes_entrevista='Diciembre',
                                                        fecha_registro__year=anno_actual).values("incorporado", "organismo_id", "ubicacion_id",
                                                                                                 "municipio_residencia__provincia_id") | \
                          LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario, mes_entrevista='Diciembre',
                                                        activo=True).values("incorporado", "organismo_id", "ubicacion_id",
                                                                            "municipio_residencia__provincia_id")
    else:
        response['Content-Disposition'] = "attachment; filename=Incorporados_por_organismos_sma_Diciemre_(%s).xlsx" % anno_actual

        PROVINCIAS = Provincia.objects.all()
        # MUNICIPIOS = Municipio.objects.all()
        LICENCIADOS_SMA = LicenciadosSMA.objects.filter(fecha_registro__year=anno_actual, mes_entrevista='Diciembre',).values("incorporado", "organismo_id", "ubicacion_id",
                                                                                                 "municipio_residencia__provincia_id") | \
                          LicenciadosSMA.objects.filter(activo=True, mes_entrevista='Diciembre',).values("incorporado", "organismo_id", "ubicacion_id",
                                                                            "municipio_residencia__provincia_id")

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet('Incorporados')

    formato = book.add_format({'bold': True,
                               'border': 1})
    formato2 = book.add_format({'border': 1})
    formato3 = book.add_format({'border': 1,
                                'font_color': 'red'})

    worksheet_data.write("A1", "OACE", formato)
    worksheet_data.set_column("A:A", 21)

    if categoria_usuario == 'administrador' or categoria_usuario == 'dpt_ee':
        provincias = [provincia.siglas for provincia in PROVINCIAS]
        cantidad_provincias = provincias.__len__()
        worksheet_data.write_row(0, 1, provincias, formato)
        worksheet_data.write(0, cantidad_provincias + 1, 'Total', formato)
    if categoria_usuario == 'dmt':
        worksheet_data.write(0, 1, municipio_usuario.nombre, formato2)

    LICENCIADOS_SMA = LICENCIADOS_SMA.filter(incorporado=1)
    ORGANISMOS = Organismo.objects.filter(activo=True)
    INICIO = 1

    if categoria_usuario == 'dpt_ee' or categoria_usuario == 'administrador':

        for organismo in ORGANISMOS:
            worksheet_data.write(INICIO, 0, organismo.siglas, formato)

            for index, provincia in enumerate(PROVINCIAS):

                worksheet_data.write(INICIO, index + 1, LICENCIADOS_SMA.filter(
                                                        organismo_id=organismo.id,
                                                        municipio_residencia__provincia_id=provincia.id).count(), formato2)
            total_organismo = '=SUM(%s)' % xl_range(INICIO, 1, INICIO, cantidad_provincias)
            worksheet_data.write(INICIO, cantidad_provincias + 1, total_organismo, formato)

            INICIO += 1

        worksheet_data.write(INICIO, 0, 'TPCP', formato3)
        for index, provincia in enumerate(PROVINCIAS):
            worksheet_data.write(INICIO, index + 1, LICENCIADOS_SMA.filter(
                                                        ubicacion_id=2,
                                                        municipio_residencia__provincia_id=provincia.id).count(), formato2)

        total_tpcp = '=SUM(%s)' % xl_range(INICIO, 1, INICIO, cantidad_provincias)
        worksheet_data.write(INICIO, cantidad_provincias + 1, total_tpcp, formato)
        INICIO += 1

        worksheet_data.write(INICIO, 0, 'DL358', formato3)
        for index, provincia in enumerate(PROVINCIAS):
            worksheet_data.write(INICIO, index + 1, LICENCIADOS_SMA.filter(
                                                        ubicacion_id=3,
                                                        municipio_residencia__provincia_id=provincia.id).count(), formato2)
        total_dl358 = '=SUM(%s)' % xl_range(INICIO, 1, INICIO, cantidad_provincias)
        worksheet_data.write(INICIO, cantidad_provincias + 1, total_dl358, formato)
        INICIO += 1

        worksheet_data.write(INICIO, 0, 'Otra no Estatal', formato3)
        for index, provincia in enumerate(PROVINCIAS):
            worksheet_data.write(INICIO, index + 1, LICENCIADOS_SMA.filter(
                                                        ubicacion_id=4,
                                                        municipio_residencia__provincia_id=provincia.id).count(), formato2)
        total_otra_no_estatal = '=SUM(%s)' % xl_range(INICIO, 1, INICIO, cantidad_provincias)
        worksheet_data.write(INICIO, cantidad_provincias + 1, total_otra_no_estatal, formato)
        INICIO += 1

        worksheet_data.write(INICIO, 0, 'Total', formato)
        for index, provincia in enumerate(PROVINCIAS):
            total_otra_no_estatal = '=SUM(%s)' % xl_range(1, index + 1, ORGANISMOS.count() + 3, index + 1)
            worksheet_data.write(INICIO, index + 1, total_otra_no_estatal, formato)

        total_general = '=SUM(%s)' % xl_range(INICIO, 1, INICIO, cantidad_provincias)
        worksheet_data.write(INICIO, cantidad_provincias + 1, total_general, formato)

    if categoria_usuario == 'dmt':

        for organismo in ORGANISMOS:
            worksheet_data.write(INICIO, 0, organismo.siglas, formato)

            for index, municipio in enumerate(MUNICIPIO):
                worksheet_data.write(INICIO, index + 1, LICENCIADOS_SMA.filter(
                    organismo_id=organismo.id,
                    municipio_residencia_id=municipio.id).count(), formato2)
            INICIO += 1

        worksheet_data.write(INICIO, 0, 'TPCP', formato3)
        for index, municipio in enumerate(MUNICIPIO):
            worksheet_data.write(INICIO, index + 1, LICENCIADOS_SMA.filter(
                ubicacion_id=2,
                municipio_residencia_id=municipio.id).count(), formato2)
        INICIO += 1

        worksheet_data.write(INICIO, 0, 'DL358', formato3)
        for index, municipio in enumerate(MUNICIPIO):
            worksheet_data.write(INICIO, index + 1, LICENCIADOS_SMA.filter(
                ubicacion_id=3,
                municipio_residencia_id=municipio.id).count(), formato2)
        INICIO += 1

        worksheet_data.write(INICIO, 0, 'Otra no Estatal', formato3)
        for index, municipio in enumerate(MUNICIPIO):
            worksheet_data.write(INICIO, index + 1, LICENCIADOS_SMA.filter(
                ubicacion_id=4,
                municipio_residencia_id=municipio.id).count(), formato2)
        INICIO += 1

        worksheet_data.write(INICIO, 0, 'Total', formato)
        for index, municipio in enumerate(MUNICIPIO):
            total_otra_no_estatal = '=SUM(%s)' % xl_range(1, index + 1, ORGANISMOS.count() + 3, index + 1)
            worksheet_data.write(INICIO, index + 1, total_otra_no_estatal, formato)

    book.close()
    # elapsed_time = time.time() - start_time
    # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
