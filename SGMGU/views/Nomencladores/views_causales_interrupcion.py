# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_causales_interrupcion(request):
    causales_interrupcion = CausalInterrupcion.objects.all()
    context = {'causales': causales_interrupcion}
    return render(request, "Nomencladores/CausalesInterrupcion/gestion_causales_interrupcion.html", context)

@login_required
@permission_required(['administrador'])
def registrar_causal_interrupcion(request):
    if request.method == 'POST':
        form = CausalInterrupcionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de interrupción se ha registrado con éxito.")
            return redirect('/causales_interrupcion')
    else:
        form = CausalInterrupcionForm()
    context = {'form': form}
    return render(request, "Nomencladores/CausalesInterrupcion/registrar_causal_interrupcion.html", context)


@login_required
@permission_required(['administrador'])
def modificar_causal_interrupcion(request, id_causal_interrupcion):
    causal_interrupcion = CausalInterrupcion.objects.get(id=id_causal_interrupcion)
    if request.method == 'POST':
        form = CausalInterrupcionForm(request.POST, instance=causal_interrupcion)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de interrupción se ha modificado con éxito.")
            return redirect('/causales_interrupcion')
    else:
        form = CausalInterrupcionForm(instance=causal_interrupcion)
    context = {'form': form}
    return render(request, "Nomencladores/CausalesInterrupcion/modificar_causal_interrupcion.html", context)



@login_required
@permission_required(['administrador'])
def eliminar_causal_interrupcion(request, id_causal_interrupcion):
    causal_interrupcion = CausalInterrupcion.objects.get(id=id_causal_interrupcion)
    causal_interrupcion.activo = False
    causal_interrupcion.save()
    messages.add_message(request, messages.SUCCESS, "La causa de interrupción se ha eliminado con éxito.")
    return redirect('/causales_interrupcion')
