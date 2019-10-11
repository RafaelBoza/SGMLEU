# -*- coding: utf-8 -*-
import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xlsxwriter import Workbook
from xlsxwriter.utility import xl_range

from SGMGU.models import *
from SGMGU.views.utiles import permission_required


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def no_ubicados_por_no_existir_oferta_cierre_mes(request):
    start_time = time.time()

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    anno = datetime.today().year
    mes = datetime.today().month

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    if categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Total_de_personas_no_ubicadas_por_no_existir_oferta_de_empleo._(%s).xlsx" % (anno)

    elif categoria_usuario == 'dmt':
        response['Content-Disposition'] = "attachment; filename=Total_de_personas_no_ubicadas_por_no_existir_oferta_de_empleo._(%s).xlsx" % (anno)

    else:
        response['Content-Disposition'] = "attachment; filename=Total_de_personas_no_ubicadas_por_no_existir_oferta_de_empleo._(%s).xlsx" % (anno)

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte 1")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    if categoria_usuario == 'dpt_ee':
        worksheet_data.write("A1", "Provincia", formato)

        provincias = Provincia.objects.filter(id=provincia_usuario.id)

    elif categoria_usuario == 'dmt':
        worksheet_data.write("A1", "Municipio", formato)

        municipio = Municipio.objects.get(id=municipio_usuario.id)

    else:
        worksheet_data.write("A1", "Provincias", formato)

        provincias = Provincia.objects.all()

    worksheet_data.write("B1", "No ubicados", formato)
    worksheet_data.write("C1", "Mujeres no ubicadas", formato)
    worksheet_data.write("D1", "Jovenes no ubicados", formato)

    fuentes_procedencia = FuenteProcedencia.objects.filter(activo=True).order_by('id')
    indice = 4

    for fuente in fuentes_procedencia:
        worksheet_data.write(0, indice, fuente.nombre, formato)
        indice = indice + 1

    worksheet_data.set_column("A:A", 17)
    worksheet_data.set_column("B:B", 10)
    worksheet_data.set_column("C:C", 10)
    worksheet_data.set_column("D:D", 10)

    if categoria_usuario == 'administrador' or categoria_usuario == 'dpt_ee':
        arr_provincias = []
        for p in provincias:
            arr_provincias.append(p.nombre)

        worksheet_data.write_column(1, 0, arr_provincias, formato2)

        cantidad_provincias = arr_provincias.__len__()

    egresados_ep = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=2,
                                                                           causa_no_ubicado_id=1,
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
                                                                           causa_no_ubicado_id=1,
                                                                           activo=True)

    query = """SELECT id
                    FROM public."SGMGU_egresadosestablecimientospenitenciarios" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 3;"""

    resultado_query = EgresadosEstablecimientosPenitenciarios.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    sancionados = sancionados.exclude(id__in=ids_listado)

    desvinculados = Desvinculado.objects.filter(activo=True, causa_no_ubicado_id=1)

    query = """SELECT id
                    FROM public."SGMGU_desvinculado" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Desvinculado.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    desvinculados = desvinculados.exclude(id__in=ids_listado)

    tecnicos_medio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6,
                                                                causa_no_ubicado_id=1,
                                                                activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 6;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    tecnicos_medio = tecnicos_medio.exclude(id__in=ids_listado)

    obreros_calificados = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=7, causa_no_ubicado_id=1,
                                                                    activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 7;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    obreros_calificados = obreros_calificados.exclude(id__in=ids_listado)

    escuelas_oficio = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=8, causa_no_ubicado_id=1,
                                                                activo=True)

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 8;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    escuelas_oficio = escuelas_oficio.exclude(id__in=ids_listado)

    egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(activo=True, causa_no_ubicado_id=1)

    query = """SELECT id
                    FROM public."SGMGU_egresadosescuelasespeciales" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEscuelasEspeciales.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_escuelas_especiales = egresados_escuelas_especiales.exclude(id__in=ids_listado)

    egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(activo=True,  causa_no_ubicado_id=1)

    query = """SELECT id
                    FROM public."SGMGU_egresadosescuelasconducta" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEscuelasConducta.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_escuelas_conducta = egresados_escuelas_conducta.exclude(id__in=ids_listado)

    egresados_efi = EgresadosEFI.objects.filter(activo=True,  causa_no_ubicado_id=1)

    query = """SELECT id
                    FROM public."SGMGU_egresadosefi" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEFI.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_efi = egresados_efi.exclude(id__in=ids_listado)

    menores_incapacitados = Menores.objects.filter(fuente_procedencia_id=12, causa_no_ubicado_id=1,
                                                   activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 12;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_incapacitados = menores_incapacitados.exclude(id__in=ids_listado)

    menores_desvinculados = Menores.objects.filter(fuente_procedencia_id=13, causa_no_ubicado_id=1, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 13;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_desvinculados = menores_desvinculados.exclude(id__in=ids_listado)

    menores_dictamen = Menores.objects.filter(fuente_procedencia_id=14, causa_no_ubicado_id=1, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 14;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores_dictamen = menores_dictamen.exclude(id__in=ids_listado)

    discapacitados = Discapacitados.objects.filter(activo=True, causa_no_ubicado_id=1)

    query = """SELECT id
                    FROM public."SGMGU_discapacitados" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Discapacitados.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    discapacitados = discapacitados.exclude(id__in=ids_listado)

    mujeres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=17, causa_no_ubicado_id=1, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 17;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    mujeres_riesgo_pnr = mujeres_riesgo_pnr.exclude(id__in=ids_listado)

    hombres_riesgo_pnr = PersonasRiesgo.objects.filter(fuente_procedencia_id=18, causa_no_ubicado_id=1, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 18;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    hombres_riesgo_pnr = hombres_riesgo_pnr.exclude(id__in=ids_listado)

    proxenetas = PersonasRiesgo.objects.filter(fuente_procedencia_id=19, causa_no_ubicado_id=1, activo=True)

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """ AND
                        t.fuente_procedencia_id = 19;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    proxenetas = proxenetas.exclude(id__in=ids_listado)

    total_no_ubicados_provincia = []
    total_mujeres_ubicadas_provincia = []
    total_jovenes_ubicados_provincia = []
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

    if categoria_usuario == 'dpt_ee' or categoria_usuario == 'administrador':

        for provincia in provincias:

            cero.append(0)

            # NO UBICADOS
            egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=False).count()
            sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=False).count()
            desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=False).count()
            tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=False).count()
            obreros_calificados_controlados = obreros_calificados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False).count()
            escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 ubicado=False).count()
            egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False).count()
            egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False).count()
            egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=False).count()
            menores_incapacitados_controlados = menores_incapacitados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False).count()
            menores_desvinculados_controlados = menores_desvinculados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False).count()
            menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   ubicado=False).count()
            discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=False).count()
            mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False).count()
            hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False).count()
            proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia,
                                                       ubicado=False).count()

            total = (egresados_ep_controlados + sancionados_controlados + desvinculados_controlados +
                     tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
                     egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
                     menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
                     proxenetas_controlados)
            total_no_ubicados_provincia.append(total)

            # MUJERES NO UBICADAS
            egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=False, sexo='F').count()
            sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=False, sexo='F').count()
            desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=False, sexo='F').count()
            tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=False, sexo='F').count()
            obreros_calificados_controlados = obreros_calificados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, sexo='F').count()
            escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 ubicado=False, sexo='F').count()
            egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, sexo='F').count()
            egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, sexo='F').count()
            egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=False, sexo='F').count()
            menores_incapacitados_controlados = menores_incapacitados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, sexo='F').count()
            menores_desvinculados_controlados = menores_desvinculados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, sexo='F').count()
            menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   ubicado=False, sexo='F').count()
            discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=False, sexo='F').count()
            mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, sexo='F').count()
            hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, sexo='F').count()
            proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False,
                                                       sexo='F').count()

            total = (
                egresados_ep_controlados + sancionados_controlados + desvinculados_controlados +
                tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
                egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
                menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
                proxenetas_controlados)
            total_mujeres_ubicadas_provincia.append(total)

            # JOVENES NO UBICADOS
            egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo__provincia=provincia,
                                                           ubicado=False, edad__lte=35).count()
            sancionados_controlados = sancionados.filter(municipio_solicita_empleo__provincia=provincia,
                                                         ubicado=False, edad__lte=35).count()
            desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=False, edad__lte=35).count()
            tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=False, edad__lte=35).count()
            obreros_calificados_controlados = obreros_calificados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, edad__lte=35).count()
            escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia,
                                                                 ubicado=False, edad__lte=35).count()
            egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, edad__lte=35).count()
            egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, edad__lte=35).count()
            egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo__provincia=provincia,
                                                             ubicado=False, edad__lte=35).count()
            menores_incapacitados_controlados = menores_incapacitados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, edad__lte=35).count()
            menores_desvinculados_controlados = menores_desvinculados.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, edad__lte=35).count()
            menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia,
                                                                   ubicado=False, edad__lte=35).count()
            discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo__provincia=provincia,
                                                               ubicado=False, edad__lte=35).count()
            mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, edad__lte=35).count()
            hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
                municipio_solicita_empleo__provincia=provincia, ubicado=False, edad__lte=35).count()
            proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False,
                                                       edad__lte=35).count()

            total = (
                egresados_ep_controlados + sancionados_controlados + desvinculados_controlados +
                tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados +
                egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados +
                menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados +
                proxenetas_controlados)
            total_jovenes_ubicados_provincia.append(total)

            # NO UBICADOS: Egresados de establecimientos penitenciarios
            total_egresados_ep_provincias.append(
                egresados_ep.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: SANCIONADOS
            total_sancionados_provincias.append(
                sancionados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: DESVINCULADOS
            total_desvinculados_provincias.append(desvinculados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Tecnicos medios
            total_tecnicos_medio_provincias.append(tecnicos_medio.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Egresados obreros calificados
            total_obreros_calificados_provincias.append(obreros_calificados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Egresados escuelas de oficio
            total_escuela_oficio_provincias.append(escuelas_oficio.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Egresados de escuelas especiales
            total_egresados_esc_especiales_provincias.append(egresados_escuelas_especiales.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Egresados de escuelas de conducta
            total_egresados_esc_conducta_provincias.append(egresados_escuelas_conducta.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Egresados de la EFI
            total_egresados_efi_provincias.append(egresados_efi.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Menores incapacitados para el estudio por dictamen médico
            total_menores_incapacitados_provincias.append(menores_incapacitados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Menores desvinculados del SNE por bajo rendimiento
            total_menores_desvinculados_provincias.append(menores_desvinculados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Menores con dictamen del CDO-MININT
            total_menores_dictamen_provincias.append(menores_dictamen.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # NO UBICADOS: Personas con discapacidad
            total_discapacitados_provincias.append(discapacitados.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # UBICADOS: Mujeres de riesgo controladas por al PNR
            total_mueres_riesgo_pnr_provincias.append(mujeres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # UBICADOS: Hombres de riesgo controlados por al PNR
            total_hombres_riesgo_pnr_provincias.append(hombres_riesgo_pnr.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

            # UBICADOS: Proxenetas de riesgo controlados por la PNR
            total_proxenetas_riesgo_pnr_provincias.append(proxenetas.filter(municipio_solicita_empleo__provincia=provincia, ubicado=False).count())

        worksheet_data.write_column(1, 1, total_no_ubicados_provincia, formato2)
        worksheet_data.write_column(1, 2, total_mujeres_ubicadas_provincia, formato2)
        worksheet_data.write_column(1, 3, total_jovenes_ubicados_provincia, formato2)
        worksheet_data.write_column(1, 4, cero, formato2)  # NO UBICADOS: LICENCIADOS DEL SMA
        worksheet_data.write_column(1, 5, total_egresados_ep_provincias, formato2)
        worksheet_data.write_column(1, 6, total_sancionados_provincias, formato2)
        worksheet_data.write_column(1, 7, total_desvinculados_provincias, formato2)
        worksheet_data.write_column(1, 8, cero, formato2)  # UBICADOS: Egresados Universitarios
        worksheet_data.write_column(1, 9, total_tecnicos_medio_provincias, formato2)
        worksheet_data.write_column(1, 10, total_obreros_calificados_provincias, formato2)
        worksheet_data.write_column(1, 11, total_escuela_oficio_provincias, formato2)
        worksheet_data.write_column(1, 12, total_egresados_esc_especiales_provincias, formato2)
        worksheet_data.write_column(1, 13, total_egresados_esc_conducta_provincias, formato2)
        worksheet_data.write_column(1, 14, total_egresados_efi_provincias, formato2)
        worksheet_data.write_column(1, 15, total_menores_incapacitados_provincias, formato2)
        worksheet_data.write_column(1, 16, total_menores_desvinculados_provincias, formato2)
        worksheet_data.write_column(1, 17, total_menores_dictamen_provincias, formato2)
        worksheet_data.write_column(1, 18, total_discapacitados_provincias, formato2)
        worksheet_data.write_column(1, 19, total_mueres_riesgo_pnr_provincias, formato2)
        worksheet_data.write_column(1, 20, total_hombres_riesgo_pnr_provincias, formato2)
        worksheet_data.write_column(1, 21, total_proxenetas_riesgo_pnr_provincias, formato2)

        if categoria_usuario == 'administrador':
            # ------------ SUMAS ABAJO-------------------
            worksheet_data.write(cantidad_provincias + 1, 0, "Total", formato)

            sumas = []
            for a in range(1, 22):
                total = '=SUM(%s)' % xl_range(1, a, cantidad_provincias, a)
                sumas.append(total)

            indice_sumas = 1
            for suma in sumas:
                worksheet_data.write(17, indice_sumas, suma, formato2)
                indice_sumas = indice_sumas + 1

    if categoria_usuario == 'dmt':

        worksheet_data.write(1, 0, municipio.nombre, formato2)

        # NO UBICADOS
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo=municipio,
                                                       ubicado=False).count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo=municipio,
                                                     ubicado=False).count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo=municipio,
                                                         ubicado=False).count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo=municipio,
                                                           ubicado=False).count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo=municipio, ubicado=False).count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo=municipio,
                                                             ubicado=False).count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo=municipio, ubicado=False).count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo=municipio, ubicado=False).count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo=municipio,
                                                         ubicado=False).count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo=municipio, ubicado=False).count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo=municipio, ubicado=False).count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo=municipio,
                                                               ubicado=False).count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo=municipio,
                                                           ubicado=False).count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo=municipio, ubicado=False).count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo=municipio, ubicado=False).count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo=municipio,
                                                   ubicado=False).count()

        no_ubicados_municipio = egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + \
                 tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados + \
                 egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados + \
                 menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados + \
                 proxenetas_controlados

        # MUJERES NO UBICADAS
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo=municipio,
                                                       ubicado=False, sexo='F').count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo=municipio,
                                                     ubicado=False, sexo='F').count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo=municipio,
                                                         ubicado=False, sexo='F').count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo=municipio,
                                                           ubicado=False, sexo='F').count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo=municipio, ubicado=False, sexo='F').count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo=municipio,
                                                             ubicado=False, sexo='F').count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo=municipio, ubicado=False, sexo='F').count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo=municipio, ubicado=False, sexo='F').count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo=municipio,
                                                         ubicado=False, sexo='F').count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo=municipio, ubicado=False, sexo='F').count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo=municipio, ubicado=False, sexo='F').count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo=municipio,
                                                               ubicado=False, sexo='F').count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo=municipio,
                                                           ubicado=False, sexo='F').count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo=municipio, ubicado=False, sexo='F').count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo=municipio, ubicado=False, sexo='F').count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=False,
                                                   sexo='F').count()

        mujeres_no_ubicadas_municipio =egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + \
            tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados + \
            egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados + \
            menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados + \
            proxenetas_controlados

        # JOVENES NO UBICADOS
        egresados_ep_controlados = egresados_ep.filter(municipio_solicita_empleo=municipio,
                                                       ubicado=False, edad__lte=35).count()
        sancionados_controlados = sancionados.filter(municipio_solicita_empleo=municipio,
                                                     ubicado=False, edad__lte=35).count()
        desvinculados_controlados = desvinculados.filter(municipio_solicita_empleo=municipio,
                                                         ubicado=False, edad__lte=35).count()
        tecnicos_medio_controlados = tecnicos_medio.filter(municipio_solicita_empleo=municipio,
                                                           ubicado=False, edad__lte=35).count()
        obreros_calificados_controlados = obreros_calificados.filter(
            municipio_solicita_empleo=municipio, ubicado=False, edad__lte=35).count()
        escuelas_oficio_controlados = escuelas_oficio.filter(municipio_solicita_empleo=municipio,
                                                             ubicado=False, edad__lte=35).count()
        egresados_escuelas_especiales_controlados = egresados_escuelas_especiales.filter(
            municipio_solicita_empleo=municipio, ubicado=False, edad__lte=35).count()
        egresados_escuelas_conducta_controlados = egresados_escuelas_conducta.filter(
            municipio_solicita_empleo=municipio, ubicado=False, edad__lte=35).count()
        egresados_efi_controlados = egresados_efi.filter(municipio_solicita_empleo=municipio,
                                                         ubicado=False, edad__lte=35).count()
        menores_incapacitados_controlados = menores_incapacitados.filter(
            municipio_solicita_empleo=municipio, ubicado=False, edad__lte=35).count()
        menores_desvinculados_controlados = menores_desvinculados.filter(
            municipio_solicita_empleo=municipio, ubicado=False, edad__lte=35).count()
        menores_dictamen_controlados = menores_dictamen.filter(municipio_solicita_empleo=municipio,
                                                               ubicado=False, edad__lte=35).count()
        discapacitados_controlados = discapacitados.filter(municipio_solicita_empleo=municipio,
                                                           ubicado=False, edad__lte=35).count()
        mujeres_riesgo_pnr_controlados = mujeres_riesgo_pnr.filter(
            municipio_solicita_empleo=municipio, ubicado=False, edad__lte=35).count()
        hombres_riesgo_pnr_controlados = hombres_riesgo_pnr.filter(
            municipio_solicita_empleo=municipio, ubicado=False, edad__lte=35).count()
        proxenetas_controlados = proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=False,
                                                   edad__lte=35).count()

        jovenes_no_ubicados = egresados_ep_controlados + sancionados_controlados + desvinculados_controlados + \
            tecnicos_medio_controlados + obreros_calificados_controlados + escuelas_oficio_controlados + egresados_escuelas_especiales_controlados + \
            egresados_escuelas_conducta_controlados + egresados_efi_controlados + menores_incapacitados_controlados + menores_desvinculados_controlados + \
            menores_dictamen_controlados + discapacitados_controlados + mujeres_riesgo_pnr_controlados + hombres_riesgo_pnr_controlados + \
            proxenetas_controlados

        worksheet_data.write(1, 1, no_ubicados_municipio, formato2)
        worksheet_data.write(1, 2, mujeres_no_ubicadas_municipio, formato2)
        worksheet_data.write(1, 3, jovenes_no_ubicados, formato2)
        worksheet_data.write(1, 4, 0, formato2)  # LICENCIADOS DEL SMA
        worksheet_data.write(1, 5, egresados_ep.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 6, sancionados.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 7, desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 8, 0, formato2)  # Egresados Universitarios
        worksheet_data.write(1, 9, tecnicos_medio.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 10, obreros_calificados.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 11, escuelas_oficio.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 12, egresados_escuelas_especiales.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 13, egresados_escuelas_conducta.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 14, egresados_efi.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 15, menores_incapacitados.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 16, menores_desvinculados.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 17, menores_dictamen.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 18, discapacitados.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 19, mujeres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 20, hombres_riesgo_pnr.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)
        worksheet_data.write(1, 21, proxenetas.filter(municipio_solicita_empleo=municipio, ubicado=False).count(), formato2)

    book.close()
    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)
    # print("Tiempo transcurrido: % segundos." % elapsed_time)
    return response
