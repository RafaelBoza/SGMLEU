# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_causales_no_reincorporacion(request):
    causales_no_reincorporacion = CausalNoReubicacion.objects.all()
    nombre_form = "Listado: Causales de no reubicación"
    context = {'causales': causales_no_reincorporacion, 'nombre_form': nombre_form}
    return render(request, "Nomencladores/CausalesNoReincorporacionInterruptos/gestion_causales_no_reincorporacion_interruptos.html", context)

@login_required
@permission_required(['administrador'])
def registrar_causal_no_reincorporacion(request):
    if request.method == 'POST':
        form = CausalNoReubicacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de no reubicación se ha registrado con éxito.")
            return redirect('/causales_no_reincorporacion')
    else:
        form = CausalNoReubicacionForm()
    nombre_form = "Registrar: Causa de no reubicación"
    context = {'form': form, 'nombre_form': nombre_form}
    return render(request, "Nomencladores/CausalesNoReincorporacionInterruptos/registrar_causal_no_reincorporacion_interrupto.html", context)


@login_required
@permission_required(['administrador'])
def modificar_causal_no_reincorporacion(request, id_causal_no_reincorporacion):
    causal_no_reincorporacion = CausalNoReubicacion.objects.get(id=id_causal_no_reincorporacion)
    if request.method == 'POST':
        form = CausalNoReubicacionForm(request.POST, instance=causal_no_reincorporacion)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de no reubicación se ha modificado con éxito.")
            return redirect('/causales_no_reincorporacion')
    else:
        form = CausalNoReubicacionForm(instance=causal_no_reincorporacion)
    nombre_form = "Modificar: Causa de no reubicación"
    context = {'form': form, 'nombre_form': nombre_form}
    return render(request, "Nomencladores/CausalesNoReincorporacionInterruptos/modificar_causal_no_reincorporacion_interrupto.html", context)



@login_required
@permission_required(['administrador'])
def eliminar_causal_no_reincorporacion(request, id_causal_no_reincorporacion):
    causal_no_reincorporacion = CausalNoReubicacion.objects.get(id=id_causal_no_reincorporacion)
    causal_no_reincorporacion.activo = False
    causal_no_reincorporacion.save()
    messages.add_message(request, messages.SUCCESS, "La causa de no reubicación se ha eliminado con éxito.")
    return redirect('/causales_no_reincorporacion')
