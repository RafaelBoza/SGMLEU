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
def mujeres_ubicadas_por_fuentes(request):
    start_time = time.time()

    anno = datetime.today().year

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Mujeres_ubicadas_por_fuentes._(%s).xlsx" % (
        anno)
    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Provincias", formato)
    worksheet_data.write(0, 1, "Total", formato)

    fuentes_procedencia = FuenteProcedencia.objects.filter(activo=True).exclude(id=5).order_by('id')
    cantidad_fuentes = fuentes_procedencia.count()
    indice = 2

    for fuente in fuentes_procedencia:
        worksheet_data.write(0, indice, fuente.nombre, formato)
        indice = indice + 1

    worksheet_data.set_column("A:A", 17)

    provincias = Provincia.objects.all()
    arr_provincias = []
    for p in provincias:
        arr_provincias.append(p.nombre)

    worksheet_data.write_column(1, 0, arr_provincias, formato2)

    cantidad_provincias = arr_provincias.__len__()
    indice_total = cantidad_provincias + 1

    worksheet_data.write(indice_total, 0, "Total", formato)

    licenciados_sma = LicenciadosSMA.objects.filter(sexo='F', activo=True)

    egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=2,
                                                                           activo=True)

    sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=3,
                                                                         activo=True)

    desvinculados = Desvinculado.objects.filter(sexo='F', ubicado=True, activo=True)

    tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=6,
                                                                activo=True)

    obreros_calificados = TMedioOCalificadoEOficio.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=7,
                                                                    activo=True)

    escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=8,
                                                                activo=True)

    egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(sexo='F', ubicado=True, activo=True)

    egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(sexo='F', ubicado=True, activo=True)

    egresados_efi = EgresadosEFI.objects.filter(sexo='F', ubicado=True, activo=True)

    menores_incapacitados = Menores.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=12, activo=True)

    menores_desvinculados = Menores.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=13, activo=True)

    menores_dictamen = Menores.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=14, activo=True)

    discapacitados = Discapacitados.objects.filter(sexo='F', ubicado=True, activo=True)

    mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=17, activo=True)

    hombres_riesgo_pnr = PersonasRiesgo.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=18, activo=True)

    proxenetas = PersonasRiesgo.objects.filter(sexo='F', ubicado=True, fuente_procedencia_id=19, activo=True)

    total_licenciados_sma_provincias = []
    total_egresados_ep_provincias = []
    total_sancionados_provincias = []
    total_desvinculados_provincias = []
    total_tecnicos_medio_provincias = []
    total_obreros_calificados_provincias = []
    total_escuela_oficio_provincias = []
    total_egresados_esc_especiales_provincias = []
    total_egresados_esc_conducta_provincias = []
    total_egresados_efi_provincias = []
    total_menores_incapacitados_provincias = []
    total_menores_desvinculados_provincias = []
    total_menores_dictamen_provincias = []
    total_discapacitados_provincias = []
    total_mueres_riesgo_pnr_provincias = []
    total_hombres_riesgo_pnr_provincias = []
    total_proxenetas_riesgo_pnr_provincias = []

    for provincia in provincias:

        # UBICADOS: Licenciados del SMA
        total_licenciados_sma_provincias.append(
            licenciados_sma.filter(municipio_residencia__provincia=provincia).count())

        # UBICADOS: Egresados de establecimientos penitenciarios
        total_egresados_ep_provincias.append(
            egresados_ep.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: SANCIONADOS
        total_sancionados_provincias.append(
            sancionados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: DESVINCULADOS
        total_desvinculados_provincias.append(
            desvinculados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Tecnicos medios
        total_tecnicos_medio_provincias.append(
            tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Egresados obreros calificados
        total_obreros_calificados_provincias.append(
            obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Egresados escuelas de oficio
        total_escuela_oficio_provincias.append(
            escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Egresados de escuelas especiales
        total_egresados_esc_especiales_provincias.append(
            egresados_escuelas_especiales.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Egresados de escuelas de conducta
        total_egresados_esc_conducta_provincias.append(
            egresados_escuelas_conducta.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Egresados de la EFI
        total_egresados_efi_provincias.append(
            egresados_efi.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Menores incapacitados para el estudio por dictamen médico
        total_menores_incapacitados_provincias.append(
            menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Menores desvinculados del SNE por bajo rendimiento
        total_menores_desvinculados_provincias.append(
            menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Menores con dictamen del CDO-MININT
        total_menores_dictamen_provincias.append(
            menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Personas con discapacidad
        total_discapacitados_provincias.append(
            discapacitados.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Mujeres de riesgo controladas por al PNR
        total_mueres_riesgo_pnr_provincias.append(
            mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Hombres de riesgo controlados por al PNR
        total_hombres_riesgo_pnr_provincias.append(
            hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia).count())

        # UBICADOS: Proxenetas de riesgo controlados por la PNR
        total_proxenetas_riesgo_pnr_provincias.append(
            proxenetas.filter(municipio_solicita_empleo__provincia=provincia).count())

    worksheet_data.write_column(1, 2, total_licenciados_sma_provincias, formato2)
    worksheet_data.write_column(1, 3, total_egresados_ep_provincias, formato2)
    worksheet_data.write_column(1, 4, total_sancionados_provincias, formato2)
    worksheet_data.write_column(1, 5, total_desvinculados_provincias, formato2)
    worksheet_data.write_column(1, 6, total_tecnicos_medio_provincias, formato2)
    worksheet_data.write_column(1, 7, total_obreros_calificados_provincias, formato2)
    worksheet_data.write_column(1, 8, total_escuela_oficio_provincias, formato2)
    worksheet_data.write_column(1, 9, total_egresados_esc_especiales_provincias, formato2)
    worksheet_data.write_column(1, 10, total_egresados_esc_conducta_provincias, formato2)
    worksheet_data.write_column(1, 11, total_egresados_efi_provincias, formato2)
    worksheet_data.write_column(1, 12, total_menores_incapacitados_provincias, formato2)
    worksheet_data.write_column(1, 13, total_menores_desvinculados_provincias, formato2)
    worksheet_data.write_column(1, 14, total_menores_dictamen_provincias, formato2)
    worksheet_data.write_column(1, 15, total_discapacitados_provincias, formato2)
    worksheet_data.write_column(1, 16, total_mueres_riesgo_pnr_provincias, formato2)
    worksheet_data.write_column(1, 17, total_hombres_riesgo_pnr_provincias, formato2)
    worksheet_data.write_column(1, 18, total_proxenetas_riesgo_pnr_provincias, formato2)

    # ------------ SUMAS ABAJO-------------------

    sumas = []
    for a in range(1, 19):
        total = '=SUM(%s)' % xl_range(1, a, cantidad_provincias, a)
        sumas.append(total)

    indice_sumas = 1
    for suma in sumas:
        worksheet_data.write(17, indice_sumas, suma, formato2)
        indice_sumas = indice_sumas + 1

    # ------------ SUMAS ARRIBA-------------------
    sumas_abajo = []
    inicio = 2
    for i in range(1, cantidad_provincias + 1):
        total2 = '=SUM(%s)' % xl_range(i, inicio, i, cantidad_fuentes + inicio - 1)
        sumas_abajo.append(total2)

    indice_sumas = 1
    for suma in sumas_abajo:
        worksheet_data.write(indice_sumas, 1, suma, formato2)
        indice_sumas = indice_sumas + 1

    book.close()
    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
