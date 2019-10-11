# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range

from SGMGU.models import *
from SGMGU.views.utiles import permission_required


@login_required()
@permission_required(['administrador'])
def comportamiento_figuras_priorizadas_general_provincias(request):
    anno_actual = datetime.today().year
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Reporte_General_por_Provincias._Comportamiento_de_las_figuras_priorizadas_(ubicados_y_pendientes)(%s).xlsx" % (
        anno_actual)
    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Provincias", formato)
    worksheet_data.write("B1", "Controlados", formato)
    worksheet_data.write("C1", "Ubicados", formato)
    worksheet_data.write("D1", "Sector Estatal", formato)
    worksheet_data.write("E1", "TPCP", formato)
    worksheet_data.write("F1", "DL 300", formato)
    worksheet_data.write("G1", "SMA", formato)
    worksheet_data.write("H1", "Otro no estatal", formato)
    worksheet_data.write("I1", "No ubicados", formato)

    causales_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    indice = 9

    for causa in causales_no_ubicado:
        worksheet_data.write(0, indice, causa.causa, formato)
        indice = indice + 1

    worksheet_data.set_column("A:A", 54)
    worksheet_data.set_column("B:B", 11)
    worksheet_data.set_column("C:C", 8.43)
    worksheet_data.set_column("D:D", 12.14)
    worksheet_data.set_column("E:E", 6)
    worksheet_data.set_column("F:F", 5.86)
    worksheet_data.set_column("G:G", 6)
    worksheet_data.set_column("H:H", 13.57)
    worksheet_data.set_column("I:I", 9.29)

    provincias = Provincia.objects.all()
    arr_provincias = []
    for p in provincias:
        arr_provincias.append(p.nombre)
    provincias.order_by('-nombre')

    worksheet_data.write_column(1, 0, arr_provincias, formato2)

    licenciados_sma = LicenciadosSMA.objects.filter(fecha_registro__year=anno_actual, recibio_oferta=True, acepto_oferta='S').exclude(causa_baja=5)
    egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=2, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=3, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    desvinculados = Desvinculado.objects.filter(fecha_registro__year=anno_actual).exclude(causa_baja=5)
    egresados_universitarios = UbicacionLaboral.objects.filter(anno_graduado=anno_actual)
    tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    obreros_calificados = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=7, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=8, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(fecha_registro__year=anno_actual).exclude(causa_baja=5)
    egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(fecha_registro__year=anno_actual).exclude(causa_baja=5)
    egresados_efi = EgresadosEFI.objects.filter(fecha_registro__year=anno_actual).exclude(causa_baja=5)
    menores_incapacitados = Menores.objects.filter(fuente_procedencia_id=12, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    menores_desvinculados = Menores.objects.filter(fuente_procedencia_id=13, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    menores_dictamen = Menores.objects.filter(fuente_procedencia_id=14, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    discapacitados = Discapacitados.objects.filter(fecha_registro__year=anno_actual).exclude(causa_baja=5)
    mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=17, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    hombres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=18, fecha_registro__year=anno_actual).exclude(causa_baja=5)
    proxenetas = PersonasRiesgo.objects.filter(fuente_procedencia_id=19, fecha_registro__year=anno_actual).exclude(causa_baja=5)

    # CONTROLADOS
    total_controlados_provincia = []

    for provincia in provincias:
        licenciados_sma_controlados = licenciados_sma.filter(municipio_residencia__provincia=provincia).count()
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia).count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia).count()
        egresados_universitarios_controlados = egresados_universitarios.filter(municipio_residencia__provincia=provincia).count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_controlados = obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_controlados = menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_controlados = menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia).count()

        total = (licenciados_sma_controlados + egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + egresados_universitarios_controlados +
                 tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
                 egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
                 menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
                 proxenetas_controlados)
        total_controlados_provincia.append(total)
    worksheet_data.write_column(1, 1, total_controlados_provincia, formato2)

    # UBICADOS
    total_ubicados_provincias = []
    for provincia in provincias:
        licenciados_sma_ubicados = licenciados_sma.filter(recibio_oferta=True, municipio_residencia__provincia=provincia).count()
        egresados_ep_ubicados = egresados_ep.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_ubicados = sancionados.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_ubicados = desvinculados.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        egresados_universitarios_ubicados = egresados_universitarios.filter(municipio_residencia__provincia=provincia).count()
        tecnicos_medio_ubicados = tecnicos_medio.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_ubicados = obreros_calificados.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_ubicados = escuelas_oficio.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_ubicados = egresados_escuelas_especiales.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_ubicados = egresados_escuelas_conducta.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_ubicados = egresados_efi.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_ubicados = menores_incapacitados.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_ubicados = menores_desvinculados.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_ubicados = menores_dictamen.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_ubicados = discapacitados.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_ubicados = mujeres_riesgo_pnr.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_ubicados = hombres_riesgo_pnr.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_ubicados = proxenetas.filter(ubicado=True, municipio_solicita_empleo__provincia=provincia).count()

        total = (licenciados_sma_ubicados + egresados_ep_ubicados + sancionados_ubicados + desvinculados_ubicados + egresados_universitarios_ubicados +
                tecnicos_medio_ubicados + obreros_calificados_ubicados + escuelas_oficio_ubicados + egresados_escuelas_especiales_ubicados +
                egresados_escuelas_conducta_ubicados + egresados_efi_ubicados + menores_incapacitados_ubicados + menores_desvinculados_ubicados +
                menores_dictamen_ubicados + discapacitados_ubicados + mujeres_riesgo_pnr_ubicados + hombres_riesgo_pnr_ubicados +
                proxenetas_ubicados)
        total_ubicados_provincias.append(total)
    worksheet_data.write_column(1, 2, total_ubicados_provincias, formato2)


    # EMPLEO ESTATAL
    total_empleo_estatal_provincias = []
    for provincia in provincias:
        licenciados_sma_empleo_estatal = licenciados_sma.filter(ubicacion_id=1, municipio_residencia__provincia=provincia).count()
        egresados_ep_empleo_estatal = egresados_ep.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_empleo_estatal = sancionados.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_empleo_estatal = desvinculados.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        egresados_universitarios_empleo_estatal = egresados_universitarios.filter(municipio_residencia__provincia=provincia).count()
        tecnicos_medio_empleo_estatal = tecnicos_medio.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_empleo_estatal = obreros_calificados.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_empleo_estatal = escuelas_oficio.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_empleo_estatal = egresados_escuelas_especiales.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_empleo_estatal = egresados_escuelas_conducta.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_empleo_estatal = egresados_efi.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_empleo_estatal = menores_incapacitados.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_empleo_estatal = menores_desvinculados.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_empleo_estatal = menores_dictamen.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_empleo_estatal = discapacitados.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_empleo_estatal = mujeres_riesgo_pnr.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_empleo_estatal = hombres_riesgo_pnr.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_empleo_estatal = proxenetas.filter(ubicacion_id=1, municipio_solicita_empleo__provincia=provincia).count()

        total = (licenciados_sma_empleo_estatal + egresados_ep_empleo_estatal + sancionados_empleo_estatal + desvinculados_empleo_estatal + egresados_universitarios_empleo_estatal +
                tecnicos_medio_empleo_estatal + obreros_calificados_empleo_estatal + escuelas_oficio_empleo_estatal + egresados_escuelas_especiales_empleo_estatal +
                egresados_escuelas_conducta_empleo_estatal + egresados_efi_empleo_estatal + menores_incapacitados_empleo_estatal + menores_desvinculados_empleo_estatal +
                menores_dictamen_empleo_estatal + discapacitados_empleo_estatal + mujeres_riesgo_pnr_empleo_estatal + hombres_riesgo_pnr_empleo_estatal +
                proxenetas_empleo_estatal)
        total_empleo_estatal_provincias.append(total)
    worksheet_data.write_column(1, 3, total_empleo_estatal_provincias, formato2)

    # TPCP
    total_tpcp_provincias = []

    for provincia in provincias:
        licenciados_sma_tpcp = licenciados_sma.filter(ubicacion_id=2, municipio_residencia__provincia=provincia).count()
        egresados_ep_tpcp = egresados_ep.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_tpcp = sancionados.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_tpcp = desvinculados.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_tpcp = tecnicos_medio.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_tpcp = obreros_calificados.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_tpcp = escuelas_oficio.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_tpcp = egresados_escuelas_especiales.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_tpcp = egresados_escuelas_conducta.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_tpcp = egresados_efi.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_tpcp = menores_incapacitados.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_tpcp = menores_desvinculados.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_tpcp = menores_dictamen.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_tpcp = discapacitados.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_tpcp = mujeres_riesgo_pnr.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_tpcp = hombres_riesgo_pnr.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_tpcp = proxenetas.filter(ubicacion_id=2, municipio_solicita_empleo__provincia=provincia).count()

        total = (licenciados_sma_tpcp + egresados_ep_tpcp + sancionados_tpcp + desvinculados_tpcp +
                tecnicos_medio_tpcp + obreros_calificados_tpcp + escuelas_oficio_tpcp + egresados_escuelas_especiales_tpcp +
                egresados_escuelas_conducta_tpcp + egresados_efi_tpcp + menores_incapacitados_tpcp + menores_desvinculados_tpcp +
                menores_dictamen_tpcp + discapacitados_tpcp + mujeres_riesgo_pnr_tpcp + hombres_riesgo_pnr_tpcp +
                proxenetas_tpcp)
        total_tpcp_provincias.append(total)

    worksheet_data.write_column(1, 4, total_tpcp_provincias, formato2)

    # DL 300
    total_dl300_provincias = []

    for provincia in provincias:
        licenciados_sma_dl300 = licenciados_sma.filter(ubicacion_id=3, municipio_residencia__provincia=provincia).count()
        egresados_ep_dl300 = egresados_ep.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_dl300 = sancionados.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_dl300 = desvinculados.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_dl300 = tecnicos_medio.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_dl300 = obreros_calificados.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_dl300 = escuelas_oficio.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_dl300 = egresados_escuelas_especiales.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_dl300 = egresados_escuelas_conducta.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_dl300 = egresados_efi.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_dl300 = menores_incapacitados.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_dl300 = menores_desvinculados.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_dl300 = menores_dictamen.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_dl300 = discapacitados.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_dl300 = mujeres_riesgo_pnr.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_dl300 = hombres_riesgo_pnr.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_dl300 = proxenetas.filter(ubicacion_id=3, municipio_solicita_empleo__provincia=provincia).count()

        total = (licenciados_sma_dl300 + egresados_ep_dl300 + sancionados_dl300 + desvinculados_dl300 +
                 tecnicos_medio_dl300 + obreros_calificados_dl300 + escuelas_oficio_dl300 + egresados_escuelas_especiales_dl300 +
                 egresados_escuelas_conducta_dl300 + egresados_efi_dl300 + menores_incapacitados_dl300 + menores_desvinculados_dl300 +
                 menores_dictamen_dl300 + discapacitados_dl300 + mujeres_riesgo_pnr_dl300 + hombres_riesgo_pnr_dl300 +
                 proxenetas_dl300)
        total_dl300_provincias.append(total)

    worksheet_data.write_column(1, 5, total_dl300_provincias, formato2)

    # SMA
    total_sma_provincias = []

    for provincia in provincias:
        licenciados_sma_sma = licenciados_sma.filter(ubicacion_id=5, municipio_residencia__provincia=provincia).count()
        egresados_ep_sma = egresados_ep.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_sma = sancionados.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_sma = desvinculados.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_sma = tecnicos_medio.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_sma = obreros_calificados.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_sma = escuelas_oficio.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_sma = egresados_escuelas_especiales.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_sma = egresados_escuelas_conducta.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_sma = egresados_efi.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_sma = menores_incapacitados.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_sma = menores_desvinculados.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_sma = menores_dictamen.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_sma = discapacitados.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_sma = mujeres_riesgo_pnr.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_sma = hombres_riesgo_pnr.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_sma = proxenetas.filter(ubicacion_id=5, municipio_solicita_empleo__provincia=provincia).count()

        total = (licenciados_sma_sma + egresados_ep_sma + sancionados_sma + desvinculados_sma +
                 tecnicos_medio_sma + obreros_calificados_sma + escuelas_oficio_sma + egresados_escuelas_especiales_sma +
                 egresados_escuelas_conducta_sma + egresados_efi_sma + menores_incapacitados_sma + menores_desvinculados_sma +
                 menores_dictamen_sma + discapacitados_sma + mujeres_riesgo_pnr_sma + hombres_riesgo_pnr_sma +
                 proxenetas_sma)
        total_sma_provincias.append(total)

    worksheet_data.write_column(1, 6, total_sma_provincias, formato2)

    # OTRA NO ESTATAL
    total_otra_no_estatal_provincias = []

    for provincia in provincias:
        licenciados_sma_otra_no_estatal = licenciados_sma.filter(ubicacion_id=4, municipio_residencia__provincia=provincia).count()
        egresados_ep_otra_no_estatal = egresados_ep.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_otra_no_estatal = sancionados.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_otra_no_estatal = desvinculados.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_otra_no_estatal = tecnicos_medio.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_otra_no_estatal = obreros_calificados.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_otra_no_estatal = escuelas_oficio.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_otra_no_estatal = egresados_escuelas_especiales.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_otra_no_estatal = egresados_escuelas_conducta.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_otra_no_estatal = egresados_efi.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_otra_no_estatal = menores_incapacitados.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_otra_no_estatal = menores_desvinculados.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_otra_no_estatal = menores_dictamen.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_otra_no_estatal = discapacitados.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_otra_no_estatal = mujeres_riesgo_pnr.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_otra_no_estatal = hombres_riesgo_pnr.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_otra_no_estatal = proxenetas.filter(ubicacion_id=4, municipio_solicita_empleo__provincia=provincia).count()

        total = (licenciados_sma_otra_no_estatal + egresados_ep_otra_no_estatal + sancionados_otra_no_estatal + desvinculados_otra_no_estatal +
                 tecnicos_medio_otra_no_estatal + obreros_calificados_otra_no_estatal + escuelas_oficio_otra_no_estatal + egresados_escuelas_especiales_otra_no_estatal +
                 egresados_escuelas_conducta_otra_no_estatal + egresados_efi_otra_no_estatal + menores_incapacitados_otra_no_estatal + menores_desvinculados_otra_no_estatal +
                 menores_dictamen_otra_no_estatal + discapacitados_otra_no_estatal + mujeres_riesgo_pnr_otra_no_estatal + hombres_riesgo_pnr_otra_no_estatal +
                 proxenetas_otra_no_estatal)
        total_otra_no_estatal_provincias.append(total)

    worksheet_data.write_column(1, 7, total_otra_no_estatal_provincias, formato2)

    # NO UBICADOS
    total_no_ubicados_provincias = []

    for provincia in provincias:
        egresados_ep_no_ubicados = egresados_ep.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_no_ubicados = sancionados.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_no_ubicados = desvinculados.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_no_ubicados = tecnicos_medio.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_no_ubicados = obreros_calificados.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_no_ubicados = escuelas_oficio.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_no_ubicados = egresados_escuelas_especiales.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_no_ubicados = egresados_escuelas_conducta.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_no_ubicados = egresados_efi.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_no_ubicados = menores_incapacitados.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_no_ubicados = menores_desvinculados.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_no_ubicados = menores_dictamen.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_no_ubicados = discapacitados.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_no_ubicados = mujeres_riesgo_pnr.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_no_ubicados = hombres_riesgo_pnr.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_no_ubicados = proxenetas.filter(ubicado=False, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_no_ubicados + sancionados_no_ubicados + desvinculados_no_ubicados +
                 tecnicos_medio_no_ubicados + obreros_calificados_no_ubicados + escuelas_oficio_no_ubicados + egresados_escuelas_especiales_no_ubicados +
                 egresados_escuelas_conducta_no_ubicados + egresados_efi_no_ubicados + menores_incapacitados_no_ubicados + menores_desvinculados_no_ubicados +
                 menores_dictamen_no_ubicados + discapacitados_no_ubicados + mujeres_riesgo_pnr_no_ubicados + hombres_riesgo_pnr_no_ubicados +
                 proxenetas_no_ubicados)
        total_no_ubicados_provincias.append(total)

    worksheet_data.write_column(1, 8, total_no_ubicados_provincias, formato2)

    # NO EXISTE OFERTA DE EMPLEO
    total_no_existe_oferta_provincias = []

    for provincia in provincias:
        egresados_ep_no_existe_oferta = egresados_ep.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_no_existe_oferta = sancionados.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_no_existe_oferta = desvinculados.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_no_existe_oferta = tecnicos_medio.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_no_existe_oferta = obreros_calificados.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_no_existe_oferta = escuelas_oficio.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_no_existe_oferta = egresados_escuelas_especiales.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_no_existe_oferta = egresados_escuelas_conducta.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_no_existe_oferta = egresados_efi.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_no_existe_oferta = menores_incapacitados.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_no_existe_oferta = menores_desvinculados.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_no_existe_oferta = menores_dictamen.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_no_existe_oferta = discapacitados.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_no_existe_oferta = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_no_existe_oferta = hombres_riesgo_pnr.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_no_existe_oferta = proxenetas.filter(causa_no_ubicado_id=1, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_no_existe_oferta + sancionados_no_existe_oferta + desvinculados_no_existe_oferta +
                 tecnicos_medio_no_existe_oferta + obreros_calificados_no_existe_oferta + escuelas_oficio_no_existe_oferta + egresados_escuelas_especiales_no_existe_oferta +
                 egresados_escuelas_conducta_no_existe_oferta + egresados_efi_no_existe_oferta + menores_incapacitados_no_existe_oferta + menores_desvinculados_no_existe_oferta +
                 menores_dictamen_no_existe_oferta + discapacitados_no_existe_oferta + mujeres_riesgo_pnr_no_existe_oferta + hombres_riesgo_pnr_no_existe_oferta +
                 proxenetas_no_existe_oferta)
        total_no_existe_oferta_provincias.append(total)

    worksheet_data.write_column(1, 9, total_no_existe_oferta_provincias, formato2)

    # NO LE GUSTA LAS OFERTAS QUE HAY
    total_no_le_gustan_provincias = []

    for provincia in provincias:
        egresados_ep_no_le_gustan = egresados_ep.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_no_le_gustan = sancionados.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_no_le_gustan = desvinculados.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_no_le_gustan = tecnicos_medio.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_no_le_gustan = obreros_calificados.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_no_le_gustan = escuelas_oficio.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_no_le_gustan = egresados_escuelas_especiales.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_no_le_gustan = egresados_escuelas_conducta.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_no_le_gustan = egresados_efi.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_no_le_gustan = menores_incapacitados.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_no_le_gustan = menores_desvinculados.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_no_le_gustan = menores_dictamen.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_no_le_gustan = discapacitados.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_no_le_gustan = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_no_le_gustan = hombres_riesgo_pnr.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_no_le_gustan = proxenetas.filter(causa_no_ubicado_id=2, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_no_le_gustan + sancionados_no_le_gustan + desvinculados_no_le_gustan +
                 tecnicos_medio_no_le_gustan + obreros_calificados_no_le_gustan + escuelas_oficio_no_le_gustan + egresados_escuelas_especiales_no_le_gustan +
                 egresados_escuelas_conducta_no_le_gustan + egresados_efi_no_le_gustan + menores_incapacitados_no_le_gustan + menores_desvinculados_no_le_gustan +
                 menores_dictamen_no_le_gustan + discapacitados_no_le_gustan + mujeres_riesgo_pnr_no_le_gustan + hombres_riesgo_pnr_no_le_gustan +
                 proxenetas_no_le_gustan)

        total_no_le_gustan_provincias.append(total)

    worksheet_data.write_column(1, 10, total_no_le_gustan_provincias, formato2)

    # INCAPACITADO TEMPORALMENTE PARA EL EMPLEO (MENOS DE 1 AÑO)
    total_incapacitado_provincias = []

    for provincia in provincias:
        egresados_ep_incapacitado = egresados_ep.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_incapacitado = sancionados.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_incapacitado = desvinculados.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_incapacitado = tecnicos_medio.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_incapacitado = obreros_calificados.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_incapacitado = escuelas_oficio.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_incapacitado = egresados_escuelas_especiales.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_incapacitado = egresados_escuelas_conducta.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_incapacitado = egresados_efi.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_incapacitado = menores_incapacitados.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_incapacitado = menores_desvinculados.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_incapacitado = menores_dictamen.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_incapacitado = discapacitados.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_incapacitado = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_incapacitado = hombres_riesgo_pnr.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_incapacitado = proxenetas.filter(causa_no_ubicado_id=3, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_incapacitado + sancionados_incapacitado + desvinculados_incapacitado +
                 tecnicos_medio_incapacitado + obreros_calificados_incapacitado + escuelas_oficio_incapacitado + egresados_escuelas_especiales_incapacitado +
                 egresados_escuelas_conducta_incapacitado + egresados_efi_incapacitado + menores_incapacitados_incapacitado + menores_desvinculados_incapacitado +
                 menores_dictamen_incapacitado + discapacitados_incapacitado + mujeres_riesgo_pnr_incapacitado + hombres_riesgo_pnr_incapacitado +
                 proxenetas_incapacitado)
        total_incapacitado_provincias.append(total)

    worksheet_data.write_column(1, 11, total_incapacitado_provincias, formato2)

    # SANCIONADOS POR LOS TRIBUNALES
    total_sancionados_provincias = []

    for provincia in provincias:
        egresados_ep_sancionados = egresados_ep.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_sancionados = sancionados.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_sancionados = desvinculados.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_sancionados = tecnicos_medio.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_sancionados = obreros_calificados.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_sancionados = escuelas_oficio.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_sancionados = egresados_escuelas_especiales.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_sancionados = egresados_escuelas_conducta.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_sancionados = egresados_efi.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_sancionados = menores_incapacitados.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_sancionados = menores_desvinculados.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_sancionados = menores_dictamen.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_sancionados = discapacitados.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_sancionados = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_sancionados = hombres_riesgo_pnr.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_sancionados = proxenetas.filter(causa_no_ubicado_id=4, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_sancionados + sancionados_sancionados + desvinculados_sancionados +
                 tecnicos_medio_sancionados + obreros_calificados_sancionados + escuelas_oficio_sancionados + egresados_escuelas_especiales_sancionados +
                 egresados_escuelas_conducta_sancionados + egresados_efi_sancionados + menores_incapacitados_sancionados + menores_desvinculados_sancionados +
                 menores_dictamen_sancionados + discapacitados_sancionados + mujeres_riesgo_pnr_sancionados + hombres_riesgo_pnr_sancionados +
                 proxenetas_sancionados)
        total_sancionados_provincias.append(total)

    worksheet_data.write_column(1, 12, total_sancionados_provincias, formato2)

    # NO ESTA INTERESADO EN TRABAJAR
    total_no_interesados_provincias = []

    for provincia in provincias:
        egresados_ep_no_interesados = egresados_ep.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_no_interesados = sancionados.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_no_interesados = desvinculados.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_no_interesados = tecnicos_medio.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_no_interesados = obreros_calificados.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_no_interesados = escuelas_oficio.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_no_interesados = egresados_escuelas_especiales.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_no_interesados = egresados_escuelas_conducta.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_no_interesados = egresados_efi.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_no_interesados = menores_incapacitados.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_no_interesados = menores_desvinculados.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_no_interesados = menores_dictamen.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_no_interesados = discapacitados.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_no_interesados = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_no_interesados = hombres_riesgo_pnr.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_no_interesados = proxenetas.filter(causa_no_ubicado_id=5, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_no_interesados + sancionados_no_interesados + desvinculados_no_interesados +
                 tecnicos_medio_no_interesados + obreros_calificados_no_interesados + escuelas_oficio_no_interesados + egresados_escuelas_especiales_no_interesados +
                 egresados_escuelas_conducta_no_interesados + egresados_efi_no_interesados + menores_incapacitados_no_interesados + menores_desvinculados_no_interesados +
                 menores_dictamen_no_interesados + discapacitados_no_interesados + mujeres_riesgo_pnr_no_interesados + hombres_riesgo_pnr_no_interesados +
                 proxenetas_no_interesados)
        total_no_interesados_provincias.append(total)

    worksheet_data.write_column(1, 13, total_no_interesados_provincias, formato2)

    # TRAMITE DE TRASLADO DE PROVINCIA O MUNICIPIO
    total_tramite_traslado_provincias = []

    for provincia in provincias:
        egresados_ep_tramite_traslado = egresados_ep.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_tramite_traslado = sancionados.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_tramite_traslado = desvinculados.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_tramite_traslado = tecnicos_medio.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_tramite_traslado = obreros_calificados.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_tramite_traslado = escuelas_oficio.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_tramite_traslado = egresados_escuelas_especiales.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_tramite_traslado = egresados_escuelas_conducta.filter(causa_no_ubicado_id=6).count()
        egresados_efi_tramite_traslado = egresados_efi.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_tramite_traslado = menores_incapacitados.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_tramite_traslado = menores_desvinculados.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_tramite_traslado = menores_dictamen.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_tramite_traslado = discapacitados.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_tramite_traslado = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_tramite_traslado = hombres_riesgo_pnr.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_tramite_traslado = proxenetas.filter(causa_no_ubicado_id=6, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_tramite_traslado + sancionados_tramite_traslado + desvinculados_tramite_traslado +
                 tecnicos_medio_tramite_traslado + obreros_calificados_tramite_traslado + escuelas_oficio_tramite_traslado + egresados_escuelas_especiales_tramite_traslado +
                 egresados_escuelas_conducta_tramite_traslado + egresados_efi_tramite_traslado + menores_incapacitados_tramite_traslado + menores_desvinculados_tramite_traslado +
                 menores_dictamen_tramite_traslado + discapacitados_tramite_traslado + mujeres_riesgo_pnr_tramite_traslado + hombres_riesgo_pnr_tramite_traslado +
                 proxenetas_tramite_traslado)
        total_tramite_traslado_provincias.append(total)

    worksheet_data.write_column(1, 14, total_tramite_traslado_provincias, formato2)

    # NO AUTORIZADO POR LOS PADRES
    total_no_autorizado_padres_provincias = []

    for provincia in provincias:
        egresados_ep_no_autorizado_padres = egresados_ep.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_no_autorizado_padres = sancionados.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_no_autorizado_padres = desvinculados.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_no_autorizado_padres = tecnicos_medio.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_no_autorizado_padres = obreros_calificados.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_no_autorizado_padres = escuelas_oficio.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_no_autorizado_padres = egresados_escuelas_especiales.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_no_autorizado_padres = egresados_escuelas_conducta.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_no_autorizado_padres = egresados_efi.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_no_autorizado_padres = menores_incapacitados.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_no_autorizado_padres = menores_desvinculados.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_no_autorizado_padres = menores_dictamen.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_no_autorizado_padres = discapacitados.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_no_autorizado_padres = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_no_autorizado_padres = hombres_riesgo_pnr.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_no_autorizado_padres = proxenetas.filter(causa_no_ubicado_id=7, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_no_autorizado_padres + sancionados_no_autorizado_padres + desvinculados_no_autorizado_padres +
                 tecnicos_medio_no_autorizado_padres + obreros_calificados_no_autorizado_padres + escuelas_oficio_no_autorizado_padres + egresados_escuelas_especiales_no_autorizado_padres +
                 egresados_escuelas_conducta_no_autorizado_padres + egresados_efi_no_autorizado_padres + menores_incapacitados_no_autorizado_padres + menores_desvinculados_no_autorizado_padres +
                 menores_dictamen_no_autorizado_padres + discapacitados_no_autorizado_padres + mujeres_riesgo_pnr_no_autorizado_padres + hombres_riesgo_pnr_no_autorizado_padres +
                 proxenetas_no_autorizado_padres)
        total_no_autorizado_padres_provincias.append(total)

    worksheet_data.write_column(1, 15, total_no_autorizado_padres_provincias, formato2)

    # AL CUIDADO DE UN FAMILIAR
    total_cuidado_familiar_provincias = []

    for provincia in provincias:
        egresados_ep_cuidado_familiar = egresados_ep.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_cuidado_familiar = sancionados.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_cuidado_familiar = desvinculados.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_cuidado_familiar = tecnicos_medio.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_cuidado_familiar = obreros_calificados.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_cuidado_familiar = escuelas_oficio.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_cuidado_familiar = egresados_escuelas_especiales.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_cuidado_familiar = egresados_escuelas_conducta.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_cuidado_familiar = egresados_efi.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_cuidado_familiar = menores_incapacitados.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_cuidado_familiar = menores_desvinculados.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_cuidado_familiar = menores_dictamen.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_cuidado_familiar = discapacitados.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_cuidado_familiar = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_cuidado_familiar = hombres_riesgo_pnr.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_cuidado_familiar = proxenetas.filter(causa_no_ubicado_id=8, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_cuidado_familiar + sancionados_cuidado_familiar + desvinculados_cuidado_familiar +
                 tecnicos_medio_cuidado_familiar + obreros_calificados_cuidado_familiar + escuelas_oficio_cuidado_familiar + egresados_escuelas_especiales_cuidado_familiar +
                 egresados_escuelas_conducta_cuidado_familiar + egresados_efi_cuidado_familiar + menores_incapacitados_cuidado_familiar + menores_desvinculados_cuidado_familiar +
                 menores_dictamen_cuidado_familiar + discapacitados_cuidado_familiar + mujeres_riesgo_pnr_cuidado_familiar + hombres_riesgo_pnr_cuidado_familiar +
                 proxenetas_cuidado_familiar)
        total_cuidado_familiar_provincias.append(total)

    worksheet_data.write_column(1, 16, total_cuidado_familiar_provincias, formato2)

    # NO HAY OFERTAS ACORDE A SU DISCAPACIDAD
    total_no_ofertas_acorde_discapacidad_provincias = []

    for provincia in provincias:
        egresados_ep_no_ofertas_acorde_discapacidad = egresados_ep.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_no_ofertas_acorde_discapacidad = sancionados.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_no_ofertas_acorde_discapacidad = desvinculados.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_no_ofertas_acorde_discapacidad = tecnicos_medio.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_no_ofertas_acorde_discapacidad = obreros_calificados.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_no_ofertas_acorde_discapacidad = escuelas_oficio.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_no_ofertas_acorde_discapacidad = egresados_escuelas_especiales.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_no_ofertas_acorde_discapacidad = egresados_escuelas_conducta.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_no_ofertas_acorde_discapacidad = egresados_efi.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_no_ofertas_acorde_discapacidad = menores_incapacitados.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_no_ofertas_acorde_discapacidad = menores_desvinculados.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_no_ofertas_acorde_discapacidad = menores_dictamen.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_no_ofertas_acorde_discapacidad = discapacitados.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_no_ofertas_acorde_discapacidad = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_no_ofertas_acorde_discapacidad = hombres_riesgo_pnr.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_no_ofertas_acorde_discapacidad = proxenetas.filter(causa_no_ubicado_id=9, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_no_ofertas_acorde_discapacidad + sancionados_no_ofertas_acorde_discapacidad + desvinculados_no_ofertas_acorde_discapacidad +
                 tecnicos_medio_no_ofertas_acorde_discapacidad + obreros_calificados_no_ofertas_acorde_discapacidad + escuelas_oficio_no_ofertas_acorde_discapacidad + egresados_escuelas_especiales_no_ofertas_acorde_discapacidad +
                 egresados_escuelas_conducta_no_ofertas_acorde_discapacidad + egresados_efi_no_ofertas_acorde_discapacidad + menores_incapacitados_no_ofertas_acorde_discapacidad + menores_desvinculados_no_ofertas_acorde_discapacidad +
                 menores_dictamen_no_ofertas_acorde_discapacidad + discapacitados_no_ofertas_acorde_discapacidad + mujeres_riesgo_pnr_no_ofertas_acorde_discapacidad + hombres_riesgo_pnr_no_ofertas_acorde_discapacidad +
                 proxenetas_no_ofertas_acorde_discapacidad)
        total_no_ofertas_acorde_discapacidad_provincias.append(total)

    worksheet_data.write_column(1, 17, total_no_ofertas_acorde_discapacidad_provincias, formato2)

    # LO DEJO
    total_lo_dejo_provincias = []

    for provincia in provincias:
        egresados_ep_lo_dejo = egresados_ep.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        sancionados_lo_dejo = sancionados.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        desvinculados_lo_dejo = desvinculados.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        tecnicos_medio_lo_dejo = tecnicos_medio.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        obreros_calificados_lo_dejo = obreros_calificados.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        escuelas_oficio_lo_dejo = escuelas_oficio.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_especiales_lo_dejo = egresados_escuelas_especiales.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        egresados_escuelas_conducta_lo_dejo = egresados_escuelas_conducta.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        egresados_efi_lo_dejo = egresados_efi.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        menores_incapacitados_lo_dejo = menores_incapacitados.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        menores_desvinculados_lo_dejo = menores_desvinculados.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        menores_dictamen_lo_dejo = menores_dictamen.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        discapacitados_lo_dejo = discapacitados.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        mujeres_riesgo_pnr_lo_dejo = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        hombres_riesgo_pnr_lo_dejo = hombres_riesgo_pnr.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()
        proxenetas_lo_dejo = proxenetas.filter(causa_no_ubicado_id=10, municipio_solicita_empleo__provincia=provincia).count()

        total = (egresados_ep_lo_dejo + sancionados_lo_dejo + desvinculados_lo_dejo +
                 tecnicos_medio_lo_dejo + obreros_calificados_lo_dejo + escuelas_oficio_lo_dejo + egresados_escuelas_especiales_lo_dejo +
                 egresados_escuelas_conducta_lo_dejo + egresados_efi_lo_dejo + menores_incapacitados_lo_dejo + menores_desvinculados_lo_dejo +
                 menores_dictamen_lo_dejo + discapacitados_lo_dejo + mujeres_riesgo_pnr_lo_dejo + hombres_riesgo_pnr_lo_dejo +
                 proxenetas_lo_dejo)
        total_lo_dejo_provincias.append(total)

    worksheet_data.write_column(1, 18, total_lo_dejo_provincias, formato2)

    cantidad_fuentes = arr_provincias.__len__()

    total_controlados = '=SUM(%s)' % xl_range(1, 1, cantidad_fuentes, 1)
    total_ubicados = '=SUM(%s)' % xl_range(1, 2, cantidad_fuentes, 2)
    total_empleo_estatal = '=SUM(%s)' % xl_range(1, 3, cantidad_fuentes, 3)
    total_tpcp = '=SUM(%s)' % xl_range(1, 4, cantidad_fuentes, 4)
    total_dl300 = '=SUM(%s)' % xl_range(1, 5, cantidad_fuentes, 5)
    total_sma = '=SUM(%s)' % xl_range(1, 6, cantidad_fuentes, 6)
    total_otra_no_estatal = '=SUM(%s)' % xl_range(1, 7, cantidad_fuentes, 7)
    total_no_ubicados = '=SUM(%s)' % xl_range(1, 8, cantidad_fuentes, 8)
    total_no_existe_oferta = '=SUM(%s)' % xl_range(1, 9, cantidad_fuentes, 9)
    total_no_le_gustan = '=SUM(%s)' % xl_range(1, 10, cantidad_fuentes, 10)
    total_incapacitado = '=SUM(%s)' % xl_range(1, 11, cantidad_fuentes, 11)
    total_sancionados = '=SUM(%s)' % xl_range(1, 12, cantidad_fuentes, 12)
    total_no_interesados = '=SUM(%s)' % xl_range(1, 13, cantidad_fuentes, 13)
    total_tramite_traslado = '=SUM(%s)' % xl_range(1, 14, cantidad_fuentes, 14)
    total_no_autorizado_padres = '=SUM(%s)' % xl_range(1, 15, cantidad_fuentes, 15)
    total_cuidado_familiar = '=SUM(%s)' % xl_range(1, 16, cantidad_fuentes, 16)
    total_no_ofertas_acorde_discapacidad = '=SUM(%s)' % xl_range(1, 17, cantidad_fuentes, 17)
    total_lo_dejo = '=SUM(%s)' % xl_range(1, 18, cantidad_fuentes, 18)

    indice_total = cantidad_fuentes + 1

    worksheet_data.write(indice_total, 0, "Total", formato)
    worksheet_data.write(indice_total, 1, total_controlados, formato2)
    worksheet_data.write(indice_total, 2, total_ubicados, formato2)
    worksheet_data.write(indice_total, 3, total_empleo_estatal, formato2)
    worksheet_data.write(indice_total, 4, total_tpcp, formato2)
    worksheet_data.write(indice_total, 5, total_dl300, formato2)
    worksheet_data.write(indice_total, 6, total_sma, formato2)
    worksheet_data.write(indice_total, 7, total_otra_no_estatal, formato2)
    worksheet_data.write(indice_total, 8, total_no_ubicados, formato2)
    worksheet_data.write(indice_total, 9, total_no_existe_oferta, formato2)
    worksheet_data.write(indice_total, 10, total_no_le_gustan, formato2)
    worksheet_data.write(indice_total, 11, total_incapacitado, formato2)
    worksheet_data.write(indice_total, 12, total_sancionados, formato2)
    worksheet_data.write(indice_total, 13, total_no_interesados, formato2)
    worksheet_data.write(indice_total, 14, total_tramite_traslado, formato2)
    worksheet_data.write(indice_total, 15, total_no_autorizado_padres, formato2)
    worksheet_data.write(indice_total, 16, total_cuidado_familiar, formato2)
    worksheet_data.write(indice_total, 17, total_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(indice_total, 18, total_lo_dejo, formato2)

    return response