# -*- coding: utf-8 -*-
from itertools import permutations

from django.shortcuts import render, redirect
from SGMGU.models import *
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utiles import *
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.db import models
import time

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string


def devolver_listado_annos(anno):
    annos = {'anno1': anno + 1, 'anno2': anno + 2, 'anno3': anno + 3, 'anno4': anno + 4, 'anno5': anno + 5,
             'anno6': anno + 6, 'anno7': anno + 7, 'anno8': anno + 8, 'anno9': anno + 9, 'anno10': anno + 10}
    return annos


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def buscar_demanda(request):
    if request.method == "POST":
        texto = request.POST['texto_demanda'].lower()

        demandas = DemandaGraduados.objects.filter(entidad__e_nombre__contains=texto)
    else:
        demandas = []
    demandas = paginar(request, demandas)
    context = {'demandas': demandas, 'paginas': crear_lista_pages(demandas), 'busqueda': True,
               'texto': request.POST['texto_demanda']}
    return render(request, "Demandas/gestion_demanda.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def gestion_demanda(request):
    anno = int(time.strftime("%Y"))
    annos = devolver_listado_annos(anno)

    perfil = Perfil_usuario.objects.get(usuario=request.user)

    if perfil.categoria.nombre == "organismo":
        demandas = DemandaGraduados.objects.filter(organismo=perfil.organismo)
    else:
        demandas = DemandaGraduados.objects.all()

    demandas = paginar(request, demandas)
    context = {'demandas': demandas, 'paginas': crear_lista_pages(demandas), 'anno': anno, 'annos': annos}
    return render(request, "Demandas/gestion_demanda.html", context)


# ---------------------------------------------------------------------



# ---------------------------------------------------------------------


# registrar demanda
@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def registrar_demanda(request):
    perfil = Perfil_usuario.objects.get(usuario=request.user)

    if perfil.categoria.nombre == "organismo":
        lista_organismos_por_usuario = Organismo.objects.filter(id=perfil.organismo_id)
        lista_entidades_por_usuario = Entidad.objects.filter(id_organismo_s=perfil.organismo_id)
    else:
        lista_organismos_por_usuario = Organismo.objects.all()
        lista_entidades_por_usuario = Entidad.objects.all()

    if request.method == 'POST':
        form = DemandaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La demanda se ha registrado con éxito.")
            return redirect('/demandas')
    else:
        # --------------------------------

        form = DemandaForm()
    context = {'form': form, 'lista_organismos_por_usuario': lista_organismos_por_usuario,
               'lista_entidades_por_usuario': lista_entidades_por_usuario, 'nombre_accion': 'Registrar'}
    return render(request, "demandas/form_demanda.html", context)


# 'lista_entidades_por_usuario': lista_entidades_por_usuario,

# para modificar una demanda:

@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def modificar_demanda(request, identificador):

    perfil = Perfil_usuario.objects.get(usuario=request.user)

    if perfil.categoria.nombre == "organismo":
        lista_organismos_por_usuario = Organismo.objects.filter(id=perfil.organismo_id)
        lista_entidades_por_usuario = Entidad.objects.filter(id_organismo_s=perfil.organismo_id)
    else:
        lista_organismos_por_usuario = Organismo.objects.all()
        lista_entidades_por_usuario = Entidad.objects.all()

    demanda = DemandaGraduados.objects.get(codigo_demanda=identificador)
    if request.method == 'POST':
        form = DemandaForm(request.POST, instance=demanda)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La demanda se ha modificado con éxito.")
            return redirect('/demandas')
    else:
        form = DemandaForm(instance=demanda)
    # Creamos el contexto
    context = {'form': form, 'nombre_accion': 'Modificar','lista_organismos_por_usuario':lista_organismos_por_usuario,'lista_entidades_por_usuario':lista_entidades_por_usuario}
    # Y mostramos los datos
    return render(request, "demandas/form_demanda.html", context)


# -----------pruebas con AJAX------------------------------------------------------------------------
@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def demanda_create(request):
    data = dict()

    if request.method == 'POST':
        form = DemandaForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = DemandaForm()

    context = {'form': form}
    data['html_form'] = render_to_string('Demandas/form_demanda_modal.html', context, request=request)

    return JsonResponse(data)


# primera version del create demanda
# @login_required
# @permission_required(['administrador','especialista','organismo'])
# def demanda_create(request):
#     form = DemandaForm()
#     context = {'form':form}
#     html_form = render_to_string('Demandas/form_demanda_modal.html',context,request=request)
#     return JsonResponse({'html_form':html_form})








# -----------------------------------------------------------------------------------
# eliminar una entidad

@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def eliminar_demanda(request, identificador):
    demanda = DemandaGraduados.objects.get(codigo_demanda=identificador)
    #    demanda.estado = False
    demanda.delete()
    messages.add_message(request, messages.SUCCESS, "La demanda ha sido eliminada con éxito.")
    return redirect('/demandas')
