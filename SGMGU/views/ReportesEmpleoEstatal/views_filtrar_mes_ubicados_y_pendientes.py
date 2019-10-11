# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range
from SGMGU.models import *
from SGMGU.views.utiles import permission_required


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def comportamiento_figuras_priorizadas_filtrar_mes(request):
    anno_actual = datetime.today().year
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    if request.method == 'POST':
        mes_seleccionado = int(request.POST['mes'])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response[
            'Content-Disposition'] = "attachment; filename=Comportamiento_de_las_figuras_priorizadas_(ubicados_y_pendientes)(%s).xlsx" % (
            anno_actual)
        book = Workbook(response, {'in_memory': True})
        worksheet_data = book.add_worksheet("Reporte 1")
        formato = book.add_format({'bold': True, 'border': 1})
        formato2 = book.add_format({'border': 1})

        worksheet_data.write("A1", "Fuentes de Procedencia", formato)
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

        # fuentes_procedencia = FuenteProcedencia.objects.filter(activo=True)
        fuentes = []

        fuente1 = FuenteProcedencia.objects.get(id=1)
        fuente2 = FuenteProcedencia.objects.get(id=2)
        fuente3 = FuenteProcedencia.objects.get(id=3)
        fuente4 = FuenteProcedencia.objects.get(id=4)
        fuente5 = FuenteProcedencia.objects.get(id=5)
        fuente6 = FuenteProcedencia.objects.get(id=6)
        fuente7 = FuenteProcedencia.objects.get(id=7)
        fuente8 = FuenteProcedencia.objects.get(id=8)
        fuente9 = FuenteProcedencia.objects.get(id=9)
        fuente10 = FuenteProcedencia.objects.get(id=10)
        fuente11 = FuenteProcedencia.objects.get(id=11)
        fuente12 = FuenteProcedencia.objects.get(id=12)
        fuente13 = FuenteProcedencia.objects.get(id=13)
        fuente14 = FuenteProcedencia.objects.get(id=14)
        fuente15 = FuenteProcedencia.objects.get(id=15)
        fuente17 = FuenteProcedencia.objects.get(id=17)
        fuente18 = FuenteProcedencia.objects.get(id=18)
        fuente19 = FuenteProcedencia.objects.get(id=19)
        fuentes.append(fuente1.nombre)
        fuentes.append(fuente2.nombre)
        fuentes.append(fuente3.nombre)
        fuentes.append(fuente4.nombre)
        fuentes.append(fuente5.nombre)
        fuentes.append(fuente6.nombre)
        fuentes.append(fuente7.nombre)
        fuentes.append(fuente8.nombre)
        fuentes.append(fuente9.nombre)
        fuentes.append(fuente10.nombre)
        fuentes.append(fuente11.nombre)
        fuentes.append(fuente12.nombre)
        fuentes.append(fuente13.nombre)
        fuentes.append(fuente14.nombre)
        fuentes.append(fuente15.nombre)
        fuentes.append(fuente17.nombre)
        fuentes.append(fuente18.nombre)
        fuentes.append(fuente19.nombre)

        worksheet_data.write_column(1, 0, fuentes, formato2)

        # Licenciados del SMA
        if categoria_usuario == 'dmt':
            licenciados_sma = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='S',
                                                            municipio_residencia=municipio_usuario,
                                                            fecha_registro__year=anno_actual).\
                                                            exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            licenciados_sma = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='S',
                                                            municipio_residencia__provincia=provincia_usuario,
                                                            fecha_registro__year=anno_actual).\
                                                            exclude(activo=False, causa_baja=5)
        else:
            licenciados_sma = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='S',
                                                            fecha_registro__year=anno_actual).\
                                                            exclude(activo=False, causa_baja=5)

        # Egresados de Establecimientos penitenciarios
        if categoria_usuario == 'dmt':
            egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                            municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=2,
                                            fecha_registro__year=anno_actual).\
                                            exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                        municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=2,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        else:
            egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=2,
                                                                                  fecha_registro__year=anno_actual).\
                                                                                  exclude(activo=False, causa_baja=5)

        # Sancionados sin Internamiento
        if categoria_usuario == 'dmt':
            sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                        municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=3,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                        municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=3,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        else:
            sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=3,
                                                                                 fecha_registro__year=anno_actual).\
                                                                                 exclude(activo=False, causa_baja=5)

        # Desvinculados
        if categoria_usuario == 'dmt':
            desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                        fecha_registro__year=anno_actual). \
                                                        exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                        fecha_registro__year=anno_actual).\
                                                        exclude(activo=False, causa_baja=5)
        else:
            desvinculados = Desvinculado.objects.filter(fecha_registro__year=anno_actual).\
                                                        exclude(activo=False, causa_baja=5)

        # Egresados universitarios
        if categoria_usuario == 'dmt':
            egresados_universitarios = UbicacionLaboral.objects.filter(anno_graduado=anno_actual)
        elif categoria_usuario == 'dpt_ee':
            egresados_universitarios = UbicacionLaboral.objects.filter(anno_graduado=anno_actual)
        else:
            egresados_universitarios = UbicacionLaboral.objects.filter(anno_graduado=anno_actual)

        # Tecnicos medios
        if categoria_usuario == 'dmt':
            tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                                     fuente_procedencia_id=6,
                                                                     fecha_registro__year=anno_actual).\
                                                                     exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(
                                        municipio_solicita_empleo__provincia=provincia_usuario,
                                        fuente_procedencia_id=6,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        else:
            tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6,
                                                                     fecha_registro__year=anno_actual).\
                                                                     exclude(activo=False, causa_baja=5)

        # Obreros calificados
        if categoria_usuario == 'dmt':
            obreros_calificados = TMedioOCalificadoEOficio.objects.filter(
                                            municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=7,
                                            fecha_registro__year=anno_actual).\
                                            exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            obreros_calificados = TMedioOCalificadoEOficio.objects.filter(
                                        municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=7,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        else:
            obreros_calificados = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=7,
                                                                          fecha_registro__year=anno_actual).\
                                                                          exclude(activo=False, causa_baja=5)

        # Escuelas de oficio
        if categoria_usuario == 'dmt':
            escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(
                                            municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=8,
                                            fecha_registro__year=anno_actual).\
                                            exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(
                                        municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=8,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        else:
            escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=8,
                                                                      fecha_registro__year=anno_actual).\
                                                                      exclude(activo=False, causa_baja=5)

        # Egresados de escuelas especiales
        if categoria_usuario == 'dmt':
            egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                        municipio_solicita_empleo=municipio_usuario,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)

        elif categoria_usuario == 'dpt_ee':
            egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                        municipio_solicita_empleo__provincia=provincia_usuario,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        else:
            egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)

        # Egresados de escuelas de conducta
        if categoria_usuario == 'dmt':
            egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
                                        municipio_solicita_empleo=municipio_usuario,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
                                        municipio_solicita_empleo__provincia=provincia_usuario,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        else:
            egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)

        # Egresados de la EFI
        if categoria_usuario == 'dmt':
            egresados_efi = EgresadosEFI.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            egresados_efi = EgresadosEFI.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                        fecha_registro__year=anno_actual).\
                                                        exclude(activo=False, causa_baja=5)
        else:
            egresados_efi = EgresadosEFI.objects.filter(fecha_registro__year=anno_actual).\
                                                        exclude(activo=False, causa_baja=5)

        # Menores incapacitados para el estudio por dictamen medico
        if categoria_usuario == 'dmt':
            menores_incapacitados = Menores.objects.filter(
                                        municipio_solicita_empleo=municipio_usuario, fuente_procedencia_id=12,
                                        fecha_registro__year=anno_actual).\
                                        exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            menores_incapacitados = Menores.objects.filter(
                                    municipio_solicita_empleo__provincia=provincia_usuario, fuente_procedencia_id=12,
                                    fecha_registro__year=anno_actual).\
                                    exclude(activo=False, causa_baja=5)
        else:
            menores_incapacitados = Menores.objects.filter(fuente_procedencia_id=12,
                                                           fecha_registro__year=anno_actual).\
                                                           exclude(activo=False, causa_baja=5)

        # Menores desvinculados del SNE por bajo rendimiento
        if categoria_usuario == 'dmt':
            menores_desvinculados = Menores.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                           fuente_procedencia_id=13,
                                                           fecha_registro__year=anno_actual).\
                                                           exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            menores_desvinculados = Menores.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                           fuente_procedencia_id=13,
                                                           fecha_registro__year=anno_actual).\
                                                           exclude(activo=False, causa_baja=5)
        else:
            menores_desvinculados = Menores.objects.filter(fuente_procedencia_id=13,
                                                           fecha_registro__year=anno_actual).\
                                                           exclude(activo=False, causa_baja=5)

        # Menores con dictamen del CDO-MININT
        if categoria_usuario == 'dmt':
            menores_dictamen = Menores.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                      fuente_procedencia_id=14,
                                                      fecha_registro__year=anno_actual).\
                                                      exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            menores_dictamen = Menores.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                      fuente_procedencia_id=14,
                                                      fecha_registro__year=anno_actual).\
                                                      exclude(activo=False, causa_baja=5)
        else:
            menores_dictamen = Menores.objects.filter(fuente_procedencia_id=14,
                                                      fecha_registro__year=anno_actual).\
                                                      exclude(activo=False, causa_baja=5)

        # Discapacitados
        if categoria_usuario == 'dmt':
            discapacitados = Discapacitados.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                           fecha_registro__year=anno_actual).\
                                                           exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            discapacitados = Discapacitados.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                           fecha_registro__year=anno_actual).\
                                                           exclude(activo=False, causa_baja=5)
        else:
            discapacitados = Discapacitados.objects.filter(fecha_registro__year=anno_actual).\
                                                           exclude(activo=False, causa_baja=5)

        # Mujeres de riesgo controladas por la PNR
        if categoria_usuario == 'dmt':
            mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                               fuente_procedencia_id=17,
                                                               fecha_registro__year=anno_actual).\
                                                               exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                               fuente_procedencia_id=17,
                                                               fecha_registro__year=anno_actual).\
                                                               exclude(activo=False, causa_baja=5)
        else:
            mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=17,
                                                               fecha_registro__year=anno_actual).\
                                                               exclude(activo=False, causa_baja=5)

        # Hombres de riesgo controlados por la PNR
        if categoria_usuario == 'dmt':
            hombres_riesgo_pnr = PersonasRiesgo.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                               fuente_procedencia_id=18,
                                                               fecha_registro__year=anno_actual).\
                                                               exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            hombres_riesgo_pnr = PersonasRiesgo.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                               fuente_procedencia_id=18,
                                                               fecha_registro__year=anno_actual).\
                                                               exclude(activo=False, causa_baja=5)
        else:
            hombres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=18,
                                                               fecha_registro__year=anno_actual).\
                                                               exclude(activo=False, causa_baja=5)

        # Proxenetas de riesgo controlados por la PNR
        if categoria_usuario == 'dmt':
            proxenetas = PersonasRiesgo.objects.filter(municipio_solicita_empleo=municipio_usuario,
                                                       fuente_procedencia_id=19,
                                                       fecha_registro__year=anno_actual).\
                                                       exclude(activo=False, causa_baja=5)
        elif categoria_usuario == 'dpt_ee':
            proxenetas = PersonasRiesgo.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                       fuente_procedencia_id=19,
                                                       fecha_registro__year=anno_actual).\
                                                       exclude(activo=False, causa_baja=5)
        else:
            proxenetas = PersonasRiesgo.objects.filter(fuente_procedencia_id=19,
                                                       fecha_registro__year=anno_actual).\
                                                       exclude(activo=False, causa_baja=5)

        # CONTROLADOS
        arr_cantidad = []

        cantidad = 0
        for persona in licenciados_sma:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_universitarios:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 1, arr_cantidad, formato2)

        # UBICADOS
        arr_cantidad = []

        cantidad = 0
        for persona in licenciados_sma:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_universitarios:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 2, arr_cantidad, formato2)

        # EMPLEO ESTATAL
        arr_cantidad = []

        cantidad = 0
        for persona in licenciados_sma:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_universitarios:
            if persona.fecha_registro.month <= mes_seleccionado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 3, arr_cantidad, formato2)

        # TPCP
        arr_cantidad = []

        cantidad = 0
        for persona in licenciados_sma:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 4, arr_cantidad, formato2)

        # DL 300
        arr_cantidad = []

        cantidad = 0
        for persona in licenciados_sma:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 5, arr_cantidad, formato2)

        # SMA
        arr_cantidad = []

        cantidad = 0
        for persona in licenciados_sma:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 6, arr_cantidad, formato2)

        # OTRA NO ESTATAL
        arr_cantidad = []

        cantidad = 0
        for persona in licenciados_sma:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.ubicacion_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 7, arr_cantidad, formato2)

        # NO UBICADOS
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and not persona.ubicado:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 8, arr_cantidad, formato2)

        # NO EXISTE OFERTA DE EMPLEO
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 1:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 9, arr_cantidad, formato2)

        # NO LE GUSTA LAS OFERTAS QUE HAY
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 2:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 10, arr_cantidad, formato2)

        # INCAPACITADO TEMPORALMENTE PARA EL EMPLEO (MENOS DE 1 AÑO)
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 3:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 11, arr_cantidad, formato2)

        # SANCIONADOS POR LOS TRIBUNALES
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 4:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 12, arr_cantidad, formato2)

        # NO ESTA INTERESADO EN TRABAJAR
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 5:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 13, arr_cantidad, formato2)

        # TRAMITE DE TRASLADO DE PROVINCIA O MUNICIPIO
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 6:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 14, arr_cantidad, formato2)

        # NO AUTORIZADO POR LOS PADRES
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 7:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 15, arr_cantidad, formato2)

        # AL CUIDADO DE UN FAMILIAR
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 8:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 16, arr_cantidad, formato2)

        # NO HAY OFERTAS ACORDE A SU DISCAPACIDAD
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 9:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 17, arr_cantidad, formato2)

        # LO DEJO
        arr_cantidad = []

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_ep:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in sancionados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in tecnicos_medio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in obreros_calificados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in escuelas_oficio:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_especiales:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_escuelas_conducta:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in egresados_efi:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_incapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_desvinculados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in menores_dictamen:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in discapacitados:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in mujeres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in hombres_riesgo_pnr:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        cantidad = 0
        for persona in proxenetas:
            if persona.fecha_registro.month <= mes_seleccionado and persona.causa_no_ubicado_id == 10:
                cantidad = cantidad + 1
        arr_cantidad.append(cantidad)

        worksheet_data.write_column(1, 18, arr_cantidad, formato2)

        cantidad_fuentes = fuentes.__len__()

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

        book.close()
        return response
    return render(request, "Reportes/ReportesEmpleoEstatal/filtrar_mes_ubicados_pendientes.html", locals())
