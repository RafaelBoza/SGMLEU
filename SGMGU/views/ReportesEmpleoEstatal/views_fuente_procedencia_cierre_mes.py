# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range
from SGMGU.models import *
from SGMGU.views.utiles import permission_required
import time

@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def totales_fuentes_procedencia_cierre_mes(request):
    start_time = time.time()

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    anno = datetime.today().year
    mes = datetime.today().month

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    if categoria_usuario == 'dmt':
        response['Content-Disposition'] = "attachment; filename=Comportamiento_de_las_figuras_priorizadas_(ubicados_y_pendientes)(%s_%s)_(%s).xlsx" % (
            municipio_usuario, str(provincia_usuario).replace(" ", "_"), anno)
    elif categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Comportamiento_de_las_figuras_priorizadas_(ubicados_y_pendientes)(%s)_(%s).xlsx" % (
            str(provincia_usuario).replace(" ", "_"), anno)
    else:
        response['Content-Disposition'] = "attachment; filename=Comportamiento_de_las_figuras_priorizadas_(ubicados_y_pendientes)(%s).xlsx" % anno

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Ubicados y pendientes")
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

    # Licenciados SMA
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        licenciados_sma = LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario,
                                                        activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        licenciados_sma = LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario,
                                                        activo=True)
    else:
        licenciados_sma = LicenciadosSMA.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_licenciadossma" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = LicenciadosSMA.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    licenciados_sma = licenciados_sma.exclude(id__in=ids_listado)

    # Egresados Establecimientos Penitenciarios
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(
                           municipio_solicita_empleo=request.user.perfil_usuario.municipio, fuente_procedencia_id=2,
                           activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(
                           municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                           fuente_procedencia_id=2, activo=True)
    else:
        egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=2,
                                                                               activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosestablecimientospenitenciarios" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 2;"""

    resultado_query = EgresadosEstablecimientosPenitenciarios.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_ep = egresados_ep.exclude(id__in=ids_listado)

    # Sancionados
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
                          municipio_solicita_empleo=request.user.perfil_usuario.municipio, fuente_procedencia_id=3,
                          activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
                          municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                          fuente_procedencia_id=3, activo=True)
    else:
        sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=3,
                                                                             activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosestablecimientospenitenciarios" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 3;"""

    resultado_query = EgresadosEstablecimientosPenitenciarios.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    sancionados = sancionados.exclude(id__in=ids_listado)

    # Desvinculados
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                    activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                    activo=True)
    else:
        desvinculados = Desvinculado.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_desvinculado" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Desvinculado.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    desvinculados = desvinculados.exclude(id__in=ids_listado)

    # Tecnicos medios
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(
                             municipio_solicita_empleo=request.user.perfil_usuario.municipio, fuente_procedencia_id=6,
                             activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(
                             municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                             fuente_procedencia_id=6, activo=True)
    else:
        tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 6;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    tecnicos_medio = tecnicos_medio.exclude(id__in=ids_listado)

    # Obreros calificados
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        obreros_calificados = TMedioOCalificadoEOficio.objects.filter(
                                  municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                  fuente_procedencia_id=7, activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        obreros_calificados = TMedioOCalificadoEOficio.objects.filter(
                                  municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                  fuente_procedencia_id=7, activo=True)
    else:
        obreros_calificados = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=7,
                                                                      activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 7;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    obreros_calificados = obreros_calificados.exclude(id__in=ids_listado)

    # Escuelas de oficio
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(
                              municipio_solicita_empleo=request.user.perfil_usuario.municipio, fuente_procedencia_id=8,
                              activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(
                              municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                              fuente_procedencia_id=8, activo=True)
    else:
        escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=8, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 8;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    escuelas_oficio = escuelas_oficio.exclude(id__in=ids_listado)

    # Egresados de escuelas especiales
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                            municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                            activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                            municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                            activo=True)
    else:
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosescuelasespeciales" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEscuelasEspeciales.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_escuelas_especiales = egresados_escuelas_especiales.exclude(id__in=ids_listado)

    # Egresados de escuelas de conducta
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
                                          municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                          activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
                                          municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                          activo=True)
    else:
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosescuelasconducta" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEscuelasConducta.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_escuelas_conducta = egresados_escuelas_conducta.exclude(id__in=ids_listado)

    # Egresados de la EFI
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        egresados_efi = EgresadosEFI.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                    activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        egresados_efi = EgresadosEFI.objects.filter(
                            municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                            activo=True)
    else:
        egresados_efi = EgresadosEFI.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosefi" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEFI.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_efi = egresados_efi.exclude(id__in=ids_listado)

    # Menores incapacitados
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        menores_incapacitados = Menores.objects.filter(
                                    municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                    fuente_procedencia_id=12, activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        menores_incapacitados = Menores.objects.filter(
                                    municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                    fuente_procedencia_id=12, activo=True)
    else:
        menores_incapacitados = Menores.objects.filter(fuente_procedencia_id=12, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 12;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_incapacitados = menores_incapacitados.exclude(id__in=ids_listado)

    # Menores desvinculados
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        menores_desvinculados = Menores.objects.filter(
                                    municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                    fuente_procedencia_id=13, activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        menores_desvinculados = Menores.objects.filter(
                                    municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                    fuente_procedencia_id=13, activo=True)
    else:
        menores_desvinculados = Menores.objects.filter(fuente_procedencia_id=13, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 13;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_desvinculados = menores_desvinculados.exclude(id__in=ids_listado)

    # Menores con dictamen
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        menores_dictamen = Menores.objects.filter(
                               municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                               fuente_procedencia_id=14, activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        menores_dictamen = Menores.objects.filter(
                               municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                               fuente_procedencia_id=14, activo=True)
    else:
        menores_dictamen = Menores.objects.filter(fuente_procedencia_id=14, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 14;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_dictamen = menores_dictamen.exclude(id__in=ids_listado)

    # Discapacitados
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        discapacitados = Discapacitados.objects.filter(
                             municipio_solicita_empleo=request.user.perfil_usuario.municipio, activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        discapacitados = Discapacitados.objects.filter(
                             municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                             activo=True)
    else:
        discapacitados = Discapacitados.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_discapacitados" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Discapacitados.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    discapacitados = discapacitados.exclude(id__in=ids_listado)

    # Mujeres de riesgo PNR
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(
                                 municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                 fuente_procedencia_id=17, activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(
                                 municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                 activo=True, fuente_procedencia_id=17)
    else:
        mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=17, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 17;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    mujeres_riesgo_pnr = mujeres_riesgo_pnr.exclude(id__in=ids_listado)

    # Hombres de riesgo PNR
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        hombres_riesgo_pnr = PersonasRiesgo.objects.filter(
                                 municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                 fuente_procedencia_id=18, activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        hombres_riesgo_pnr = PersonasRiesgo.objects.filter(
                                 municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                 activo=True, fuente_procedencia_id=18)
    else:
        hombres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=18, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 18;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    hombres_riesgo_pnr = hombres_riesgo_pnr.exclude(id__in=ids_listado)

    # Proxenetas
    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        proxenetas = PersonasRiesgo.objects.filter(
                         municipio_solicita_empleo=request.user.perfil_usuario.municipio, fuente_procedencia_id=19,
                         activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        proxenetas = PersonasRiesgo.objects.filter(
                         municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                         activo=True, fuente_procedencia_id=19)
    else:
        proxenetas = PersonasRiesgo.objects.filter(fuente_procedencia_id=19, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 19;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    proxenetas = proxenetas.exclude(id__in=ids_listado)



    # CONTROLADOS
    licenciados_sma_controlados = licenciados_sma.count()
    egresados_ep_controlados = egresados_ep.count()
    sancionados_controlados = sancionados.count()
    desvinculados_controlados = desvinculados.count()
    tecnicos_medio_controlados = tecnicos_medio.count()
    obreros_calificados_controlados = obreros_calificados.count()
    escuelas_oficio_controlados = escuelas_oficio.count()
    egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.count()
    egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.count()
    egresados_efi_controlados = egresados_efi.count()
    menores_incapacitados_controlados = menores_incapacitados.count()
    menores_desvinculados_controlados = menores_desvinculados.count()
    menores_dictamen_controlados = menores_dictamen.count()
    discapacitados_controlados = discapacitados.count()
    mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.count()
    hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.count()
    proxenetas_controlados = proxenetas.count()

    worksheet_data.write(1, 1, licenciados_sma_controlados, formato2)
    worksheet_data.write(2, 1, egresados_ep_controlados, formato2)
    worksheet_data.write(3, 1, sancionados_controlados, formato2)
    worksheet_data.write(4, 1, desvinculados_controlados, formato2)
    worksheet_data.write(5, 1, 0, formato2)
    worksheet_data.write(6, 1, tecnicos_medio_controlados, formato2)
    worksheet_data.write(7, 1, obreros_calificados_controlados, formato2)
    worksheet_data.write(8, 1, escuelas_oficio_controlados, formato2)
    worksheet_data.write(9, 1, egresados_escuelas_especiales_controlados, formato2)
    worksheet_data.write(10, 1, egresados_escuelas_conducta_controlados, formato2)
    worksheet_data.write(11, 1, egresados_efi_controlados, formato2)
    worksheet_data.write(12, 1, menores_incapacitados_controlados, formato2)
    worksheet_data.write(13, 1, menores_desvinculados_controlados, formato2)
    worksheet_data.write(14, 1, menores_dictamen_controlados, formato2)
    worksheet_data.write(15, 1, discapacitados_controlados, formato2)
    worksheet_data.write(16, 1, mujeres_riesgo_pnr_controlados, formato2)
    worksheet_data.write(17, 1, hombres_riesgo_pnr_controlados, formato2)
    worksheet_data.write(18, 1, proxenetas_controlados, formato2)

    # UBICADOS
    licenciados_sma_ubicados = licenciados_sma.count()
    egresados_ep_ubicados = egresados_ep.filter(ubicado=True).count()
    sancionados_ubicados = sancionados.filter(ubicado=True).count()
    desvinculados_ubicados = desvinculados.filter(ubicado=True).count()
    tecnicos_medio_ubicados = tecnicos_medio.filter(ubicado=True).count()
    obreros_calificados_ubicados = obreros_calificados.filter(ubicado=True).count()
    escuelas_oficio_ubicados = escuelas_oficio.filter(ubicado=True).count()
    egresados_escuelas_especiales_ubicados = egresados_escuelas_especiales.filter(ubicado=True).count()
    egresados_escuelas_conducta_ubicados = egresados_escuelas_conducta.filter(ubicado=True).count()
    egresados_efi_ubicados = egresados_efi.filter(ubicado=True).count()
    menores_incapacitados_ubicados = menores_incapacitados.filter(ubicado=True).count()
    menores_desvinculados_ubicados = menores_desvinculados.filter(ubicado=True).count()
    menores_dictamen_ubicados = menores_dictamen.filter(ubicado=True).count()
    discapacitados_ubicados = discapacitados.filter(ubicado=True).count()
    mujeres_riesgo_pnr_ubicados = mujeres_riesgo_pnr.filter(ubicado=True).count()
    hombres_riesgo_pnr_ubicados = hombres_riesgo_pnr.filter(ubicado=True).count()
    proxenetas_ubicados = proxenetas.filter(ubicado=True).count()

    worksheet_data.write(1, 2, licenciados_sma_ubicados, formato2)
    worksheet_data.write(2, 2, egresados_ep_ubicados, formato2)
    worksheet_data.write(3, 2, sancionados_ubicados, formato2)
    worksheet_data.write(4, 2, desvinculados_ubicados, formato2)
    worksheet_data.write(5, 2, 0, formato2)
    worksheet_data.write(6, 2, tecnicos_medio_ubicados, formato2)
    worksheet_data.write(7, 2, obreros_calificados_ubicados, formato2)
    worksheet_data.write(8, 2, escuelas_oficio_ubicados, formato2)
    worksheet_data.write(9, 2, egresados_escuelas_especiales_ubicados, formato2)
    worksheet_data.write(10, 2, egresados_escuelas_conducta_ubicados, formato2)
    worksheet_data.write(11, 2, egresados_efi_ubicados, formato2)
    worksheet_data.write(12, 2, menores_incapacitados_ubicados, formato2)
    worksheet_data.write(13, 2, menores_desvinculados_ubicados, formato2)
    worksheet_data.write(14, 2, menores_dictamen_ubicados, formato2)
    worksheet_data.write(15, 2, discapacitados_ubicados, formato2)
    worksheet_data.write(16, 2, mujeres_riesgo_pnr_ubicados, formato2)
    worksheet_data.write(17, 2, hombres_riesgo_pnr_ubicados, formato2)
    worksheet_data.write(18, 2, proxenetas_ubicados, formato2)

    # EMPLEO ESTATAL
    licenciados_sma_empleo_estatal = licenciados_sma.filter(ubicacion_id=1).count()
    egresados_ep_empleo_estatal = egresados_ep.filter(ubicacion_id=1).count()
    sancionados_empleo_estatal = sancionados.filter(ubicacion_id=1).count()
    desvinculados_empleo_estatal = desvinculados.filter(ubicacion_id=1).count()
    tecnicos_medio_empleo_estatal = tecnicos_medio.filter(ubicacion_id=1).count()
    obreros_calificados_empleo_estatal = obreros_calificados.filter(ubicacion_id=1).count()
    escuelas_oficio_empleo_estatal = escuelas_oficio.filter(ubicacion_id=1).count()
    egresados_escuelas_especiales_empleo_estatal = egresados_escuelas_especiales.filter(ubicacion_id=1).count()
    egresados_escuelas_conducta_empleo_estatal = egresados_escuelas_conducta.filter(ubicacion_id=1).count()
    egresados_efi_empleo_estatal = egresados_efi.filter(ubicacion_id=1).count()
    menores_incapacitados_empleo_estatal = menores_incapacitados.filter(ubicacion_id=1).count()
    menores_desvinculados_empleo_estatal = menores_desvinculados.filter(ubicacion_id=1).count()
    menores_dictamen_empleo_estatal = menores_dictamen.filter(ubicacion_id=1).count()
    discapacitados_empleo_estatal = discapacitados.filter(ubicacion_id=1).count()
    mujeres_riesgo_pnr_empleo_estatal = mujeres_riesgo_pnr.filter(ubicacion_id=1).count()
    hombres_riesgo_pnr_empleo_estatal = hombres_riesgo_pnr.filter(ubicacion_id=1).count()
    proxenetas_empleo_estatal = proxenetas.filter(ubicacion_id=1).count()

    worksheet_data.write(1, 3, licenciados_sma_empleo_estatal, formato2)
    worksheet_data.write(2, 3, egresados_ep_empleo_estatal, formato2)
    worksheet_data.write(3, 3, sancionados_empleo_estatal, formato2)
    worksheet_data.write(4, 3, desvinculados_empleo_estatal, formato2)
    worksheet_data.write(5, 3, 0, formato2)
    worksheet_data.write(6, 3, tecnicos_medio_empleo_estatal, formato2)
    worksheet_data.write(7, 3, obreros_calificados_empleo_estatal, formato2)
    worksheet_data.write(8, 3, escuelas_oficio_empleo_estatal, formato2)
    worksheet_data.write(9, 3, egresados_escuelas_especiales_empleo_estatal, formato2)
    worksheet_data.write(10, 3, egresados_escuelas_conducta_empleo_estatal, formato2)
    worksheet_data.write(11, 3, egresados_efi_empleo_estatal, formato2)
    worksheet_data.write(12, 3, menores_incapacitados_empleo_estatal, formato2)
    worksheet_data.write(13, 3, menores_desvinculados_empleo_estatal, formato2)
    worksheet_data.write(14, 3, menores_dictamen_empleo_estatal, formato2)
    worksheet_data.write(15, 3, discapacitados_empleo_estatal, formato2)
    worksheet_data.write(16, 3, mujeres_riesgo_pnr_empleo_estatal, formato2)
    worksheet_data.write(17, 3, hombres_riesgo_pnr_empleo_estatal, formato2)
    worksheet_data.write(18, 3, proxenetas_empleo_estatal, formato2)

    # TPCP
    licenciados_sma_tpcp = licenciados_sma.filter(ubicacion_id=2).count()
    egresados_ep_tpcp = egresados_ep.filter(ubicacion_id=2).count()
    sancionados_tpcp = sancionados.filter(ubicacion_id=2).count()
    desvinculados_tpcp = desvinculados.filter(ubicacion_id=2).count()
    tecnicos_medio_tpcp = tecnicos_medio.filter(ubicacion_id=2).count()
    obreros_calificados_tpcp = obreros_calificados.filter(ubicacion_id=2).count()
    escuelas_oficio_tpcp = escuelas_oficio.filter(ubicacion_id=2).count()
    egresados_escuelas_especiales_tpcp = egresados_escuelas_especiales.filter(ubicacion_id=2).count()
    egresados_escuelas_conducta_tpcp = egresados_escuelas_conducta.filter(ubicacion_id=2).count()
    egresados_efi_tpcp = egresados_efi.filter(ubicacion_id=2).count()
    menores_incapacitados_tpcp = menores_incapacitados.filter(ubicacion_id=2).count()
    menores_desvinculados_tpcp = menores_desvinculados.filter(ubicacion_id=2).count()
    menores_dictamen_tpcp = menores_dictamen.filter(ubicacion_id=2).count()
    discapacitados_tpcp = discapacitados.filter(ubicacion_id=2).count()
    mujeres_riesgo_pnr_tpcp = mujeres_riesgo_pnr.filter(ubicacion_id=2).count()
    hombres_riesgo_pnr_tpcp = hombres_riesgo_pnr.filter(ubicacion_id=2).count()
    proxenetas_tpcp = proxenetas.filter(ubicacion_id=2).count()

    worksheet_data.write(1, 4, licenciados_sma_tpcp, formato2)
    worksheet_data.write(2, 4, egresados_ep_tpcp, formato2)
    worksheet_data.write(3, 4, sancionados_tpcp, formato2)
    worksheet_data.write(4, 4, desvinculados_tpcp, formato2)
    worksheet_data.write(5, 4, 0, formato2)
    worksheet_data.write(6, 4, tecnicos_medio_tpcp, formato2)
    worksheet_data.write(7, 4, obreros_calificados_tpcp, formato2)
    worksheet_data.write(8, 4, escuelas_oficio_tpcp, formato2)
    worksheet_data.write(9, 4, egresados_escuelas_especiales_tpcp, formato2)
    worksheet_data.write(10, 4, egresados_escuelas_conducta_tpcp, formato2)
    worksheet_data.write(11, 4, egresados_efi_tpcp, formato2)
    worksheet_data.write(12, 4, menores_incapacitados_tpcp, formato2)
    worksheet_data.write(13, 4, menores_desvinculados_tpcp, formato2)
    worksheet_data.write(14, 4, menores_dictamen_tpcp, formato2)
    worksheet_data.write(15, 4, discapacitados_tpcp, formato2)
    worksheet_data.write(16, 4, mujeres_riesgo_pnr_tpcp, formato2)
    worksheet_data.write(17, 4, hombres_riesgo_pnr_tpcp, formato2)
    worksheet_data.write(18, 4, proxenetas_tpcp, formato2)

    # DL 300
    licenciados_sma_dl300 = licenciados_sma.filter(ubicacion_id=3).count()
    egresados_ep_dl300 = egresados_ep.filter(ubicacion_id=3).count()
    sancionados_dl300 = sancionados.filter(ubicacion_id=3).count()
    desvinculados_dl300 = desvinculados.filter(ubicacion_id=3).count()
    tecnicos_medio_dl300 = tecnicos_medio.filter(ubicacion_id=3).count()
    obreros_calificados_dl300 = obreros_calificados.filter(ubicacion_id=3).count()
    escuelas_oficio_dl300 = escuelas_oficio.filter(ubicacion_id=3).count()
    egresados_escuelas_especiales_dl300 = egresados_escuelas_especiales.filter(ubicacion_id=3).count()
    egresados_escuelas_conducta_dl300 = egresados_escuelas_conducta.filter(ubicacion_id=3).count()
    egresados_efi_dl300 = egresados_efi.filter(ubicacion_id=3).count()
    menores_incapacitados_dl300 = menores_incapacitados.filter(ubicacion_id=3).count()
    menores_desvinculados_dl300 = menores_desvinculados.filter(ubicacion_id=3).count()
    menores_dictamen_dl300 = menores_dictamen.filter(ubicacion_id=3).count()
    discapacitados_dl300 = discapacitados.filter(ubicacion_id=3).count()
    mujeres_riesgo_pnr_dl300 = mujeres_riesgo_pnr.filter(ubicacion_id=3).count()
    hombres_riesgo_pnr_dl300 = hombres_riesgo_pnr.filter(ubicacion_id=3).count()
    proxenetas_dl300 = proxenetas.filter(ubicacion_id=3).count()

    worksheet_data.write(1, 5, licenciados_sma_dl300, formato2)
    worksheet_data.write(2, 5, egresados_ep_dl300, formato2)
    worksheet_data.write(3, 5, sancionados_dl300, formato2)
    worksheet_data.write(4, 5, desvinculados_dl300, formato2)
    worksheet_data.write(5, 5, 0, formato2)
    worksheet_data.write(6, 5, tecnicos_medio_dl300, formato2)
    worksheet_data.write(7, 5, obreros_calificados_dl300, formato2)
    worksheet_data.write(8, 5, escuelas_oficio_dl300, formato2)
    worksheet_data.write(9, 5, egresados_escuelas_especiales_dl300, formato2)
    worksheet_data.write(10, 5, egresados_escuelas_conducta_dl300, formato2)
    worksheet_data.write(11, 5, egresados_efi_dl300, formato2)
    worksheet_data.write(12, 5, menores_incapacitados_dl300, formato2)
    worksheet_data.write(13, 5, menores_desvinculados_dl300, formato2)
    worksheet_data.write(14, 5, menores_dictamen_dl300, formato2)
    worksheet_data.write(15, 5, discapacitados_dl300, formato2)
    worksheet_data.write(16, 5, mujeres_riesgo_pnr_dl300, formato2)
    worksheet_data.write(17, 5, hombres_riesgo_pnr_dl300, formato2)
    worksheet_data.write(18, 5, proxenetas_dl300, formato2)

    # SMA
    licenciados_sma_dl300 = licenciados_sma.filter(ubicacion_id=5).count()
    egresados_ep_dl300 = egresados_ep.filter(ubicacion_id=5).count()
    sancionados_dl300 = sancionados.filter(ubicacion_id=5).count()
    desvinculados_dl300 = desvinculados.filter(ubicacion_id=5).count()
    tecnicos_medio_dl300 = tecnicos_medio.filter(ubicacion_id=5).count()
    obreros_calificados_dl300 = obreros_calificados.filter(ubicacion_id=5).count()
    escuelas_oficio_dl300 = escuelas_oficio.filter(ubicacion_id=5).count()
    egresados_escuelas_especiales_dl300 = egresados_escuelas_especiales.filter(ubicacion_id=5).count()
    egresados_escuelas_conducta_dl300 = egresados_escuelas_conducta.filter(ubicacion_id=5).count()
    egresados_efi_dl300 = egresados_efi.filter(ubicacion_id=5).count()
    menores_incapacitados_dl300 = menores_incapacitados.filter(ubicacion_id=5).count()
    menores_desvinculados_dl300 = menores_desvinculados.filter(ubicacion_id=5).count()
    menores_dictamen_dl300 = menores_dictamen.filter(ubicacion_id=5).count()
    discapacitados_dl300 = discapacitados.filter(ubicacion_id=5).count()
    mujeres_riesgo_pnr_dl300 = mujeres_riesgo_pnr.filter(ubicacion_id=5).count()
    hombres_riesgo_pnr_dl300 = hombres_riesgo_pnr.filter(ubicacion_id=5).count()
    proxenetas_dl300 = proxenetas.filter(ubicacion_id=5).count()

    worksheet_data.write(1, 6, licenciados_sma_dl300, formato2)
    worksheet_data.write(2, 6, egresados_ep_dl300, formato2)
    worksheet_data.write(3, 6, sancionados_dl300, formato2)
    worksheet_data.write(4, 6, desvinculados_dl300, formato2)
    worksheet_data.write(5, 6, 0, formato2)
    worksheet_data.write(6, 6, tecnicos_medio_dl300, formato2)
    worksheet_data.write(7, 6, obreros_calificados_dl300, formato2)
    worksheet_data.write(8, 6, escuelas_oficio_dl300, formato2)
    worksheet_data.write(9, 6, egresados_escuelas_especiales_dl300, formato2)
    worksheet_data.write(10, 6, egresados_escuelas_conducta_dl300, formato2)
    worksheet_data.write(11, 6, egresados_efi_dl300, formato2)
    worksheet_data.write(12, 6, menores_incapacitados_dl300, formato2)
    worksheet_data.write(13, 6, menores_desvinculados_dl300, formato2)
    worksheet_data.write(14, 6, menores_dictamen_dl300, formato2)
    worksheet_data.write(15, 6, discapacitados_dl300, formato2)
    worksheet_data.write(16, 6, mujeres_riesgo_pnr_dl300, formato2)
    worksheet_data.write(17, 6, hombres_riesgo_pnr_dl300, formato2)
    worksheet_data.write(18, 6, proxenetas_dl300, formato2)

    # OTRA NO ESTATAL
    licenciados_sma_otra_no_estatal = licenciados_sma.filter(ubicacion_id=4).count()
    egresados_ep_otra_no_estatal = egresados_ep.filter(ubicacion_id=4).count()
    sancionados_otra_no_estatal = sancionados.filter(ubicacion_id=4).count()
    desvinculados_otra_no_estatal = desvinculados.filter(ubicacion_id=4).count()
    tecnicos_medio_otra_no_estatal = tecnicos_medio.filter(ubicacion_id=4).count()
    obreros_calificados_otra_no_estatal = obreros_calificados.filter(ubicacion_id=4).count()
    escuelas_oficio_otra_no_estatal = escuelas_oficio.filter(ubicacion_id=4).count()
    egresados_escuelas_especiales_otra_no_estatal = egresados_escuelas_especiales.filter(ubicacion_id=4).count()
    egresados_escuelas_conducta_otra_no_estatal = egresados_escuelas_conducta.filter(ubicacion_id=4).count()
    egresados_efi_otra_no_estatal = egresados_efi.filter(ubicacion_id=4).count()
    menores_incapacitados_otra_no_estatal = menores_incapacitados.filter(ubicacion_id=4).count()
    menores_desvinculados_otra_no_estatal = menores_desvinculados.filter(ubicacion_id=4).count()
    menores_dictamen_otra_no_estatal = menores_dictamen.filter(ubicacion_id=4).count()
    discapacitados_otra_no_estatal = discapacitados.filter(ubicacion_id=4).count()
    mujeres_riesgo_pnr_otra_no_estatal = mujeres_riesgo_pnr.filter(ubicacion_id=4).count()
    hombres_riesgo_pnr_otra_no_estatal = hombres_riesgo_pnr.filter(ubicacion_id=4).count()
    proxenetas_otra_no_estatal = proxenetas.filter(ubicacion_id=4).count()

    worksheet_data.write(1, 7, licenciados_sma_otra_no_estatal, formato2)
    worksheet_data.write(2, 7, egresados_ep_otra_no_estatal, formato2)
    worksheet_data.write(3, 7, sancionados_otra_no_estatal, formato2)
    worksheet_data.write(4, 7, desvinculados_otra_no_estatal, formato2)
    worksheet_data.write(5, 7, 0, formato2)
    worksheet_data.write(6, 7, tecnicos_medio_otra_no_estatal, formato2)
    worksheet_data.write(7, 7, obreros_calificados_otra_no_estatal, formato2)
    worksheet_data.write(8, 7, escuelas_oficio_otra_no_estatal, formato2)
    worksheet_data.write(9, 7, egresados_escuelas_especiales_otra_no_estatal, formato2)
    worksheet_data.write(10, 7, egresados_escuelas_conducta_otra_no_estatal, formato2)
    worksheet_data.write(11, 7, egresados_efi_otra_no_estatal, formato2)
    worksheet_data.write(12, 7, menores_incapacitados_otra_no_estatal, formato2)
    worksheet_data.write(13, 7, menores_desvinculados_otra_no_estatal, formato2)
    worksheet_data.write(14, 7, menores_dictamen_otra_no_estatal, formato2)
    worksheet_data.write(15, 7, discapacitados_otra_no_estatal, formato2)
    worksheet_data.write(16, 7, mujeres_riesgo_pnr_otra_no_estatal, formato2)
    worksheet_data.write(17, 7, hombres_riesgo_pnr_otra_no_estatal, formato2)
    worksheet_data.write(18, 7, proxenetas_otra_no_estatal, formato2)

    # NO UBICADOS
    egresados_ep_no_ubicados = egresados_ep.filter(ubicado=False).count()
    sancionados_no_ubicados = sancionados.filter(ubicado=False).count()
    desvinculados_no_ubicados = desvinculados.filter(ubicado=False).count()
    tecnicos_medio_no_ubicados = tecnicos_medio.filter(ubicado=False).count()
    obreros_calificados_no_ubicados = obreros_calificados.filter(ubicado=False).count()
    escuelas_oficio_no_ubicados = escuelas_oficio.filter(ubicado=False).count()
    egresados_escuelas_especiales_no_ubicados = egresados_escuelas_especiales.filter(ubicado=False).count()
    egresados_escuelas_conducta_no_ubicados = egresados_escuelas_conducta.filter(ubicado=False).count()
    egresados_efi_no_ubicados = egresados_efi.filter(ubicado=False).count()
    menores_incapacitados_no_ubicados = menores_incapacitados.filter(ubicado=False).count()
    menores_desvinculados_no_ubicados = menores_desvinculados.filter(ubicado=False).count()
    menores_dictamen_no_ubicados = menores_dictamen.filter(ubicado=False).count()
    discapacitados_no_ubicados = discapacitados.filter(ubicado=False).count()
    mujeres_riesgo_pnr_no_ubicados = mujeres_riesgo_pnr.filter(ubicado=False).count()
    hombres_riesgo_pnr_no_ubicados = hombres_riesgo_pnr.filter(ubicado=False).count()
    proxenetas_no_ubicados = proxenetas.filter(ubicado=False).count()

    worksheet_data.write(1, 8, 0, formato2)
    worksheet_data.write(2, 8, egresados_ep_no_ubicados, formato2)
    worksheet_data.write(3, 8, sancionados_no_ubicados, formato2)
    worksheet_data.write(4, 8, desvinculados_no_ubicados, formato2)
    worksheet_data.write(5, 8, 0, formato2)
    worksheet_data.write(6, 8, tecnicos_medio_no_ubicados, formato2)
    worksheet_data.write(7, 8, obreros_calificados_no_ubicados, formato2)
    worksheet_data.write(8, 8, escuelas_oficio_no_ubicados, formato2)
    worksheet_data.write(9, 8, egresados_escuelas_especiales_no_ubicados, formato2)
    worksheet_data.write(10, 8, egresados_escuelas_conducta_no_ubicados, formato2)
    worksheet_data.write(11, 8, egresados_efi_no_ubicados, formato2)
    worksheet_data.write(12, 8, menores_incapacitados_no_ubicados, formato2)
    worksheet_data.write(13, 8, menores_desvinculados_no_ubicados, formato2)
    worksheet_data.write(14, 8, menores_dictamen_no_ubicados, formato2)
    worksheet_data.write(15, 8, discapacitados_no_ubicados, formato2)
    worksheet_data.write(16, 8, mujeres_riesgo_pnr_no_ubicados, formato2)
    worksheet_data.write(17, 8, hombres_riesgo_pnr_no_ubicados, formato2)
    worksheet_data.write(18, 8, proxenetas_no_ubicados, formato2)

    # NO EXISTE OFERTA DE EMPLEO
    egresados_ep_no_existe_oferta = egresados_ep.filter(causa_no_ubicado_id=1).count()
    sancionados_no_existe_oferta = sancionados.filter(causa_no_ubicado_id=1).count()
    desvinculados_no_existe_oferta = desvinculados.filter(causa_no_ubicado_id=1).count()
    tecnicos_medio_no_existe_oferta = tecnicos_medio.filter(causa_no_ubicado_id=1).count()
    obreros_calificados_no_existe_oferta = obreros_calificados.filter(causa_no_ubicado_id=1).count()
    escuelas_oficio_no_existe_oferta = escuelas_oficio.filter(causa_no_ubicado_id=1).count()
    egresados_escuelas_especiales_no_existe_oferta = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=1).count()
    egresados_escuelas_conducta_no_existe_oferta = egresados_escuelas_conducta.filter(causa_no_ubicado_id=1).count()
    egresados_efi_no_existe_oferta = egresados_efi.filter(causa_no_ubicado_id=1).count()
    menores_incapacitados_no_existe_oferta = menores_incapacitados.filter(causa_no_ubicado_id=1).count()
    menores_desvinculados_no_existe_oferta = menores_desvinculados.filter(causa_no_ubicado_id=1).count()
    menores_dictamen_no_existe_oferta = menores_dictamen.filter(causa_no_ubicado_id=1).count()
    discapacitados_no_existe_oferta = discapacitados.filter(causa_no_ubicado_id=1).count()
    mujeres_riesgo_pnr_no_existe_oferta = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=1).count()
    hombres_riesgo_pnr_no_existe_oferta = hombres_riesgo_pnr.filter(causa_no_ubicado_id=1).count()
    proxenetas_no_existe_oferta = proxenetas.filter(causa_no_ubicado_id=1).count()

    worksheet_data.write(1, 9, 0, formato2)
    worksheet_data.write(2, 9, egresados_ep_no_existe_oferta, formato2)
    worksheet_data.write(3, 9, sancionados_no_existe_oferta, formato2)
    worksheet_data.write(4, 9, desvinculados_no_existe_oferta, formato2)
    worksheet_data.write(5, 9, 0, formato2)
    worksheet_data.write(6, 9, tecnicos_medio_no_existe_oferta, formato2)
    worksheet_data.write(7, 9, obreros_calificados_no_existe_oferta, formato2)
    worksheet_data.write(8, 9, escuelas_oficio_no_existe_oferta, formato2)
    worksheet_data.write(9, 9, egresados_escuelas_especiales_no_existe_oferta, formato2)
    worksheet_data.write(10, 9, egresados_escuelas_conducta_no_existe_oferta, formato2)
    worksheet_data.write(11, 9, egresados_efi_no_existe_oferta, formato2)
    worksheet_data.write(12, 9, menores_incapacitados_no_existe_oferta, formato2)
    worksheet_data.write(13, 9, menores_desvinculados_no_existe_oferta, formato2)
    worksheet_data.write(14, 9, menores_dictamen_no_existe_oferta, formato2)
    worksheet_data.write(15, 9, discapacitados_no_existe_oferta, formato2)
    worksheet_data.write(16, 9, mujeres_riesgo_pnr_no_existe_oferta, formato2)
    worksheet_data.write(17, 9, hombres_riesgo_pnr_no_existe_oferta, formato2)
    worksheet_data.write(18, 9, proxenetas_no_existe_oferta, formato2)

    # NO LE GUSTA LAS OFERTAS QUE HAY
    egresados_ep_no_le_gustan = egresados_ep.filter(causa_no_ubicado_id=2).count()
    sancionados_no_le_gustan = sancionados.filter(causa_no_ubicado_id=2).count()
    desvinculados_no_le_gustan = desvinculados.filter(causa_no_ubicado_id=2).count()
    tecnicos_medio_no_le_gustan = tecnicos_medio.filter(causa_no_ubicado_id=2).count()
    obreros_calificados_no_le_gustan = obreros_calificados.filter(causa_no_ubicado_id=2).count()
    escuelas_oficio_no_le_gustan = escuelas_oficio.filter(causa_no_ubicado_id=2).count()
    egresados_escuelas_especiales_no_le_gustan = egresados_escuelas_especiales.filter(causa_no_ubicado_id=2).count()
    egresados_escuelas_conducta_no_le_gustan = egresados_escuelas_conducta.filter(causa_no_ubicado_id=2).count()
    egresados_efi_no_le_gustan = egresados_efi.filter(causa_no_ubicado_id=2).count()
    menores_incapacitados_no_le_gustan = menores_incapacitados.filter(causa_no_ubicado_id=2).count()
    menores_desvinculados_no_le_gustan = menores_desvinculados.filter(causa_no_ubicado_id=2).count()
    menores_dictamen_no_le_gustan = menores_dictamen.filter(causa_no_ubicado_id=2).count()
    discapacitados_no_le_gustan = discapacitados.filter(causa_no_ubicado_id=2).count()
    mujeres_riesgo_pnr_no_le_gustan = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=2).count()
    hombres_riesgo_pnr_no_le_gustan = hombres_riesgo_pnr.filter(causa_no_ubicado_id=2).count()
    proxenetas_no_le_gustan = proxenetas.filter(causa_no_ubicado_id=2).count()

    worksheet_data.write(1, 10, 0, formato2)
    worksheet_data.write(2, 10, egresados_ep_no_le_gustan, formato2)
    worksheet_data.write(3, 10, sancionados_no_le_gustan, formato2)
    worksheet_data.write(4, 10, desvinculados_no_le_gustan, formato2)
    worksheet_data.write(5, 10, 0, formato2)
    worksheet_data.write(6, 10, tecnicos_medio_no_le_gustan, formato2)
    worksheet_data.write(7, 10, obreros_calificados_no_le_gustan, formato2)
    worksheet_data.write(8, 10, escuelas_oficio_no_le_gustan, formato2)
    worksheet_data.write(9, 10, egresados_escuelas_especiales_no_le_gustan, formato2)
    worksheet_data.write(10, 10, egresados_escuelas_conducta_no_le_gustan, formato2)
    worksheet_data.write(11, 10, egresados_efi_no_le_gustan, formato2)
    worksheet_data.write(12, 10, menores_incapacitados_no_le_gustan, formato2)
    worksheet_data.write(13, 10, menores_desvinculados_no_le_gustan, formato2)
    worksheet_data.write(14, 10, menores_dictamen_no_le_gustan, formato2)
    worksheet_data.write(15, 10, discapacitados_no_le_gustan, formato2)
    worksheet_data.write(16, 10, mujeres_riesgo_pnr_no_le_gustan, formato2)
    worksheet_data.write(17, 10, hombres_riesgo_pnr_no_le_gustan, formato2)
    worksheet_data.write(18, 10, proxenetas_no_le_gustan, formato2)

    # INCAPACITADO TEMPORALMENTE PARA EL EMPLEO (MENOS DE 1 AÑO)
    egresados_ep_incapacitado = egresados_ep.filter(causa_no_ubicado_id=3).count()
    sancionados_incapacitado = sancionados.filter(causa_no_ubicado_id=3).count()
    desvinculados_incapacitado = desvinculados.filter(causa_no_ubicado_id=3).count()
    tecnicos_medio_incapacitado = tecnicos_medio.filter(causa_no_ubicado_id=3).count()
    obreros_calificados_incapacitado = obreros_calificados.filter(causa_no_ubicado_id=3).count()
    escuelas_oficio_incapacitado = escuelas_oficio.filter(causa_no_ubicado_id=3).count()
    egresados_escuelas_especiales_incapacitado = egresados_escuelas_especiales.filter(causa_no_ubicado_id=3).count()
    egresados_escuelas_conducta_incapacitado = egresados_escuelas_conducta.filter(causa_no_ubicado_id=3).count()
    egresados_efi_incapacitado = egresados_efi.filter(causa_no_ubicado_id=3).count()
    menores_incapacitados_incapacitado = menores_incapacitados.filter(causa_no_ubicado_id=3).count()
    menores_desvinculados_incapacitado = menores_desvinculados.filter(causa_no_ubicado_id=3).count()
    menores_dictamen_incapacitado = menores_dictamen.filter(causa_no_ubicado_id=3).count()
    discapacitados_incapacitado = discapacitados.filter(causa_no_ubicado_id=3).count()
    mujeres_riesgo_pnr_incapacitado = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=3).count()
    hombres_riesgo_pnr_incapacitado = hombres_riesgo_pnr.filter(causa_no_ubicado_id=3).count()
    proxenetas_incapacitado = proxenetas.filter(causa_no_ubicado_id=3).count()

    worksheet_data.write(1, 11, 0, formato2)
    worksheet_data.write(2, 11, egresados_ep_incapacitado, formato2)
    worksheet_data.write(3, 11, sancionados_incapacitado, formato2)
    worksheet_data.write(4, 11, desvinculados_incapacitado, formato2)
    worksheet_data.write(5, 11, 0, formato2)
    worksheet_data.write(6, 11, tecnicos_medio_incapacitado, formato2)
    worksheet_data.write(7, 11, obreros_calificados_incapacitado, formato2)
    worksheet_data.write(8, 11, escuelas_oficio_incapacitado, formato2)
    worksheet_data.write(9, 11, egresados_escuelas_especiales_incapacitado, formato2)
    worksheet_data.write(10, 11, egresados_escuelas_conducta_incapacitado, formato2)
    worksheet_data.write(11, 11, egresados_efi_incapacitado, formato2)
    worksheet_data.write(12, 11, menores_incapacitados_incapacitado, formato2)
    worksheet_data.write(13, 11, menores_desvinculados_incapacitado, formato2)
    worksheet_data.write(14, 11, menores_dictamen_incapacitado, formato2)
    worksheet_data.write(15, 11, discapacitados_incapacitado, formato2)
    worksheet_data.write(16, 11, mujeres_riesgo_pnr_incapacitado, formato2)
    worksheet_data.write(17, 11, hombres_riesgo_pnr_incapacitado, formato2)
    worksheet_data.write(18, 11, proxenetas_incapacitado, formato2)

    # SANCIONADOS POR LOS TRIBUNALES
    egresados_ep_sancionados = egresados_ep.filter(causa_no_ubicado_id=4).count()
    sancionados_sancionados = sancionados.filter(causa_no_ubicado_id=4).count()
    desvinculados_sancionados = desvinculados.filter(causa_no_ubicado_id=4).count()
    tecnicos_medio_sancionados = tecnicos_medio.filter(causa_no_ubicado_id=4).count()
    obreros_calificados_sancionados = obreros_calificados.filter(causa_no_ubicado_id=4).count()
    escuelas_oficio_sancionados = escuelas_oficio.filter(causa_no_ubicado_id=4).count()
    egresados_escuelas_especiales_sancionados = egresados_escuelas_especiales.filter(causa_no_ubicado_id=4).count()
    egresados_escuelas_conducta_sancionados = egresados_escuelas_conducta.filter(causa_no_ubicado_id=4).count()
    egresados_efi_sancionados = egresados_efi.filter(causa_no_ubicado_id=4).count()
    menores_incapacitados_sancionados = menores_incapacitados.filter(causa_no_ubicado_id=4).count()
    menores_desvinculados_sancionados = menores_desvinculados.filter(causa_no_ubicado_id=4).count()
    menores_dictamen_sancionados = menores_dictamen.filter(causa_no_ubicado_id=4).count()
    discapacitados_sancionados = discapacitados.filter(causa_no_ubicado_id=4).count()
    mujeres_riesgo_pnr_sancionados = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=4).count()
    hombres_riesgo_pnr_sancionados = hombres_riesgo_pnr.filter(causa_no_ubicado_id=4).count()
    proxenetas_sancionados = proxenetas.filter(causa_no_ubicado_id=4).count()

    worksheet_data.write(1, 12, 0, formato2)
    worksheet_data.write(2, 12, egresados_ep_sancionados, formato2)
    worksheet_data.write(3, 12, sancionados_sancionados, formato2)
    worksheet_data.write(4, 12, desvinculados_sancionados, formato2)
    worksheet_data.write(5, 12, 0, formato2)
    worksheet_data.write(6, 12, tecnicos_medio_sancionados, formato2)
    worksheet_data.write(7, 12, obreros_calificados_sancionados, formato2)
    worksheet_data.write(8, 12, escuelas_oficio_sancionados, formato2)
    worksheet_data.write(9, 12, egresados_escuelas_especiales_sancionados, formato2)
    worksheet_data.write(10, 12, egresados_escuelas_conducta_sancionados, formato2)
    worksheet_data.write(11, 12, egresados_efi_sancionados, formato2)
    worksheet_data.write(12, 12, menores_incapacitados_sancionados, formato2)
    worksheet_data.write(13, 12, menores_desvinculados_sancionados, formato2)
    worksheet_data.write(14, 12, menores_dictamen_sancionados, formato2)
    worksheet_data.write(15, 12, discapacitados_sancionados, formato2)
    worksheet_data.write(16, 12, mujeres_riesgo_pnr_sancionados, formato2)
    worksheet_data.write(17, 12, hombres_riesgo_pnr_sancionados, formato2)
    worksheet_data.write(18, 12, proxenetas_sancionados, formato2)

    # NO ESTA INTERESADO EN TRABAJAR
    egresados_ep_no_interesados = egresados_ep.filter(causa_no_ubicado_id=5).count()
    sancionados_no_interesados = sancionados.filter(causa_no_ubicado_id=5).count()
    desvinculados_no_interesados = desvinculados.filter(causa_no_ubicado_id=5).count()
    tecnicos_medio_no_interesados = tecnicos_medio.filter(causa_no_ubicado_id=5).count()
    obreros_calificados_no_interesados = obreros_calificados.filter(causa_no_ubicado_id=5).count()
    escuelas_oficio_no_interesados = escuelas_oficio.filter(causa_no_ubicado_id=5).count()
    egresados_escuelas_especiales_no_interesados = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=5).count()
    egresados_escuelas_conducta_no_interesados = egresados_escuelas_conducta.filter(causa_no_ubicado_id=5).count()
    egresados_efi_no_interesados = egresados_efi.filter(causa_no_ubicado_id=5).count()
    menores_incapacitados_no_interesados = menores_incapacitados.filter(causa_no_ubicado_id=5).count()
    menores_desvinculados_no_interesados = menores_desvinculados.filter(causa_no_ubicado_id=5).count()
    menores_dictamen_no_interesados = menores_dictamen.filter(causa_no_ubicado_id=5).count()
    discapacitados_no_interesados = discapacitados.filter(causa_no_ubicado_id=5).count()
    mujeres_riesgo_pnr_no_interesados = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=5).count()
    hombres_riesgo_pnr_no_interesados = hombres_riesgo_pnr.filter(causa_no_ubicado_id=5).count()
    proxenetas_no_interesados = proxenetas.filter(causa_no_ubicado_id=5).count()

    worksheet_data.write(1, 13, 0, formato2)
    worksheet_data.write(2, 13, egresados_ep_no_interesados, formato2)
    worksheet_data.write(3, 13, sancionados_no_interesados, formato2)
    worksheet_data.write(4, 13, desvinculados_no_interesados, formato2)
    worksheet_data.write(5, 13, 0, formato2)
    worksheet_data.write(6, 13, tecnicos_medio_no_interesados, formato2)
    worksheet_data.write(7, 13, obreros_calificados_no_interesados, formato2)
    worksheet_data.write(8, 13, escuelas_oficio_no_interesados, formato2)
    worksheet_data.write(9, 13, egresados_escuelas_especiales_no_interesados, formato2)
    worksheet_data.write(10, 13, egresados_escuelas_conducta_no_interesados, formato2)
    worksheet_data.write(11, 13, egresados_efi_no_interesados, formato2)
    worksheet_data.write(12, 13, menores_incapacitados_no_interesados, formato2)
    worksheet_data.write(13, 13, menores_desvinculados_no_interesados, formato2)
    worksheet_data.write(14, 13, menores_dictamen_no_interesados, formato2)
    worksheet_data.write(15, 13, discapacitados_no_interesados, formato2)
    worksheet_data.write(16, 13, mujeres_riesgo_pnr_no_interesados, formato2)
    worksheet_data.write(17, 13, hombres_riesgo_pnr_no_interesados, formato2)
    worksheet_data.write(18, 13, proxenetas_no_interesados, formato2)

    # TRAMITE DE TRASLADO DE PROVINCIA O MUNICIPIO
    egresados_ep_tramite_traslado = egresados_ep.filter(causa_no_ubicado_id=6).count()
    sancionados_tramite_traslado = sancionados.filter(causa_no_ubicado_id=6).count()
    desvinculados_tramite_traslado = desvinculados.filter(causa_no_ubicado_id=6).count()
    tecnicos_medio_tramite_traslado = tecnicos_medio.filter(causa_no_ubicado_id=6).count()
    obreros_calificados_tramite_traslado = obreros_calificados.filter(causa_no_ubicado_id=6).count()
    escuelas_oficio_tramite_traslado = escuelas_oficio.filter(causa_no_ubicado_id=6).count()
    egresados_escuelas_especiales_tramite_traslado = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=6).count()
    egresados_escuelas_conducta_tramite_traslado = egresados_escuelas_conducta.filter(causa_no_ubicado_id=6).count()
    egresados_efi_tramite_traslado = egresados_efi.filter(causa_no_ubicado_id=6).count()
    menores_incapacitados_tramite_traslado = menores_incapacitados.filter(causa_no_ubicado_id=6).count()
    menores_desvinculados_tramite_traslado = menores_desvinculados.filter(causa_no_ubicado_id=6).count()
    menores_dictamen_tramite_traslado = menores_dictamen.filter(causa_no_ubicado_id=6).count()
    discapacitados_tramite_traslado = discapacitados.filter(causa_no_ubicado_id=6).count()
    mujeres_riesgo_pnr_tramite_traslado = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=6).count()
    hombres_riesgo_pnr_tramite_traslado = hombres_riesgo_pnr.filter(causa_no_ubicado_id=6).count()
    proxenetas_tramite_traslado = proxenetas.filter(causa_no_ubicado_id=6).count()

    worksheet_data.write(1, 14, 0, formato2)
    worksheet_data.write(2, 14, egresados_ep_tramite_traslado, formato2)
    worksheet_data.write(3, 14, sancionados_tramite_traslado, formato2)
    worksheet_data.write(4, 14, desvinculados_tramite_traslado, formato2)
    worksheet_data.write(5, 14, 0, formato2)
    worksheet_data.write(6, 14, tecnicos_medio_tramite_traslado, formato2)
    worksheet_data.write(7, 14, obreros_calificados_tramite_traslado, formato2)
    worksheet_data.write(8, 14, escuelas_oficio_tramite_traslado, formato2)
    worksheet_data.write(9, 14, egresados_escuelas_especiales_tramite_traslado, formato2)
    worksheet_data.write(10, 14, egresados_escuelas_conducta_tramite_traslado, formato2)
    worksheet_data.write(11, 14, egresados_efi_tramite_traslado, formato2)
    worksheet_data.write(12, 14, menores_incapacitados_tramite_traslado, formato2)
    worksheet_data.write(13, 14, menores_desvinculados_tramite_traslado, formato2)
    worksheet_data.write(14, 14, menores_dictamen_tramite_traslado, formato2)
    worksheet_data.write(15, 14, discapacitados_tramite_traslado, formato2)
    worksheet_data.write(16, 14, mujeres_riesgo_pnr_tramite_traslado, formato2)
    worksheet_data.write(17, 14, hombres_riesgo_pnr_tramite_traslado, formato2)
    worksheet_data.write(18, 14, proxenetas_tramite_traslado, formato2)

    # NO AUTORIZADO POR LOS PADRES
    egresados_ep_no_autorizado_padres = egresados_ep.filter(causa_no_ubicado_id=7).count()
    sancionados_no_autorizado_padres = sancionados.filter(causa_no_ubicado_id=7).count()
    desvinculados_no_autorizado_padres = desvinculados.filter(causa_no_ubicado_id=7).count()
    tecnicos_medio_no_autorizado_padres = tecnicos_medio.filter(causa_no_ubicado_id=7).count()
    obreros_calificados_no_autorizado_padres = obreros_calificados.filter(causa_no_ubicado_id=7).count()
    escuelas_oficio_no_autorizado_padres = escuelas_oficio.filter(causa_no_ubicado_id=7).count()
    egresados_escuelas_especiales_no_autorizado_padres = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=7).count()
    egresados_escuelas_conducta_no_autorizado_padres = egresados_escuelas_conducta.filter(
        causa_no_ubicado_id=7).count()
    egresados_efi_no_autorizado_padres = egresados_efi.filter(causa_no_ubicado_id=7).count()
    menores_incapacitados_no_autorizado_padres = menores_incapacitados.filter(causa_no_ubicado_id=7).count()
    menores_desvinculados_no_autorizado_padres = menores_desvinculados.filter(causa_no_ubicado_id=7).count()
    menores_dictamen_no_autorizado_padres = menores_dictamen.filter(causa_no_ubicado_id=7).count()
    discapacitados_no_autorizado_padres = discapacitados.filter(causa_no_ubicado_id=7).count()
    mujeres_riesgo_pnr_no_autorizado_padres = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=7).count()
    hombres_riesgo_pnr_no_autorizado_padres = hombres_riesgo_pnr.filter(causa_no_ubicado_id=7).count()
    proxenetas_no_autorizado_padres = proxenetas.filter(causa_no_ubicado_id=7).count()

    worksheet_data.write(1, 15, 0, formato2)
    worksheet_data.write(2, 15, egresados_ep_no_autorizado_padres, formato2)
    worksheet_data.write(3, 15, sancionados_no_autorizado_padres, formato2)
    worksheet_data.write(4, 15, desvinculados_no_autorizado_padres, formato2)
    worksheet_data.write(5, 15, 0, formato2)
    worksheet_data.write(6, 15, tecnicos_medio_no_autorizado_padres, formato2)
    worksheet_data.write(7, 15, obreros_calificados_no_autorizado_padres, formato2)
    worksheet_data.write(8, 15, escuelas_oficio_no_autorizado_padres, formato2)
    worksheet_data.write(9, 15, egresados_escuelas_especiales_no_autorizado_padres, formato2)
    worksheet_data.write(10, 15, egresados_escuelas_conducta_no_autorizado_padres, formato2)
    worksheet_data.write(11, 15, egresados_efi_no_autorizado_padres, formato2)
    worksheet_data.write(12, 15, menores_incapacitados_no_autorizado_padres, formato2)
    worksheet_data.write(13, 15, menores_desvinculados_no_autorizado_padres, formato2)
    worksheet_data.write(14, 15, menores_dictamen_no_autorizado_padres, formato2)
    worksheet_data.write(15, 15, discapacitados_no_autorizado_padres, formato2)
    worksheet_data.write(16, 15, mujeres_riesgo_pnr_no_autorizado_padres, formato2)
    worksheet_data.write(17, 15, hombres_riesgo_pnr_no_autorizado_padres, formato2)
    worksheet_data.write(18, 15, proxenetas_no_autorizado_padres, formato2)

    # AL CUIDADO DE UN FAMILIAR
    egresados_ep_cuidado_familiar = egresados_ep.filter(causa_no_ubicado_id=8).count()
    sancionados_cuidado_familiar = sancionados.filter(causa_no_ubicado_id=8).count()
    desvinculados_cuidado_familiar = desvinculados.filter(causa_no_ubicado_id=8).count()
    tecnicos_medio_cuidado_familiar = tecnicos_medio.filter(causa_no_ubicado_id=8).count()
    obreros_calificados_cuidado_familiar = obreros_calificados.filter(causa_no_ubicado_id=8).count()
    escuelas_oficio_cuidado_familiar = escuelas_oficio.filter(causa_no_ubicado_id=8).count()
    egresados_escuelas_especiales_cuidado_familiar = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=8).count()
    egresados_escuelas_conducta_cuidado_familiar = egresados_escuelas_conducta.filter(causa_no_ubicado_id=8).count()
    egresados_efi_cuidado_familiar = egresados_efi.filter(causa_no_ubicado_id=8).count()
    menores_incapacitados_cuidado_familiar = menores_incapacitados.filter(causa_no_ubicado_id=8).count()
    menores_desvinculados_cuidado_familiar = menores_desvinculados.filter(causa_no_ubicado_id=8).count()
    menores_dictamen_cuidado_familiar = menores_dictamen.filter(causa_no_ubicado_id=8).count()
    discapacitados_cuidado_familiar = discapacitados.filter(causa_no_ubicado_id=8).count()
    mujeres_riesgo_pnr_cuidado_familiar = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=8).count()
    hombres_riesgo_pnr_cuidado_familiar = hombres_riesgo_pnr.filter(causa_no_ubicado_id=8).count()
    proxenetas_cuidado_familiar = proxenetas.filter(causa_no_ubicado_id=8).count()

    worksheet_data.write(1, 16, 0, formato2)
    worksheet_data.write(2, 16, egresados_ep_cuidado_familiar, formato2)
    worksheet_data.write(3, 16, sancionados_cuidado_familiar, formato2)
    worksheet_data.write(4, 16, desvinculados_cuidado_familiar, formato2)
    worksheet_data.write(5, 16, 0, formato2)
    worksheet_data.write(6, 16, tecnicos_medio_cuidado_familiar, formato2)
    worksheet_data.write(7, 16, obreros_calificados_cuidado_familiar, formato2)
    worksheet_data.write(8, 16, escuelas_oficio_cuidado_familiar, formato2)
    worksheet_data.write(9, 16, egresados_escuelas_especiales_cuidado_familiar, formato2)
    worksheet_data.write(10, 16, egresados_escuelas_conducta_cuidado_familiar, formato2)
    worksheet_data.write(11, 16, egresados_efi_cuidado_familiar, formato2)
    worksheet_data.write(12, 16, menores_incapacitados_cuidado_familiar, formato2)
    worksheet_data.write(13, 16, menores_desvinculados_cuidado_familiar, formato2)
    worksheet_data.write(14, 16, menores_dictamen_cuidado_familiar, formato2)
    worksheet_data.write(15, 16, discapacitados_cuidado_familiar, formato2)
    worksheet_data.write(16, 16, mujeres_riesgo_pnr_cuidado_familiar, formato2)
    worksheet_data.write(17, 16, hombres_riesgo_pnr_cuidado_familiar, formato2)
    worksheet_data.write(18, 16, proxenetas_cuidado_familiar, formato2)

    # NO HAY OFERTAS ACORDE A SU DISCAPACIDAD
    egresados_ep_no_ofertas_acorde_discapacidad = egresados_ep.filter(causa_no_ubicado_id=9).count()
    sancionados_no_ofertas_acorde_discapacidad = sancionados.filter(causa_no_ubicado_id=9).count()
    desvinculados_no_ofertas_acorde_discapacidad = desvinculados.filter(causa_no_ubicado_id=9).count()
    tecnicos_medio_no_ofertas_acorde_discapacidad = tecnicos_medio.filter(causa_no_ubicado_id=9).count()
    obreros_calificados_no_ofertas_acorde_discapacidad = obreros_calificados.filter(causa_no_ubicado_id=9).count()
    escuelas_oficio_no_ofertas_acorde_discapacidad = escuelas_oficio.filter(causa_no_ubicado_id=9).count()
    egresados_escuelas_especiales_no_ofertas_acorde_discapacidad = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=9).count()
    egresados_escuelas_conducta_no_ofertas_acorde_discapacidad = egresados_escuelas_conducta.filter(
        causa_no_ubicado_id=9).count()
    egresados_efi_no_ofertas_acorde_discapacidad = egresados_efi.filter(causa_no_ubicado_id=9).count()
    menores_incapacitados_no_ofertas_acorde_discapacidad = menores_incapacitados.filter(
        causa_no_ubicado_id=9).count()
    menores_desvinculados_no_ofertas_acorde_discapacidad = menores_desvinculados.filter(
        causa_no_ubicado_id=9).count()
    menores_dictamen_no_ofertas_acorde_discapacidad = menores_dictamen.filter(causa_no_ubicado_id=9).count()
    discapacitados_no_ofertas_acorde_discapacidad = discapacitados.filter(causa_no_ubicado_id=9).count()
    mujeres_riesgo_pnr_no_ofertas_acorde_discapacidad = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=9).count()
    hombres_riesgo_pnr_no_ofertas_acorde_discapacidad = hombres_riesgo_pnr.filter(causa_no_ubicado_id=9).count()
    proxenetas_no_ofertas_acorde_discapacidad = proxenetas.filter(causa_no_ubicado_id=9).count()

    worksheet_data.write(1, 17, 0, formato2)
    worksheet_data.write(2, 17, egresados_ep_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(3, 17, sancionados_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(4, 17, desvinculados_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(5, 17, 0, formato2)
    worksheet_data.write(6, 17, tecnicos_medio_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(7, 17, obreros_calificados_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(8, 17, escuelas_oficio_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(9, 17, egresados_escuelas_especiales_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(10, 17, egresados_escuelas_conducta_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(11, 17, egresados_efi_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(12, 17, menores_incapacitados_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(13, 17, menores_desvinculados_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(14, 17, menores_dictamen_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(15, 17, discapacitados_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(16, 17, mujeres_riesgo_pnr_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(17, 17, hombres_riesgo_pnr_no_ofertas_acorde_discapacidad, formato2)
    worksheet_data.write(18, 17, proxenetas_no_ofertas_acorde_discapacidad, formato2)

    # LO DEJO
    egresados_ep_lo_dejo = egresados_ep.filter(causa_no_ubicado_id=10).count()
    sancionados_lo_dejo = sancionados.filter(causa_no_ubicado_id=10).count()
    desvinculados_lo_dejo = desvinculados.filter(causa_no_ubicado_id=10).count()
    tecnicos_medio_lo_dejo = tecnicos_medio.filter(causa_no_ubicado_id=10).count()
    obreros_calificados_lo_dejo = obreros_calificados.filter(causa_no_ubicado_id=10).count()
    escuelas_oficio_lo_dejo = escuelas_oficio.filter(causa_no_ubicado_id=10).count()
    egresados_escuelas_especiales_lo_dejo = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=10).count()
    egresados_escuelas_conducta_lo_dejo = egresados_escuelas_conducta.filter(
        causa_no_ubicado_id=10).count()
    egresados_efi_lo_dejo = egresados_efi.filter(causa_no_ubicado_id=10).count()
    menores_incapacitados_lo_dejo = menores_incapacitados.filter(
        causa_no_ubicado_id=10).count()
    menores_desvinculados_lo_dejo = menores_desvinculados.filter(
        causa_no_ubicado_id=10).count()
    menores_dictamen_lo_dejo = menores_dictamen.filter(causa_no_ubicado_id=10).count()
    discapacitados_lo_dejo = discapacitados.filter(causa_no_ubicado_id=10).count()
    mujeres_riesgo_pnr_lo_dejo = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=10).count()
    hombres_riesgo_pnr_lo_dejo = hombres_riesgo_pnr.filter(causa_no_ubicado_id=10).count()
    proxenetas_lo_dejo = proxenetas.filter(causa_no_ubicado_id=10).count()

    worksheet_data.write(1, 18, 0, formato2)
    worksheet_data.write(2, 18, egresados_ep_lo_dejo, formato2)
    worksheet_data.write(3, 18, sancionados_lo_dejo, formato2)
    worksheet_data.write(4, 18, desvinculados_lo_dejo, formato2)
    worksheet_data.write(5, 18, 0, formato2)
    worksheet_data.write(6, 18, tecnicos_medio_lo_dejo, formato2)
    worksheet_data.write(7, 18, obreros_calificados_lo_dejo, formato2)
    worksheet_data.write(8, 18, escuelas_oficio_lo_dejo, formato2)
    worksheet_data.write(9, 18, egresados_escuelas_especiales_lo_dejo, formato2)
    worksheet_data.write(10, 18, egresados_escuelas_conducta_lo_dejo, formato2)
    worksheet_data.write(11, 18, egresados_efi_lo_dejo, formato2)
    worksheet_data.write(12, 18, menores_incapacitados_lo_dejo, formato2)
    worksheet_data.write(13, 18, menores_desvinculados_lo_dejo, formato2)
    worksheet_data.write(14, 18, menores_dictamen_lo_dejo, formato2)
    worksheet_data.write(15, 18, discapacitados_lo_dejo, formato2)
    worksheet_data.write(16, 18, mujeres_riesgo_pnr_lo_dejo, formato2)
    worksheet_data.write(17, 18, hombres_riesgo_pnr_lo_dejo, formato2)
    worksheet_data.write(18, 18, proxenetas_lo_dejo, formato2)

    # Revocado por los tribunales
    egresados_ep_embarazada = egresados_ep.filter(causa_no_ubicado_id=11).count()
    sancionados_embarazada = sancionados.filter(causa_no_ubicado_id=11).count()
    desvinculados_embarazada = desvinculados.filter(causa_no_ubicado_id=11).count()
    tecnicos_medio_embarazada = tecnicos_medio.filter(causa_no_ubicado_id=11).count()
    obreros_calificados_embarazada = obreros_calificados.filter(causa_no_ubicado_id=11).count()
    escuelas_oficio_embarazada = escuelas_oficio.filter(causa_no_ubicado_id=11).count()
    egresados_escuelas_especiales_embarazada = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=11).count()
    egresados_escuelas_conducta_embarazada = egresados_escuelas_conducta.filter(
        causa_no_ubicado_id=11).count()
    egresados_efi_embarazada = egresados_efi.filter(causa_no_ubicado_id=11).count()
    menores_incapacitados_embarazada = menores_incapacitados.filter(
        causa_no_ubicado_id=11).count()
    menores_desvinculados_embarazada = menores_desvinculados.filter(
        causa_no_ubicado_id=11).count()
    menores_dictamen_embarazada = menores_dictamen.filter(causa_no_ubicado_id=11).count()
    discapacitados_embarazada = discapacitados.filter(causa_no_ubicado_id=11).count()
    mujeres_riesgo_pnr_embarazada = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=11).count()
    hombres_riesgo_pnr_embarazada = hombres_riesgo_pnr.filter(causa_no_ubicado_id=11).count()
    proxenetas_embarazada = proxenetas.filter(causa_no_ubicado_id=11).count()

    worksheet_data.write(1, 19, 0, formato2)
    worksheet_data.write(2, 19, egresados_ep_embarazada, formato2)
    worksheet_data.write(3, 19, sancionados_embarazada, formato2)
    worksheet_data.write(4, 19, desvinculados_embarazada, formato2)
    worksheet_data.write(5, 19, 0, formato2)
    worksheet_data.write(6, 19, tecnicos_medio_embarazada, formato2)
    worksheet_data.write(7, 19, obreros_calificados_embarazada, formato2)
    worksheet_data.write(8, 19, escuelas_oficio_embarazada, formato2)
    worksheet_data.write(9, 19, egresados_escuelas_especiales_embarazada, formato2)
    worksheet_data.write(10, 19, egresados_escuelas_conducta_embarazada, formato2)
    worksheet_data.write(11, 19, egresados_efi_embarazada, formato2)
    worksheet_data.write(12, 9, menores_incapacitados_embarazada, formato2)
    worksheet_data.write(13, 19, menores_desvinculados_embarazada, formato2)
    worksheet_data.write(14, 9, menores_dictamen_embarazada, formato2)
    worksheet_data.write(15, 19, discapacitados_embarazada, formato2)
    worksheet_data.write(16, 19, mujeres_riesgo_pnr_embarazada, formato2)
    worksheet_data.write(17, 19, hombres_riesgo_pnr_embarazada, formato2)
    worksheet_data.write(18, 9, proxenetas_embarazada, formato2)

    # Revocado por los tribunales
    egresados_ep_revocado_tribunales = egresados_ep.filter(causa_no_ubicado_id=12).count()
    sancionados_revocado_tribunales = sancionados.filter(causa_no_ubicado_id=12).count()
    desvinculados_revocado_tribunales = desvinculados.filter(causa_no_ubicado_id=12).count()
    tecnicos_medio_revocado_tribunales = tecnicos_medio.filter(causa_no_ubicado_id=12).count()
    obreros_calificados_revocado_tribunales = obreros_calificados.filter(causa_no_ubicado_id=12).count()
    escuelas_oficio_revocado_tribunales = escuelas_oficio.filter(causa_no_ubicado_id=12).count()
    egresados_escuelas_especiales_revocado_tribunales = egresados_escuelas_especiales.filter(
        causa_no_ubicado_id=12).count()
    egresados_escuelas_conducta_revocado_tribunales = egresados_escuelas_conducta.filter(
        causa_no_ubicado_id=12).count()
    egresados_efi_revocado_tribunales = egresados_efi.filter(causa_no_ubicado_id=12).count()
    menores_incapacitados_revocado_tribunales = menores_incapacitados.filter(
        causa_no_ubicado_id=12).count()
    menores_desvinculados_revocado_tribunales = menores_desvinculados.filter(
        causa_no_ubicado_id=12).count()
    menores_dictamen_revocado_tribunales = menores_dictamen.filter(causa_no_ubicado_id=12).count()
    discapacitados_revocado_tribunales = discapacitados.filter(causa_no_ubicado_id=12).count()
    mujeres_riesgo_pnr_revocado_tribunales = mujeres_riesgo_pnr.filter(causa_no_ubicado_id=12).count()
    hombres_riesgo_pnr_revocado_tribunales = hombres_riesgo_pnr.filter(causa_no_ubicado_id=12).count()
    proxenetas_revocado_tribunales = proxenetas.filter(causa_no_ubicado_id=12).count()

    worksheet_data.write(1, 20, 0, formato2)
    worksheet_data.write(2, 20, egresados_ep_revocado_tribunales, formato2)
    worksheet_data.write(3, 20, sancionados_revocado_tribunales, formato2)
    worksheet_data.write(4, 20, desvinculados_revocado_tribunales, formato2)
    worksheet_data.write(5, 20, 0, formato2)
    worksheet_data.write(6, 20, tecnicos_medio_revocado_tribunales, formato2)
    worksheet_data.write(7, 20, obreros_calificados_revocado_tribunales, formato2)
    worksheet_data.write(8, 20, escuelas_oficio_revocado_tribunales, formato2)
    worksheet_data.write(9, 20, egresados_escuelas_especiales_revocado_tribunales, formato2)
    worksheet_data.write(10, 20, egresados_escuelas_conducta_revocado_tribunales, formato2)
    worksheet_data.write(11, 20, egresados_efi_revocado_tribunales, formato2)
    worksheet_data.write(12, 20, menores_incapacitados_revocado_tribunales, formato2)
    worksheet_data.write(13, 20, menores_desvinculados_revocado_tribunales, formato2)
    worksheet_data.write(14, 20, menores_dictamen_revocado_tribunales, formato2)
    worksheet_data.write(15, 20, discapacitados_revocado_tribunales, formato2)
    worksheet_data.write(16, 20, mujeres_riesgo_pnr_revocado_tribunales, formato2)
    worksheet_data.write(17, 20, hombres_riesgo_pnr_revocado_tribunales, formato2)
    worksheet_data.write(18, 20, proxenetas_revocado_tribunales, formato2)

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
    total_embarazada = '=SUM(%s)' % xl_range(1, 19, cantidad_fuentes, 19)
    total_revocado_tribunales= '=SUM(%s)' % xl_range(1, 20, cantidad_fuentes, 20)

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
    worksheet_data.write(indice_total, 19, total_embarazada, formato2)
    worksheet_data.write(indice_total, 20, total_revocado_tribunales, formato2)

    book.close()

    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    return response
