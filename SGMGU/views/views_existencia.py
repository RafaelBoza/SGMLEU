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
def buscar_existencias(request):
    if request.method == "POST":
        texto = request.POST['texto_existencia'].lower()

        existencias = Existencia.objects.filter(id_codigo_entidad__e_nombre__icontains=texto)

        # carreras=Carrera.objects.filter(activo=True,nombre__icontains=texto)
    else:
        existencias = []
    existencias = paginar(request, existencias)
    context = {'existencias': existencias, 'paginas': crear_lista_pages(existencias), 'busqueda': True,
               'texto': request.POST['texto_existencia']}
    return render(request, "Existencias/gestion_existencia.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def gestion_existencias(request):
    existencias = Existencia.objects.all()
    existencias = paginar(request, existencias)
    context = {'existencias': existencias, 'paginas': crear_lista_pages(existencias)}
    return render(request, "Existencias/gestion_existencia.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def registrar_existencia(request):
    perfil = Perfil_usuario.objects.get(usuario=request.user)

    if perfil.categoria.nombre == "organismo":
        lista_organismos_por_usuario = Organismo.objects.filter(id=perfil.organismo_id)
        lista_entidades_por_usuario = Entidad.objects.filter(id_organismo_s=perfil.organismo_id)
    else:
        lista_organismos_por_usuario = Organismo.objects.all()
        lista_entidades_por_usuario = Entidad.objects.all()

    if request.method == 'POST':
        form = ExistenciaFotm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La existencia se ha registrado con éxito.")
            return redirect('/existencias')
    else:
        form = ExistenciaFotm()
    context = {'form': form, 'nombre_accion': 'Registrar', 'lista_organismos_por_usuario': lista_organismos_por_usuario,
               'lista_entidades_por_usuario': lista_entidades_por_usuario}
    return render(request, "existencias/form_existencia.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def modificar_existencia(request, id_existencia):
    existencia = Existencia.objects.get(id_ocupados=id_existencia)

    perfil = Perfil_usuario.objects.get(usuario=request.user)

    if perfil.categoria.nombre == "organismo":
        lista_organismos_por_usuario = Organismo.objects.filter(id=perfil.organismo_id)
        lista_entidades_por_usuario = Entidad.objects.filter(id_organismo_s=perfil.organismo_id)
    else:
        lista_organismos_por_usuario = Organismo.objects.all()
        lista_entidades_por_usuario = Entidad.objects.all()

    if request.method == 'POST':
        form = ExistenciaFotm(request.POST, instance=existencia)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La existencia se ha modificado con éxito.")
            return redirect('/existencias')
    else:
        form = ExistenciaFotm(instance=existencia)
    # Creamos el contexto
    context = {'form': form, 'nombre_accion': 'Modificar', 'lista_organismos_por_usuario': lista_organismos_por_usuario,
               'lista_entidades_por_usuario': lista_entidades_por_usuario}
    # Y mostramos los datos
    return render(request, "existencias/form_existencia.html", context)


@login_required
@permission_required(['administrador', 'especialista', 'organismo'])
def eliminar_existencia(request, id_existencia):
    existencia = Existencia.objects.get(id_ocupados=id_existencia)
    existencia.delete()
    messages.add_message(request, messages.SUCCESS, "La existencia ha sido eliminada con éxito.")
    return redirect('/existencias')
