# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from SGMGU.models import *
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utiles import *
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.db import models


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def buscar_fluctuaciones(request):
    if request.method == "POST":
        texto = request.POST['texto_fluctuacion'].lower()

        fluctuaciones = Fluctuacion.objects.filter(id_entidad__e_nombre__icontains=texto)

        # carreras=Carrera.objects.filter(activo=True,nombre__icontains=texto)
    else:
        fluctuaciones = []
    fluctuaciones = paginar(request, fluctuaciones)
    context = {'fluctuaciones': fluctuaciones, 'paginas': crear_lista_pages(fluctuaciones), 'busqueda': True,
               'texto': request.POST['texto_fluctuacion']}
    return render(request, "Fluctuaciones/gestion_fluctuaciones.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def gestion_fluctuacion(request):
    fluctuaciones = Fluctuacion.objects.all()
    fluctuaciones = paginar(request, fluctuaciones)
    context = {'fluctuaciones': fluctuaciones, 'paginas': crear_lista_pages(fluctuaciones)}
    return render(request, "Fluctuaciones/gestion_fluctuaciones.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def registrar_fluctuacion(request):
    perfil = Perfil_usuario.objects.get(usuario=request.user)

    if perfil.categoria.nombre == "organismo":
        lista_organismos_por_usuario = Organismo.objects.filter(id=perfil.organismo_id)
        lista_entidades_por_usuario = Entidad.objects.filter(id_organismo_s=perfil.organismo_id)
    else:
        lista_organismos_por_usuario = Organismo.objects.all()
        lista_entidades_por_usuario = Entidad.objects.all()

    if request.method == 'POST':
        form = FluctuacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La fluctuación se ha registrado con éxito.")
            return redirect('/fluctuaciones')
    else:
        form = FluctuacionForm()
    context = {'form': form, 'nombre_accion': 'Registrar', 'lista_organismos_por_usuario': lista_organismos_por_usuario,
               'lista_entidades_por_usuario': lista_entidades_por_usuario}
    return render(request, "Fluctuaciones/form_fluctuacion.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def modificar_fluctuacion(request, id_fluctuacion):
    perfil = Perfil_usuario.objects.get(usuario=request.user)

    if perfil.categoria.nombre == "organismo":
        lista_organismos_por_usuario = Organismo.objects.filter(id=perfil.organismo_id)
        lista_entidades_por_usuario = Entidad.objects.filter(id_organismo_s=perfil.organismo_id)
    else:
        lista_organismos_por_usuario = Organismo.objects.all()
        lista_entidades_por_usuario = Entidad.objects.all()

    fluctuacion = Fluctuacion.objects.get(id_fluctuacion=id_fluctuacion)
    if request.method == 'POST':
        form = FluctuacionForm(request.POST, instance=fluctuacion)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La fluctuación se ha modificado con éxito.")
            return redirect('/fluctuaciones')
    else:
        form = FluctuacionForm(instance=fluctuacion)
    # Creamos el contexto
    context = {'form': form, 'nombre_accion': 'Modificar', 'lista_organismos_por_usuario': lista_organismos_por_usuario,
               'lista_entidades_por_usuario': lista_entidades_por_usuario}
    # Y mostramos los datos
    return render(request, "Fluctuaciones/form_fluctuacion.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def eliminar_fluctuacion(request, id_fluctuacion):
    fluctuacion = Fluctuacion.objects.get(id_fluctuacion=id_fluctuacion)
    fluctuacion.delete()
    messages.add_message(request, messages.SUCCESS, "La fluctuación ha sido eliminada con éxito.")
    return redirect('/fluctuaciones')
