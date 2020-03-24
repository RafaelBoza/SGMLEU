# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from SGMGU.forms import InterruptosCovidForm
from SGMGU.models import InterruptosCovid, Municipio, Entidad, Organismo
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dmt', 'dpt_ee'])
def gestion_interruptos_covid(request):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    categoria = request.user.perfil_usuario.categoria.nombre
    organismo = request.user.perfil_usuario.organismo
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia

    if categoria == 'dmt':
        interruptos_covid = InterruptosCovid.objects.filter(municipio=municipio_usuario).all()

    elif categoria == 'administrador':
        interruptos_covid = InterruptosCovid.objects.all()

    elif categoria == 'dpt_ee':
        interruptos_covid = InterruptosCovid.objects.filter(municipio_provincia=provincia_usuario).all()

    interruptos_covid = paginar(request, interruptos_covid)
    paginas = crear_lista_pages(interruptos_covid)
    nombre_pag = "Listado: Interruptos (COVID)"

    return render(request, "Interruptos/InterruptosCOVID/gestion_interruptos_covid.html", locals())


@login_required()
@permission_required(['administrador', 'dmt'])
def registrar_interrupto_covid(request):

    if request.method == 'POST':
        form = InterruptosCovidForm(request.POST)
        if form.is_valid():
            interrupto = form.save(commit=False)
            interrupto.save()
            messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
            return redirect('/interruptos_covid')
        else:
            context = {'form': form, 'nombre_form': "Registrar:"}
            return render(request, "Interruptos/InterruptosCOVID/registrar_interrupto_covid.html", context)
    else:
        form = InterruptosCovidForm()
    context = {'form': form, 'nombre_form': "Registrar:"}
    return render(request, "Interruptos/InterruptosCOVID/registrar_interrupto_covid.html", context)


@login_required()
@permission_required(['administrador', 'dmt'])
def modificar_interrupto_covid(request, id_interrupto):
    interrupto = InterruptosCovid.objects.get(id=id_interrupto)
    entidad = interrupto.entidad.e_nombre

    if request.method == 'POST':
        form = InterruptosCovidForm(request.POST, instance=interrupto)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Modificado con éxito.")
            return redirect('/interruptos_covid')
        else:
            context = {'form': form, 'nombre_form': "Modificar:"}
            return render(request, "Interruptos/InterruptosCOVID/modificar_interrupto_covid.html", context)
    else:
        form = InterruptosCovidForm(instance=interrupto)

    context = {'form': form, 'nombre_form': "Modificar:", 'entidad': entidad}
    return render(request, "Interruptos/InterruptosCOVID/modificar_interrupto_covid.html", context)


@login_required()
@permission_required(['administrador', 'interrupto'])
def eliminar_interrupto_covid(request, id_interrupto):
    interrupto = InterruptosCovid.objects.get(id=id_interrupto)
    interrupto.delete()
    messages.add_message(request, messages.SUCCESS, "Eliminado con éxito.")
    return redirect('/interruptos_covid')


#                  PETICION AJAX
from django.http import HttpResponse
from django.views.generic import TemplateView
import json


class PeticionAjaxFiltrarEntidadesInterruptosCOVID(TemplateView):

    def get(self, request, *args, **kwargs):

        id_organismo = Organismo.objects.get(id=request.GET['id_organismo']).id
        id_municipio = Municipio.objects.get(id=request.GET['id_municipio']).codigo_mes

        entidades = Entidad.objects.filter(id_organismo_s__id=id_organismo, municipio__codigo_mes=id_municipio,
                                           estado=True)
        #  -------------------------------

        entidades = [entidades_serializer(entidad) for entidad in entidades]
        return HttpResponse(json.dumps(entidades), content_type='application/json')


def entidades_serializer(entidad):
    return {'codigo_ent': entidad.id_codigo_entidad, 'e_nombre': entidad.e_nombre}
