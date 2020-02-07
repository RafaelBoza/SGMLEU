# -*- coding: utf-8 -*-
from django.contrib import messages

from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def listado_egresados_efi(request):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # start_time = time.time()

    if 11 <= dia_actual <= 18 and mes_actual == 1:

        comprobado = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=11,
                                                                   fecha_comprobacion__year=anno_actual)

        if comprobado.count() == 0:
            listado = EgresadosEFI.objects.filter(activo=True). \
                        exclude(fecha_registro__year=anno_actual). \
                        exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=11, fecha_comprobacion=timezone.now())

            # elapsed_time = time.time() - start_time
            # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        egresados_efi = EgresadosEFI.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                    fecha_registro__year=anno_actual) | \
                        EgresadosEFI.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                    activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        egresados_efi = EgresadosEFI.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                    fecha_registro__year=anno_actual) | \
                        EgresadosEFI.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                    activo=True)
    else:
        egresados_efi = EgresadosEFI.objects.all()

    egresados_efi = paginar(request, egresados_efi)
    paginas = crear_lista_pages(egresados_efi)
    nombre_pag = "Listado: Egresados de la EFI"
    return render(request, "EmpleoEstatal/EgresadosEFI/listar_egresados_efi.html", locals())


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def buscar_ci_egresado_efi(request, ci):
    anno_actual = datetime.datetime.today().year
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    if categoria_usuario == 'dmt':
        egresados_efi = EgresadosEFI.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                    fecha_registro__year=anno_actual) | \
                        EgresadosEFI.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                    activo=True)
    elif categoria_usuario == 'dpt_ee':
        egresados_efi = EgresadosEFI.objects.filter(ci__contains=ci,
                                                    municipio_solicita_empleo__provincia=provincia_usuario,
                                                    fecha_registro__year=anno_actual) | \
                        EgresadosEFI.objects.filter(ci__contains=ci, municipio_solicita_empleo__provincia=provincia_usuario,
                                                    activo=True)
    else:
        egresados_efi = EgresadosEFI.objects.filter(ci__contains=ci)

    egresados_efi = paginar(request, egresados_efi)
    paginas = crear_lista_pages(egresados_efi)
    context = {'egresados_efi': egresados_efi, 'nombre_pag': "Listado por ci: %s" % ci,
               'busqueda': 'si', "valor_busqueda": ci, 'paginas': paginas}
    return render(request, "EmpleoEstatal/EgresadosEFI/listar_egresados_efi.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def registrar_egresado_efi(request):
    municipio_solicita_empleo = request.user.perfil_usuario.municipio
    carreras = Carrera.objects.filter(activo=True, tipo='oc')
    causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()
    estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
    if request.method == 'POST':
        form = EgresadosEFIForm(request.POST)
        if form.is_valid():
            egresados_efi = form.save(commit=False)
            ci = egresados_efi.ci
            egresados_efi.edad = obtener_edad(ci)
            egresados_efi.sexo = obtener_sexo(ci)
            egresados_efi.save()
            messages.add_message(request, messages.SUCCESS, "El egresado ha sido registrado con éxito.")
            return redirect('/egresados_efi')
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
            context = {'form_egresado_efi': form, 'nombre_form': "Registrar:",
                       'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
                       'organismos': organismos, 'municipios': municipios,
                       'estados_incorporado': estados_incorporado, 'id_carrera': id_carrera,
                       'id_ubicacion': id_ubicacion, 'id_ubicado': id_ubicado, 'id_organismo': id_organismo,
                       'id_entidad': id_entidad, 'id_municipio_entidad': id_municipio_entidad,
                       'id_incorporado': id_incorporado, 'id_causa_no_ubicado': id_causa_no_ubicado,
                       'municipio_solicita_empleo': municipio_solicita_empleo}
            return render(request, "EmpleoEstatal/EgresadosEFI/registrar_egresado_efi.html", context)
    else:
        form = EgresadosEFIForm()
    context = {'form_egresado_efi': form, 'nombre_form': "Registrar:",
               'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
               'organismos': organismos, 'municipios': municipios,
               'estados_incorporado': estados_incorporado, 'municipio_solicita_empleo': municipio_solicita_empleo}
    return render(request, "EmpleoEstatal/EgresadosEFI/registrar_egresado_efi.html", context)


@login_required()
@permission_required(['administrador'])
def modificar_egresado_efi(request, id_egresado_efi):
    egresado_efi = EgresadosEFI.objects.get(id=id_egresado_efi)
    if request.method == 'POST':
        form = EgresadosEFIForm(request.POST, instance=egresado_efi)
        if form.is_valid():
            ci = egresado_efi.ci
            egresado_efi.edad = obtener_edad(ci)
            egresado_efi.sexo = obtener_sexo(ci)
            form.save()
            messages.add_message(request, messages.SUCCESS, "El egresado se ha modificado con éxito.")
            return redirect('/egresados_efi')
    else:
        form = EgresadosEFIForm(instance=egresado_efi)
    context = {'form': form}
    return render(request,
                  "EmpleoEstatal/EgresadosEFI/modificar_egresado_efi.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def dar_baja_egresado_efi(request, id_egresado_efi):
    egresado_efi = EgresadosEFI.objects.get(id=id_egresado_efi)
    if request.method == 'POST':
        form = DarBajaEgresadosEFIForm(request.POST, instance=egresado_efi)
        if form.is_valid():
            id_causa = int(request.POST['causa_baja'])
            if id_causa == 5:
                egresado_efi.delete()
            else:
                egresado_efi.activo = False
                egresado_efi.causa_baja = CausalBaja.objects.get(id=request.POST['causa_baja'])
                egresado_efi.fecha_baja = datetime.datetime.now()
                form.save()
            messages.add_message(request, messages.SUCCESS, "El egresado ha sido dado de baja con éxito.")
            return redirect('/egresados_efi')
    else:
        form = DarBajaEgresadosEFIForm()
    context = {'form': form}
    return render(request, "EmpleoEstatal/EgresadosEFI/dar_baja_egresado_efi.html", context)


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def detalle_egresado_efi(request, id_egresado_efi):
    egresado = EgresadosEFI.objects.get(id=id_egresado_efi)
    historiales = HistorialEgresadosEFI.objects.filter(id_egresado_efi=id_egresado_efi)
    return render(request, "EmpleoEstatal/EgresadosEFI/detalles_egresado_efi.html", locals())


@login_required()
@permission_required(['administrador', 'dmt'])
def re_incorporar_egresado_efi(request, id_egresado_efi):
    if request.method == 'POST':
        form = HistorialEgresadosEFIForm(request.POST)
        if form.is_valid():
            historial_egresados_efi= form.save(commit=False)
            historial_egresados_efi.id_egresado_efi = id_egresado_efi
            historial_egresados_efi.save()
            messages.add_message(request, messages.SUCCESS,"Re-incorporado con éxito.")
            href = "/egresados_efi/" + id_egresado_efi
            return redirect(href)
    else:
        form = HistorialEgresadosEFIForm()
    context = {'form': form, 'nombre_form': "Re-incorporar", 'id_egresado_efi': id_egresado_efi}
    return render(request, "EmpleoEstatal/EgresadosEFI/re_incorporar.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def habilitar_egresado_efi(request):

    ci = str(request.GET.get("ci", ""))
    errors = []
    context = {}

    if ci != "":
        try:
            busqueda = EgresadosEFI.objects.filter(ci=ci)
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
                        return redirect('/egresados_efi')
                    else:
                        errors.append("CI {} ya se encuentra habilitado.".format(ci))
                else:
                    errors.append("CI {} pertenece al municipio {}.".format(ci, str(persona.municipio_solicita_empleo.nombre.encode('utf-8').strip())))
            else:
                errors.append("CI {} no se encuentra registrado.".format(ci))

        except Exception as e:
            errors.append("Error. Vuelva a introducir el CI.")
            print("Error habilitando egresado de escuela de conducta: {}, {}".format(e.args, e.message))

    context['ci'] = ci
    context['errors'] = errors
    return render(request, "EmpleoEstatal/EgresadosEFI/habilitar_egresado_efi.html", context)


@login_required()
@permission_required(['administrador'])
def reportes_egresados_efi(request):
    return render(request, "EmpleoEstatal/EgresadosEFI/Reportes/reportes_egresados_efi.html")


def comprobar_pendientes(listado):

    causal_baja_automatica = CausalBaja.objects.get(id=10)
    fecha_actual = timezone.now()

    for persona in listado:
        persona.activo = False
        persona.causa_baja = causal_baja_automatica
        persona.fecha_baja = fecha_actual
        persona.save()