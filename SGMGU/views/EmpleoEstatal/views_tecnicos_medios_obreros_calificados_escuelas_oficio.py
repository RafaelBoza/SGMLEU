# -*- coding: utf-8 -*-
from django.contrib import messages

from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def listado_tm_oc_eo(request):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # tm = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6, ubicado=False, causa_no_ubicado__id=1,
    #                                              fecha_registro__year=2019)
    # print tm.count()
    # for t in tm:
    #     print t.fecha_registro

    start_time = time.time()

    if 11 <= dia_actual <= 18 and mes_actual == 1:

        comprobado_tm = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=6,
                                                                      fecha_comprobacion__year=anno_actual)
        comprobado_oc = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=7,
                                                                      fecha_comprobacion__year=anno_actual)
        comprobado_eo = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=8,
                                                                      fecha_comprobacion__year=anno_actual)

        if comprobado_tm.count() == 0:
            listado_tm = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=6, activo=True). \
                            exclude(fecha_registro__year=anno_actual). \
                            exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado_tm)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=6, fecha_comprobacion=timezone.now())

        if comprobado_oc.count() == 0:
            listado_oc = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=7, activo=True). \
                            exclude(fecha_registro__year=anno_actual). \
                            exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado_oc)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=7, fecha_comprobacion=timezone.now())

        if comprobado_eo.count() == 0:
            listado_eo = TMedioOCalificadoEOficio.objects.filter(fuente_procedencia_id=8, activo=True). \
                exclude(fecha_registro__year=anno_actual). \
                exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado_eo)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=8, fecha_comprobacion=timezone.now())

            elapsed_time = time.time() - start_time
            print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                           fecha_registro__year=anno_actual) | \
                   TMedioOCalificadoEOficio.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                           activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                           fecha_registro__year=anno_actual) | \
                   TMedioOCalificadoEOficio.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                           activo=True)
    else:
        tm_oc_eo = TMedioOCalificadoEOficio.objects.all()

    tm_oc_eo = paginar(request, tm_oc_eo)
    paginas = crear_lista_pages(tm_oc_eo)
    nombre_pag = "Listado: Técnicos Medios, Obreros Calificados y Escuelas de Oficio"
    return render(request, "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/listar_tm_oc_eo.html",
                  locals())


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def buscar_ci_tm_oc_eo(request, ci):
    anno_actual = datetime.datetime.today().year
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    if categoria_usuario == 'dmt':
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                           fecha_registro__year=anno_actual) | \
                   TMedioOCalificadoEOficio.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                           activo=True)
    elif categoria_usuario == 'dpt_ee':
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(ci__contains=ci,
                                                           municipio_solicita_empleo__provincia=provincia_usuario,
                                                           fecha_registro__year=anno_actual) | \
                   TMedioOCalificadoEOficio.objects.filter(ci__contains=ci,
                                                           municipio_solicita_empleo__provincia=provincia_usuario,
                                                           activo=True)
    else:
        tm_oc_eo = TMedioOCalificadoEOficio.objects.filter(ci__contains=ci)

    tm_oc_eo = paginar(request, tm_oc_eo)
    paginas = crear_lista_pages(tm_oc_eo)

    context = {'tm_oc_eo': tm_oc_eo, 'nombre_pag': "Listado por ci: %s" % ci,
               'busqueda': 'si', 'valor_busqueda': ci, 'paginas': paginas}

    return render(request, "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/listar_tm_oc_eo.html",
                  context)


@login_required()
@permission_required(['administrador', 'dmt'])
def registrar_tm_oc_eo(request):
    municipio_solicita_empleo = request.user.perfil_usuario.municipio
    carreras = Carrera.objects.filter(activo=True)
    causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    ids_ubicaciones = [1, 2, 3, 4, 5]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()
    estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
    if request.method == 'POST':
        form = TMedioOCalificadoEOficioForm(request.POST)
        if form.is_valid():
            tm_oc_eo = form.save(commit=False)
            ci = tm_oc_eo.ci
            tm_oc_eo.edad = obtener_edad(ci)
            tm_oc_eo.sexo = obtener_sexo(ci)
            tm_oc_eo.save()
            if 'aceptar' in request.POST:
                messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
                return redirect('/tecnicosmedios_obreroscalificados_escuelasoficio')
            elif 'aceptar_continuar' in request.POST:
                messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
                form = TMedioOCalificadoEOficioForm()
                context = {'form_tm_oc_eo': form, 'nombre_form': "Registrar:", 'carreras': carreras,
                           'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones, 'organismos': organismos,
                           'municipios': municipios, 'estados_incorporado': estados_incorporado,
                           'municipio_solicita_empleo': municipio_solicita_empleo}
                return render(request,
                              "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/registrar_tm_oc_eo.html",
                              context)
        else:
            id_carrera = ''
            id_cumple_servicio_social = ''
            folio = ''
            id_ubicado = ''
            id_ubicacion = ''
            id_organismo = ''
            id_entidad = ''
            id_municipio_entidad = ''
            id_causa_no_ubicado = ''
            id_incorporado = ''
            if 'carrera' in request.POST:
                id_carrera = request.POST['carrera']
            if 'cumple_servicio_social' in request.POST:
                id_cumple_servicio_social = request.POST['cumple_servicio_social']
            if 'folio_boleta' in request.POST:
                folio = request.POST['folio_boleta']
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
            context = {'form_tm_oc_eo': form, 'nombre_form': "Registrar:", 'carreras': carreras,
                       'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones, 'organismos': organismos,
                       'municipios': municipios, 'estados_incorporado': estados_incorporado,
                       'id_carrera': id_carrera, 'id_ubicacion': id_ubicacion, 'id_ubicado': id_ubicado,
                       'id_organismo': id_organismo, 'id_entidad': id_entidad,
                       'id_municipio_entidad': id_municipio_entidad, 'id_incorporado': id_incorporado,
                       'id_causa_no_ubicado': id_causa_no_ubicado, 'id_cumple_servicio_social': id_cumple_servicio_social,
                       'folio': folio, 'municipio_solicita_empleo': municipio_solicita_empleo}
            return render(request,
                          "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/registrar_tm_oc_eo.html",
                          context)
    else:
        form = TMedioOCalificadoEOficioForm()
    context = {'form_tm_oc_eo': form, 'nombre_form': "Registrar:", 'carreras': carreras,
               'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones, 'organismos': organismos,
               'municipios': municipios,  'estados_incorporado': estados_incorporado,
               'municipio_solicita_empleo': municipio_solicita_empleo}
    return render(request, "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/registrar_tm_oc_eo.html",
                  context)


@login_required()
@permission_required(['administrador'])
def modificar_tm_oc_eo(request, id_tm_oc_eo):
    tm_oc_eo = TMedioOCalificadoEOficio.objects.get(id=id_tm_oc_eo)
    carreras = Carrera.objects.filter(activo=True)
    causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    ubicaciones = Ubicacion.objects.filter(activo=True)
    organismos = Organismo.objects.filter(activo=True)
    entidades = Entidad.objects.filter(estado=True)
    municipios = Municipio.objects.all()
    estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
    errores = ''
    if request.method == 'POST':
        form = TMedioOCalificadoEOficioForm(request.POST, instance=tm_oc_eo)
        if form.is_valid():
            ci = tm_oc_eo.ci
            tm_oc_eo.edad = obtener_edad(ci)
            tm_oc_eo.sexo = obtener_sexo(ci)
            form.save()
            messages.add_message(request, messages.SUCCESS, "Modificado con éxito.")
            return redirect('/tecnicosmedios_obreroscalificados_escuelasoficio')
        else:
            id_carrera = ''
            id_cumple_servicio_social = ''
            folio = ''
            id_ubicado = ''
            id_ubicacion = ''
            id_organismo = ''
            id_entidad = ''
            id_municipio_entidad = ''
            id_causa_no_ubicado = ''
            id_incorporado = ''
            if 'carrera' in request.POST:
                id_carrera = request.POST['carrera']
            if 'cumple_servicio_social' in request.POST:
                id_cumple_servicio_social = request.POST['cumple_servicio_social']
            if 'folio_boleta' in request.POST:
                folio = request.POST['folio_boleta']
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
            context = {'form_tm_oc_eo': form, 'nombre_form': "Registrar:", 'carreras': carreras,
                       'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones, 'organismos': organismos,
                       'entidades': entidades, 'municipios': municipios, 'estados_incorporado': estados_incorporado,
                       'id_carrera': id_carrera, 'id_ubicacion': id_ubicacion, 'id_ubicado': id_ubicado,
                       'id_organismo': id_organismo, 'id_entidad': id_entidad,
                       'id_municipio_entidad': id_municipio_entidad, 'id_incorporado': id_incorporado,
                       'id_causa_no_ubicado': id_causa_no_ubicado,
                       'id_cumple_servicio_social': id_cumple_servicio_social,
                       'folio': folio, 'errores': errores}
            return render(request,
                          "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/modificar_tm_oc_eo.html",
                          context)
    else:
        form = TMedioOCalificadoEOficioForm(instance=tm_oc_eo)
    context = {'form_tm_oc_eo': form, 'nombre_form': "Registrar:", 'carreras': carreras,
               'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones, 'organismos': organismos,
               'entidades': entidades, 'municipios': municipios, 'estados_incorporado': estados_incorporado,
               'errores': errores, 'tm_oc_eo': tm_oc_eo}
    return render(request,
                  "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/modificar_tm_oc_eo.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def dar_baja_tm_oc_eo(request, id_tm_oc_eo):
    tm_oc_eo = TMedioOCalificadoEOficio.objects.get(id=id_tm_oc_eo)
    if request.method == 'POST':
        form = DarBajaTMedioOCalificadoEOficioForm(request.POST, instance=tm_oc_eo)
        if form.is_valid():
            id_causa = int(request.POST['causa_baja'])
            if id_causa == 5:
                tm_oc_eo.delete()
            else:
                tm_oc_eo.activo = False
                tm_oc_eo.causa_baja = CausalBaja.objects.get(id=request.POST['causa_baja'])
                tm_oc_eo.fecha_baja = datetime.datetime.now()
                form.save()
            messages.add_message(request, messages.SUCCESS, "El egresado ha sido dado de baja con éxito.")
            return redirect('/tecnicosmedios_obreroscalificados_escuelasoficio')
    else:
        form = DarBajaTMedioOCalificadoEOficioForm()
    context = {'form': form}
    return render(request, "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/dar_baja_tm_oc_eo.html", context)


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def detalle_tm_oc_eo(request, id_tm_oc_eo):
    tm_oc_eo = TMedioOCalificadoEOficio.objects.get(id=id_tm_oc_eo)
    historiales = HistorialTMedioOCalificadoEOficio.objects.filter(id_tm_oc_eo=id_tm_oc_eo)
    return render(request, "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/detalles_tm_oc_eo.html", locals())


@login_required()
@permission_required(['administrador', 'dmt'])
def re_incorporar_tm_oc_eo(request, id_tm_oc_eo):
    if request.method == 'POST':
        form = HistorialTMedioOCalificadoEOficioForm(request.POST)
        if form.is_valid():
            historial_tm_oc_eo= form.save(commit=False)
            historial_tm_oc_eo.id_tm_oc_eo = id_tm_oc_eo
            historial_tm_oc_eo.save()
            messages.add_message(request, messages.SUCCESS, "Re-incorporado con éxito.")
            href = "/tecnicosmedios_obreroscalificados_escuelasoficio/" + id_tm_oc_eo
            return redirect(href)
    else:
        form = HistorialTMedioOCalificadoEOficioForm()
    context = {'form': form, 'nombre_form': "Re-incorporar", 'id_tm_oc_eo': id_tm_oc_eo}
    return render(request, "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/re_incorporar.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def habilitar_tm_oc_eo(request):

    ci = str(request.GET.get("ci", ""))
    errors = []
    context = {}

    if ci != "":
        try:
            busqueda = TMedioOCalificadoEOficio.objects.filter(ci=ci)
            if busqueda.count() != 0:
                persona = busqueda.first()
                if request.user.perfil_usuario.categoria.nombre == 'administrador' or str(persona.municipio_solicita_empleo.nombre) == str(request.user.perfil_usuario.municipio.nombre):
                    if not persona.activo:
                        persona.activo = True
                        persona.causa_baja = None
                        persona.fecha_baja = None
                        persona.save()

                        messages.add_message(request, messages.SUCCESS, "Habilitado con éxito.")
                        return redirect('/tecnicosmedios_obreroscalificados_escuelasoficio')
                    else:
                        errors.append("CI {} ya se encuentra habilitado.".format(ci))
                else:
                    errors.append("CI {} pertenece al municipio {}.".format(ci, persona.municipio_solicita_empleo))
            else:
                errors.append("CI {} no se encuentra registrado.".format(ci))

        except Exception as e:
            errors.append("Error. Vuelva a introducir el CI.")
            print("Error habilitando desvinculado: {}, {}".format(e.args, e.message))

    context['ci'] = ci
    context['errors'] = errors
    return render(request, "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/habilitar_tm_oc_eo.html", context)




@login_required
@permission_required(['administrador'])
def reportes_tm_oc_eo(request):
    return render(request,
                  "EmpleoEstatal/TecnicosMedios_ObrerosCalificados_EscuelasOficio/Reportes/reportes_tm_oc_eo.html")


def comprobar_pendientes(listado):

    causal_baja_automatica = CausalBaja.objects.get(id=10)
    fecha_actual = timezone.now()

    for persona in listado:
        persona.activo = False
        persona.causa_baja = causal_baja_automatica
        persona.fecha_baja = fecha_actual
        persona.save()

