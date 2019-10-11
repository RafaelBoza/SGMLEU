# -*- coding: utf-8 -*-
from django.contrib import messages
from django.utils import timezone

from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def listado_desvinculados(request):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # start_time = time.time()

    if 11 <= dia_actual <= 18 and mes_actual == 1:

        comprobado = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=4,
                                                                   fecha_comprobacion__year=anno_actual)

        if comprobado.count() == 0:

            listado = Desvinculado.objects.filter(activo=True).\
                            exclude(fecha_registro__year=anno_actual).\
                            exclude(ubicado=False, causa_no_ubicado__id=1)

            comprobar_pendientes(listado)

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=4, fecha_comprobacion=timezone.now())

    # elapsed_time = time.time() - start_time
    # print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                    fecha_registro__year=anno_actual) | \
                        Desvinculado.objects.filter(municipio_solicita_empleo=request.user.perfil_usuario.municipio,
                                                    activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        desvinculados = Desvinculado.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                    fecha_registro__year=anno_actual) | \
                        Desvinculado.objects.filter(municipio_solicita_empleo__provincia=request.user.perfil_usuario.provincia,
                                                    activo=True)
    else:
        desvinculados = Desvinculado.objects.all()

    desvinculados = paginar(request, desvinculados)
    paginas = crear_lista_pages(desvinculados)
    nombre_pag = "Listado: Desvinculados"
    return render(request, "EmpleoEstatal/Desvinculados/listar_desvinculados.html", locals())


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def buscar_ci_desvinculados(request, ci):
    anno_actual = datetime.datetime.today().year
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    if categoria_usuario == 'dmt':
        desvinculados = Desvinculado.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                    fecha_registro__year=anno_actual) | \
                        Desvinculado.objects.filter(ci__contains=ci, municipio_solicita_empleo=municipio_usuario,
                                                    activo=True)
    elif categoria_usuario == 'dpt_ee':
        desvinculados = Desvinculado.objects.filter(ci__contains=ci,
                                                    municipio_solicita_empleo__provincia=provincia_usuario,
                                                    fecha_registro__year=anno_actual) | \
                        Desvinculado.objects.filter(ci__contains=ci, municipio_solicita_empleo__provincia=provincia_usuario,
                                                    activo=True)
    else:
        desvinculados = Desvinculado.objects.filter(ci__contains=ci)

    desvinculados = paginar(request, desvinculados)
    paginas = crear_lista_pages(desvinculados)

    context = {'desvinculados': desvinculados, 'nombre_pag': "Listado por ci: %s" % ci,
               'busqueda': 'si', "valor_busqueda": ci, 'paginas': paginas}
    return render(request, "EmpleoEstatal/Desvinculados/listar_desvinculados.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def registrar_desvinculado(request):

    if request.method == 'POST':
        form = DesvinculadosForm(request.POST)
        if form.is_valid():
            desvinculado = form.save(commit=False)
            if desvinculado.ubicado:
                desvinculado.fecha_ubicacion = datetime.datetime.now()
            ci = desvinculado.ci
            desvinculado.edad = obtener_edad(ci)
            desvinculado.sexo = obtener_sexo(ci)
            desvinculado.save()
            messages.add_message(request, messages.SUCCESS, "El desvinculado ha sido registrado con éxito.")
            return redirect('/desvinculados')
        else:
            municipio_solicita_empleo = request.user.perfil_usuario.municipio
            carreras = Carrera.objects.filter(activo=True)
            causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
            ids_ubicaciones = [1, 2, 3, 4]
            ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
            organismos = Organismo.objects.filter(activo=True)
            municipios = Municipio.objects.all()
            estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
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
            context = {'form_desvinculados': form, 'nombre_form': "Registrar: Desvinculado",
                       'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
                       'organismos': organismos, 'municipios': municipios,
                       'estados_incorporado': estados_incorporado, 'id_carrera': id_carrera,
                       'id_ubicacion': id_ubicacion, 'id_ubicado': id_ubicado, 'id_organismo': id_organismo,
                       'id_entidad': id_entidad, 'id_municipio_entidad': id_municipio_entidad,
                       'id_incorporado': id_incorporado, 'id_causa_no_ubicado': id_causa_no_ubicado,
                       'municipio_solicita_empleo': municipio_solicita_empleo}
            return render(request, "EmpleoEstatal/Desvinculados/registrar_desvinculado.html", context)
    else:
        form = DesvinculadosForm()
    municipio_solicita_empleo = request.user.perfil_usuario.municipio
    carreras = Carrera.objects.filter(activo=True)
    causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()
    estados_incorporado = EstadoIncorporado.objects.filter(activo=True)
    context = {'form_desvinculados': form, 'nombre_form': "Registrar: Desvinculado",
               'carreras': carreras, 'causas_no_ubicado': causas_no_ubicado, 'ubicaciones': ubicaciones,
               'organismos': organismos, 'municipios': municipios,
               'estados_incorporado': estados_incorporado, 'municipio_solicita_empleo': municipio_solicita_empleo}
    return render(request, "EmpleoEstatal/Desvinculados/registrar_desvinculado.html", context)


@login_required
@permission_required(['administrador'])
def modificar_desvinculado(request, id_desvinculado):
    desvinculado = Desvinculado.objects.get(id=id_desvinculado)
    if request.method == 'POST':
        form = DesvinculadosForm(request.POST, instance=desvinculado)
        if form.is_valid():
            ci = desvinculado.ci
            desvinculado.edad = obtener_edad(ci)
            desvinculado.sexo = obtener_sexo(ci)
            form.save()
            messages.add_message(request, messages.SUCCESS, "El desvinculado se ha modificado con éxito.")
            return redirect('/desvinculados')
    else:
        form = DesvinculadosForm(instance=desvinculado)
    context = {'form': form}
    return render(request,
                  "EmpleoEstatal/Desvinculados/modificar_desvinculado.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def ubicar_desvinculado(request, id_desvinculado):
    desvinculado = Desvinculado.objects.get(id=id_desvinculado)

    if request.method == 'POST':
        form = UbicarDesvinculadoForm(request.POST, instance=desvinculado)

        if form.is_valid():
            desvinculado = form.save(commit=False)
            cleaned_data = form.cleaned_data

            desvinculado.ubicado = True
            desvinculado.causa_no_ubicado = None

            desvinculado.ubicacion = cleaned_data.get('ubicacion')
            desvinculado.organismo = cleaned_data.get('organismo')
            desvinculado.municipio_entidad = cleaned_data.get('municipio_entidad')
            desvinculado.entidad = cleaned_data.get('entidad')
            desvinculado.fecha_ubicacion = datetime.datetime.now()

            form.save()
            messages.add_message(request, messages.SUCCESS, "Ubicado con éxito.")
            return redirect('/desvinculados')
    else:
        form = UbicarDesvinculadoForm()

    context = {'form': form, 'id_desvinculado': id_desvinculado, 'nombre_form': "Ubicar: Desvinculado"}
    return render(request, "EmpleoEstatal/Desvinculados/ubicar_desvinculado.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def dar_baja_desvinculado(request, id_desvinculado):
    desvinculado = Desvinculado.objects.get(id=id_desvinculado)
    if request.method == 'POST':
        form = DarBajaDesvinculadoForm(request.POST, instance=desvinculado)
        if form.is_valid():
            id_causa = int(request.POST['causa_baja'])
            if id_causa == 5:
                desvinculado.delete()
            else:
                desvinculado.activo = False
                desvinculado.causa_baja = CausalBaja.objects.get(id=request.POST['causa_baja'])
                desvinculado.fecha_baja = datetime.datetime.now()
                form.save()
            messages.add_message(request, messages.SUCCESS, "El desvinculado ha sido dado de baja con éxito.")
            return redirect('/desvinculados')
    else:
        form = DarBajaDesvinculadoForm(instance=desvinculado)
    context = {'form': form}
    return render(request, "EmpleoEstatal/Desvinculados/dar_baja_desvinculado.html", context)


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def detalle_desvinculado(request, id_desvinculado):
    desvinculado = Desvinculado.objects.get(id=id_desvinculado)
    historiales = HistorialDesvinculado.objects.filter(id_desvinculado=id_desvinculado)
    return render(request, "EmpleoEstatal/Desvinculados/detalles_desvinculado.html", locals())


@login_required
@permission_required(['administrador', 'dmt'])
def re_incorporar_desvinculado(request, id_desvinculado):
    if request.method == 'POST':
        form = HistorialDesvinculadoForm(request.POST)
        if form.is_valid():
            historial_desvinculado = form.save(commit=False)
            historial_desvinculado.id_desvinculado = id_desvinculado
            historial_desvinculado.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Re-incorporado con éxito.")
            href = "/desvinculados/" + id_desvinculado
            return redirect(href)
    else:
        form = HistorialDesvinculadoForm()
    context = {'form': form, 'nombre_form': "Re-incorporar", 'id_desvinculado': id_desvinculado}
    return render(request, "EmpleoEstatal/Desvinculados/re_incorporar.html", context)


@login_required
@permission_required(['administrador'])
def reportes_desvinculados(request):
    return render(request, "EmpleoEstatal/Desvinculados/Reportes/reportes_desvinculados.html")


def comprobar_pendientes(listado):

    causal_baja_automatica = CausalBaja.objects.get(id=10)
    fecha_actual = timezone.now()

    for persona in listado:
        persona.activo = False
        persona.causa_baja = causal_baja_automatica
        persona.fecha_baja = fecha_actual
        persona.save()


#                  PETICION AJAX
from django.http import HttpResponse
from django.views.generic import TemplateView
import json


class PeticionAjaxFiltrarEntidadesEmpleoEstatal(TemplateView):

    def get(self, request, *args, **kwargs):

        id_organismo = int(request.GET['id_organismo'])
        id_municipio = Municipio.objects.get(id=request.GET['id_municipio']).codigo_mes
        print(id_organismo)
        print(id_municipio)

        entidades = Entidad.objects.filter(id_organismo_s__id=id_organismo, municipio__codigo_mes=id_municipio)
        print(entidades.count())
        #  -------------------------------

        entidades = [entidades_serializer(entidad) for entidad in entidades]
        return HttpResponse(json.dumps(entidades), content_type='application/json')


def entidades_serializer(entidad):
    return {'codigo_ent': entidad.id_codigo_entidad, 'e_nombre': entidad.e_nombre}