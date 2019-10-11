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
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def comportamiento_figuras_priorizadas_organismos(request):
    start_time = time.time()

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    anno = datetime.today().year

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = "attachment; filename=Controlados_ubicados_y_pendientes_Totales_por_organismos_(%s).xlsx" % (
        anno)
    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Organismo", formato)
    worksheet_data.write("B1", "Ubicados", formato)

    fuentes_procedencia = FuenteProcedencia.objects.filter(activo=True).order_by('id')
    indice = 2

    for fuente in fuentes_procedencia:
        worksheet_data.write(0, indice, fuente.nombre, formato)
        indice = indice + 1

    worksheet_data.set_column("A:A", 75.43)
    worksheet_data.set_column("B:B", 10)

    organismos = Organismo.objects.filter(activo=True)
    arr_organismos = [organismo.nombre for organismo in organismos]

    worksheet_data.write_column(1, 0, arr_organismos, formato2)

    # Licenciados del SMA
    if categoria_usuario == 'dmt':
        licenciados_sma = LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario, activo=True)
    elif categoria_usuario == 'dpt_ee':
        licenciados_sma = LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario, activo=True)
    else:
        licenciados_sma = LicenciadosSMA.objects.filter(activo=True)

    # Egresados de Establecimientos penitenciarios
    if categoria_usuario == 'dmt':
        egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(
            municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=2,
            activo=True)
    elif categoria_usuario == 'dpt_ee':
        egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(
            municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=2,
            activo=True)
    else:
        egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(
            fuente_procedencia_id=2, activo=True)

    # Sancionados sin Internamiento
    if categoria_usuario == 'dmt':
        sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
            municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=3,
            activo=True)
    elif categoria_usuario == 'dpt_ee':
        sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
            municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=3,
            activo=True)
    else:
        sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
            fuente_procedencia_id=3, activo=True)

    # Desvinculados
    if categoria_usuario == 'dmt':
        desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                    activo=True)
    elif categoria_usuario == 'dpt_ee':
        desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                    activo=True)
    else:
        desvinculados = Desvinculado.objects.filter(activo=True)

    # Tecnicos medios
    if categoria_usuario == 'dmt':
        tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                                 fuente_procedencia_id=6,
                                                                 activo=True)
    elif categoria_usuario == 'dpt_ee':
        tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(
            municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=6,
            activo=True)
    else:
        tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6,
                                                                 activo=True)

    # Obreros calificados
    if categoria_usuario == 'dmt':
        obreros_calificados = TMedioOCalificadoEOficio.objects.filter(
            municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=7,
            activo=True)
    elif categoria_usuario == 'dpt_ee':
        obreros_calificados = TMedioOCalificadoEOficio.objects.filter(
            municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=7,
            activo=True)
    else:
        obreros_calificados = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=7,
                                                                      activo=True)

    # Escuelas de oficio
    if categoria_usuario == 'dmt':
        escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(
            municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=8,
            activo=True)
    elif categoria_usuario == 'dpt_ee':
        escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(
            municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=8,
            activo=True)
    else:
        escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=8,
                                                                  activo=True)

    # Egresados de escuelas especiales
    if categoria_usuario == 'dmt':
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
            municipio_solicita_empleo=municipio_usuario,
            activo=True)

    elif categoria_usuario == 'dpt_ee':
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
            municipio_solicita_empleo__provincia=provincia_usuario,
            activo=True)
    else:
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
            activo=True)

    # Egresados de escuelas de conducta
    if categoria_usuario == 'dmt':
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
            municipio_solicita_empleo=municipio_usuario,
            activo=True)
    elif categoria_usuario == 'dpt_ee':
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
            municipio_solicita_empleo__provincia=provincia_usuario,
            activo=True)
    else:
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
            activo=True)

    # Egresados de la EFI
    if categoria_usuario == 'dmt':
        egresados_efi = EgresadosEFI.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                    activo=True)
    elif categoria_usuario == 'dpt_ee':
        egresados_efi = EgresadosEFI.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                    activo=True)
    else:
        egresados_efi = EgresadosEFI.objects.filter(activo=True)

    # Menores incapacitados para el estudio por dictamen medico
    if categoria_usuario == 'dmt':
        menores_incapacitados = Menores.objects.filter(
            municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=12,
            activo=True)
    elif categoria_usuario == 'dpt_ee':
        menores_incapacitados = Menores.objects.filter(
            municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=12,
            activo=True)
    else:
        menores_incapacitados = Menores.objects.filter(fuente_procedencia_id=12,
                                                       activo=True)

    # Menores desvinculados del SNE por bajo rendimiento
    if categoria_usuario == 'dmt':
        menores_desvinculados = Menores.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                       fuente_procedencia_id=13,
                                                       activo=True)
    elif categoria_usuario == 'dpt_ee':
        menores_desvinculados = Menores.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                       fuente_procedencia_id=13,
                                                       activo=True)
    else:
        menores_desvinculados = Menores.objects.filter(fuente_procedencia_id=13,
                                                       activo=True)

    # Menores con dictamen del CDO-MININT
    if categoria_usuario == 'dmt':
        menores_dictamen = Menores.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                  fuente_procedencia_id=14,
                                                  activo=True)
    elif categoria_usuario == 'dpt_ee':
        menores_dictamen = Menores.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                  fuente_procedencia_id=14,
                                                  activo=True)
    else:
        menores_dictamen = Menores.objects.filter(fuente_procedencia_id=14,
                                                  activo=True)

    # Discapacitados
    if categoria_usuario == 'dmt':
        discapacitados = Discapacitados.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                       activo=True)
    elif categoria_usuario == 'dpt_ee':
        discapacitados = Discapacitados.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                       activo=True)
    else:
        discapacitados = Discapacitados.objects.filter(activo=True)

    # Mujeres de riesgo controladas por la PNR
    if categoria_usuario == 'dmt':
        mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                           fuente_procedencia_id=17,
                                                           activo=True)
    elif categoria_usuario == 'dpt_ee':
        mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                           fuente_procedencia_id=17,
                                                           activo=True)
    else:
        mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=17,
                                                           activo=True)

    # Hombres de riesgo controlados por la PNR
    if categoria_usuario == 'dmt':
        hombres_riesgo_pnr = PersonasRiesgo.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                           fuente_procedencia_id=18,
                                                           activo=True)
    elif categoria_usuario == 'dpt_ee':
        hombres_riesgo_pnr = PersonasRiesgo.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                           fuente_procedencia_id=18,
                                                           activo=True)
    else:
        hombres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=18,
                                                           activo=True)

    # Proxenetas de riesgo controlados por la PNR
    if categoria_usuario == 'dmt':
        proxenetas = PersonasRiesgo.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                   fuente_procedencia_id=19,
                                                   activo=True)
    elif categoria_usuario == 'dpt_ee':
        proxenetas = PersonasRiesgo.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                   fuente_procedencia_id=19,
                                                   activo=True)
    else:
        proxenetas = PersonasRiesgo.objects.filter(fuente_procedencia_id=19,
                                                   activo=True)

    cero = []
    arr_cantidad_ubicados = []
    arr_cantidad_licenciados_sma = []
    arr_cantidad_egresados_ep = []
    arr_cantidad_sancionados = []
    arr_cantidad_desvinculados = []
    arr_cantidad_tecnicos_medios = []
    arr_cantidad_obreros_calificados = []
    arr_cantidad_escuelas_oficio = []
    arr_cantidad_escuelas_especiales = []
    arr_cantidad_escuelas_conducta = []
    arr_cantidad_egresados_efi = []
    arr_cantidad_menores_incapacitados = []
    arr_cantidad_menores_desvinculados = []
    arr_cantidad_menores_dictamen = []
    arr_cantidad_discapacitados = []
    arr_cantidad_mujeres_riesgo = []
    arr_cantidad_hombres_riesgo = []
    arr_cantidad_proxenetas = []

    for org in organismos:
        cero.append(0)

        # UBICADOS
        cantidad_licenciados_sma = licenciados_sma.filter(organismo_id=org.id).count()
        cantidad_egresados_ep = egresados_ep.filter(organismo_id=org.id).count()
        cantidad_sancionados = sancionados.filter(organismo_id=org.id).count()
        cantidad_desvinculados = desvinculados.filter(organismo_id=org.id).count()
        cantidad_tecnicos_medio = tecnicos_medio.filter(organismo_id=org.id).count()
        cantidad_obreros_calificados = obreros_calificados.filter(organismo_id=org.id).count()
        cantidad_escuelas_oficio = escuelas_oficio.filter(organismo_id=org.id).count()
        cantidad_egresados_escuelas_especiales = egresados_escuelas_especiales.filter(organismo_id=org.id).count()
        cantidad_egresados_escuelas_conducta = egresados_escuelas_conducta.filter(organismo_id=org.id).count()
        cantidad_egresados_efi = egresados_efi.filter(organismo_id=org.id).count()
        cantidad_menores_incapacitados = menores_incapacitados.filter(organismo_id=org.id).count()
        cantidad_menores_desvinculados = menores_desvinculados.filter(organismo_id=org.id).count()
        cantidad_menores_dictamen = menores_dictamen.filter(organismo_id=org.id).count()
        cantidad_discapacitados = discapacitados.filter(organismo_id=org.id).count()
        cantidad_mujeres_riesgo = mujeres_riesgo_pnr.filter(organismo_id=org.id).count()
        cantidad_hombres_riesgo = hombres_riesgo_pnr.filter(organismo_id=org.id).count()
        cantidad_proxenetas = proxenetas.filter(organismo_id=org.id).count()

        total = cantidad_egresados_ep + cantidad_sancionados + cantidad_desvinculados + cantidad_tecnicos_medio + \
                cantidad_obreros_calificados + cantidad_escuelas_oficio + cantidad_egresados_escuelas_especiales + \
                cantidad_egresados_escuelas_conducta + cantidad_egresados_efi + cantidad_menores_incapacitados + \
                cantidad_menores_desvinculados + cantidad_menores_dictamen + cantidad_discapacitados + \
                cantidad_mujeres_riesgo + cantidad_hombres_riesgo + cantidad_proxenetas + cantidad_licenciados_sma

        arr_cantidad_ubicados.append(total)
        arr_cantidad_licenciados_sma.append(cantidad_licenciados_sma)
        arr_cantidad_egresados_ep.append(cantidad_egresados_ep)
        arr_cantidad_sancionados.append(cantidad_sancionados)
        arr_cantidad_desvinculados.append(cantidad_desvinculados)
        arr_cantidad_tecnicos_medios.append(cantidad_tecnicos_medio)
        arr_cantidad_obreros_calificados.append(cantidad_obreros_calificados)
        arr_cantidad_escuelas_oficio.append(cantidad_escuelas_oficio)
        arr_cantidad_escuelas_especiales.append(cantidad_egresados_escuelas_especiales)
        arr_cantidad_escuelas_conducta.append(cantidad_egresados_escuelas_conducta)
        arr_cantidad_egresados_efi.append(cantidad_egresados_efi)
        arr_cantidad_menores_incapacitados.append(cantidad_menores_incapacitados)
        arr_cantidad_menores_desvinculados.append(cantidad_menores_desvinculados)
        arr_cantidad_menores_dictamen.append(cantidad_menores_dictamen)
        arr_cantidad_discapacitados.append(cantidad_discapacitados)
        arr_cantidad_mujeres_riesgo.append(cantidad_mujeres_riesgo)
        arr_cantidad_hombres_riesgo.append(cantidad_hombres_riesgo)
        arr_cantidad_proxenetas.append(cantidad_proxenetas)

    worksheet_data.write_column(1, 1, arr_cantidad_ubicados, formato2)
    # Licenciados del SMA
    worksheet_data.write_column(1, 2, arr_cantidad_licenciados_sma, formato2)
    # Egresados de Establecimientos Penitenciarios
    worksheet_data.write_column(1, 3, arr_cantidad_egresados_ep, formato2)
    # Sancionados sin internamiento
    worksheet_data.write_column(1, 4, arr_cantidad_sancionados, formato2)
    # Desvinculados
    worksheet_data.write_column(1, 5, arr_cantidad_desvinculados, formato2)
    # Universitarios
    worksheet_data.write_column(1, 6, cero, formato2)
    # Tecnicos Medios
    worksheet_data.write_column(1, 7, arr_cantidad_tecnicos_medios, formato2)
    # Obreros Calificados
    worksheet_data.write_column(1, 8, arr_cantidad_obreros_calificados, formato2)
    # Escuelas de Oficio
    worksheet_data.write_column(1, 9, arr_cantidad_escuelas_oficio, formato2)
    # Escuelas Especiales
    worksheet_data.write_column(1, 10, arr_cantidad_escuelas_especiales, formato2)
    # Escuelas de Conducta
    worksheet_data.write_column(1, 11, arr_cantidad_escuelas_conducta, formato2)
    # Egresados de la EFI
    worksheet_data.write_column(1, 12, arr_cantidad_egresados_efi, formato2)
    # Menores Incapacitados
    worksheet_data.write_column(1, 13, arr_cantidad_menores_incapacitados, formato2)
    # Menores Desvinculados del SNE
    worksheet_data.write_column(1, 14, arr_cantidad_menores_desvinculados, formato2)
    # Menores con Dictamen del CDO
    worksheet_data.write_column(1, 15, arr_cantidad_menores_dictamen, formato2)
    # Discapacitados
    worksheet_data.write_column(1, 16, arr_cantidad_discapacitados, formato2)
    # Mujeres de Riesgo
    worksheet_data.write_column(1, 17, arr_cantidad_mujeres_riesgo, formato2)
    # Hombres de Riesgo
    worksheet_data.write_column(1, 18, arr_cantidad_hombres_riesgo, formato2)
    # Proxenetas
    worksheet_data.write_column(1, 19, arr_cantidad_proxenetas, formato2)

    # ------------------------------------------------------------------------------

    cantidad_organismos = arr_organismos.__len__()

    total_ubicados = '=SUM(%s)' % xl_range(1, 1, cantidad_organismos, 1)
    total_licenciados_sma = '=SUM(%s)' % xl_range(1, 2, cantidad_organismos, 2)
    total_ep = '=SUM(%s)' % xl_range(1, 3, cantidad_organismos, 3)
    total_sancionados = '=SUM(%s)' % xl_range(1, 4, cantidad_organismos, 4)
    total_desvinculados = '=SUM(%s)' % xl_range(1, 5, cantidad_organismos, 5)
    total_universitarios = '=SUM(%s)' % xl_range(1, 6, cantidad_organismos, 6)
    total_tecnico_medio = '=SUM(%s)' % xl_range(1, 7, cantidad_organismos, 7)
    total_obrero_calificado = '=SUM(%s)' % xl_range(1, 8, cantidad_organismos, 8)
    total_escuela_oficio = '=SUM(%s)' % xl_range(1, 9, cantidad_organismos, 9)
    total_egresados_escuelas_especiales = '=SUM(%s)' % xl_range(1, 10, cantidad_organismos, 10)
    total_egresados_escuelas_conducta = '=SUM(%s)' % xl_range(1, 11, cantidad_organismos, 11)
    total_egresados_efi = '=SUM(%s)' % xl_range(1, 12, cantidad_organismos, 12)
    total_menores_incapacitados = '=SUM(%s)' % xl_range(1, 13, cantidad_organismos, 13)
    total_menores_desvinculados = '=SUM(%s)' % xl_range(1, 14, cantidad_organismos, 14)
    total_menores_dictamen_cdo = '=SUM(%s)' % xl_range(1, 15, cantidad_organismos, 15)
    total_discapacitados = '=SUM(%s)' % xl_range(1, 16, cantidad_organismos, 16)
    total_mujeres_riesgo = '=SUM(%s)' % xl_range(1, 17, cantidad_organismos, 17)
    total_hombres_riesgo = '=SUM(%s)' % xl_range(1, 18, cantidad_organismos, 18)
    total_proxenetas = '=SUM(%s)' % xl_range(1, 19, cantidad_organismos, 19)

    indice_total = cantidad_organismos + 1

    worksheet_data.write(indice_total, 0, "Total", formato)
    worksheet_data.write(indice_total, 1, total_ubicados, formato2)
    worksheet_data.write(indice_total, 2, total_licenciados_sma, formato2)
    worksheet_data.write(indice_total, 3, total_ep, formato2)
    worksheet_data.write(indice_total, 4, total_sancionados, formato2)
    worksheet_data.write(indice_total, 5, total_desvinculados, formato2)
    worksheet_data.write(indice_total, 6, total_universitarios, formato2)
    worksheet_data.write(indice_total, 7, total_tecnico_medio, formato2)
    worksheet_data.write(indice_total, 8, total_obrero_calificado, formato2)
    worksheet_data.write(indice_total, 9, total_escuela_oficio, formato2)
    worksheet_data.write(indice_total, 10, total_egresados_escuelas_especiales, formato2)
    worksheet_data.write(indice_total, 11, total_egresados_escuelas_conducta, formato2)
    worksheet_data.write(indice_total, 12, total_egresados_efi, formato2)
    worksheet_data.write(indice_total, 13, total_menores_incapacitados, formato2)
    worksheet_data.write(indice_total, 14, total_menores_desvinculados, formato2)
    worksheet_data.write(indice_total, 15, total_menores_dictamen_cdo, formato2)
    worksheet_data.write(indice_total, 16, total_discapacitados, formato2)
    worksheet_data.write(indice_total, 17, total_mujeres_riesgo, formato2)
    worksheet_data.write(indice_total, 18, total_hombres_riesgo, formato2)
    worksheet_data.write(indice_total, 19, total_proxenetas, formato2)

    book.close()

    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    return response
