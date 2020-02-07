# -*- coding: utf-8 -*-
from django.contrib import messages
from django.utils import timezone

from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def listado_discapacitados(request):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # start_time = time.time()

    if 11 <= dia_actual <= 18 and mes_actual == 1:

        comprobado = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=15,
                                                                   fecha_comprobacion__year=anno_actual)

        if comprobado.count() == 0:
            listado = Discapacitados.objects.filter(activo=True). \
                        exclude(fecha_registro__year=anno_actual). \
                        exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=15, fecha_comprobacion=timezone.now())

            # elapsed_time = time.time() - start_time
            # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        discapacitados = Discapacitados.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                       fecha_registro__year=anno_actual) | \
                         Discapacitados.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                       activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        discapacitados = Discapacitados.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                       fecha_registro__year=anno_actual) | \
                         Discapacitados.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                       activo=True)
    else:
        discapacitados = Discapacitados.objects.all()

    discapacitados = paginar(request, discapacitados)
    paginas = crear_lista_pages(discapacitados)
    nombre_pag = "Listado: Discapacitados"

    return render(request, "EmpleoEstatal/Discapacitados/listar_discapacitados.html", locals())


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def buscar_ci_discapacitado(request, ci):
    anno_actual = datetime.datetime.today().year
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    if categoria_usuario == 'dmt':
        discapacitados = Discapacitados.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                       fecha_registro__year=anno_actual) | \
                         Discapacitados.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                       activo=True)
    elif categoria_usuario == 'dpt_ee':
        discapacitados = Discapacitados.objects.filter(ci__contains=ci,
                                                       municipio_solicita_empleo__provincia=provincia_usuario,
                                                       fecha_registro__year=anno_actual) | \
                         Discapacitados.objects.filter(ci__contains=ci,
                                                       municipio_solicita_empleo__provincia=provincia_usuario,
                                                       activo=True)
    else:
        discapacitados = Discapacitados.objects.filter(ci__contains=ci)

    discapacitados = paginar(request, discapacitados)
    paginas = crear_lista_pages(discapacitados)
    context = {'discapacitados': discapacitados, 'nombre_pag': "Listado por ci: %s" % ci,
               'busqueda': 'si', "valor_busqueda": ci, 'paginas': paginas}
    return render(request, "EmpleoEstatal/Discapacitados/listar_discapacitados.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def registrar_discapacitado(request):
    municipio_solicita_empleo = request.user.perfil_usuario.municipio
    carreras = Carrera.objects.filter(activo=True)
    causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()
    estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
    if request.method == 'POST':
        form = DiscapacitadosForm(request.POST)
        if form.is_valid():
            discapacitados = form.save(commit=False)
            ci = discapacitados.ci
            discapacitados.edad = obtener_edad(ci)
            discapacitados.sexo = obtener_sexo(ci)
            discapacitados.save()
            messages.add_message(request, messages.SUCCESS, "El discapacitado ha sido registrado con éxito.")
            return redirect('/discapacitados')
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
            context = {'form_discapacitados': form, 'nombre_form': "Registrar:",
                       'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
                       'organismos': organismos, 'municipios': municipios,
                       'estados_incorporado': estados_incorporado, 'id_carrera': id_carrera,
                       'id_ubicacion': id_ubicacion, 'id_ubicado': id_ubicado, 'id_organismo': id_organismo,
                       'id_entidad': id_entidad, 'id_municipio_entidad': id_municipio_entidad,
                       'id_incorporado': id_incorporado, 'id_causa_no_ubicado': id_causa_no_ubicado,
                       'municipio_solicita_empleo': municipio_solicita_empleo}
            return render(request, "EmpleoEstatal/Discapacitados/registrar_discapacitado.html", context)
    else:
        form = DiscapacitadosForm()
    context = {'form_discapacitados': form, 'nombre_form': "Registrar:",
               'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
               'organismos': organismos,'municipios': municipios,
               'estados_incorporado': estados_incorporado, 'municipio_solicita_empleo': municipio_solicita_empleo}
    return render(request, "EmpleoEstatal/Discapacitados/registrar_discapacitado.html", context)


@login_required()
@permission_required(['administrador'])
def modificar_discapacitado(request, id_discapacitado):
    discapacitado = Discapacitados.objects.get(id=id_discapacitado)
    if request.method == 'POST':
        form = DiscapacitadosForm(request.POST, instance=discapacitado)
        if form.is_valid():
            ci = discapacitado.ci
            discapacitado.edad = obtener_edad(ci)
            discapacitado.sexo = obtener_sexo(ci)
            form.save()
            messages.add_message(request, messages.SUCCESS, "El discapacitado se ha modificado con éxito.")
            return redirect('/discapacitados')
    else:
        form = DiscapacitadosForm(instance=discapacitado)
    context = {'form': form}
    return render(request,
                  "EmpleoEstatal/Discapacitados/modificar_discapacitado.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def dar_baja_discapacitado(request, id_discapacitado):
    discapacitado = Discapacitados.objects.get(id=id_discapacitado)
    if request.method == 'POST':
        form = DarBajaDiscapacitadosForm(request.POST, instance=discapacitado)
        if form.is_valid():
            id_causa = int(request.POST['causa_baja'])
            if id_causa == 5:
                discapacitado.delete()
            else:
                discapacitado.activo = False
                discapacitado.causa_baja = CausalBaja.objects.get(id=request.POST['causa_baja'])
                discapacitado.fecha_baja = datetime.datetime.now()
                form.save()
            messages.add_message(request, messages.SUCCESS, "El discapacitado ha sido dado de baja con éxito.")
            return redirect('/discapacitados')
    else:
        form = DarBajaDiscapacitadosForm()
    context = {'form': form}
    return render(request, "EmpleoEstatal/Discapacitados/dar_baja_discapacitado.html", context)


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def detalle_discapacitado(request, id_discapacitado):
    discapacitado = Discapacitados.objects.get(id=id_discapacitado)
    historiales = HistorialDiscapacitados.objects.filter(id_discapacitado=id_discapacitado)
    return render(request, "EmpleoEstatal/Discapacitados/detalles_discapacitado.html", locals())


@login_required()
@permission_required(['administrador', 'dmt'])
def re_incorporar_discapacitado(request, id_discapacitado):
    if request.method == 'POST':
        form = HistorialDiscapacitadoForm(request.POST)
        if form.is_valid():
            historial_discapacitado= form.save(commit=False)
            historial_discapacitado.id_discapacitado= id_discapacitado
            historial_discapacitado.save()
            messages.add_message(request, messages.SUCCESS, "Re-incorporado con éxito.")
            href = "/discapacitados/" + id_discapacitado
            return redirect(href)
    else:
        form = HistorialDiscapacitadoForm()
    context = {'form': form, 'nombre_form': "Re-incorporar", 'id_discapacitado': id_discapacitado}
    return render(request, "EmpleoEstatal/Discapacitados/re_incorporar.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def habilitar_discapacitado(request):

    ci = str(request.GET.get("ci", ""))
    errors = []
    context = {}

    if ci != "":
        try:
            busqueda = Discapacitados.objects.filter(ci=ci)
            if busqueda.count() != 0:
                persona = busqueda.first()
                if request.user.perfil_usuario.categoria.nombre == 'administrador' or \
                        str(persona.municipio_solicita_empleo.nombre.encode('utf-8').strip()) == str(request.user.perfil_usuario.municipio.nombre.encode('utf-8').strip()):
                    if not persona.activo:
                        persona.activo = True
                        persona.causa_baja = None
                        persona.fecha_baja = None
                        persona.save()

                        messages.add_message(request, messages.SUCCESS, "Habilitado con éxito.")
                        return redirect('/discapacitados')
                    else:
                        errors.append("CI {} ya se encuentra habilitado.".format(ci))
                else:
                    errors.append("CI {} pertenece al municipio {}.".format(ci, str(persona.municipio_solicita_empleo.nombre.encode('utf-8').strip())))
            else:
                errors.append("CI {} no se encuentra registrado.".format(ci))

        except Exception as e:
            errors.append("Error. Vuelva a introducir el CI.")
            print("Error habilitando discapacitado: {}, {}".format(e.args, e.message))

    context['ci'] = ci
    context['errors'] = errors
    return render(request, "EmpleoEstatal/Discapacitados/habilitar_discapacitado.html", context)


@login_required
@permission_required(['administrador'])
def reportes_discapacitados(request):
    return render(request, "EmpleoEstatal/Discapacitados/Reportes/reportes_discapacitados.html")


def comprobar_pendientes(listado):

    causal_baja_automatica = CausalBaja.objects.get(id=10)
    fecha_actual = timezone.now()

    for persona in listado:
        persona.activo = False
        persona.causa_baja = causal_baja_automatica
        persona.fecha_baja = fecha_actual
        persona.save()