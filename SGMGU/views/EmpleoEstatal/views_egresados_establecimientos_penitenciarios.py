# -*- coding: utf-8 -*-
from django.contrib import messages
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def listado_egresados_establecimientos_penitenciarios(request):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # start_time = time.time()

    if 11 <= dia_actual <= 18 and mes_actual == 1:

        egresados_ep = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=2,
                                                                     fecha_comprobacion__year=anno_actual)
        sancionados = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=3,
                                                                    fecha_comprobacion__year=anno_actual)

        if egresados_ep.count() == 0:
            listado_eep = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=2,
                                                                                 activo=True). \
                exclude(fecha_registro__year=anno_actual).\
                exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado_eep)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=2, fecha_comprobacion=timezone.now())

        if sancionados.count() == 0:
            listado_desvinculados = EgresadosEstablecimientosPenitenciarios.objects.filter(fuente_procedencia_id=3,
                                                                                           activo=True). \
                exclude(fecha_registro__year=anno_actual). \
                exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado_desvinculados)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=3, fecha_comprobacion=timezone.now())

    # elapsed_time = time.time() - start_time
    # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        egresados_establecimientos_penitenciarios = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                        fecha_registro__year=anno_actual) | \
                                                    EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                        activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        egresados_establecimientos_penitenciarios = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                        fecha_registro__year=anno_actual) | \
                                                    EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                        activo=True)
    else:
        egresados_establecimientos_penitenciarios = EgresadosEstablecimientosPenitenciarios.objects.all()

    egresados_establecimientos_penitenciarios = paginar(request, egresados_establecimientos_penitenciarios)
    paginas = crear_lista_pages(egresados_establecimientos_penitenciarios)
    nombre_pag = "Listado: Egresados de Establecimientos Penitenciarios y Sancionados sin Internamiento"
    return render(request, "EmpleoEstatal/EgresadosYSancionados/listar_egresados_establecimientos_penitenciarios.html", locals())


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def buscar_ci_egresados_sancionados(request, ci):
    anno_actual = datetime.datetime.today().year
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    if categoria_usuario == 'dmt':
        egresados_establecimientos_penitenciarios = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                        fecha_registro__year=anno_actual) | \
                                                    EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                        activo=True)
    elif categoria_usuario == 'dpt_ee':
        egresados_establecimientos_penitenciarios = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        ci__contains=ci,
                                                        municipio_solicita_empleo__provincia=provincia_usuario,
                                                        fecha_registro__year=anno_actual) | \
                                                    EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        ci__contains=ci,
                                                        municipio_solicita_empleo__provincia=provincia_usuario,
                                                        activo=True)
    else:
        egresados_establecimientos_penitenciarios = EgresadosEstablecimientosPenitenciarios.objects.filter(
                                                        ci__contains=ci)

    egresados_establecimientos_penitenciarios = paginar(request, egresados_establecimientos_penitenciarios)
    paginas = crear_lista_pages(egresados_establecimientos_penitenciarios)

    context = {'egresados_establecimientos_penitenciarios': egresados_establecimientos_penitenciarios, 'nombre_pag': "Listado por ci: %s" % ci,
               'busqueda': 'si', "valor_busqueda": ci, 'paginas': paginas}
    return render(request, "EmpleoEstatal/EgresadosYSancionados/listar_egresados_establecimientos_penitenciarios.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def registrar_egresado_establecimiento_penitenciario(request):
    municipio_solicita_empleo = request.user.perfil_usuario.municipio
    carreras = Carrera.objects.filter(activo=True)
    causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()
    delitos = Delito.objects.filter(activo=True)
    motivos_egreso = MotivoEgreso.objects.filter(activo=True)
    estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
    if request.method == 'POST':
        form = EgresadosEstablecimientosPenitenciariosForm(request.POST)
        if form.is_valid():
            egresados_establecimientos_penitenciarios = form.save(commit=False)
            ci = egresados_establecimientos_penitenciarios.ci
            egresados_establecimientos_penitenciarios.edad = obtener_edad(ci)
            egresados_establecimientos_penitenciarios.sexo = obtener_sexo(ci)
            egresados_establecimientos_penitenciarios.save()
            if egresados_establecimientos_penitenciarios.fuente_procedencia.id == 2:
                messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
            if egresados_establecimientos_penitenciarios.fuente_procedencia.id == 3:
                messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
            return redirect('/egresados_establecimientos_penitenciarios')
        else:
            id_delito = ''
            id_motivo_egreso = ''
            id_carrera = ''
            id_ubicado = ''
            id_ubicacion = ''
            id_organismo = ''
            id_entidad = ''
            id_municipio_entidad = ''
            id_causa_no_ubicado = ''
            id_incorporado = ''
            if 'delito' in request.POST:
                id_delito = request.POST['delito']
            if 'motivo_egreso' in request.POST:
                id_motivo_egreso = request.POST['motivo_egreso']
            if 'carrera' in request.POST:
                id_carrera = request.POST['carrera']
            if 'ubicado' in request.POST:
                id_ubicado = request.POST['ubicado']
            if 'ubicacion' in request.POST:
                id_ubicacion = request.POST['ubicacion']
            if 'organismo' in request.POST:
                id_organismo = request.POST['organismo']
            if 'entidad' in request.POST:
                id_entidad = request.POST['entidad']
            if 'municipio_entidad' in request.POST:
                id_municipio_entidad = request.POST['municipio_entidad']
            if 'causa_no_ubicado' in request.POST:
                id_causa_no_ubicado = request.POST['causa_no_ubicado']
            if 'incorporado' in request.POST:
                id_incorporado = request.POST['incorporado']
            context = {'form_egresado_establecimiento_penitenciario': form, 'nombre_form': "Registrar:",
                       'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
                       'delitos': delitos, 'motivos_egreso': motivos_egreso, 'organismos': organismos,
                       'municipios': municipios, 'id_delito': id_delito,
                       'id_motivo_egreso': id_motivo_egreso, 'id_carrera': id_carrera, 'id_ubicacion': id_ubicacion,
                       'id_ubicado': id_ubicado, 'id_organismo': id_organismo, 'id_entidad': id_entidad,
                       'id_municipio_entidad': id_municipio_entidad, 'id_incorporado': id_incorporado,
                       'id_causa_no_ubicado': id_causa_no_ubicado, 'estados_incorporado': estados_incorporado,
                       'municipio_solicita_empleo': municipio_solicita_empleo}
            return render(request,
                          "EmpleoEstatal/EgresadosYSancionados/registrar_egresado_establecimiento_penitenciario.html",
                          context)
    else:
        form = EgresadosEstablecimientosPenitenciariosForm()
    context = {'form_egresado_establecimiento_penitenciario': form, 'nombre_form': "Registrar:", 'delitos': delitos,
               'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
               'motivos_egreso': motivos_egreso, 'organismos': organismos,
               'municipios': municipios, 'estados_incorporado': estados_incorporado,
               'municipio_solicita_empleo': municipio_solicita_empleo}
    return render(request, "EmpleoEstatal/EgresadosYSancionados/registrar_egresado_establecimiento_penitenciario.html",
                  context)


@login_required
@permission_required(['administrador'])
def modificar_egresado_establecimiento_penitenciario(request, id_egresado_establecimiento_penitenciario):
    egresados_establecimientos_penitenciarios = EgresadosEstablecimientosPenitenciarios.objects.get(id=id_egresado_establecimiento_penitenciario)
    if request.method == 'POST':
        form = EgresadosEstablecimientosPenitenciariosForm(request.POST, instance=egresados_establecimientos_penitenciarios)
        if form.is_valid():
            ci = egresados_establecimientos_penitenciarios.ci
            egresados_establecimientos_penitenciarios.edad = obtener_edad(ci)
            egresados_establecimientos_penitenciarios.sexo = obtener_sexo(ci)
            form.save()
            messages.add_message(request, messages.SUCCESS, "El egresado se ha modificado con éxito.")
            return redirect('/egresados_establecimientos_penitenciarios')
    else:
        form = EgresadosEstablecimientosPenitenciariosForm(instance=egresados_establecimientos_penitenciarios)
    context = {'form': form}
    return render(request,
                  "EmpleoEstatal/EgresadosYSancionados/modificar_egresados_establecimientos_penitenciarios.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def dar_baja_egresado_ep(request, id_egresado_establecimiento_penitenciario):
    egresado_ep = EgresadosEstablecimientosPenitenciarios.objects.get(id=id_egresado_establecimiento_penitenciario)
    ids1 = [1, 2, 3, 4, 5, 6, 7]
    causales_baja_egresados = CausalBaja.objects.filter(id__in=ids1)
    ids2 = [1, 2, 4, 5, 7, 8, 9]
    causales_baja_sancionados = CausalBaja.objects.filter(id__in=ids2)
    if request.method == 'POST':
        form = DarBajaEgresadoEPForm(request.POST, instance=egresado_ep)
        if form.is_valid():
            id_causa = int(request.POST['dar_baja'])
            if id_causa == 5:
                egresado_ep.delete()
            else:
                egresado_ep.activo = False
                egresado_ep.causa_baja = CausalBaja.objects.get(id=request.POST['dar_baja'])
                egresado_ep.fecha_baja = datetime.datetime.now()
                form.save()
            messages.add_message(request, messages.SUCCESS, "El egresado ha sido dado de baja con éxito.")
            return redirect('/egresados_establecimientos_penitenciarios')
    else:
        form = DarBajaEgresadoEPForm()

    if egresado_ep.fuente_procedencia.id == 2:
        context = {'form': form, 'causales_baja': causales_baja_egresados}
    else:
        context = {'form': form, 'causales_baja': causales_baja_sancionados}
    return render(request, "EmpleoEstatal/EgresadosYSancionados/dar_baja_egresado_establecimiento_penitenciario.html", context)


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def detalle_egresado_establecimiento_penitenciario(request, id_egresado_establecimiento_penitenciario):
    egresado = EgresadosEstablecimientosPenitenciarios.objects.get(id=id_egresado_establecimiento_penitenciario)
    historiales = HistorialEgresadosYSancionados.objects.filter(id_egresado_sancionado=id_egresado_establecimiento_penitenciario)
    return render(request, "EmpleoEstatal/EgresadosYSancionados/detalles_egresado_establecimiento_penitenciario.html", locals())


@login_required
@permission_required(['administrador', 'dmt'])
def re_incorporar_egresado_establecimiento_penitenciario(request, id_egresado_establecimiento_penitenciario):
    if request.method == 'POST':
        form = HistorialEgresadosYSancionadosForm(request.POST)
        if form.is_valid():
            historial_egresado_sancionado= form.save(commit=False)
            historial_egresado_sancionado.id_egresado_sancionado = id_egresado_establecimiento_penitenciario
            historial_egresado_sancionado.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Re-incorporado con éxito.")
            href = "/egresados_establecimientos_penitenciarios/" + id_egresado_establecimiento_penitenciario
            return redirect(href)
    else:
        form = HistorialEgresadosYSancionadosForm()
    context = {'form': form, 'nombre_form': "Re-incorporar", 'id_egresado_establecimiento_penitenciario': id_egresado_establecimiento_penitenciario}
    return render(request, "EmpleoEstatal/EgresadosYSancionados/re_incorporar.html", context)


@login_required
@permission_required(['administrador'])
def reportes_egresados_establecimientos_penitenciarios(request):
    return render(request, "EmpleoEstatal/EgresadosYSancionados/Reportes/reportes_egresados_ep.html")


def comprobar_pendientes(listado):

    causal_baja_automatica = CausalBaja.objects.get(id=10)
    fecha_actual = timezone.now()

    for persona in listado:
        persona.activo = False
        persona.causa_baja = causal_baja_automatica
        persona.fecha_baja = fecha_actual
        persona.save()
