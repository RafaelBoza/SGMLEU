# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from xlsxwriter import Workbook
from SGMGU.models import *
from SGMGU.views.utiles import permission_required
import time


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt', 'organismo'])
def reporte_nominal_cierre_mes(request):
    start_time = time.time()

    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    organismo_usuario = request.user.perfil_usuario.organismo.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    anno = datetime.today().year
    mes = datetime.today().month

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    if categoria_usuario == 'dmt':
        response['Content-Disposition'] = "attachment; filename=Reporte_nominal_(%s_%s)_(%s).xlsx" % (
            municipio_usuario, str(provincia_usuario).replace(" ", "_"), anno)
    elif categoria_usuario == 'dpt_ee':
        response['Content-Disposition'] = "attachment; filename=Reporte_nominal_(%s)_(%s).xlsx" % (
            str(provincia_usuario).replace(" ", "_"), anno)
    elif categoria_usuario == 'organismo':
        response['Content-Disposition'] = "attachment; filename=Reporte_nominal_(%s)_(%s).xlsx" % (
            str(organismo_usuario).replace(" ", "_"), anno)
    else:
        response['Content-Disposition'] = "attachment; filename=Reporte_nominal_(%s).xlsx" % anno

    book = Workbook(response, {'in_memory': True})
    worksheet_data = book.add_worksheet("Reporte nominal")
    formato = book.add_format({'bold': True, 'border': 1})
    formato2 = book.add_format({'border': 1})

    worksheet_data.write("A1", "Nombre y Apellidos", formato)
    worksheet_data.write("B1", "Sexo", formato)
    worksheet_data.write("C1", "CI", formato)
    worksheet_data.write("D1", "Direccion Particular", formato)
    worksheet_data.write("E1", "Nivel Escolar", formato)
    worksheet_data.write("F1", "Carrera / Especialidad", formato)
    worksheet_data.write("G1", "Fuente", formato)
    worksheet_data.write("H1", "Ubicado", formato)
    worksheet_data.write("I1", "Organismo", formato)
    worksheet_data.write("J1", "Entidad", formato)
    worksheet_data.write("K1", "Ubicacion", formato)

    if categoria_usuario == 'dpt_ee':
        worksheet_data.write("L1", "Municipios", formato)
        worksheet_data.set_column("L:L", 20)
    elif categoria_usuario == 'organismo':
        worksheet_data.write("L1", "Municipios", formato)
        worksheet_data.write("M1", "Provincias", formato)
        worksheet_data.write("N1", "Edad", formato)
        worksheet_data.set_column("L:L", 10.29)
        worksheet_data.set_column("M:M", 10.29)
        worksheet_data.set_column("N:N", 5.00)
    elif categoria_usuario == 'administrador':
        worksheet_data.write("L1", "Municipios", formato)
        worksheet_data.write("M1", "Provincias", formato)
        worksheet_data.write("N1", "Edad", formato)
        worksheet_data.write("O1", "Causa no ubicado", formato)
        worksheet_data.write("P1", "Estado", formato)
        worksheet_data.set_column("L:L", 10.29)
        worksheet_data.set_column("M:M", 10.29)
        worksheet_data.set_column("N:N", 5.00)
        worksheet_data.set_column("O:O", 15.00)
        worksheet_data.set_column("P:P", 20.00)

    worksheet_data.set_column("A:A", 20)
    worksheet_data.set_column("B:B", 20)
    worksheet_data.set_column("C:C", 15)
    worksheet_data.set_column("D:D", 20)
    worksheet_data.set_column("E:E", 25)
    worksheet_data.set_column("F:F", 20)
    worksheet_data.set_column("G:G", 20)
    worksheet_data.set_column("H:H", 20)
    worksheet_data.set_column("I:I", 20)
    worksheet_data.set_column("J:J", 20)
    worksheet_data.set_column("K:K", 20)

    # INICIO -> LICENCIADOS SMA

    if categoria_usuario == 'dmt':
        licenciados_sma = LicenciadosSMA.objects.filter(municipio_residencia=municipio_usuario,
                                                        activo=True). \
                              values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                     "nivel_escolar__nombre",
                                     "carrera__nombre",
                                     "acepto_oferta", "organismo__nombre", "entidad__e_nombre",
                                     "ubicacion__ubicacion", "municipio_residencia__nombre",
                                     "municipio_residencia__provincia__nombre",
                                     "edad", "activo")
    elif categoria_usuario == 'dpt_ee':
        licenciados_sma = LicenciadosSMA.objects.filter(municipio_residencia__provincia=provincia_usuario,
                                                        activo=True). \
                              values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                     "nivel_escolar__nombre",
                                     "carrera__nombre",
                                     "acepto_oferta", "organismo__nombre", "entidad__e_nombre",
                                     "ubicacion__ubicacion", "municipio_residencia__nombre",
                                     "municipio_residencia__provincia__nombre", "edad", "activo")
    elif categoria_usuario == 'organismo':
        licenciados_sma = []
    else:
        licenciados_sma = LicenciadosSMA.objects.filter(activo=True). \
                              values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                     "nivel_escolar__nombre",
                                     "carrera__nombre",
                                     "acepto_oferta", "organismo__nombre", "entidad__e_nombre",
                                     "ubicacion__ubicacion", "municipio_residencia__nombre",
                                     "municipio_residencia__provincia__nombre",
                                     "edad", "activo")

    query = """SELECT id
                    FROM public."SGMGU_licenciadossma" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = LicenciadosSMA.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    licenciados_sma = licenciados_sma.exclude(id__in=ids_listado)

    if categoria_usuario != 'organismo':
        nombre_apellidos = []
        sexo = []
        ci = []
        direccion_particular = []
        nivel_escolar = []
        carrera = []
        fuente = []
        ubicado = []
        organismo = []
        entidad = []
        ubicacion = []
        municipios = []
        provincias = []
        edad = []
        causa_no_ubicado = []
        activo = []

        for persona in licenciados_sma:
            nombre_apellidos.append(persona['nombre_apellidos'])
            sexo.append(persona['sexo'])
            edad.append(persona['edad'])
            ci.append(persona['ci'])
            direccion_particular.append(persona['direccion_particular'])
            nivel_escolar.append(persona['nivel_escolar__nombre'])
            if not persona['carrera__nombre']:
                carrera.append("---")
            else:
                carrera.append(persona['carrera__nombre'])
            fuente.append("Licenciados SMA")
            ubicado.append("Si")
            # if persona['acepto_oferta'] == 'S':
            #     ubicado.append("Si")
            # else:
            #     ubicado.append("No")
            if not persona['organismo__nombre']:
                organismo.append("---")
            else:
                organismo.append(persona['organismo__nombre'])
            if not persona['entidad__e_nombre']:
                entidad.append("---")
            else:
                entidad.append(persona['entidad__e_nombre'])

            if not persona['ubicacion__ubicacion']:
                ubicacion.append("---")
            else:
                ubicacion.append(persona['ubicacion__ubicacion'])
            municipios.append(persona['municipio_residencia__nombre'])
            provincias.append(persona['municipio_residencia__provincia__nombre'])
            causa_no_ubicado.append("---")
            if not persona['activo']:
                activo.append("Baja")
            else:
                activo.append("Activo")

        inicio_licenciados_sma = 1
        fin_licenciados_sma = inicio_licenciados_sma + nombre_apellidos.__len__()

        for indice_columna in range(inicio_licenciados_sma, fin_licenciados_sma):
            worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_licenciados_sma],
                                 formato2)
            worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_licenciados_sma], formato2)
            worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_licenciados_sma], formato2)
            worksheet_data.write(indice_columna, 3, direccion_particular[indice_columna - inicio_licenciados_sma],
                                 formato2)
            worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_licenciados_sma],
                                 formato2)
            worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_licenciados_sma], formato2)
            worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_licenciados_sma], formato2)
            worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_licenciados_sma], formato2)
            worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_licenciados_sma], formato2)
            worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_licenciados_sma], formato2)
            worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_licenciados_sma], formato2)
            if categoria_usuario == 'dpt_ee':
                worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_licenciados_sma],
                                     formato2)
            elif categoria_usuario == 'administrador':
                worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_licenciados_sma],
                                     formato2)
                worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_licenciados_sma],
                                     formato2)
                worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_licenciados_sma], formato2)
                worksheet_data.write(indice_columna, 14,
                                     causa_no_ubicado[indice_columna - inicio_licenciados_sma], formato2)
                worksheet_data.write(indice_columna, 15,
                                     activo[indice_columna - inicio_licenciados_sma], formato2)

    # FIN -> LICENCIADOS SMA

    # INICIO -> EGRESADOS DE ESTABLECIMIENTOS PENITENCIARIO Y SANCIONADOS

    if categoria_usuario == 'dmt':
        egresados_sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                    municipio_solicita_empleo=municipio_usuario, activo=True). \
                                    values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                           "nivel_escolar__nombre",
                                           "carrera__nombre",
                                           "fuente_procedencia__nombre", "ubicado", "organismo__nombre",
                                           "entidad__e_nombre",
                                           "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                           "municipio_solicita_empleo__provincia__nombre", "edad",
                                           "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'dpt_ee':
        egresados_sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                    municipio_solicita_empleo__provincia=provincia_usuario, activo=True). \
                                    values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                           "nivel_escolar__nombre",
                                           "carrera__nombre",
                                           "fuente_procedencia__nombre", "ubicado", "organismo__nombre",
                                           "entidad__e_nombre",
                                           "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                           "municipio_solicita_empleo__provincia__nombre", "edad",
                                           "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'organismo':
        egresados_sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                    organismo__nombre=organismo_usuario, activo=True). \
                                    values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                           "nivel_escolar__nombre",
                                           "carrera__nombre",
                                           "fuente_procedencia__nombre", "ubicado", "organismo__nombre",
                                           "entidad__e_nombre",
                                           "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                           "municipio_solicita_empleo__provincia__nombre", "edad",
                                           "causa_no_ubicado__causa", "activo")
    else:
        egresados_sancionados = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                    activo=True). \
                                    values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                           "nivel_escolar__nombre",
                                           "carrera__nombre",
                                           "fuente_procedencia__nombre", "ubicado", "organismo__nombre",
                                           "entidad__e_nombre",
                                           "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                           "municipio_solicita_empleo__provincia__nombre", "edad",
                                           "causa_no_ubicado__causa", "activo")

    query = """SELECT id
                    FROM public."SGMGU_egresadosestablecimientospenitenciarios" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEstablecimientosPenitenciarios.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_sancionados = egresados_sancionados.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in egresados_sancionados:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append(persona['fuente_procedencia__nombre'])
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])

        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    if categoria_usuario == 'organismo':
        inicio_egresados_sancionados = 1
    else:
        inicio_egresados_sancionados = fin_licenciados_sma
    fin_egresados_sancionados = inicio_egresados_sancionados + nombre_apellidos.__len__()

    for indice_columna in range(inicio_egresados_sancionados, fin_egresados_sancionados):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_egresados_sancionados],
                             formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_egresados_sancionados], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_egresados_sancionados], formato2)
        worksheet_data.write(indice_columna, 3, direccion_particular[indice_columna - inicio_egresados_sancionados],
                             formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_egresados_sancionados],
                             formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_egresados_sancionados], formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_egresados_sancionados], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_egresados_sancionados], formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_egresados_sancionados], formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_egresados_sancionados], formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_egresados_sancionados], formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresados_sancionados],
                                 formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresados_sancionados],
                                 formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_egresados_sancionados],
                                 formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_egresados_sancionados], formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresados_sancionados],
                                 formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_egresados_sancionados],
                                 formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_egresados_sancionados], formato2)
            worksheet_data.write(indice_columna, 14, causa_no_ubicado[indice_columna - inicio_egresados_sancionados],
                                 formato2)
            worksheet_data.write(indice_columna, 15, activo[indice_columna - inicio_egresados_sancionados],
                                 formato2)

    # FIN -> EGRESADOS DE ESTABLECIMIENTOS PENITENCIARIO Y SANCIONADOS

    # INICIO -> DESVINCULADOS

    if categoria_usuario == 'dmt':
        desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo=municipio_usuario, activo=True). \
                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                   "nivel_escolar__nombre",
                                   "carrera__nombre",
                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                   "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'dpt_ee':
        desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario,
                                                    activo=True). \
                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                   "nivel_escolar__nombre",
                                   "carrera__nombre",
                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                   "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'organismo':
        desvinculados = Desvinculado.objects.filter(organismo__nombre=organismo_usuario, activo=True). \
                            values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                                   "carrera__nombre",
                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                   "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                                   "activo")
    else:
        desvinculados = Desvinculado.objects.filter(activo=True). \
                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                   "nivel_escolar__nombre", "carrera__nombre",
                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                   "causa_no_ubicado__causa", "activo")

    query = """SELECT id
                    FROM public."SGMGU_desvinculado" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Desvinculado.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    desvinculados = desvinculados.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in desvinculados:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append("Desvinculados")
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])
        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    inicio_desvinculados = fin_egresados_sancionados
    fin_desvinculados = inicio_desvinculados + nombre_apellidos.__len__()

    for indice_columna in range(inicio_desvinculados, fin_desvinculados):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 3, direccion_particular[indice_columna - inicio_desvinculados],
                             formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_desvinculados], formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_desvinculados], formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_desvinculados], formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_desvinculados], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_desvinculados], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_desvinculados], formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_desvinculados], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_desvinculados], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_desvinculados], formato2)
            worksheet_data.write(indice_columna, 14, causa_no_ubicado[indice_columna - inicio_desvinculados],
                                 formato2)
            worksheet_data.write(indice_columna, 15, activo[indice_columna - inicio_desvinculados],
                                 formato2)

    # FIN -> DESVINCULADOS

    # INICIO -> TECNICOS MEDIOS, OBREROS CALIFICADO, ESCUELAS DE OFICIO

    if categoria_usuario == 'dmt':
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(
                       municipio_solicita_empleo=municipio_usuario, activo=True). \
                       values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                              "carrera__nombre",
                              "fuente_procedencia__nombre", "ubicado", "organismo__nombre", "entidad__e_nombre",
                              "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                              "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                              "activo")
    elif categoria_usuario == 'dpt_ee':
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(
                       municipio_solicita_empleo__provincia=provincia_usuario, activo=True). \
                       values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                              "carrera__nombre",
                              "fuente_procedencia__nombre", "ubicado", "organismo__nombre", "entidad__e_nombre",
                              "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                              "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                              "activo")
    elif categoria_usuario == 'organismo':
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(organismo__nombre=organismo_usuario, activo=True). \
                       values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                              "carrera__nombre",
                              "fuente_procedencia__nombre", "ubicado", "organismo__nombre", "entidad__e_nombre",
                              "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                              "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                              "activo")
    else:
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(activo=True). \
                       values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                              "carrera__nombre", "fuente_procedencia__nombre", "ubicado", "organismo__nombre",
                              "entidad__e_nombre", "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                              "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                              "activo")

    query = """SELECT id
                    FROM public."SGMGU_tmedioocalificadoeoficio" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = TMedioOCalificadoEOficio.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    tm_oc_eo = tm_oc_eo.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in tm_oc_eo:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append(persona['fuente_procedencia__nombre'])
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])
        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    inicio_tm_oc_eo = fin_desvinculados
    fin_tm_oc_eo = inicio_tm_oc_eo + nombre_apellidos.__len__()

    for indice_columna in range(inicio_tm_oc_eo, fin_tm_oc_eo):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 3, direccion_particular[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_tm_oc_eo], formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_tm_oc_eo], formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_tm_oc_eo], formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_tm_oc_eo], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_tm_oc_eo], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_tm_oc_eo], formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_tm_oc_eo], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_tm_oc_eo], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_tm_oc_eo], formato2)
            worksheet_data.write(indice_columna, 14, causa_no_ubicado[indice_columna - inicio_tm_oc_eo], formato2)
            worksheet_data.write(indice_columna, 15, activo[indice_columna - inicio_tm_oc_eo], formato2)

    # FIN -> TECNICOS MEDIOS, OBREROS CALIFICADO, ESCUELAS DE OFICIO

    # INICIO -> EGRESADOS ESCUELAS ESPECIALES

    if categoria_usuario == 'dmt':
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                            municipio_solicita_empleo=municipio_usuario, activo=True). \
                                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                                   "nivel_escolar__nombre",
                                                   "carrera__nombre",
                                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                                   "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'dpt_ee':
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                            municipio_solicita_empleo__provincia=municipio_usuario, activo=True). \
                                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                                   "nivel_escolar__nombre",
                                                   "carrera__nombre",
                                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                                   "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'organismo':
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                            organismo__nombre=organismo_usuario, activo=True). \
                                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                                   "nivel_escolar__nombre", "carrera__nombre",
                                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                                   "causa_no_ubicado__causa", "activo")
    else:
        egresados_escuelas_especiales = EgresadosEscuelasEspeciales.objects.filter(
                                            activo=True). \
                                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                                   "nivel_escolar__nombre",
                                                   "carrera__nombre",
                                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                                   "causa_no_ubicado__causa", "activo")

    query = """SELECT id
                    FROM public."SGMGU_egresadosescuelasespeciales" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEscuelasEspeciales.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_escuelas_especiales = egresados_escuelas_especiales.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in egresados_escuelas_especiales:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append("Egresados de escuelas especiales")
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])
        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    inicio_egresado_escuela_especial = fin_tm_oc_eo
    fin_egresado_escuela_especial = inicio_egresado_escuela_especial + nombre_apellidos.__len__()

    for indice_columna in range(inicio_egresado_escuela_especial, fin_egresado_escuela_especial):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_egresado_escuela_especial],
                             formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_egresado_escuela_especial], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_egresado_escuela_especial], formato2)
        worksheet_data.write(indice_columna, 3,
                             direccion_particular[indice_columna - inicio_egresado_escuela_especial], formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_egresado_escuela_especial],
                             formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_egresado_escuela_especial],
                             formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_egresado_escuela_especial], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_egresado_escuela_especial],
                             formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_egresado_escuela_especial],
                             formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_egresado_escuela_especial],
                             formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_egresado_escuela_especial],
                             formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_escuela_especial],
                                 formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_escuela_especial],
                                 formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_egresado_escuela_especial],
                                 formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_egresado_escuela_especial],
                                 formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_escuela_especial],
                                 formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_egresado_escuela_especial],
                                 formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_egresado_escuela_especial],
                                 formato2)
            worksheet_data.write(indice_columna, 14,
                                 causa_no_ubicado[indice_columna - inicio_egresado_escuela_especial], formato2)
            worksheet_data.write(indice_columna, 15,
                                 activo[indice_columna - inicio_egresado_escuela_especial], formato2)

    # FIN -> EGRESADOS ESCUELAS ESPECIALES

    # INICIO -> EGRESADOS ESCUELAS CONDUCTA

    if categoria_usuario == 'dmt':
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
                                          municipio_solicita_empleo=municipio_usuario, activo=True). \
                                          values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                                 "nivel_escolar__nombre", "carrera__nombre", "ubicado",
                                                 "organismo__nombre", "entidad__e_nombre",
                                                 "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                                 "municipio_solicita_empleo__provincia__nombre", "edad",
                                                 "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'dpt_ee':
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(
                                          municipio_solicita_empleo__provincia=provincia_usuario, activo=True). \
                                          values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                                 "nivel_escolar__nombre", "carrera__nombre", "ubicado",
                                                 "organismo__nombre", "entidad__e_nombre",
                                                 "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                                 "municipio_solicita_empleo__provincia__nombre", "edad",
                                                 "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'organismo':
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(organismo__nombre=organismo_usuario,
                                                                               activo=True). \
                                          values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                                 "nivel_escolar__nombre", "carrera__nombre", "ubicado",
                                                 "organismo__nombre", "entidad__e_nombre",
                                                 "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                                 "municipio_solicita_empleo__provincia__nombre", "edad",
                                                 "causa_no_ubicado__causa", "activo")
    else:
        egresados_escuelas_conducta = EgresadosEscuelasConducta.objects.filter(activo=True). \
                                          values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                                 "nivel_escolar__nombre", "carrera__nombre", "ubicado",
                                                 "organismo__nombre", "entidad__e_nombre",
                                                 "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                                 "municipio_solicita_empleo__provincia__nombre", "edad",
                                                 "causa_no_ubicado__causa", "activo")

    query = """SELECT id
                    FROM public."SGMGU_egresadosescuelasconducta" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEscuelasConducta.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_escuelas_conducta = egresados_escuelas_conducta.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in egresados_escuelas_conducta:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append("Egresados de escuelas conducta")
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])

        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    inicio_egresado_escuela_conducta = fin_egresado_escuela_especial
    fin_egresado_escuela_conducta = inicio_egresado_escuela_conducta + nombre_apellidos.__len__()

    for indice_columna in range(inicio_egresado_escuela_conducta, fin_egresado_escuela_conducta):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_egresado_escuela_conducta],
                             formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_egresado_escuela_conducta], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_egresado_escuela_conducta], formato2)
        worksheet_data.write(indice_columna, 3,
                             direccion_particular[indice_columna - inicio_egresado_escuela_conducta], formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_egresado_escuela_conducta],
                             formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_egresado_escuela_conducta],
                             formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_egresado_escuela_conducta], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_egresado_escuela_conducta],
                             formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_egresado_escuela_conducta],
                             formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_egresado_escuela_conducta],
                             formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_egresado_escuela_conducta],
                             formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_escuela_conducta],
                                 formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_escuela_conducta],
                                 formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_egresado_escuela_conducta],
                                 formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_egresado_escuela_conducta],
                                 formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_escuela_conducta],
                                 formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_egresado_escuela_conducta],
                                 formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_egresado_escuela_conducta],
                                 formato2)
            worksheet_data.write(indice_columna, 14,
                                 causa_no_ubicado[indice_columna - inicio_egresado_escuela_conducta], formato2)
            worksheet_data.write(indice_columna, 15,
                                 activo[indice_columna - inicio_egresado_escuela_conducta], formato2)

    # FIN -> EGRESADOS ESCUELAS CONDUCTA

    # INICIO -> EGRESADOS DE LA EFI

    if categoria_usuario == 'dmt':
        egresados_efi = EgresadosEFI.objects.filter(
                            municipio_solicita_empleo=municipio_usuario, activo=True). \
                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                   "nivel_escolar__nombre", "carrera__nombre", "ubicado", "organismo__nombre",
                                   "entidad__e_nombre",
                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                   "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'dpt_ee':
        egresados_efi = EgresadosEFI.objects.filter(
                            municipio_solicita_empleo__provincia=provincia_usuario, activo=True). \
                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                   "nivel_escolar__nombre", "carrera__nombre", "ubicado", "organismo__nombre",
                                   "entidad__e_nombre",
                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                   "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                                   "activo")
    elif categoria_usuario == 'organismo':
        egresados_efi = EgresadosEFI.objects.filter(organismo__nombre=organismo_usuario, activo=True). \
                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                   "nivel_escolar__nombre", "carrera__nombre", "ubicado", "organismo__nombre",
                                   "entidad__e_nombre",
                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                   "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                                   "activo")
    else:
        egresados_efi = EgresadosEFI.objects.filter(activo=True). \
                            values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                   "nivel_escolar__nombre",
                                   "carrera__nombre",
                                   "ubicado", "organismo__nombre", "entidad__e_nombre",
                                   "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                   "municipio_solicita_empleo__provincia__nombre", "edad",
                                   "causa_no_ubicado__causa", "activo")

    query = """SELECT id
                    FROM public."SGMGU_egresadosefi" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = EgresadosEFI.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    egresados_efi = egresados_efi.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in egresados_efi:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append("Egresados de la EFI")
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])
        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    inicio_egresado_efi = fin_egresado_escuela_conducta
    fin_egresado_efi = inicio_egresado_efi + nombre_apellidos.__len__()

    for indice_columna in range(inicio_egresado_efi, fin_egresado_efi):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 3, direccion_particular[indice_columna - inicio_egresado_efi],
                             formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_egresado_efi], formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_egresado_efi], formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_efi], formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_efi], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_egresado_efi], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_egresado_efi], formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_egresado_efi], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_egresado_efi], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_egresado_efi], formato2)
            worksheet_data.write(indice_columna, 14, causa_no_ubicado[indice_columna - inicio_egresado_efi],
                                 formato2)
            worksheet_data.write(indice_columna, 15, activo[indice_columna - inicio_egresado_efi],
                                 formato2)

    # FIN -> EGRESADOS DE LA EFI

    # INICIO -> MENORES

    if categoria_usuario == 'dmt':
        menores = Menores.objects.filter(municipio_solicita_empleo=municipio_usuario, activo=True). \
                      values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                             "carrera__nombre",
                             "fuente_procedencia__nombre", "ubicado", "organismo__nombre", "entidad__e_nombre",
                             "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                             "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                             "activo")
    elif categoria_usuario == 'dpt_ee':
        menores = Menores.objects.filter(municipio_solicita_empleo__provincia=provincia_usuario, activo=True). \
                      values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                             "carrera__nombre",
                             "fuente_procedencia__nombre", "ubicado", "organismo__nombre", "entidad__e_nombre",
                             "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                             "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                             "activo")
    elif categoria_usuario == 'organismo':
        menores = Menores.objects.filter(organismo__nombre=organismo_usuario, activo=True). \
                      values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                             "carrera__nombre",
                             "fuente_procedencia__nombre", "ubicado", "organismo__nombre", "entidad__e_nombre",
                             "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                             "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                             "activo")
    else:
        menores = Menores.objects.filter(activo=True). \
                      values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                             "carrera__nombre",
                             "fuente_procedencia__nombre", "ubicado", "organismo__nombre", "entidad__e_nombre",
                             "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                             "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                             "activo")

    query = """SELECT id
                    FROM public."SGMGU_menores" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Menores.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    menores = menores.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in menores:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append(persona['fuente_procedencia__nombre'])
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])

        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    inicio_menor = fin_egresado_efi
    fin_menor = inicio_menor + nombre_apellidos.__len__()

    for indice_columna in range(inicio_menor, fin_menor):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 3, direccion_particular[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_menor], formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_menor], formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_menor], formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_menor], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_menor], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_menor], formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_menor], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_menor], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_menor], formato2)
            worksheet_data.write(indice_columna, 14, causa_no_ubicado[indice_columna - inicio_menor], formato2)
            worksheet_data.write(indice_columna, 15, activo[indice_columna - inicio_menor], formato2)

    # FIN -> MENORES

    # INICIO -> DISCAPACITADOS

    if categoria_usuario == 'dmt':
        discapacitados = Discapacitados.objects.filter(
                             municipio_solicita_empleo=municipio_usuario, activo=True). \
                             values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                    "nivel_escolar__nombre",
                                    "carrera__nombre",
                                    "ubicado", "organismo__nombre", "entidad__e_nombre",
                                    "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                    "municipio_solicita_empleo__provincia__nombre", "edad",
                                    "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'dpt_ee':
        discapacitados = Discapacitados.objects.filter(
                             municipio_solicita_empleo__provincia=provincia_usuario, activo=True). \
                             values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                    "nivel_escolar__nombre", "carrera__nombre", "ubicado", "organismo__nombre",
                                    "entidad__e_nombre",
                                    "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                    "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                                    "activo")
    elif categoria_usuario == 'organismo':
        discapacitados = Discapacitados.objects.filter(organismo__nombre=organismo_usuario, activo=True). \
                             values("nombre_apellidos", "sexo", "ci", "direccion_particular", "nivel_escolar__nombre",
                                    "carrera__nombre", "ubicado", "organismo__nombre", "entidad__e_nombre",
                                    "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                    "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                                    "activo")
    else:
        discapacitados = Discapacitados.objects.filter(activo=True). \
                             values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                    "nivel_escolar__nombre", "carrera__nombre", "ubicado", "organismo__nombre",
                                    "entidad__e_nombre",
                                    "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                    "municipio_solicita_empleo__provincia__nombre", "edad", "causa_no_ubicado__causa",
                                    "activo")

    query = """SELECT id
                    FROM public."SGMGU_discapacitados" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = Discapacitados.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    discapacitados = discapacitados.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in discapacitados:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append("Discapacitados")
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])
        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    inicio_discapacitado = fin_menor
    fin_discapacitado = inicio_discapacitado + nombre_apellidos.__len__()

    for indice_columna in range(inicio_discapacitado, fin_discapacitado):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 3, direccion_particular[indice_columna - inicio_discapacitado],
                             formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_discapacitado], formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_discapacitado], formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_discapacitado], formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_discapacitado], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_discapacitado], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_discapacitado], formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_discapacitado], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_discapacitado], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_discapacitado], formato2)
            worksheet_data.write(indice_columna, 14, causa_no_ubicado[indice_columna - inicio_discapacitado],
                                 formato2)
            worksheet_data.write(indice_columna, 15, activo[indice_columna - inicio_discapacitado],
                                 formato2)

    # FIN -> DISCAPACITADOS

    # INICIO -> PERSONAS DE RIESGO

    if categoria_usuario == 'dmt':
        personas_riesgo = PersonasRiesgo.objects.filter(
                              municipio_solicita_empleo=municipio_usuario, activo=True). \
                              values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                     "nivel_escolar__nombre",
                                     "carrera__nombre",
                                     "fuente_procedencia__nombre", "ubicado", "organismo__nombre",
                                     "entidad__e_nombre",
                                     "ubicacion__ubicacion", "municipio_solicita_empleo__nombre",
                                     "municipio_solicita_empleo__provincia__nombre", "edad",
                                     "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'dpt_ee':
        personas_riesgo = PersonasRiesgo.objects.filter(
                              municipio_solicita_empleo__provincia=provincia_usuario, activo=True). \
                              values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                     "nivel_escolar__nombre", "carrera__nombre", "fuente_procedencia__nombre",
                                     "ubicado",
                                     "organismo__nombre", "entidad__e_nombre", "ubicacion__ubicacion",
                                     "municipio_solicita_empleo__nombre",
                                     "municipio_solicita_empleo__provincia__nombre", "edad",
                                     "causa_no_ubicado__causa", "activo")
    elif categoria_usuario == 'organismo':
        personas_riesgo = PersonasRiesgo.objects.filter(organismo__nombre=organismo_usuario, activo=True). \
                              values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                     "nivel_escolar__nombre", "carrera__nombre", "fuente_procedencia__nombre",
                                     "ubicado",
                                     "organismo__nombre", "entidad__e_nombre", "ubicacion__ubicacion",
                                     "municipio_solicita_empleo__nombre",
                                     "municipio_solicita_empleo__provincia__nombre", "edad",
                                     "causa_no_ubicado__causa", "activo")
    else:
        personas_riesgo = PersonasRiesgo.objects.filter(activo=True). \
                              values("nombre_apellidos", "sexo", "ci", "direccion_particular",
                                     "nivel_escolar__nombre", "carrera__nombre", "fuente_procedencia__nombre",
                                     "ubicado",
                                     "organismo__nombre", "entidad__e_nombre", "ubicacion__ubicacion",
                                     "municipio_solicita_empleo__nombre",
                                     "municipio_solicita_empleo__provincia__nombre", "edad",
                                     "causa_no_ubicado__causa", "activo")

    query = """SELECT id
                    FROM public."SGMGU_personasriesgo" t where
                        date_part('year', t.fecha_registro)=""" + unicode(anno) + """ AND
                        date_part('month', t.fecha_registro)=""" + unicode(mes) + """;"""

    resultado_query = PersonasRiesgo.objects.raw(query)
    ids_listado = [persona.id for persona in resultado_query]
    personas_riesgo = personas_riesgo.exclude(id__in=ids_listado)

    nombre_apellidos = []
    sexo = []
    ci = []
    direccion_particular = []
    nivel_escolar = []
    carrera = []
    fuente = []
    ubicado = []
    organismo = []
    entidad = []
    ubicacion = []
    municipios = []
    provincias = []
    edad = []
    causa_no_ubicado = []
    activo = []

    for persona in personas_riesgo:
        nombre_apellidos.append(persona['nombre_apellidos'])
        sexo.append(persona['sexo'])
        edad.append(persona['edad'])
        ci.append(persona['ci'])
        direccion_particular.append(persona['direccion_particular'])
        nivel_escolar.append(persona['nivel_escolar__nombre'])
        if not persona['carrera__nombre']:
            carrera.append("---")
        else:
            carrera.append(persona['carrera__nombre'])
        fuente.append(persona['fuente_procedencia__nombre'])
        if persona['ubicado']:
            ubicado.append("Si")
        else:
            ubicado.append("No")
        if not persona['organismo__nombre']:
            organismo.append("---")
        else:
            organismo.append(persona['organismo__nombre'])
        if not persona['entidad__e_nombre']:
            entidad.append("---")
        else:
            entidad.append(persona['entidad__e_nombre'])
        if not persona['ubicacion__ubicacion']:
            ubicacion.append("---")
        else:
            ubicacion.append(persona['ubicacion__ubicacion'])
        municipios.append(persona['municipio_solicita_empleo__nombre'])
        provincias.append(persona['municipio_solicita_empleo__provincia__nombre'])
        if not persona['causa_no_ubicado__causa']:
            causa_no_ubicado.append("---")
        else:
            causa_no_ubicado.append(persona['causa_no_ubicado__causa'])
        if not persona['activo']:
            activo.append("Baja")
        else:
            activo.append("Activo")

    inicio_persona_riesgo = fin_discapacitado
    fin_persona_riesgo = inicio_persona_riesgo + nombre_apellidos.__len__()

    for indice_columna in range(inicio_persona_riesgo, fin_persona_riesgo):
        worksheet_data.write(indice_columna, 0, nombre_apellidos[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 1, sexo[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 2, ci[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 3, direccion_particular[indice_columna - inicio_persona_riesgo],
                             formato2)
        worksheet_data.write(indice_columna, 4, nivel_escolar[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 5, carrera[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 6, fuente[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 7, ubicado[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 8, organismo[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 9, entidad[indice_columna - inicio_persona_riesgo], formato2)
        worksheet_data.write(indice_columna, 10, ubicacion[indice_columna - inicio_persona_riesgo], formato2)
        if categoria_usuario == 'dpt_ee':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_persona_riesgo], formato2)
        elif categoria_usuario == 'organismo':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_persona_riesgo], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_persona_riesgo], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_persona_riesgo], formato2)
        elif categoria_usuario == 'administrador':
            worksheet_data.write(indice_columna, 11, municipios[indice_columna - inicio_persona_riesgo], formato2)
            worksheet_data.write(indice_columna, 12, provincias[indice_columna - inicio_persona_riesgo], formato2)
            worksheet_data.write(indice_columna, 13, edad[indice_columna - inicio_persona_riesgo], formato2)
            worksheet_data.write(indice_columna, 14, causa_no_ubicado[indice_columna - inicio_persona_riesgo],
                                 formato2)
            worksheet_data.write(indice_columna, 15, activo[indice_columna - inicio_persona_riesgo],
                                 formato2)

    # FIN -> PERSONAS DE RIESGO

    book.close()

    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    return response
