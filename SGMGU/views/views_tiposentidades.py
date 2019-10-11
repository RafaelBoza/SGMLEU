# -*- coding: utf-8 -*-
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
@permission_required(['administrador','especialista'])
def gestion_tiposentidades(request):
    tipos_entidades=Tipo_Entidad.objects.all()
    context = {'tiposentidades': tipos_entidades}
    return render(request, "tiposentidades/gestion_tiposentidades.html", context)

@login_required
@permission_required(['administrador','especialista'])
def registrar_tipoentidad(request):
    if request.method == 'POST':
        form=TipoEntidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El tipo de entidad se ha registrado con éxito.")
            return redirect('/tiposentidades')
    else:
        form = TipoEntidadForm()
    context = {'form':form}
    return render(request, "tiposentidades/form_tipoentidad.html", context)

@login_required
@permission_required(['administrador','especialista'])
def modificar_tipoentidad(request,identificador):
    tipo_entidad=Tipo_Entidad.objects.get(identificador=identificador)
    if request.method == 'POST':
        form=TipoEntidadForm(request.POST,instance=tipo_entidad)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El tipo de entidad se ha modificado con éxito.")
            return redirect('/tiposentidades')
    else:
        form = TipoEntidadForm(instance=tipo_entidad)
    # Creamos el contexto
    context = {'form':form}
    # Y mostramos los datos
    return render(request, "tiposentidades/form_tipoentidad.html", context)



@login_required
@permission_required(['administrador','especialista'])
def eliminar_tipoentidad(request,identificador):
    tipoentidad=Tipo_Entidad.objects.get(identificador=identificador)

    if not tipoentidad.estado:
        tipoentidad.estado = True
    else:
        tipoentidad.estado = False

    tipoentidad.save()
    messages.add_message(request, messages.SUCCESS, "El tipo de entidad se ha modificado con éxito.")
    return redirect('/tiposentidades')
