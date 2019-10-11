# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_causales_no_aceptacion(request):
    causales_no_aceptacion = CausalNoAceptacion.objects.all()
    return render(request, "CausalesNoAceptacion/gestion_causales_no_aceptacion.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_causal_no_aceptacion(request):
    if request.method == 'POST':
        form = CausalNoAceptacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de no aceptación se ha registrado con éxito.")
            return redirect('/causales_no_aceptacion')
    else:
        form = CausalNoAceptacionForm()
    context = {'form': form, 'nombre_form': "Registrar Causa de no Aceptación"}
    return render(request, "CausalesNoAceptacion/registrar_causales_no_aceptacion.html", context)


@login_required
@permission_required(['administrador'])
def modificar_causal_no_aceptacion(request, id_causal_no_aceptacion):
    causal_no_aceptacion = CausalNoAceptacion.objects.get(id=id_causal_no_aceptacion)
    if request.method == 'POST':
        form = CausalNoAceptacionForm(request.POST, instance=causal_no_aceptacion)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de no aceptación se ha modificado con éxito.")
            return redirect('/causales_no_aceptacion')
    else:
        form = CausalNoAceptacionForm(instance=causal_no_aceptacion)
    context = {'form': form}
    return render(request, "CausalesNoAceptacion/modificar_causales_no_aceptacion.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_causal_no_aceptacion(request, id_causal_no_aceptacion):
    causal_no_aceptacion = CausalNoAceptacion.objects.get(id=id_causal_no_aceptacion)
    causal_no_aceptacion.activo = False
    causal_no_aceptacion.save()
    messages.add_message(request, messages.SUCCESS, "La causa de no aceptación se ha eliminado con éxito.")
    return redirect('/causales_no_aceptacion')
