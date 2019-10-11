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
def total_personas_ubicadas_provincias_y_municipios_cierre_mes(request):
    start_time = time.time()

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    anno = datetime.today().year
    mes = datetime.today().month
    nombre_anno = anno

    if mes == 1:
        nombre_anno = anno - 1

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    if categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Total_de_personas_ubicadas_por_provincia_y_municipios_(Cierre_del_mes_anterior)._(%s).xlsx" % (nombre_anno)

    elif categoria_usuario == 'dmt':
        response['Content-Disposition'] = "attachment; filename=Total_de_personas_ubicadas_(Cierre_del_mes_anterior)._(%s).xlsx" % (nombre_anno)

    else:
        response['Content-Disposition'] = "attachment; filename=Total_de_personas_ubicadas_por_provincias_y_municipios_(Cierre_del_mes_anterior)._(%s).xlsx" % (nombre_anno)

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    fuentes_procedencia = FuenteProcedencia.objects.filter(activo=True).exclude(id=5).order_by('id')
    cantidad_fuentes = fuentes_procedencia.count()
    indice = 7

    for fuente in fuentes_procedencia:
        worksheet_data.write(0, indice, fuente.nombre, formato)
        indice = indice + 1

    if categoria_usuario == 'dpt_ee':
        worksheet_data.write("A1", "Provincia / Municipios", formato)
        worksheet_data.set_column("A:A", 21)

        provincias = Provincia.objects.filter(id=provincia_usuario.id)
        municipios = Municipio.objects.filter(provincia=provincia_usuario)

    elif categoria_usuario == 'dmt':
        worksheet_data.write("A1", "Municipio", formato)
        worksheet_data.set_column("A:A", 17)

        municipio = Municipio.objects.get(id=municipio_usuario.id)
    else:
        worksheet_data.write("A1", "Provincias / Municipio", formato)
        worksheet_data.set_column("A:A", 21)

        provincias = Provincia.objects.all()
        municipios = Municipio.objects.all()

    worksheet_data.write("B1", "Controlados", formato)
    worksheet_data.write("C1", "Mujeres controladas", formato)
    worksheet_data.write("D1", "Jovenes controlados", formato)
    worksheet_data.write("E1", "Ubicados", formato)
    worksheet_data.write("F1", "Mujeres ubicadas", formato)
    worksheet_data.write("G1", "Jovenes ubicados", formato)

    worksheet_data.set_column("A:A", 17)
    worksheet_data.set_column("B:B", 11)
    worksheet_data.set_column("C:C", 10)
    worksheet_data.set_column("D:D", 10)
    worksheet_data.set_column("E:E", 10)
    worksheet_data.set_column("F:F", 10)
    worksheet_data.set_column("G:G", 10)

    licenciados_sma = LicenciadosSMA.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_licenciadossma" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = LicenciadosSMA.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    licenciados_sma = licenciados_sma.exclude(id__in=ids_listado)

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

    desvinculados = Desvinculado.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_desvinculado" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Desvinculado.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    desvinculados = desvinculados.exclude(id__in=ids_listado)

    tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6,
                                                             activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 6;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    tecnicos_medio = tecnicos_medio.exclude(id__in=ids_listado)

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

    escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=8,
                                                                activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 8;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    escuelas_oficio = escuelas_oficio.exclude(id__in=ids_listado)

    egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosescuelasespeciales" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEscuelasEspeciales.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_escuelas_especiales = egresados_escuelas_especiales.exclude(id__in=ids_listado)

    egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosescuelasconducta" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEscuelasConducta.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_escuelas_conducta = egresados_escuelas_conducta.exclude(id__in=ids_listado)

    egresados_efi = EgresadosEFI.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosefi" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEFI.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_efi = egresados_efi.exclude(id__in=ids_listado)

    menores_incapacitados = Menores.objects.filter(fuente_procedencia_id=12, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 12;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_incapacitados = menores_incapacitados.exclude(id__in=ids_listado)

    menores_desvinculados = Menores.objects.filter(fuente_procedencia_id=13, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 13;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_desvinculados = menores_desvinculados.exclude(id__in=ids_listado)

    menores_dictamen = Menores.objects.filter(fuente_procedencia_id=14, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 14;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_dictamen = menores_dictamen.exclude(id__in=ids_listado)

    discapacitados = Discapacitados.objects.filter(activo=True)

    query = """SELECT id
                    FROM public."SGMGU_discapacitados" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Discapacitados.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    discapacitados = discapacitados.exclude(id__in=ids_listado)

    mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=17, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 17;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    mujeres_riesgo_pnr = mujeres_riesgo_pnr.exclude(id__in=ids_listado)

    hombres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=18, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 18;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    hombres_riesgo_pnr = hombres_riesgo_pnr.exclude(id__in=ids_listado)

    proxenetas = PersonasRiesgo.objects.filter(fuente_procedencia_id=19, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 19;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    proxenetas = proxenetas.exclude(id__in=ids_listado)

    edades_jovenes = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    INDICE = 1

    total_controlados = 0
    total_mujeres_controladas = 0
    total_jovenes_controlados = 0
    total_ubicados = 0
    total_mujeres_ubicadas = 0
    total_jovenes_ubicados = 0
    total_licenciados_sma = 0
    total_egresados_ep = 0
    total_sancionados = 0
    total_desvinculados = 0
    total_tecnicos_medio = 0
    total_obreros_calificados = 0
    total_escuelas_oficio = 0
    total_egresados_escuelas_especiales = 0
    total_egresados_escuelas_conducta = 0
    total_egresados_efi = 0
    total_menores_incapacitados = 0
    total_menores_desvinculados = 0
    total_menores_dictamen = 0
    total_discapacitados = 0
    total_mujeres_riesgo_pnr = 0
    total_hombres_riesgo_pnr = 0
    total_proxenetas = 0

    if categoria_usuario == 'administrador' or categoria_usuario == 'dpt_ee':

        for provincia in provincias:

            worksheet_data.write(INDICE, 0, provincia.nombre, formato)

            controlados_provincia = licenciados_sma.filter(municipio_residencia__provincia=provincia).count() + \
                                    egresados_ep.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    sancionados.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    desvinculados.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    egresados_escuelas_especiales.filter(
                                        municipio_solicita_empleo__provincia=provincia).count() + \
                                    egresados_escuelas_conducta.filter(
                                        municipio_solicita_empleo__provincia=provincia).count() + \
                                    egresados_efi.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    discapacitados.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia).count() + \
                                    proxenetas.filter(municipio_solicita_empleo__provincia=provincia).count()

            total_controlados += controlados_provincia
            worksheet_data.write(INDICE, 1, controlados_provincia, formato)

            mujeres_controladas_provincia = licenciados_sma.filter(municipio_residencia__provincia=provincia,
                                                                   sexo='F').count() + \
                                            egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                                sexo='F').count() + \
                                            sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                               sexo='F').count() + \
                                            desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 sexo='F').count() + \
                                            tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                  sexo='F').count() + \
                                            obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                       sexo='F').count() + \
                                            escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   sexo='F').count() + \
                                            egresados_escuelas_especiales.filter(
                                                municipio_solicita_empleo__provincia=provincia, sexo='F').count() + \
                                            egresados_escuelas_conducta.filter(
                                                municipio_solicita_empleo__provincia=provincia, sexo='F').count() + \
                                            egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 sexo='F').count() + \
                                            menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                         sexo='F').count() + \
                                            menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                         sexo='F').count() + \
                                            menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                                    sexo='F').count() + \
                                            discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                  sexo='F').count() + \
                                            mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      sexo='F').count() + \
                                            hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      sexo='F').count() + \
                                            proxenetas.filter(municipio_solicita_empleo__provincia=provincia,
                                                              sexo='F').count()

            total_mujeres_controladas += mujeres_controladas_provincia
            worksheet_data.write(INDICE, 2, mujeres_controladas_provincia, formato)

            jovenes_controlados_provincia = licenciados_sma.filter(municipio_residencia__provincia=provincia,
                                                                   edad__in=edades_jovenes).count() + \
                                            egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                                edad__in=edades_jovenes).count() + \
                                            sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                               edad__in=edades_jovenes).count() + \
                                            desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 edad__in=edades_jovenes).count() + \
                                            tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                  edad__in=edades_jovenes).count() + \
                                            obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                       edad__in=edades_jovenes).count() + \
                                            escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   edad__in=edades_jovenes).count() + \
                                            egresados_escuelas_especiales.filter(
                                                municipio_solicita_empleo__provincia=provincia,
                                                edad__in=edades_jovenes).count() + \
                                            egresados_escuelas_conducta.filter(
                                                municipio_solicita_empleo__provincia=provincia,
                                                edad__in=edades_jovenes).count() + \
                                            egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 edad__in=edades_jovenes).count() + \
                                            menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                         edad__in=edades_jovenes).count() + \
                                            menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                         edad__in=edades_jovenes).count() + \
                                            menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                                    edad__in=edades_jovenes).count() + \
                                            discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                  edad__in=edades_jovenes).count() + \
                                            mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      edad__in=edades_jovenes).count() + \
                                            hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      edad__in=edades_jovenes).count() + \
                                            proxenetas.filter(municipio_solicita_empleo__provincia=provincia,
                                                              edad__in=edades_jovenes).count()

            total_jovenes_controlados += jovenes_controlados_provincia
            worksheet_data.write(INDICE, 3, jovenes_controlados_provincia, formato)

            ubicados_provincia = licenciados_sma.filter(municipio_residencia__provincia=provincia).count() + \
                                 egresados_ep.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count() + \
                                 sancionados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count() + \
                                 desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                      ubicado=True).count() + \
                                 tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                       ubicado=True).count() + \
                                 obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia,
                                                            ubicado=True).count() + \
                                 escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                        ubicado=True).count() + \
                                 egresados_escuelas_especiales.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      ubicado=True).count() + \
                                 egresados_escuelas_conducta.filter(municipio_solicita_empleo__provincia=provincia,
                                                                    ubicado=True).count() + \
                                 egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                      ubicado=True).count() + \
                                 menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                              ubicado=True).count() + \
                                 menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                              ubicado=True).count() + \
                                 menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=True).count() + \
                                 discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                       ubicado=True).count() + \
                                 mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True).count() + \
                                 hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True).count() + \
                                 proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count()

            total_ubicados += ubicados_provincia
            worksheet_data.write(INDICE, 4, ubicados_provincia, formato)

            mujeres_ubicadas_provincia = licenciados_sma.filter(municipio_residencia__provincia=provincia,
                                                                sexo='F').count() + \
                                         egresados_ep.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                             sexo='F').count() + \
                                         sancionados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                            sexo='F').count() + \
                                         desvinculados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                              sexo='F').count() + \
                                         tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                               sexo='F').count() + \
                                         obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                    ubicado=True, sexo='F').count() + \
                                         escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                ubicado=True, sexo='F').count() + \
                                         egresados_escuelas_especiales.filter(
                                             municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                             sexo='F').count() + \
                                         egresados_escuelas_conducta.filter(municipio_solicita_empleo__provincia=provincia,
                                                                            ubicado=True, sexo='F').count() + \
                                         egresados_efi.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                              sexo='F').count() + \
                                         menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      ubicado=True, sexo='F').count() + \
                                         menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      ubicado=True, sexo='F').count() + \
                                         menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 ubicado=True, sexo='F').count() + \
                                         discapacitados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                               sexo='F').count() + \
                                         mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   ubicado=True, sexo='F').count() + \
                                         hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   ubicado=True, sexo='F').count() + \
                                         proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                           sexo='F').count()

            total_mujeres_ubicadas += mujeres_ubicadas_provincia
            worksheet_data.write(INDICE, 5, mujeres_ubicadas_provincia, formato)

            jovenes_ubicados_provincia = licenciados_sma.filter(municipio_residencia__provincia=provincia,
                                                                edad__in=edades_jovenes).count() + \
                                         egresados_ep.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                             edad__in=edades_jovenes).count() + \
                                         sancionados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                            edad__in=edades_jovenes).count() + \
                                         desvinculados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                              edad__in=edades_jovenes).count() + \
                                         tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                               edad__in=edades_jovenes).count() + \
                                         obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                    ubicado=True, edad__in=edades_jovenes).count() + \
                                         escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                ubicado=True, edad__in=edades_jovenes).count() + \
                                         egresados_escuelas_especiales.filter(
                                             municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                             edad__in=edades_jovenes).count() + \
                                         egresados_escuelas_conducta.filter(municipio_solicita_empleo__provincia=provincia,
                                                                            ubicado=True, edad__in=edades_jovenes).count() + \
                                         egresados_efi.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                              edad__in=edades_jovenes).count() + \
                                         menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      ubicado=True, edad__in=edades_jovenes).count() + \
                                         menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                      ubicado=True, edad__in=edades_jovenes).count() + \
                                         menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 ubicado=True, edad__in=edades_jovenes).count() + \
                                         discapacitados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                               edad__in=edades_jovenes).count() + \
                                         mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   ubicado=True, edad__in=edades_jovenes).count() + \
                                         hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   ubicado=True, edad__in=edades_jovenes).count() + \
                                         proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True,
                                                           edad__in=edades_jovenes).count()

            total_jovenes_ubicados += jovenes_ubicados_provincia
            worksheet_data.write(INDICE, 6, jovenes_ubicados_provincia, formato)

            licenciados_sma_provincia = licenciados_sma.filter(municipio_residencia__provincia=provincia).count()
            egresados_ep_provincia = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=True).count()
            sancionados_provincia = sancionados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
            desvinculados_provincia = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True).count()
            tecnicos_medio_provincia = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=True).count()
            obreros_calificados_provincia = obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                       ubicado=True).count()
            escuelas_oficio_provincia = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=True).count()
            egresados_escuelas_especiales_provincia = egresados_escuelas_especiales.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
            egresados_escuelas_conducta_provincia = egresados_escuelas_conducta.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=True).count()
            egresados_efi_provincia = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=True).count()
            menores_incapacitados_provincia = menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                           ubicado=True).count()
            menores_desvinculados_provincia = menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                                           ubicado=True).count()
            menores_dictamen_provincia = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 ubicado=True).count()
            discapacitados_provincia = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=True).count()
            mujeres_riesgo_pnr_provincia = mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                     ubicado=True).count()
            hombres_riesgo_pnr_provincia = hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia,
                                                                     ubicado=True).count()
            proxenetas_provincia = proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=True).count()

            total_licenciados_sma += licenciados_sma_provincia
            total_egresados_ep += egresados_ep_provincia
            total_sancionados += sancionados_provincia
            total_desvinculados += desvinculados_provincia
            total_tecnicos_medio += tecnicos_medio_provincia
            total_obreros_calificados += obreros_calificados_provincia
            total_escuelas_oficio += escuelas_oficio_provincia
            total_egresados_escuelas_especiales += egresados_escuelas_especiales_provincia
            total_egresados_escuelas_conducta += egresados_escuelas_conducta_provincia
            total_egresados_efi += egresados_efi_provincia
            total_menores_incapacitados += menores_incapacitados_provincia
            total_menores_desvinculados += menores_desvinculados_provincia
            total_menores_dictamen += menores_dictamen_provincia
            total_discapacitados += discapacitados_provincia
            total_mujeres_riesgo_pnr += mujeres_riesgo_pnr_provincia
            total_hombres_riesgo_pnr += hombres_riesgo_pnr_provincia
            total_proxenetas += proxenetas_provincia

            worksheet_data.write(INDICE, 7, licenciados_sma_provincia, formato)
            worksheet_data.write(INDICE, 8, egresados_ep_provincia, formato)
            worksheet_data.write(INDICE, 9, sancionados_provincia, formato)
            worksheet_data.write(INDICE, 10, desvinculados_provincia, formato)
            worksheet_data.write(INDICE, 11, tecnicos_medio_provincia, formato)
            worksheet_data.write(INDICE, 12, obreros_calificados_provincia, formato)
            worksheet_data.write(INDICE, 13, escuelas_oficio_provincia, formato)
            worksheet_data.write(INDICE, 14, egresados_escuelas_especiales_provincia, formato)
            worksheet_data.write(INDICE, 15, egresados_escuelas_conducta_provincia, formato)
            worksheet_data.write(INDICE, 16, egresados_efi_provincia, formato)
            worksheet_data.write(INDICE, 17, menores_incapacitados_provincia, formato)
            worksheet_data.write(INDICE, 18, menores_desvinculados_provincia, formato)
            worksheet_data.write(INDICE, 19, menores_dictamen_provincia, formato)
            worksheet_data.write(INDICE, 20, discapacitados_provincia, formato)
            worksheet_data.write(INDICE, 21, mujeres_riesgo_pnr_provincia, formato)
            worksheet_data.write(INDICE, 22, hombres_riesgo_pnr_provincia, formato)
            worksheet_data.write(INDICE, 23, proxenetas_provincia, formato)

            INDICE += 1

            MUNICIPIOS_X = municipios.filter(provincia=provincia)
            for municipio in MUNICIPIOS_X:
                worksheet_data.write(INDICE, 0, municipio.nombre, formato2)

                controlados_provincia = licenciados_sma.filter(municipio_residencia=municipio).count() + \
                                        egresados_ep.filter(municipio_solicita_empleo=municipio).count() + \
                                        sancionados.filter(municipio_solicita_empleo=municipio).count() + \
                                        desvinculados.filter(municipio_solicita_empleo=municipio).count() + \
                                        tecnicos_medio.filter(municipio_solicita_empleo=municipio).count() + \
                                        obreros_calificados.filter(municipio_solicita_empleo=municipio).count() + \
                                        escuelas_oficio.filter(municipio_solicita_empleo=municipio).count() + \
                                        egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio).count() + \
                                        egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio).count() + \
                                        egresados_efi.filter(municipio_solicita_empleo=municipio).count() + \
                                        menores_incapacitados.filter(municipio_solicita_empleo=municipio).count() + \
                                        menores_desvinculados.filter(municipio_solicita_empleo=municipio).count() + \
                                        menores_dictamen.filter(municipio_solicita_empleo=municipio).count() + \
                                        discapacitados.filter(municipio_solicita_empleo=municipio).count() + \
                                        mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio).count() + \
                                        hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio).count() + \
                                        proxenetas.filter(municipio_solicita_empleo=municipio).count()

                worksheet_data.write(INDICE, 1, controlados_provincia, formato2)

                mujeres_controladas_provincia = licenciados_sma.filter(municipio_residencia=municipio, sexo='F').count() + \
                                                egresados_ep.filter(municipio_solicita_empleo=municipio, sexo='F').count() + \
                                                sancionados.filter(municipio_solicita_empleo=municipio, sexo='F').count() + \
                                                desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                     sexo='F').count() + \
                                                tecnicos_medio.filter(municipio_solicita_empleo=municipio,
                                                                      sexo='F').count() + \
                                                obreros_calificados.filter(municipio_solicita_empleo=municipio,
                                                                           sexo='F').count() + \
                                                escuelas_oficio.filter(municipio_solicita_empleo=municipio,
                                                                       sexo='F').count() + \
                                                egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                                     sexo='F').count() + \
                                                egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                                   sexo='F').count() + \
                                                egresados_efi.filter(municipio_solicita_empleo=municipio,
                                                                     sexo='F').count() + \
                                                menores_incapacitados.filter(municipio_solicita_empleo=municipio,
                                                                             sexo='F').count() + \
                                                menores_desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                             sexo='F').count() + \
                                                menores_dictamen.filter(municipio_solicita_empleo=municipio,
                                                                        sexo='F').count() + \
                                                discapacitados.filter(municipio_solicita_empleo=municipio,
                                                                      sexo='F').count() + \
                                                mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio,
                                                                          sexo='F').count() + \
                                                hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio,
                                                                          sexo='F').count() + \
                                                proxenetas.filter(municipio_solicita_empleo=municipio, sexo='F').count()

                worksheet_data.write(INDICE, 2, mujeres_controladas_provincia, formato2)

                jovenes_controlados_provincia = licenciados_sma.filter(municipio_residencia=municipio,
                                                                       edad__in=edades_jovenes).count() + \
                                                egresados_ep.filter(municipio_solicita_empleo=municipio,
                                                                    edad__in=edades_jovenes).count() + \
                                                sancionados.filter(municipio_solicita_empleo=municipio,
                                                                   edad__in=edades_jovenes).count() + \
                                                desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                     edad__in=edades_jovenes).count() + \
                                                tecnicos_medio.filter(municipio_solicita_empleo=municipio,
                                                                      edad__in=edades_jovenes).count() + \
                                                obreros_calificados.filter(municipio_solicita_empleo=municipio,
                                                                           edad__in=edades_jovenes).count() + \
                                                escuelas_oficio.filter(municipio_solicita_empleo=municipio,
                                                                       edad__in=edades_jovenes).count() + \
                                                egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                                     edad__in=edades_jovenes).count() + \
                                                egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                                   edad__in=edades_jovenes).count() + \
                                                egresados_efi.filter(municipio_solicita_empleo=municipio,
                                                                     edad__in=edades_jovenes).count() + \
                                                menores_incapacitados.filter(municipio_solicita_empleo=municipio,
                                                                             edad__in=edades_jovenes).count() + \
                                                menores_desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                             edad__in=edades_jovenes).count() + \
                                                menores_dictamen.filter(municipio_solicita_empleo=municipio,
                                                                        edad__in=edades_jovenes).count() + \
                                                discapacitados.filter(municipio_solicita_empleo=municipio,
                                                                      edad__in=edades_jovenes).count() + \
                                                mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio,
                                                                          edad__in=edades_jovenes).count() + \
                                                hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio,
                                                                          edad__in=edades_jovenes).count() + \
                                                proxenetas.filter(municipio_solicita_empleo=municipio,
                                                                  edad__in=edades_jovenes).count()

                worksheet_data.write(INDICE, 3, jovenes_controlados_provincia, formato2)

                ubicados_provincia = licenciados_sma.filter(municipio_residencia=municipio).count() + \
                                     egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     sancionados.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                          ubicado=True).count() + \
                                     egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                        ubicado=True).count() + \
                                     egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     menores_incapacitados.filter(municipio_solicita_empleo=municipio,
                                                                  ubicado=True).count() + \
                                     menores_desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                  ubicado=True).count() + \
                                     menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                                     proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=True).count()

                worksheet_data.write(INDICE, 4, ubicados_provincia, formato2)

                mujeres_ubicadas_provincia = licenciados_sma.filter(municipio_residencia=municipio, sexo='F').count() + \
                                             egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                 sexo='F').count() + \
                                             sancionados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                sexo='F').count() + \
                                             desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                  sexo='F').count() + \
                                             tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                   sexo='F').count() + \
                                             obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                        sexo='F').count() + \
                                             escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                    sexo='F').count() + \
                                             egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                                  ubicado=True, sexo='F').count() + \
                                             egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                                ubicado=True, sexo='F').count() + \
                                             egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                  sexo='F').count() + \
                                             menores_incapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                          sexo='F').count() + \
                                             menores_desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                          sexo='F').count() + \
                                             menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                     sexo='F').count() + \
                                             discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                   sexo='F').count() + \
                                             mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                       sexo='F').count() + \
                                             hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                       sexo='F').count() + \
                                             proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                               sexo='F').count()

                worksheet_data.write(INDICE, 5, mujeres_ubicadas_provincia, formato2)

                jovenes_ubicados_provincia = licenciados_sma.filter(municipio_residencia=municipio,
                                                                    edad__in=edades_jovenes).count() + \
                                             egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                 edad__in=edades_jovenes).count() + \
                                             sancionados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                edad__in=edades_jovenes).count() + \
                                             desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                  edad__in=edades_jovenes).count() + \
                                             tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                   edad__in=edades_jovenes).count() + \
                                             obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                        edad__in=edades_jovenes).count() + \
                                             escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                    edad__in=edades_jovenes).count() + \
                                             egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                                  ubicado=True,
                                                                                  edad__in=edades_jovenes).count() + \
                                             egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                                ubicado=True,
                                                                                edad__in=edades_jovenes).count() + \
                                             egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                  edad__in=edades_jovenes).count() + \
                                             menores_incapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                          edad__in=edades_jovenes).count() + \
                                             menores_desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                          edad__in=edades_jovenes).count() + \
                                             menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                     edad__in=edades_jovenes).count() + \
                                             discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                   edad__in=edades_jovenes).count() + \
                                             mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                       edad__in=edades_jovenes).count() + \
                                             hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                       edad__in=edades_jovenes).count() + \
                                             proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                               edad__in=edades_jovenes).count()

                worksheet_data.write(INDICE, 6, jovenes_ubicados_provincia, formato2)

                worksheet_data.write(INDICE, 7, licenciados_sma.filter(municipio_residencia=municipio).count(), formato2)
                worksheet_data.write(INDICE, 8,
                                     egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 9,
                                     sancionados.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 10,
                                     desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 11,
                                     tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 12,
                                     obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 13,
                                     escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 14, egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                                      ubicado=True).count(), formato2)
                worksheet_data.write(INDICE, 15, egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                                    ubicado=True).count(), formato2)
                worksheet_data.write(INDICE, 16,
                                     egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 17, menores_incapacitados.filter(municipio_solicita_empleo=municipio,
                                                                              ubicado=True).count(), formato2)
                worksheet_data.write(INDICE, 18, menores_desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                              ubicado=True).count(), formato2)
                worksheet_data.write(INDICE, 19,
                                     menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 20,
                                     discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 21,
                                     mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 22,
                                     hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                                     formato2)
                worksheet_data.write(INDICE, 23,
                                     proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=True).count(), formato2)

                INDICE += 1

        if categoria_usuario == 'administrador':
            # ------------ SUMAS ABAJO-------------------
            worksheet_data.write(INDICE, 0, "Total", formato)
            worksheet_data.write(INDICE, 1, total_controlados, formato)
            worksheet_data.write(INDICE, 2, total_mujeres_controladas, formato)
            worksheet_data.write(INDICE, 3, total_jovenes_controlados, formato)
            worksheet_data.write(INDICE, 4, total_ubicados, formato)
            worksheet_data.write(INDICE, 5, total_mujeres_ubicadas, formato)
            worksheet_data.write(INDICE, 6, total_jovenes_ubicados, formato)
            worksheet_data.write(INDICE, 7, total_licenciados_sma, formato)
            worksheet_data.write(INDICE, 8, total_egresados_ep, formato)
            worksheet_data.write(INDICE, 9, total_sancionados, formato)
            worksheet_data.write(INDICE, 10, total_desvinculados, formato)
            worksheet_data.write(INDICE, 11, total_tecnicos_medio, formato)
            worksheet_data.write(INDICE, 12, total_obreros_calificados, formato)
            worksheet_data.write(INDICE, 13, total_escuelas_oficio, formato)
            worksheet_data.write(INDICE, 14, total_egresados_escuelas_especiales, formato)
            worksheet_data.write(INDICE, 15, total_egresados_escuelas_conducta, formato)
            worksheet_data.write(INDICE, 16, total_egresados_efi, formato)
            worksheet_data.write(INDICE, 17, total_menores_incapacitados, formato)
            worksheet_data.write(INDICE, 18, total_menores_desvinculados, formato)
            worksheet_data.write(INDICE, 19, total_menores_dictamen, formato)
            worksheet_data.write(INDICE, 20, total_discapacitados, formato)
            worksheet_data.write(INDICE, 21, total_mujeres_riesgo_pnr, formato)
            worksheet_data.write(INDICE, 22, total_hombres_riesgo_pnr, formato)
            worksheet_data.write(INDICE, 23, total_proxenetas, formato)

    if categoria_usuario == 'dmt':

        worksheet_data.write(INDICE, 0, municipio.nombre, formato2)

        controlados_provincia = licenciados_sma.filter(municipio_residencia=municipio).count() + \
                                egresados_ep.filter(municipio_solicita_empleo=municipio).count() + \
                                sancionados.filter(municipio_solicita_empleo=municipio).count() + \
                                desvinculados.filter(municipio_solicita_empleo=municipio).count() + \
                                tecnicos_medio.filter(municipio_solicita_empleo=municipio).count() + \
                                obreros_calificados.filter(municipio_solicita_empleo=municipio).count() + \
                                escuelas_oficio.filter(municipio_solicita_empleo=municipio).count() + \
                                egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio).count() + \
                                egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio).count() + \
                                egresados_efi.filter(municipio_solicita_empleo=municipio).count() + \
                                menores_incapacitados.filter(municipio_solicita_empleo=municipio).count() + \
                                menores_desvinculados.filter(municipio_solicita_empleo=municipio).count() + \
                                menores_dictamen.filter(municipio_solicita_empleo=municipio).count() + \
                                discapacitados.filter(municipio_solicita_empleo=municipio).count() + \
                                mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio).count() + \
                                hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio).count() + \
                                proxenetas.filter(municipio_solicita_empleo=municipio).count()

        worksheet_data.write(INDICE, 1, controlados_provincia, formato2)

        mujeres_controladas_provincia = licenciados_sma.filter(municipio_residencia=municipio, sexo='F').count() + \
                                        egresados_ep.filter(municipio_solicita_empleo=municipio, sexo='F').count() + \
                                        sancionados.filter(municipio_solicita_empleo=municipio, sexo='F').count() + \
                                        desvinculados.filter(municipio_solicita_empleo=municipio,
                                                             sexo='F').count() + \
                                        tecnicos_medio.filter(municipio_solicita_empleo=municipio,
                                                              sexo='F').count() + \
                                        obreros_calificados.filter(municipio_solicita_empleo=municipio,
                                                                   sexo='F').count() + \
                                        escuelas_oficio.filter(municipio_solicita_empleo=municipio,
                                                               sexo='F').count() + \
                                        egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                             sexo='F').count() + \
                                        egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                           sexo='F').count() + \
                                        egresados_efi.filter(municipio_solicita_empleo=municipio,
                                                             sexo='F').count() + \
                                        menores_incapacitados.filter(municipio_solicita_empleo=municipio,
                                                                     sexo='F').count() + \
                                        menores_desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                     sexo='F').count() + \
                                        menores_dictamen.filter(municipio_solicita_empleo=municipio,
                                                                sexo='F').count() + \
                                        discapacitados.filter(municipio_solicita_empleo=municipio,
                                                              sexo='F').count() + \
                                        mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio,
                                                                  sexo='F').count() + \
                                        hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio,
                                                                  sexo='F').count() + \
                                        proxenetas.filter(municipio_solicita_empleo=municipio, sexo='F').count()

        worksheet_data.write(INDICE, 2, mujeres_controladas_provincia, formato2)

        jovenes_controlados_provincia = licenciados_sma.filter(municipio_residencia=municipio,
                                                               edad__in=edades_jovenes).count() + \
                                        egresados_ep.filter(municipio_solicita_empleo=municipio,
                                                            edad__in=edades_jovenes).count() + \
                                        sancionados.filter(municipio_solicita_empleo=municipio,
                                                           edad__in=edades_jovenes).count() + \
                                        desvinculados.filter(municipio_solicita_empleo=municipio,
                                                             edad__in=edades_jovenes).count() + \
                                        tecnicos_medio.filter(municipio_solicita_empleo=municipio,
                                                              edad__in=edades_jovenes).count() + \
                                        obreros_calificados.filter(municipio_solicita_empleo=municipio,
                                                                   edad__in=edades_jovenes).count() + \
                                        escuelas_oficio.filter(municipio_solicita_empleo=municipio,
                                                               edad__in=edades_jovenes).count() + \
                                        egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                             edad__in=edades_jovenes).count() + \
                                        egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                           edad__in=edades_jovenes).count() + \
                                        egresados_efi.filter(municipio_solicita_empleo=municipio,
                                                             edad__in=edades_jovenes).count() + \
                                        menores_incapacitados.filter(municipio_solicita_empleo=municipio,
                                                                     edad__in=edades_jovenes).count() + \
                                        menores_desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                     edad__in=edades_jovenes).count() + \
                                        menores_dictamen.filter(municipio_solicita_empleo=municipio,
                                                                edad__in=edades_jovenes).count() + \
                                        discapacitados.filter(municipio_solicita_empleo=municipio,
                                                              edad__in=edades_jovenes).count() + \
                                        mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio,
                                                                  edad__in=edades_jovenes).count() + \
                                        hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio,
                                                                  edad__in=edades_jovenes).count() + \
                                        proxenetas.filter(municipio_solicita_empleo=municipio,
                                                          edad__in=edades_jovenes).count()

        worksheet_data.write(INDICE, 3, jovenes_controlados_provincia, formato2)

        ubicados_provincia = licenciados_sma.filter(municipio_residencia=municipio).count() + \
                             egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             sancionados.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                  ubicado=True).count() + \
                             egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                ubicado=True).count() + \
                             egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             menores_incapacitados.filter(municipio_solicita_empleo=municipio,
                                                          ubicado=True).count() + \
                             menores_desvinculados.filter(municipio_solicita_empleo=municipio,
                                                          ubicado=True).count() + \
                             menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True).count() + \
                             proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=True).count()

        worksheet_data.write(INDICE, 4, ubicados_provincia, formato2)

        mujeres_ubicadas_provincia = licenciados_sma.filter(municipio_residencia=municipio, sexo='F').count() + \
                                     egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                         sexo='F').count() + \
                                     sancionados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                        sexo='F').count() + \
                                     desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                          sexo='F').count() + \
                                     tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                           sexo='F').count() + \
                                     obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                sexo='F').count() + \
                                     escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                            sexo='F').count() + \
                                     egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                          ubicado=True, sexo='F').count() + \
                                     egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                        ubicado=True, sexo='F').count() + \
                                     egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                          sexo='F').count() + \
                                     menores_incapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                  sexo='F').count() + \
                                     menores_desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                  sexo='F').count() + \
                                     menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                             sexo='F').count() + \
                                     discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                           sexo='F').count() + \
                                     mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                               sexo='F').count() + \
                                     hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                               sexo='F').count() + \
                                     proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                       sexo='F').count()

        worksheet_data.write(INDICE, 5, mujeres_ubicadas_provincia, formato2)

        jovenes_ubicados_provincia = licenciados_sma.filter(municipio_residencia=municipio,
                                                            edad__in=edades_jovenes).count() + \
                                     egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                         edad__in=edades_jovenes).count() + \
                                     sancionados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                        edad__in=edades_jovenes).count() + \
                                     desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                          edad__in=edades_jovenes).count() + \
                                     tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                           edad__in=edades_jovenes).count() + \
                                     obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                edad__in=edades_jovenes).count() + \
                                     escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                            edad__in=edades_jovenes).count() + \
                                     egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                          ubicado=True,
                                                                          edad__in=edades_jovenes).count() + \
                                     egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                        ubicado=True,
                                                                        edad__in=edades_jovenes).count() + \
                                     egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                          edad__in=edades_jovenes).count() + \
                                     menores_incapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                  edad__in=edades_jovenes).count() + \
                                     menores_desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                                  edad__in=edades_jovenes).count() + \
                                     menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                             edad__in=edades_jovenes).count() + \
                                     discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                           edad__in=edades_jovenes).count() + \
                                     mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                               edad__in=edades_jovenes).count() + \
                                     hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                               edad__in=edades_jovenes).count() + \
                                     proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=True,
                                                       edad__in=edades_jovenes).count()

        worksheet_data.write(INDICE, 6, jovenes_ubicados_provincia, formato2)

        worksheet_data.write(INDICE, 7, licenciados_sma.filter(municipio_residencia=municipio).count(), formato2)
        worksheet_data.write(INDICE, 8,
                             egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 9,
                             sancionados.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 10,
                             desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 11,
                             tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 12,
                             obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 13,
                             escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 14, egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio,
                                                                              ubicado=True).count(), formato2)
        worksheet_data.write(INDICE, 15, egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio,
                                                                            ubicado=True).count(), formato2)
        worksheet_data.write(INDICE, 16,
                             egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 17, menores_incapacitados.filter(municipio_solicita_empleo=municipio,
                                                                      ubicado=True).count(), formato2)
        worksheet_data.write(INDICE, 18, menores_desvinculados.filter(municipio_solicita_empleo=municipio,
                                                                      ubicado=True).count(), formato2)
        worksheet_data.write(INDICE, 19,
                             menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 20,
                             discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 21,
                             mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 22,
                             hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=True).count(),
                             formato2)
        worksheet_data.write(INDICE, 23,
                             proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=True).count(), formato2)

        INDICE += 1

    book.close()
    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    return response
