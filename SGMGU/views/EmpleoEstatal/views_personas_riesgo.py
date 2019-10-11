# -*- coding: utf-8 -*-
from django.contrib import messages

from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def listado_personas_riesgo(request):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # start_time = time.time()

    if 11 <= dia_actual <= 18 and mes_actual == 1:

        comprobando_mujeres_riesgo = ComprobacionAnualEmpleoEstatal.objects.filter(
                                                                    fuente_procedencia_id=17,
                                                                    fecha_comprobacion__year=anno_actual)
        comprobado_hombres_riesgo = ComprobacionAnualEmpleoEstatal.objects.filter(
                                                                    fuente_procedencia_id=18,
                                                                    fecha_comprobacion__year=anno_actual)
        comprobado_proxenetas = ComprobacionAnualEmpleoEstatal.objects.filter(
                                                                    fuente_procedencia_id=19,
                                                                    fecha_comprobacion__year=anno_actual)

        if comprobando_mujeres_riesgo.count() == 0:
            listado = PersonasRiesgo.objects.filter(fuente_procedencia_id=17, activo=True). \
                        exclude(fecha_registro__year=anno_actual). \
                        exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=17, fecha_comprobacion=timezone.now())

        if comprobado_hombres_riesgo.count() == 0:
            listado = PersonasRiesgo.objects.filter(fuente_procedencia_id=18, activo=True). \
                        exclude(fecha_registro__year=anno_actual). \
                        exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=18, fecha_comprobacion=timezone.now())

        if comprobado_proxenetas.count() == 0:
            listado = PersonasRiesgo.objects.filter(fuente_procedencia_id=19, activo=True). \
                        exclude(fecha_registro__year=anno_actual). \
                        exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=19, fecha_comprobacion=timezone.now())

            # elapsed_time = time.time() - start_time
            # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        personas_riesgo = PersonasRiesgo.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                        fecha_registro__year=anno_actual) | \
                          PersonasRiesgo.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                        activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        personas_riesgo = PersonasRiesgo.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                        fecha_registro__year=anno_actual) | \
                          PersonasRiesgo.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                        activo=True)
    else:
        personas_riesgo = PersonasRiesgo.objects.all()

    return render(request, "EmpleoEstatal/PersonasRiesgo/listar_personas_riesgo.html", locals())


# TODO: hacer el buscar

@login_required()
@permission_required(['administrador', 'dmt'])
def registrar_personas_riesgo(request):
    municipio_solicita_empleo = request.user.perfil_usuario.municipio
    carreras = Carrera.objects.filter(activo=True)
    ids_causas_no_ubicado = [1, 2, 3, 4, 5, 6, 11]
    causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True, id__in=ids_causas_no_ubicado)
    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()
    estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
    if request.method == 'POST':
        form = PersonasRiesgoForm(request.POST)
        if form.is_valid():
            personas_riesgo = form.save(commit=False)
            ci = personas_riesgo.ci
            personas_riesgo.edad = obtener_edad(ci)
            personas_riesgo.sexo = obtener_sexo(ci)
            personas_riesgo.save()
            messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
            return redirect('/personas_riesgo')
        else:
            id_carrera = ''
            id_ubicado = ''
            id_ubicacion = ''
            id_organismo = ''
            id_entidad = ''
            id_municipio_entidad = ''
            id_causa_no_ubicado = ''
            id_incorporado = ''
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
            context = {'form_personas_riesgo': form, 'nombre_form': "Registrar:",
                       'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
                       'organismos': organismos, 'municipios': municipios,
                       'estados_incorporado': estados_incorporado, 'id_carrera': id_carrera,
                       'id_ubicacion': id_ubicacion, 'id_ubicado': id_ubicado, 'id_organismo': id_organismo,
                       'id_entidad': id_entidad, 'id_municipio_entidad': id_municipio_entidad,
                       'id_incorporado': id_incorporado, 'id_causa_no_ubicado': id_causa_no_ubicado,
                       'municipio_solicita_empleo': municipio_solicita_empleo}
            return render(request, "EmpleoEstatal/PersonasRiesgo/registrar_personas_riesgo.html", context)
    else:
        form = PersonasRiesgoForm()
    context = {'form_personas_riesgo': form, 'nombre_form': "Registrar:",
               'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
               'organismos': organismos, 'municipios': municipios,
               'estados_incorporado': estados_incorporado, 'municipio_solicita_empleo': municipio_solicita_empleo}
    return render(request, "EmpleoEstatal/PersonasRiesgo/registrar_personas_riesgo.html", context)


@login_required()
@permission_required(['administrador'])
def modificar_personas_riesgo(request, id_persona_riesgo):
    persona_riesgo = PersonasRiesgo.objects.get(id=id_persona_riesgo)
    if request.method == 'POST':
        form = PersonasRiesgoForm(request.POST, instance=persona_riesgo)
        if form.is_valid():
            ci = persona_riesgo.ci
            persona_riesgo.edad = obtener_edad(ci)
            persona_riesgo.sexo = obtener_sexo(ci)
            form.save()
            messages.add_message(request, messages.SUCCESS, "Modificado con éxito.")
            return redirect('/personas_riesgo')
    else:
        form = PersonasRiesgoForm(instance=persona_riesgo)
    context = {'form': form}
    return render(request,
                  "EmpleoEstatal/PersonasRiesgo/modificar_persona_riesgo.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def dar_baja_persona_riesgo(request, id_persona_riesgo):
    persona_riesgo = PersonasRiesgo.objects.get(id=id_persona_riesgo)
    if request.method == 'POST':
        form = DarBajaPersonasRiesgoForm(request.POST, instance=persona_riesgo)
        if form.is_valid():
            id_causa = int(request.POST['causa_baja'])
            if id_causa == 5:
                persona_riesgo.delete()
            else:
                persona_riesgo.activo = False
                persona_riesgo.causa_baja = CausalBaja.objects.get(id=request.POST['causa_baja'])
                persona_riesgo.fecha_baja = datetime.datetime.now()
                form.save()
            messages.add_message(request, messages.SUCCESS, "La persona ha sido dado de baja con éxito.")
            return redirect('/personas_riesgo')
    else:
        form = DarBajaPersonasRiesgoForm()
    context = {'form': form}
    return render(request, "EmpleoEstatal/PersonasRiesgo/dar_baja_persona_riesgo.html", context)


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def detalle_persona_riesgo(request, id_persona_riesgo):
    persona_riesgo = PersonasRiesgo.objects.get(id=id_persona_riesgo)
    historiales = HistorialPersonasRiesgo.objects.filter(id_persona_riesgo=id_persona_riesgo)
    return render(request, "EmpleoEstatal/PersonasRiesgo/detalles_persona_riesgo.html", locals())


@login_required()
@permission_required(['administrador', 'dmt'])
def re_incorporar_persona_riesgo(request, id_persona_riesgo):
    if request.method == 'POST':
        form = HistorialPersonaRiesgoForm(request.POST)
        if form.is_valid():
            historial_persona_riesgo= form.save(commit=False)
            historial_persona_riesgo.id_persona_riesgo= id_persona_riesgo
            historial_persona_riesgo.save()
            messages.add_message(request, messages.SUCCESS, "Re-incorporado con éxito.")
            href = "/personas_riesgo/" + id_persona_riesgo
            return redirect(href)
    else:
        form = HistorialPersonaRiesgoForm()
    context = {'form': form, 'nombre_form': "Re-incorporar", 'id_persona_riesgo': id_persona_riesgo}
    return render(request, "EmpleoEstatal/PersonasRiesgo/re_incorporar.html", context)


@login_required
@permission_required(['administrador'])
def reportes_personas_riesgo(request):
    return render(request, "EmpleoEstatal/Menores/Reportes/reportes_menores.html")


def comprobar_pendientes(listado):

    causal_baja_automatica = CausalBaja.objects.get(id=10)
    fecha_actual = timezone.now()

    for persona in listado:
        persona.activo = False
        persona.causa_baja = causal_baja_automatica
        persona.fecha_baja = fecha_actual
        persona.save()