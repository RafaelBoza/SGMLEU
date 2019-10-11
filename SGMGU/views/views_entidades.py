# -*- coding: utf-8 -*-
from random import randrange

from django.shortcuts import render,redirect
from SGMGU.models import *
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utiles import *
from django.http import HttpResponse,Http404
from django.db.models import Q
from django.db import models


@login_required
@permission_required(['administrador', 'especialista', 'dpt_ee', 'interrupto'])
def gestion_entidades(request):
    categoria = request.user.perfil_usuario.categoria.nombre
    organismo = request.user.perfil_usuario.organismo

    if categoria == 'interrupto':
        entidades = Entidad.objects.filter(id_organismo_s=organismo)
    else:
        entidades = Entidad.objects.all()

    q = request.GET.get("q")
    if q:
        entidades = entidades.filter(
            Q(e_nombre__icontains=q) |
            Q(id_codigo_entidad__icontains=q) |
            Q(id_organismo_s__nombre__icontains=q) |
            Q(municipio__nombre__icontains=q)
        )

    entidades = paginar(request, entidades)
    paginas = crear_lista_pages(entidades)
    context = {'entidades': entidades, 'paginas': paginas}

    return render(request, "Entidades/gestion_entidades.html", context)


# aqui registro una entidad
@login_required
@permission_required(['administrador','especialista', 'dpt_ee', 'interrupto'])
def registrar_entidad(request):
    if request.method == 'POST':
        form=EntidadForm(request.POST)
        if form.is_valid():
            entidad = form.save(commit=False)
            organismo = str(request.POST['id_organismo_s'])
            id_organismo = organismo[0:3]
            existe = True
            while existe:
                numero_random = str(randrange(10)) + str(randrange(10)) + str(randrange(10)) + str(randrange(10)) + str(randrange(10))
                id_codigo_entidad = id_organismo + numero_random
                try:
                    codigo = Entidad.objects.get(id_codigo_entidad=id_codigo_entidad)
                except:
                    existe = False
            entidad.id_codigo_entidad = id_codigo_entidad
            entidad.save()
            messages.add_message(request, messages.SUCCESS, "La entidad se ha registrado con éxito.")
            return redirect('/entidades')
    else:
        form = EntidadForm()
    context = {'form':form}
    return render(request, "entidades/form_entidad.html", context)

# para modificar una entidad:

@login_required
@permission_required(['administrador','especialista', 'dpt_ee', 'interrupto'])
def modificar_entidad(request,id_entidad):
    entidad=Entidad.objects.get(id_codigo_entidad=id_entidad)
    if request.method == 'POST':
        form=EntidadForm(request.POST,instance=entidad)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La entidad se ha modificado con éxito.")
            return redirect('/entidades')
    else:
        form = EntidadForm(instance=entidad)
    # Creamos el contexto
    context = {'form':form,'nombre_accion':'Modificar'}
    # Y mostramos los datos
    return render(request, "entidades/form_entidad.html", context)

# eliminar una entidad

@login_required
@permission_required(['administrador','especialista', 'dpt_ee', 'interrupto'])
def eliminar_entidad(request,id_entidad):
    entidad = Entidad.objects.get(id_codigo_entidad=id_entidad)
    entidad.estado = False
    entidad.save()
    messages.add_message(request, messages.SUCCESS, "La entidad ha sido desactivada con éxito.")
    return redirect('/entidades')


@login_required
@permission_required(['administrador', 'especialista', 'dpt_ee', 'interrupto'])
def activar_entidad(request, id_entidad):
    entidad = Entidad.objects.get(id_codigo_entidad=id_entidad)
    entidad.estado = True
    entidad.save()
    messages.add_message(request, messages.SUCCESS, "La entidad ha sido activada con éxito.")
    return redirect('/entidades')
