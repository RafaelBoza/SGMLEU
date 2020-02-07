# -*- coding: utf-8 -*-
from django.contrib import messages

from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def listado_menores(request):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # start_time = time.time()

    if 11 <= dia_actual <= 18 and mes_actual == 1:

        comprobado_menores_incapacitados = ComprobacionAnualEmpleoEstatal.objects.filter(
                                                                            fuente_procedencia_id=12,
                                                                            fecha_comprobacion__year=anno_actual)
        comprobado_menores_desvinculados = ComprobacionAnualEmpleoEstatal.objects.filter(
                                                                            fuente_procedencia_id=13,
                                                                            fecha_comprobacion__year=anno_actual)
        comprobado_menores_con_dictamen = ComprobacionAnualEmpleoEstatal.objects.filter(
                                                                            fuente_procedencia_id=14,
                                                                            fecha_comprobacion__year=anno_actual)

        if comprobado_menores_incapacitados.count() == 0:
            listado_menores_incapacitados = Menores.objects.filter(fuente_procedencia_id=12, activo=True). \
                        exclude(fecha_registro__year=anno_actual). \
                        exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado_menores_incapacitados)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=12, fecha_comprobacion=timezone.now())

        if comprobado_menores_desvinculados.count() == 0:
            listado_menores_desvinculados = Menores.objects.filter(fuente_procedencia_id=13, activo=True). \
                exclude(fecha_registro__year=anno_actual). \
                exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado_menores_desvinculados)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=13, fecha_comprobacion=timezone.now())

        if comprobado_menores_con_dictamen.count() == 0:
            listado_menores_con_dictamen = Menores.objects.filter(fuente_procedencia_id=14, activo=True). \
                exclude(fecha_registro__year=anno_actual). \
                exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado_menores_con_dictamen)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=14, fecha_comprobacion=timezone.now())

            # elapsed_time = time.time() - start_time
            # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        menores = Menores.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                         fecha_registro__year=anno_actual) | \
                  Menores.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                         activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        menores = Menores.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                         fecha_registro__year=anno_actual) | \
                  Menores.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                         activo=True)
    else:
        menores = Menores.objects.filter(activo=False)

    menores = paginar(request, menores)
    paginas = crear_lista_pages(menores)
    nombre_pag = "Listado: Jóvenes de 15 y 16 años"
    return render(request, "EmpleoEstatal/Menores/listar_menores.html", locals())


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def buscar_ci_menor(request, ci):
    anno_actual = datetime.datetime.today().year
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    if categoria_usuario == 'dmt':
        menores = Menores.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                         fecha_registro__year=anno_actual) | \
                  Menores.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                         activo=True)
    elif categoria_usuario == 'dpt_ee':
        menores = Menores.objects.filter(ci__contains=ci,
                                         municipio_solicita_empleo__provincia=provincia_usuario,
                                         fecha_registro__year=anno_actual) | \
                  Menores.objects.filter(ci__contains=ci, municipio_solicita_empleo__provincia=provincia_usuario,
                                         activo=True)
    else:
        menores = Menores.objects.filter(ci__contains=ci)

    menores = paginar(request, menores)
    paginas = crear_lista_pages(menores)
    context = {'menores': menores, 'nombre_pag': "Listado por ci: %s" % ci,
               'busqueda': 'si', "valor_busqueda": ci, 'paginas': paginas}
    return render(request, "EmpleoEstatal/Menores/listar_menores.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def registrar_menor(request):
    municipio_solicita_empleo = request.user.perfil_usuario.municipio
    carreras = Carrera.objects.filter(activo=True, tipo='oc')
    causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()
    estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
    if request.method == 'POST':
        form = MenoresForm(request.POST)
        if form.is_valid():
            menores = form.save(commit=False)
            ci = menores.ci
            menores.edad = obtener_edad(ci)
            menores.sexo = obtener_sexo(ci)
            menores.save()
            messages.add_message(request, messages.SUCCESS, "El joven ha sido registrado con éxito.")
            return redirect('/menores')
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
            context = {'form_menores': form, 'nombre_form': "Registrar:",
                       'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
                       'organismos': organismos, 'municipios': municipios,
                       'estados_incorporado': estados_incorporado, 'id_carrera': id_carrera,
                       'id_ubicacion': id_ubicacion, 'id_ubicado': id_ubicado, 'id_organismo': id_organismo,
                       'id_entidad': id_entidad, 'id_municipio_entidad': id_municipio_entidad,
                       'id_incorporado': id_incorporado, 'id_causa_no_ubicado': id_causa_no_ubicado,
                       'municipio_solicita_empleo': municipio_solicita_empleo}
            return render(request, "EmpleoEstatal/Menores/registrar_menor.html", context)
    else:
        form = MenoresForm()
    context = {'form_menores': form, 'nombre_form': "Registrar:",
               'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
               'organismos': organismos, 'municipios': municipios,
               'estados_incorporado': estados_incorporado, 'municipio_solicita_empleo': municipio_solicita_empleo}
    return render(request, "EmpleoEstatal/Menores/registrar_menor.html", context)


@login_required()
@permission_required(['administrador'])
def modificar_menor(request, id_menor):
    menor = Menores.objects.get(id=id_menor)
    if request.method == 'POST':
        form = MenoresForm(request.POST, instance=menor)
        if form.is_valid():
            ci = menor.ci
            menor.edad = obtener_edad(ci)
            menor.sexo = obtener_sexo(ci)
            form.save()
            messages.add_message(request, messages.SUCCESS, "El joven se ha modificado con éxito.")
            return redirect('/menores')
    else:
        form = MenoresForm(instance=menor)
    context = {'form': form}
    return render(request,
                  "EmpleoEstatal/Menores/modificar_menor.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def dar_baja_menor(request, id_menor):
    menor = Menores.objects.get(id=id_menor)
    if request.method == 'POST':
        form = DarBajaDesvinculadoForm(request.POST, instance=menor)
        if form.is_valid():
            id_causa = int(request.POST['causa_baja'])
            if id_causa == 5:
                menor.delete()
            else:
                menor.activo = False
                menor.causa_baja = CausalBaja.objects.get(id=request.POST['causa_baja'])
                menor.fecha_baja = datetime.datetime.now()
                form.save()
            messages.add_message(request, messages.SUCCESS, "El joven ha sido dado de baja con éxito.")
            return redirect('/menores')
    else:
        form = DarBajaDesvinculadoForm()
    context = {'form': form}
    return render(request, "EmpleoEstatal/Menores/dar_baja_menor.html", context)


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def detalle_menor(request, id_menor):
    menor = Menores.objects.get(id=id_menor)
    historiales = HistorialMenores.objects.filter(id_menor=id_menor)
    return render(request, "EmpleoEstatal/Menores/detalles_menor.html", locals())


@login_required()
@permission_required(['administrador', 'dmt'])
def re_incorporar_menor(request, id_menor):
    if request.method == 'POST':
        form = HistorialMenoresForm(request.POST)
        if form.is_valid():
            historial_menor = form.save(commit=False)
            historial_menor.id_menor = id_menor
            historial_menor.save()
            messages.add_message(request, messages.SUCCESS, "Re-incorporado con éxito.")
            href = "/menores/" + id_menor
            return redirect(href)
    else:
        form = HistorialMenoresForm()
    context = {'form': form, 'nombre_form': "Re-incorporar", 'id_menor': id_menor}
    return render(request, "EmpleoEstatal/Menores/re_incorporar.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def habilitar_menor(request):

    ci = str(request.GET.get("ci", ""))
    errors = []
    context = {}

    if ci != "":
        try:
            busqueda = Menores.objects.filter(ci=ci)
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
                        return redirect('/menores')
                    else:
                        errors.append("CI {} ya se encuentra habilitado.".format(ci))
                else:
                    errors.append("CI {} pertenece al municipio {}.".format(ci, str(persona.municipio_solicita_empleo.nombre.encode('utf-8').strip())))
            else:
                errors.append("CI {} no se encuentra registrado.".format(ci))

        except Exception as e:
            errors.append("Error. Vuelva a introducir el CI.")
            print("Error habilitando menor: {}, {}".format(e.args, e.message))

    context['ci'] = ci
    context['errors'] = errors
    return render(request, "EmpleoEstatal/Menores/habilitar_menor.html", context)


@login_required
@permission_required(['administrador'])
def reportes_menores(request):
    return render(request, "EmpleoEstatal/Menores/Reportes/reportes_menores.html")


def comprobar_pendientes(listado):
    causal_baja_automatica = CausalBaja.objects.get(id=10)
    fecha_actual = timezone.now()

    for persona in listado:
        persona.activo = False
        persona.causa_baja = causal_baja_automatica
        persona.fecha_baja = fecha_actual
        persona.save()
