# -*- coding: utf-8 -*-
from django.contrib import messages

from SGMGU.forms import *
from django.contrib.auth.decorators import login_required

from SGMGU.views.ReportesInterruptos.metodos_auxiliares import totales_por_organismo
from SGMGU.views.utiles import *
import datetime
from django.db.models import Q



@login_required()
@permission_required(['administrador', 'interrupto'])
def gestion_interruptos(request):

    # listado = Interruptos.objects.all()
    # for inter in listado:
    #     inter.actividad_nueva.add(inter.actividad)
    #     inter.save()

    # for index, id in enumerate(ids):
    #     interrupto_x = Interruptos.objects.get(id=id)
    #     interrupto_x.fecha_registro = fechas[index]
    #     interrupto_x.save()

    categoria = request.user.perfil_usuario.categoria.nombre
    organismo = request.user.perfil_usuario.organismo
    autorizado = True
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month

    if categoria != 'administrador':
        try:
            organismo_autorizado = OrganismosAutorizadosRegistrarInterrupto.objects.get(organismo=organismo)
            if not cumple_limite_autorizo(organismo_autorizado):
                organismo_autorizado.delete()
                autorizado = False
        except:
            dia = int(datetime.datetime.now().day)
            if dia > 10:
                autorizado = False

    if categoria == 'interrupto':
        interruptos = Interruptos.objects.filter(organismo=organismo, fecha_registro__year=anno_actual). \
            values('id', 'organismo__nombre', 'entidad__e_nombre', 'municipio__nombre', 'aplica_proceso', 'fecha_registro')

        query = """SELECT id
                                    FROM public."SGMGU_interruptos" t where
                                        date_part('month',t.fecha_registro)=""" + unicode(mes_actual) + """;"""

        resultado_query_interruptos = Interruptos.objects.raw(query)
        ids_interruptos = [interr.id for interr in resultado_query_interruptos]
        interruptos = interruptos.filter(id__in=ids_interruptos)

    elif categoria == 'administrador':
        interruptos = Interruptos.objects.all(). \
            values('id', 'organismo__nombre', 'entidad__e_nombre', 'municipio__nombre', 'aplica_proceso',
                   'fecha_registro')

    q = request.GET.get("q")
    if q:
        if categoria == 'interrupto':
            interruptos = Interruptos.objects.filter(organismo=organismo). \
                                values('id', 'organismo__nombre', 'entidad__e_nombre', 'municipio__nombre',
                                       'aplica_proceso', 'fecha_registro')
            interruptos = interruptos.filter(
                                    Q(organismo__nombre__icontains=q) |
                                    Q(organismo__siglas__icontains=q) |
                                    Q(municipio__nombre__icontains=q) |
                                    Q(entidad__e_nombre__icontains=q)
                                )
        elif categoria == 'administrador':
            interruptos = interruptos.filter(
                Q(organismo__nombre__icontains=q) |
                Q(organismo__siglas__icontains=q) |
                Q(municipio__nombre__icontains=q) |
                Q(entidad__e_nombre__icontains=q)
            )

    interruptos = paginar(request, interruptos)
    paginas = crear_lista_pages(interruptos)
    nombre_pag = "Listado: Interruptos"

    return render(request, "Interruptos/gestion_interruptos.html", locals())


@login_required()
@permission_required(['administrador', 'interrupto'])
def registrar_interrupto(request):
    organismo = request.user.perfil_usuario.organismo
    categoria = request.user.perfil_usuario.categoria.nombre
    municipios = Municipio.objects.all()

    # --------   VALIDAR SI CUMPLE EL PLAZO
    if categoria != 'administrador':
        try:
            organismo_autorizado = OrganismosAutorizadosRegistrarInterrupto.objects.get(organismo=organismo)
            if not cumple_limite_autorizo(organismo_autorizado):
                organismo_autorizado.delete()
                messages.add_message(request, messages.SUCCESS,
                                     "El plazo para registrar interruptos es del 1 al 10 de cada mes.")
                return redirect('/interruptos')
        except:
            dia = int(datetime.datetime.now().day)
            if dia > 10:
                messages.add_message(request, messages.SUCCESS, "El plazo para registrar interruptos es del 1 al 10 de cada mes.")
                return redirect('/interruptos')
    # ----------------------------------------

    if request.method == 'POST':
        form = InterruptosForm(request.POST, request.FILES)

        ids_causa_interrupcion = []
        if 'causa_interrupcion' in request.POST:
            ids_causa_interrupcion = request.POST.getlist('causa_interrupcion')

        ids_actividades = []
        if 'actividad_nueva' in request.POST:
            ids_actividades = request.POST.getlist('actividad_nueva')

        ids_causal_no_reubicacion = []
        if 'causal_no_reubicacion' in request.POST:
            ids_causal_no_reubicacion = request.POST.getlist('causal_no_reubicacion')

        id_entidad = request.POST['entidad']
        if metodo(id_entidad, organismo.id):
            form.add_error('entidad', 'Ya se registraron los interruptos de la entidad seleccionada.')

        total_interruptos = request.POST['total_interruptos_entidad']
        actividad_directos = request.POST['actividad_directos']
        actividad_indirectos = request.POST['actividad_indirectos']

        if int(actividad_indirectos) + int(actividad_directos) != int(total_interruptos):
            form.add_error('actividad_directos', 'Error.')
            form.add_error('actividad_indirectos', 'Error.')

        if form.is_valid():
            interrupto = form.save(commit=False)
            interrupto.save()

            if ids_causal_no_reubicacion.__len__() > 0:
                for id_causal in ids_causal_no_reubicacion:
                    interrupto.causal_no_reubicacion.add(CausalNoReubicacion.objects.get(id=id_causal))

            if ids_actividades.__len__() > 0:
                for id_actividad in ids_actividades:
                    interrupto.actividad_nueva.add(ActividadInterrupto.objects.get(id=id_actividad))

            if ids_causa_interrupcion.__len__() > 0:
                for id_causal in ids_causa_interrupcion:
                    interrupto.causa_interrupcion.add(CausalInterrupcion.objects.get(id=id_causal))

            messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
            return redirect('/interruptos')
        else:
            context = {'form': form, 'nombre_form': "Registrar: Interrupto", 'organismo': organismo,
                       'municipios': municipios}
            return render(request, "Interruptos/registrar_interrupto.html", context)
    else:
        form = InterruptosForm()
    context = {'form': form, 'nombre_form': "Registrar: Interrupto", 'organismo': organismo, 'municipios': municipios}
    return render(request, "Interruptos/registrar_interrupto.html", context)


@login_required()
@permission_required(['administrador', 'interrupto'])
def modificar_interrupto(request, id_interrupto):
    interrupto = Interruptos.objects.get(id=id_interrupto)

    organismo = request.user.perfil_usuario.organismo
    municipios = Municipio.objects.all()
    categoria = request.user.perfil_usuario.categoria.nombre

    # --------   VALIDAR SI CUMPLE EL PLAZO
    if categoria != 'administrador':
        try:
            organismo_autorizado = OrganismosAutorizadosRegistrarInterrupto.objects.get(organismo=organismo)
            if not cumple_limite_autorizo(organismo_autorizado):
                organismo_autorizado.delete()
                messages.add_message(request, messages.SUCCESS,
                                     "El plazo para modificar interruptos es del 1 al 10 de cada mes.")
                return redirect('/interruptos')
        except:
            dia = int(datetime.datetime.now().day)
            if dia > 10:
                messages.add_message(request, messages.SUCCESS, "El plazo para modificar interruptos es del 1 al 10 de cada mes.")
                return redirect('/interruptos')
    # ----------------------------------------

    if request.method == 'POST':
        form = InterruptosForm(request.POST, instance=interrupto)

        ids_causa_interrupcion = []
        if 'causa_interrupcion' in request.POST:
            ids_causa_interrupcion = request.POST.getlist('causa_interrupcion')

        ids_actividades = []
        if 'actividad_nueva' in request.POST:
            ids_actividades = request.POST.getlist('actividad_nueva')

        ids_causal_no_reubicacion = []
        if 'causal_no_reubicacion' in request.POST:
            ids_causal_no_reubicacion = request.POST.getlist('causal_no_reubicacion')

        id_entidad = request.POST['entidad']
        entidad = Entidad.objects.get(id_codigo_entidad=id_entidad)

        total_interruptos = request.POST['total_interruptos_entidad']
        actividad_directos = request.POST['actividad_directos']
        actividad_indirectos = request.POST['actividad_indirectos']

        if int(actividad_indirectos) + int(actividad_directos) != int(total_interruptos):
            form.add_error('actividad_directos', 'Error.')
            form.add_error('actividad_indirectos', 'Error.')

        if interrupto.entidad_id != id_entidad and metodo(id_entidad, interrupto.organismo_id):
            form.add_error('entidad', 'Ya se registraron los interruptos de la entidad: %s.' % entidad.e_nombre)

        if form.is_valid():
            form.save()

            if ids_causal_no_reubicacion.__len__() > 0:
                for id_causal in ids_causal_no_reubicacion:
                    interrupto.causal_no_reubicacion.add(CausalNoReubicacion.objects.get(id=id_causal))

            if ids_actividades.__len__() > 0:
                for id_actividad in ids_actividades:
                    interrupto.actividad_nueva.add(ActividadInterrupto.objects.get(id=id_actividad))

            if ids_causa_interrupcion.__len__() > 0:
                for id_causal in ids_causa_interrupcion:
                    interrupto.causa_interrupcion.add(CausalInterrupcion.objects.get(id=id_causal))

            messages.add_message(request, messages.SUCCESS, "El interrupto se ha modificado con éxito.")
            return redirect('/interruptos')
        else:
            context = {'form': form, 'nombre_form': "Modificar: Interrupto", 'organismo': organismo,
                       'municipios': municipios}
            return render(request, "Interruptos/modificar_interruptos.html", context)
    else:
        form = InterruptosForm(instance=interrupto)

    nombre_form = "Modificar: interrupto"
    context = {'form': form, 'nombre_form': nombre_form, 'organismo': organismo, 'municipios': municipios}
    return render(request, "Interruptos/modificar_interruptos.html", context)


@login_required()
@permission_required(['administrador', 'interrupto'])
def eliminar_interrupto(request, id_interrupto):
    interrupto = Interruptos.objects.get(id=id_interrupto)
    interrupto.delete()
    messages.add_message(request, messages.SUCCESS, "Eliminado con éxito.")
    return redirect('/interruptos')


@login_required()
@permission_required(['administrador', 'interrupto'])
def detalles_interrupto(request, id_interrupto):

    categoria = request.user.perfil_usuario.categoria.nombre
    organismo = request.user.perfil_usuario.organismo
    autorizado = True
    mes_actual = datetime.datetime.today().month

    if categoria != 'administrador':
        try:
            organismo_autorizado = OrganismosAutorizadosRegistrarInterrupto.objects.get(organismo=organismo)
            if not cumple_limite_autorizo(organismo_autorizado):
                organismo_autorizado.delete()
                autorizado = False
        except:
            dia = int(datetime.datetime.now().day)
            if dia > 10:
                autorizado = False

    interrupto = Interruptos.objects.get(id=id_interrupto)
    # causales_no_reubicacion = interrupto.causal_no_reubicacion.all

    return render(request, "Interruptos/detalles_interrupto.html", locals())


@login_required()
@permission_required(['administrador', 'interrupto'])
def descargar_informe_valorativo(request, id_interrupto):
    try:
        informe_valorativo = Interruptos.objects.get(id=id_interrupto).informe_valorativo
        filename = unicode(informe_valorativo.file.name.split('/')[-1]).replace(" ", "_")
        response = HttpResponse(informe_valorativo.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    except:
        messages.add_message(request, messages.ERROR, "No existe informe valorativo para esta entidad.")
    return redirect('/interruptos/' + id_interrupto)


# metodos auxiliares
def cumple_limite_autorizo(organismo):

    cumple_limite = True

    start = float(organismo.tiempo_inicia)
    end = time.time()
    m, s = divmod(end - start, 60)
    h, m = divmod(m, 60)
    if h > 48:
        cumple_limite = False

    return cumple_limite


#                  PETICION AJAX
from django.http import HttpResponse
from django.views.generic import TemplateView
import json


class PeticionAjaxFiltrarEntidadesInterruptos(TemplateView):

    def get(self, request, *args, **kwargs):

        id_organismo = request.user.perfil_usuario.organismo.id
        id_municipio = Municipio.objects.get(id=request.GET['id_municipio']).codigo_mes

        # ----   VALIDAR QUE SOLO SE HAGA UN REGISTRO POR MES
        ids_entidades = entidades_de_interruptos_existentes_mes_actual(id_organismo)

        entidades = Entidad.objects.filter(id_organismo_s__id=id_organismo, municipio__codigo_mes=id_municipio,
                                           estado=True).exclude(id_codigo_entidad__in=ids_entidades)
        #  -------------------------------

        entidades = [entidades_serializer(entidad) for entidad in entidades]
        return HttpResponse(json.dumps(entidades), content_type='application/json')


class PeticionAjaxFiltrarEntidadesInterruptosModificar(TemplateView):

    def get(self, request, *args, **kwargs):

        id_organismo = request.user.perfil_usuario.organismo.id
        id_municipio = Municipio.objects.get(id=request.GET['id_municipio']).codigo_mes

        entidades = Entidad.objects.filter(id_organismo_s__id=id_organismo, municipio__codigo_mes=id_municipio,
                                           estado=True)

        entidades = [entidades_serializer(entidad) for entidad in entidades]
        return HttpResponse(json.dumps(entidades), content_type='application/json')


def entidades_serializer(entidad):
    return {'codigo_ent': entidad.id_codigo_entidad, 'e_nombre': entidad.e_nombre}


def entidades_de_interruptos_existentes_mes_actual(id_organismo):

    anno_actual = datetime.datetime.today().year
    mes_actual = datetime.datetime.today().month
    interruptos = Interruptos.objects.filter(organismo__id=id_organismo,
                                             fecha_registro__year=anno_actual)

    lista_interruptos = []
    for interrupto in interruptos:
        mes = str(interrupto.fecha_registro).split('-')
        mes = int(mes[1])

        if mes_actual == mes:
            lista_interruptos.append(interrupto)

    ids_entidades = []
    for interr in lista_interruptos:
        ids_entidades.append(interr.entidad.id_codigo_entidad)

    return ids_entidades


def metodo(id_entidad, organismo):

    existe = False

    ids_entidades = entidades_de_interruptos_existentes_mes_actual(organismo)
    if ids_entidades.__len__() > 0:
        for id in ids_entidades:
            if id == id_entidad:
                existe = True
    else:
        return existe

    return existe
