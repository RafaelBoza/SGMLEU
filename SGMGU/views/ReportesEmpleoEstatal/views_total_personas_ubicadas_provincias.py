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
def total_personas_ubicadas_provincias(request):
    start_time = time.time()

    anno = datetime.today().year

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Total_de_personas_ubicadas_por_provincias._(%s).xlsx" % (
        anno)
    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Provincias", formato)
    worksheet_data.write("B1", "Controlados", formato)
    worksheet_data.write("C1", "Mujeres controladas", formato)
    worksheet_data.write("D1", "Jovenes controlados", formato)
    worksheet_data.write("E1", "Ubicados", formato)
    worksheet_data.write("F1", "Mujeres ubicadas", formato)
    worksheet_data.write("G1", "Jovenes ubicados", formato)

    fuentes_procedencia = FuenteProcedencia.objects.filter(activo=True).order_by('id')
    cantidad_fuentes = fuentes_procedencia.count()
    indice = 7

    total_arriba = indice + cantidad_fuentes
    worksheet_data.write(0, total_arriba, "Total", formato)

    for fuente in fuentes_procedencia:
        worksheet_data.write(0, indice, fuente.nombre, formato)
        indice = indice + 1

    worksheet_data.set_column("A:A", 17)
    worksheet_data.set_column("B:B", 11)
    worksheet_data.set_column("C:C", 10)
    worksheet_data.set_column("D:D", 10)
    worksheet_data.set_column("E:E", 10)
    worksheet_data.set_column("F:F", 10)
    worksheet_data.set_column("G:G", 10)

    provincias = Provincia.objects.all()
    arr_provincias = []
    for p in provincias:
        arr_provincias.append(p.nombre)

    worksheet_data.write_column(1, 0, arr_provincias, formato2)

    cantidad_provincias = arr_provincias.__len__()
    indice_total = cantidad_provincias + 1

    worksheet_data.write(indice_total, 0, "Total", formato)

    licenciados_sma = LicenciadosSMA.objects.filter(activo=True)

    egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=2,
                                                                          activo=True)

    sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=3,
                                                                         activo=True)

    desvinculados = Desvinculado.objects.filter(activo=True)

    tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6,
                                                             activo=True)

    obreros_calificados = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=7,
                                                                    activo=True)

    escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=8,
                                                                activo=True)

    egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(activo=True)

    egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(activo=True)

    egresados_efi = EgresadosEFI.objects.filter(activo=True)

    menores_incapacitados = Menores.objects.filter(fuente_procedencia_id=12, activo=True)

    menores_desvinculados = Menores.objects.filter(fuente_procedencia_id=13, activo=True)

    menores_dictamen = Menores.objects.filter(fuente_procedencia_id=14, activo=True)

    discapacitados = Discapacitados.objects.filter(activo=True)

    mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=17, activo=True)

    hombres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=18, activo=True)

    proxenetas = PersonasRiesgo.objects.filter(fuente_procedencia_id=19, activo=True)

    total_controlados_provincia = []
    total_mujeres_controladas_provincia = []
    total_jovenes_controlados_provincia = []
    total_ubicados_provincia = []
    total_mujeres_ubicadas_provincia = []
    total_jovenes_ubicados_provincia = []
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

    cero = []

    for provincia in provincias:
        cero.append(0)

        # CONTROLADOS
        licenciados_sma_controlados = licenciados_sma.filter(municipio_residencia__provincia=provincia).count()
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia).count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia).count()
        # egresados_universitarios_controlados = egresados_universitarios.filter(municipio_residencia__provincia=provincia).count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_controlados = menores_dictamen.filter(
            municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia).count()

        total = (
        licenciados_sma_controlados + egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + 0 +
        tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
        egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
        menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
        proxenetas_controlados)
        total_controlados_provincia.append(total)

        # MUJERES CONTROLADAS
        licenciados_sma_controlados = licenciados_sma.filter(municipio_residencia__provincia=provincia,
                                                             sexo='F').count()
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                       sexo='F').count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                     sexo='F').count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                         sexo='F').count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                           sexo='F').count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo__provincia=provincia, sexo='F').count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                             sexo='F').count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo__provincia=provincia, sexo='F').count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo__provincia=provincia, sexo='F').count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                         sexo='F').count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo__provincia=provincia, sexo='F').count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo__provincia=provincia, sexo='F').count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                               sexo='F').count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                           sexo='F').count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, sexo='F').count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, sexo='F').count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia, sexo='F').count()

        total = (
            licenciados_sma_controlados + egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + 0 +
            tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
            egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
            menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
            proxenetas_controlados)
        total_mujeres_controladas_provincia.append(total)

        # JOVENES CONTROLADOS
        licenciados_sma_controlados = licenciados_sma.filter(municipio_residencia__provincia=provincia,
                                                             edad__lte=35).exclude(edad__in=[16, 17]).count()
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                       edad__lte=35).exclude(edad__in=[16, 17]).count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                     edad__lte=35).exclude(edad__in=[16, 17]).count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                         edad__lte=35).exclude(edad__in=[16, 17]).count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                           edad__lte=35).exclude(edad__in=[16, 17]).count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo__provincia=provincia, edad__lte=35).exclude(edad__in=[16, 17]).count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                             edad__lte=35).exclude(edad__in=[16, 17]).count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo__provincia=provincia, edad__lte=35).exclude(edad__in=[16, 17]).count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo__provincia=provincia, edad__lte=35).exclude(edad__in=[16, 17]).count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                         edad__lte=35).exclude(edad__in=[16, 17]).count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo__provincia=provincia, edad__lte=35).exclude(edad__in=[16, 17]).count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo__provincia=provincia, edad__lte=35).exclude(edad__in=[16, 17]).count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                               edad__lte=35).exclude(edad__in=[16, 17]).count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                           edad__lte=35).exclude(edad__in=[16, 17]).count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, edad__lte=35).exclude(edad__in=[16, 17]).count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, edad__lte=35).exclude(edad__in=[16, 17]).count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia,
                                                   edad__lte=35).exclude(edad__in=[16, 17]).count()

        total = (
            licenciados_sma_controlados + egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + 0 +
            tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
            egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
            menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
            proxenetas_controlados)
        total_jovenes_controlados_provincia.append(total)

        # UBICADOS
        licenciados_sma_controlados = licenciados_sma.filter(municipio_residencia__provincia=provincia).count()
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                       ubicado=True).count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                     ubicado=True).count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=True).count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True).count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=True).count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=True).count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=True).count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True).count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia,
                                                   ubicado=True).count()

        total = (
            licenciados_sma_controlados + egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + 0 +
            tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
            egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
            menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
            proxenetas_controlados)
        total_ubicados_provincia.append(total)

        # MUJERES UBICADAS
        licenciados_sma_controlados = licenciados_sma.filter(municipio_residencia__provincia=provincia,
                                                             sexo='F').count()
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                       ubicado=True, sexo='F').count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                     ubicado=True, sexo='F').count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=True, sexo='F').count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True, sexo='F').count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, sexo='F').count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=True, sexo='F').count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, sexo='F').count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, sexo='F').count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=True, sexo='F').count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, sexo='F').count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, sexo='F').count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=True, sexo='F').count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True, sexo='F').count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, sexo='F').count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, sexo='F').count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                   sexo='F').count()

        total = (
            licenciados_sma_controlados + egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + 0 +
            tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
            egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
            menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
            proxenetas_controlados)
        total_mujeres_ubicadas_provincia.append(total)

        # JOVENES UBICADOS
        licenciados_sma_controlados = licenciados_sma.filter(municipio_residencia__provincia=provincia,
                                                             edad__lte=35).count()
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                       ubicado=True, edad__lte=35).count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                     ubicado=True, edad__lte=35).count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=True, edad__lte=35).count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True, edad__lte=35).count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, edad__lte=35).count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=True, edad__lte=35).count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, edad__lte=35).count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, edad__lte=35).count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=True, edad__lte=35).count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, edad__lte=35).count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, edad__lte=35).count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=True, edad__lte=35).count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True, edad__lte=35).count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, edad__lte=35).count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo__provincia=provincia, ubicado=True, edad__lte=35).count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                   edad__lte=35).count()

        total = (
            licenciados_sma_controlados + egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + 0 +
            tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
            egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
            menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
            proxenetas_controlados)
        total_jovenes_ubicados_provincia.append(total)

        # UBICADOS: Licenciados del SMA
        total_licenciados_sma_provincias.append(
            licenciados_sma.filter(municipio_residencia__provincia=provincia).count())

        # UBICADOS: Egresados de establecimientos penitenciarios
        total_egresados_ep_provincias.append(
            egresados_ep.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: SANCIONADOS
        total_sancionados_provincias.append(
            sancionados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: DESVINCULADOS
        total_desvinculados_provincias.append(
            desvinculados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Tecnicos medios
        total_tecnicos_medio_provincias.append(
            tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Egresados obreros calificados
        total_obreros_calificados_provincias.append(
            obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Egresados escuelas de oficio
        total_escuela_oficio_provincias.append(
            escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Egresados de escuelas especiales
        total_egresados_esc_especiales_provincias.append(
            egresados_escuelas_especiales.filter(municipio_solicita_empleo__provincia=provincia,
                                                 ubicado=True).count())

        # UBICADOS: Egresados de escuelas de conducta
        total_egresados_esc_conducta_provincias.append(
            egresados_escuelas_conducta.filter(municipio_solicita_empleo__provincia=provincia,
                                               ubicado=True).count())

        # UBICADOS: Egresados de la EFI
        total_egresados_efi_provincias.append(
            egresados_efi.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Menores incapacitados para el estudio por dictamen médico
        total_menores_incapacitados_provincias.append(
            menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Menores desvinculados del SNE por bajo rendimiento
        total_menores_desvinculados_provincias.append(
            menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Menores con dictamen del CDO-MININT
        total_menores_dictamen_provincias.append(
            menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Personas con discapacidad
        total_discapacitados_provincias.append(
            discapacitados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Mujeres de riesgo controladas por al PNR
        total_mueres_riesgo_pnr_provincias.append(
            mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Hombres de riesgo controlados por al PNR
        total_hombres_riesgo_pnr_provincias.append(
            hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

        # UBICADOS: Proxenetas de riesgo controlados por la PNR
        total_proxenetas_riesgo_pnr_provincias.append(
            proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count())

    worksheet_data.write_column(1, 1, total_controlados_provincia, formato2)
    worksheet_data.write_column(1, 2, total_mujeres_controladas_provincia, formato2)
    worksheet_data.write_column(1, 3, total_jovenes_controlados_provincia, formato2)
    worksheet_data.write_column(1, 4, total_ubicados_provincia, formato2)
    worksheet_data.write_column(1, 5, total_mujeres_ubicadas_provincia, formato2)
    worksheet_data.write_column(1, 6, total_jovenes_ubicados_provincia, formato2)
    worksheet_data.write_column(1, 7, total_licenciados_sma_provincias, formato2)
    worksheet_data.write_column(1, 8, total_egresados_ep_provincias, formato2)
    worksheet_data.write_column(1, 9, total_sancionados_provincias, formato2)
    worksheet_data.write_column(1, 10, total_desvinculados_provincias, formato2)
    worksheet_data.write_column(1, 11, cero, formato2)  # UBICADOS: Egresados Universitarios
    worksheet_data.write_column(1, 12, total_tecnicos_medio_provincias, formato2)
    worksheet_data.write_column(1, 13, total_obreros_calificados_provincias, formato2)
    worksheet_data.write_column(1, 14, total_escuela_oficio_provincias, formato2)
    worksheet_data.write_column(1, 15, total_egresados_esc_especiales_provincias, formato2)
    worksheet_data.write_column(1, 16, total_egresados_esc_conducta_provincias, formato2)
    worksheet_data.write_column(1, 17, total_egresados_efi_provincias, formato2)
    worksheet_data.write_column(1, 18, total_menores_incapacitados_provincias, formato2)
    worksheet_data.write_column(1, 19, total_menores_desvinculados_provincias, formato2)
    worksheet_data.write_column(1, 20, total_menores_dictamen_provincias, formato2)
    worksheet_data.write_column(1, 21, total_discapacitados_provincias, formato2)
    worksheet_data.write_column(1, 22, total_mueres_riesgo_pnr_provincias, formato2)
    worksheet_data.write_column(1, 23, total_hombres_riesgo_pnr_provincias, formato2)
    worksheet_data.write_column(1, 24, total_proxenetas_riesgo_pnr_provincias, formato2)

    # ------------ SUMAS ABAJO-------------------

    sumas = []
    for a in range(1, 25):
        total = '=SUM(%s)' % xl_range(1, a, cantidad_provincias, a)
        sumas.append(total)

    indice_sumas = 1
    for suma in sumas:
        worksheet_data.write(17, indice_sumas, suma, formato2)
        indice_sumas = indice_sumas + 1

    # ------------ SUMAS ARRIBA-------------------
    sumas2 = []
    inicio = 7
    cant = cantidad_provincias + 1
    posicion1 = cantidad_fuentes + inicio - 1
    for i in range(1, cant):
        total2 = '=SUM(%s)' % xl_range(i, inicio, i, posicion1)
        sumas2.append(total2)

    indice_sumas = 1
    posicion2 = inicio + cantidad_fuentes
    for suma in sumas2:
        worksheet_data.write(indice_sumas, posicion2, suma, formato2)
        indice_sumas = indice_sumas + 1

    book.close()
    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
